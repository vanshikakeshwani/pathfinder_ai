"""Authenticated gateway smoke test (Phase A2). Never prints the API key.

Checks: basic completion + usage, strict json_schema, json_object, temperature/seed acceptance,
error-body shape. Writes the outcome to docs/gateway-compat.md and recommends LLM_STRUCTURED_MODE.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

from pydantic import BaseModel

from pathfinder.config import load_settings
from pathfinder.telemetry import utc_now


class _Probe(BaseModel):
    city: str
    population_millions: float
    tags: list[str]


PROMPT = "Return JSON describing Paris: city, approximate population_millions, and two tags."


def _check(name: str, fn) -> dict:
    started = time.perf_counter()
    try:
        detail = fn()
        return {"check": name, "ok": True, "detail": detail, "ms": round((time.perf_counter() - started) * 1000)}
    except Exception as e:  # report every failure verbatim (truncated), never the key
        return {"check": name, "ok": False, "detail": f"{type(e).__name__}: {str(e)[:300]}",
                "ms": round((time.perf_counter() - started) * 1000)}


def main() -> int:
    from openai import OpenAI

    from pathfinder.llm import strict_schema

    s = load_settings()
    if s.explabs_api_key is None:
        print("EXPLABS_API_KEY is not set; cannot run the authenticated smoke test.")
        return 2
    client = OpenAI(api_key=s.explabs_api_key.get_secret_value(), base_url=s.llm_base_url,
                    timeout=s.llm_request_timeout_s, max_retries=0)
    msgs = [{"role": "user", "content": PROMPT}]

    def basic():
        r = client.chat.completions.create(model=s.llm_model, messages=msgs)
        return {"model": r.model, "usage": r.usage.model_dump() if r.usage else None,
                "content_chars": len(r.choices[0].message.content or "")}

    def json_schema():
        r = client.chat.completions.create(model=s.llm_model, messages=msgs, response_format={
            "type": "json_schema", "json_schema": {"name": "Probe", "strict": True, "schema": strict_schema(_Probe)}})
        _Probe.model_validate_json(r.choices[0].message.content or "")
        return "validated against Pydantic schema"

    def json_object():
        r = client.chat.completions.create(model=s.llm_model, response_format={"type": "json_object"}, messages=[
            {"role": "system", "content": "Reply with JSON only: " + json.dumps(_Probe.model_json_schema())},
            *msgs])
        _Probe.model_validate_json(r.choices[0].message.content or "")
        return "validated against Pydantic schema"

    def temperature_seed():
        client.chat.completions.create(model=s.llm_model, messages=msgs, temperature=0, seed=7)
        return "accepted temperature=0 and seed=7"

    def error_shape():
        try:
            client.chat.completions.create(model="pathfinder-nonexistent-model", messages=msgs)
        except Exception as e:  # expected
            return f"{type(e).__name__} status={getattr(e, 'status_code', None)}"
        return "no error for an invalid model name"

    results = [_check(n, f) for n, f in [("basic_completion", basic), ("strict_json_schema", json_schema),
                                         ("json_object_mode", json_object), ("temperature_seed", temperature_seed),
                                         ("error_shape", error_shape)]]
    ok = {r["check"]: r["ok"] for r in results}
    mode = "json_schema" if ok["strict_json_schema"] else "json_object" if ok["json_object_mode"] else "prompt"
    lines = ["# Gateway compatibility (smoke test)", "", f"- Run at: {utc_now()}", f"- Base URL: {s.llm_base_url}",
             f"- Model: {s.llm_model}", f"- Recommended `LLM_STRUCTURED_MODE`: **{mode}**", "",
             "| Check | OK | Detail | ms |", "|---|---|---|---|"]
    lines += [f"| {r['check']} | {'yes' if r['ok'] else 'NO'} | {json.dumps(r['detail'])[:200]} | {r['ms']} |"
              for r in results]
    if not ok["temperature_seed"]:
        lines.append("\nSet `LLM_TEMPERATURE=` (empty) in .env: the gateway rejected temperature/seed.")
    text = "\n".join(lines) + "\n"
    for secret in s.secret_values():
        text = text.replace(secret, "[REDACTED]")
    Path("docs").mkdir(exist_ok=True)
    Path("docs/gateway-compat.md").write_text(text, encoding="utf-8")
    print(text)
    return 0 if ok["basic_completion"] else 1
