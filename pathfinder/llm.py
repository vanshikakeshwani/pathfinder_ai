"""LLM access: a transport protocol, the Experiential Labs gateway client and an offline fixture client.

`StructuredLLM` is the only entry point the agent uses. It renders the request, calls the transport
with bounded retries (transport errors and schema-validation failures share one retry budget), and
returns a validated Pydantic object or raises ToolError. Malformed output is never accepted.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Protocol, TypeVar

from pydantic import BaseModel, ValidationError

from pathfinder.config import Settings, StructuredMode
from pathfinder.retry import Attempt, CancelToken, RetryPolicy, ToolError, call_with_retry, classify_status
from pathfinder.telemetry import Budget, Telemetry

M = TypeVar("M", bound=BaseModel)

LLM_RETRYABLE = frozenset({"rate_limited", "transient", "timeout", "malformed"})


@dataclass
class LLMRequest:
    task: str  # plan | extract | verify | report | smoke
    system: str
    payload: dict[str, Any]
    schema: type[BaseModel]
    feedback: str | None = None  # validation error from the previous attempt

    def user_message(self) -> str:
        text = json.dumps(self.payload, ensure_ascii=False, indent=1)
        if self.feedback:
            text += ("\n\nYour previous reply failed validation. Return JSON that matches the schema "
                     f"exactly. Error: {self.feedback[:500]}")
        return text


@dataclass
class RawCompletion:
    text: str
    usage: dict | None = None


class LLMTransport(Protocol):
    model_id: str

    def complete(self, request: LLMRequest) -> RawCompletion: ...


# ------------------------------------------------------------------ gateway client


def strict_schema(schema: type[BaseModel]) -> dict:
    from openai.lib._pydantic import to_strict_json_schema

    return to_strict_json_schema(schema)


class GatewayLLM:
    """OpenAI-compatible chat-completions client pointed at the Experiential Labs gateway.

    The structured-output mode comes from LLM_STRUCTURED_MODE, which is set from the smoke test
    (docs/gateway-compat.md). SDK-level retries are disabled; retries happen in StructuredLLM.
    """

    def __init__(self, settings: Settings, mode: StructuredMode | None = None) -> None:
        if settings.explabs_api_key is None:
            raise ToolError("auth", "EXPLABS_API_KEY is not set")
        from openai import OpenAI

        self.model_id = settings.llm_model
        self.mode: StructuredMode = mode or settings.llm_structured_mode
        self.temperature = settings.llm_temperature
        self._client = OpenAI(api_key=settings.explabs_api_key.get_secret_value(),
                              base_url=settings.llm_base_url, timeout=settings.llm_request_timeout_s,
                              max_retries=0)

    def _messages(self, request: LLMRequest) -> list[dict]:
        system = request.system
        if self.mode != "json_schema":
            system += ("\n\nReply with a single JSON object only, matching this JSON schema:\n"
                       + json.dumps(request.schema.model_json_schema()))
        return [{"role": "system", "content": system}, {"role": "user", "content": request.user_message()}]

    def complete(self, request: LLMRequest) -> RawCompletion:
        import openai

        kwargs: dict[str, Any] = {"model": self.model_id, "messages": self._messages(request)}
        if self.temperature is not None:
            kwargs["temperature"] = self.temperature
        if self.mode == "json_schema":
            kwargs["response_format"] = {"type": "json_schema", "json_schema": {
                "name": request.schema.__name__, "strict": True, "schema": strict_schema(request.schema)}}
        elif self.mode == "json_object":
            kwargs["response_format"] = {"type": "json_object"}
        try:
            resp = self._client.chat.completions.create(**kwargs)
        except openai.APITimeoutError as e:
            raise ToolError("timeout", str(e)) from e
        except openai.APIConnectionError as e:
            raise ToolError("transient", str(e)) from e
        except openai.APIStatusError as e:
            retry_after = None
            try:
                ra = e.response.headers.get("retry-after")
                retry_after = float(ra) if ra else None
            except (AttributeError, ValueError):
                retry_after = None
            raise ToolError(classify_status(e.status_code), str(e)[:300], e.status_code, retry_after) from e
        if not resp.choices:
            raise ToolError("malformed", "no choices in completion")
        message = resp.choices[0].message
        if getattr(message, "refusal", None):
            raise ToolError("malformed", f"model refusal: {message.refusal[:200]}")
        usage = resp.usage.model_dump() if getattr(resp, "usage", None) else None
        return RawCompletion(message.content or "", usage)


# ------------------------------------------------------------------ fixture client

FixtureHandler = Callable[[LLMRequest], Any]


@dataclass
class FixtureLLM:
    """Offline scripted LLM. Each task maps to a handler returning a dict, a model, a raw string,
    or raising/returning an Exception. Used by tests and `demo-fixture`; never by live runs."""

    handlers: dict[str, FixtureHandler]
    model_id: str = "fixture-llm (synthetic)"
    requests: list[LLMRequest] = field(default_factory=list)

    def complete(self, request: LLMRequest) -> RawCompletion:
        self.requests.append(request)
        handler = self.handlers.get(request.task)
        if handler is None:
            raise ToolError("bad_request", f"no fixture handler for task {request.task!r}")
        out = handler(request)
        if isinstance(out, Exception):
            raise out
        if isinstance(out, BaseModel):
            return RawCompletion(out.model_dump_json(), {"fixture": True})
        if isinstance(out, str):
            return RawCompletion(out, {"fixture": True})
        return RawCompletion(json.dumps(out), {"fixture": True})


# --------------------------------------------------------------- structured facade


class StructuredLLM:
    def __init__(self, transport: LLMTransport, settings: Settings, budget: Budget,
                 telemetry: Telemetry, cancel: CancelToken,
                 sleeper: Callable[[float], bool] | None = None) -> None:
        self.transport = transport
        self.budget = budget
        self.telemetry = telemetry
        self.cancel = cancel
        self.policy = RetryPolicy(max_retries=settings.llm_max_retries)
        self.sleeper = sleeper

    @property
    def model_id(self) -> str:
        return self.transport.model_id

    def call(self, task: str, system: str, payload: dict[str, Any], schema: type[M]) -> M:
        request = LLMRequest(task=task, system=system, payload=payload, schema=schema)
        usage_box: dict[str, Any] = {}

        def attempt() -> M:
            if not self.budget.llm_allowed():
                raise ToolError("bad_request", "MAX_LLM_CALLS reached")
            self.budget.llm_calls += 1
            raw = self.transport.complete(request)
            usage_box["usage"] = raw.usage
            try:
                return schema.model_validate_json(raw.text)
            except ValidationError as e:
                request.feedback = str(e)
                raise ToolError("malformed", f"schema validation failed: {str(e)[:300]}") from e

        def record(a: Attempt) -> None:
            self.telemetry.llm_attempt(task, a, usage_box.pop("usage", None))

        # Transport errors and schema-validation failures share one bounded retry budget.
        return call_with_retry(attempt, self.policy, self.cancel, record, self.sleeper,
                               retryable=LLM_RETRYABLE)
