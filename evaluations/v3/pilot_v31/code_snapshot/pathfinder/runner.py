"""Wiring: build a RunContext from settings and clients (live or fixture)."""

from __future__ import annotations

import uuid
from collections.abc import Callable
from datetime import UTC, datetime

from pathfinder.config import Settings
from pathfinder.graph import RunContext, Strategy, run_graph
from pathfinder.llm import LLMTransport, StructuredLLM
from pathfinder.models import ResearchPlan
from pathfinder.retry import CancelToken, RetryPolicy
from pathfinder.telemetry import Budget, Telemetry
from pathfinder.tools.base import ContentsClient, SearchClient, ToolRunner


def new_run_id(prefix: str = "RUN") -> str:
    return f"{prefix}_{datetime.now(UTC).strftime('%Y%m%dT%H%M%S')}_{uuid.uuid4().hex[:6]}"


def make_context(question: str, settings: Settings, llm: LLMTransport, search: SearchClient,
                 contents: ContentsClient, *, strategy: Strategy = "adaptive",
                 user_weights: dict[str, int] | None = None, preset_plan: ResearchPlan | None = None,
                 run_id: str | None = None, synthetic: bool = False, cancel: CancelToken | None = None,
                 sleeper: Callable[[float], bool] | None = None) -> RunContext:
    run_id = run_id or new_run_id()
    cancel = cancel or CancelToken()
    budget = Budget.from_settings(settings)
    telemetry = Telemetry(run_id, settings.secret_values())
    structured = StructuredLLM(llm, settings, budget, telemetry, cancel, sleeper)
    tools = ToolRunner(search, contents, budget, telemetry, cancel,
                       RetryPolicy(max_retries=settings.exa_max_retries), settings.exa_request_timeout_s,
                       sleeper)
    return RunContext(run_id=run_id, question=question, settings=settings, llm=structured, tools=tools,
                      budget=budget, telemetry=telemetry, cancel=cancel, strategy=strategy,
                      user_weights=user_weights or {}, preset_plan=preset_plan, synthetic=synthetic)


def run(ctx: RunContext) -> RunContext:
    return run_graph(ctx)


def live_clients(settings: Settings):
    """Real gateway LLM + Exa Search + Exa Contents. Raises ToolError('auth') if a key is missing."""
    from pathfinder.llm import GatewayLLM
    from pathfinder.retry import ToolError
    from pathfinder.tools.exa_adapter import ExaContents, ExaSearch

    if settings.exa_api_key is None:
        raise ToolError("auth", "EXA_API_KEY is not set")
    key = settings.exa_api_key.get_secret_value()
    return GatewayLLM(settings), ExaSearch(key), ExaContents(key)
