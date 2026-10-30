"""Budgets, tool/LLM call accounting and the JSONL decision trace."""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from pathfinder.config import Settings
from pathfinder.retry import Attempt


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


@dataclass
class Budget:
    """Research-action budget (always enforced) plus optional LLM/time caps."""

    max_search_calls: int
    max_content_pages: int
    max_research_rounds: int
    max_llm_calls: int | None = None
    max_seconds: float | None = None
    search_calls: int = 0  # logical operations; retries are counted separately as attempts
    content_pages: int = 0
    llm_calls: int = 0
    started: float = field(default_factory=time.monotonic)

    @classmethod
    def from_settings(cls, s: Settings) -> Budget:
        return cls(s.max_search_calls, s.max_content_pages, s.max_research_rounds,
                   s.max_llm_calls, s.max_seconds)

    @property
    def search_remaining(self) -> int:
        return max(0, self.max_search_calls - self.search_calls)

    @property
    def content_remaining(self) -> int:
        return max(0, self.max_content_pages - self.content_pages)

    @property
    def research_actions_spent(self) -> int:
        return self.search_calls + self.content_pages

    def elapsed(self) -> float:
        return time.monotonic() - self.started

    def llm_allowed(self) -> bool:
        return self.max_llm_calls is None or self.llm_calls < self.max_llm_calls

    def optional_cap_hit(self) -> str | None:
        if self.max_llm_calls is not None and self.llm_calls >= self.max_llm_calls:
            return "MAX_LLM_CALLS"
        if self.max_seconds is not None and self.elapsed() >= self.max_seconds:
            return "MAX_SECONDS"
        return None

    def snapshot(self) -> dict[str, Any]:
        return {
            "search_calls": self.search_calls, "max_search_calls": self.max_search_calls,
            "content_pages": self.content_pages, "max_content_pages": self.max_content_pages,
            "research_actions_spent": self.research_actions_spent,
            "llm_calls": self.llm_calls, "max_llm_calls": self.max_llm_calls,
            "elapsed_s": round(self.elapsed(), 2), "max_seconds": self.max_seconds,
        }


class Telemetry:
    """Collects trace events, tool attempts and LLM attempts for one run."""

    def __init__(self, run_id: str, secrets: list[str] | None = None) -> None:
        self.run_id = run_id
        self.events: list[dict[str, Any]] = []
        self.tool_calls: list[dict[str, Any]] = []
        self.llm_calls: list[dict[str, Any]] = []
        self._secrets = [s for s in (secrets or []) if s]
        self._step = 0

    def _scrub(self, value: Any) -> Any:
        if isinstance(value, str):
            for s in self._secrets:
                value = value.replace(s, "[REDACTED]")
            return value
        if isinstance(value, dict):
            return {k: self._scrub(v) for k, v in value.items()}
        if isinstance(value, list):
            return [self._scrub(v) for v in value]
        return value

    def event(self, event: str, **data: Any) -> dict[str, Any]:
        self._step += 1
        entry = {"run_id": self.run_id, "step": self._step, "ts": utc_now(), "event": event}
        entry.update(self._scrub(data))
        self.events.append(entry)
        return entry

    def tool_attempt(self, tool: str, detail: str, a: Attempt) -> None:
        self.tool_calls.append(self._scrub({
            "tool": tool, "detail": detail[:300], "attempt": a.attempt, "ok": a.ok,
            "latency_ms": round(a.latency_ms, 1), "error_kind": a.error_kind, "status": a.status,
            "message": a.message,
        }))

    def llm_attempt(self, task: str, a: Attempt, usage: dict | None = None) -> None:
        self.llm_calls.append(self._scrub({
            "task": task, "attempt": a.attempt, "ok": a.ok, "latency_ms": round(a.latency_ms, 1),
            "error_kind": a.error_kind, "status": a.status, "message": a.message, "usage": usage,
        }))

    def jsonl(self) -> str:
        return "\n".join(json.dumps(e, ensure_ascii=False) for e in self.events) + "\n"
