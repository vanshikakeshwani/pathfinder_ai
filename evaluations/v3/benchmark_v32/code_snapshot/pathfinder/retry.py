"""Shared error classification, bounded retry and cancellation for Exa and the LLM gateway."""

from __future__ import annotations

import random
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal, TypeVar

ErrorKind = Literal["rate_limited", "transient", "timeout", "auth", "malformed", "bad_request",
                    "cancelled", "replay_miss"]
RETRYABLE: frozenset[str] = frozenset({"rate_limited", "transient", "timeout"})
RETRY_AFTER_CEILING_S = 60.0

T = TypeVar("T")


class ToolError(Exception):
    """A classified failure from an external call."""

    def __init__(self, kind: ErrorKind, message: str = "", status: int | None = None,
                 retry_after: float | None = None):
        super().__init__(message or kind)
        self.kind = kind
        self.status = status
        self.retry_after = retry_after


class Cancelled(Exception):
    """Raised when the run's cancel token is set."""


class CancelToken:
    def __init__(self) -> None:
        self._event = threading.Event()

    def cancel(self) -> None:
        self._event.set()

    def is_set(self) -> bool:
        return self._event.is_set()

    def wait(self, seconds: float) -> bool:
        """Interruptible sleep. Returns True if cancelled during the wait."""
        return self._event.wait(max(0.0, seconds))

    def check(self) -> None:
        if self.is_set():
            raise Cancelled()


def classify_status(status: int | None) -> ErrorKind:
    if status == 429:
        return "rate_limited"
    if status in (401, 403):
        return "auth"
    if status is not None and status >= 500:
        return "transient"
    if status in (408,):
        return "timeout"
    return "bad_request"


@dataclass
class RetryPolicy:
    max_retries: int = 2
    base_delay_s: float = 0.5
    max_delay_s: float = 8.0
    jitter: bool = True

    def delay(self, attempt: int, retry_after: float | None) -> float:
        if retry_after is not None:
            return min(max(retry_after, 0.0), RETRY_AFTER_CEILING_S)
        d = min(self.base_delay_s * (2 ** (attempt - 1)), self.max_delay_s)
        return d * (0.5 + random.random() / 2) if self.jitter else d


@dataclass
class Attempt:
    attempt: int
    ok: bool
    latency_ms: float
    error_kind: str | None = None
    status: int | None = None
    message: str = ""


def call_with_retry(fn: Callable[[], T], policy: RetryPolicy, cancel: CancelToken,
                    on_attempt: Callable[[Attempt], None] | None = None,
                    sleeper: Callable[[float], bool] | None = None,
                    retryable: frozenset[str] = RETRYABLE) -> T:
    """Run fn with bounded retries. Every attempt is reported via on_attempt.

    Raises ToolError for exhausted/non-retryable failures and Cancelled if cancelled.
    `sleeper` returns True when the wait was interrupted (defaults to cancel.wait).
    """
    sleeper = sleeper or cancel.wait
    attempts = policy.max_retries + 1
    for attempt in range(1, attempts + 1):
        cancel.check()
        started = time.perf_counter()
        try:
            result = fn()
        except ToolError as err:
            latency = (time.perf_counter() - started) * 1000
            if on_attempt:
                on_attempt(Attempt(attempt, False, latency, err.kind, err.status, str(err)[:200]))
            if err.kind not in retryable or attempt == attempts:
                raise
            if sleeper(policy.delay(attempt, err.retry_after)):
                raise Cancelled() from err
            continue
        latency = (time.perf_counter() - started) * 1000
        if on_attempt:
            on_attempt(Attempt(attempt, True, latency))
        return result
    raise AssertionError("unreachable")  # pragma: no cover
