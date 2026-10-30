"""Research-tool protocols, input/URL safety checks and the budgeted, retried tool runner.

Only two operations exist: `search` and `get_contents`. The LLM never names a tool; the graph calls
these methods directly, so retrieved text cannot add tools or change permissions.
"""

from __future__ import annotations

import ipaddress
from collections.abc import Callable
from typing import Protocol
from urllib.parse import urlparse

from pydantic import BaseModel

from pathfinder.retry import CancelToken, RetryPolicy, ToolError, call_with_retry
from pathfinder.telemetry import Budget, Telemetry

ALLOWED_TOOLS = ("exa_search", "exa_get_contents")
MAX_QUERY_CHARS = 300
MAX_RESULTS = 10
MAX_PAGE_CHARS = 20_000
_BLOCKED_SUFFIXES = (".local", ".internal", ".localhost", ".lan", ".home.arpa")


class SearchHit(BaseModel):
    url: str
    title: str = ""
    published_date: str | None = None
    result_id: str | None = None


class PageContent(BaseModel):
    url: str
    title: str = ""
    text: str = ""
    published_date: str | None = None


class SearchClient(Protocol):
    name: str

    def search(self, query: str, num_results: int, include_domains: list[str] | None,
               timeout: float) -> list[SearchHit]: ...


class ContentsClient(Protocol):
    name: str

    def get_contents(self, urls: list[str], max_chars: int, timeout: float) -> list[PageContent]: ...


def is_safe_url(url: str) -> bool:
    """https only; no localhost, private, loopback, link-local or reserved literal addresses."""
    try:
        p = urlparse(url)
    except ValueError:
        return False
    if p.scheme != "https" or not p.hostname or p.username or p.password:
        return False
    host = p.hostname.lower().rstrip(".")
    if host == "localhost" or host.endswith(_BLOCKED_SUFFIXES) or "." not in host:
        return False
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return True
    return not (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved
                or ip.is_multicast or ip.is_unspecified)


def clean_query(query: str) -> str:
    q = " ".join(query.split())
    if not q:
        raise ToolError("bad_request", "empty query")
    return q[:MAX_QUERY_CHARS]


class ToolRunner:
    """Applies safety checks, budgets, bounded retries and telemetry to the two research tools."""

    def __init__(self, search_client: SearchClient, contents_client: ContentsClient, budget: Budget,
                 telemetry: Telemetry, cancel: CancelToken, policy: RetryPolicy, timeout_s: float,
                 sleeper: Callable[[float], bool] | None = None) -> None:
        self.search_client = search_client
        self.contents_client = contents_client
        self.budget = budget
        self.telemetry = telemetry
        self.cancel = cancel
        self.policy = policy
        self.timeout_s = timeout_s
        self.sleeper = sleeper

    def search(self, query: str, num_results: int, include_domains: list[str] | None = None) -> list[SearchHit]:
        if self.budget.search_remaining <= 0:
            raise ToolError("bad_request", "search budget exhausted")
        q = clean_query(query)
        n = max(1, min(num_results, MAX_RESULTS))
        domains = [d for d in (include_domains or []) if d and "/" not in d][:5] or None
        self.budget.search_calls += 1

        def op() -> list[SearchHit]:
            return self.search_client.search(q, n, domains, self.timeout_s)

        hits = call_with_retry(op, self.policy, self.cancel,
                               lambda a: self.telemetry.tool_attempt("exa_search", q, a), self.sleeper)
        self._attach_cost(self.search_client)
        if not isinstance(hits, list) or not all(isinstance(h, SearchHit) for h in hits):
            raise ToolError("malformed", "search returned an unexpected type")
        safe = [h for h in hits if is_safe_url(h.url)]
        if len(safe) < len(hits):
            self.telemetry.event("unsafe_urls_dropped", tool="exa_search", count=len(hits) - len(safe))
        return safe[:n]

    def get_contents(self, urls: list[str]) -> list[PageContent]:
        urls = [u for u in urls if is_safe_url(u)][: self.budget.content_remaining]
        if not urls:
            raise ToolError("bad_request", "no safe URLs within content budget")
        self.budget.content_pages += len(urls)

        def op() -> list[PageContent]:
            return self.contents_client.get_contents(urls, MAX_PAGE_CHARS, self.timeout_s)

        pages = call_with_retry(op, self.policy, self.cancel,
                                lambda a: self.telemetry.tool_attempt("exa_get_contents", " ".join(urls), a),
                                self.sleeper)
        self._attach_cost(self.contents_client)
        if not isinstance(pages, list) or not all(isinstance(p, PageContent) for p in pages):
            raise ToolError("malformed", "contents returned an unexpected type")
        requested = set(urls)
        return [p for p in pages if p.url in requested]

    def _attach_cost(self, client) -> None:
        """Copy the provider-reported cost (if the client exposes one) onto the successful attempt."""
        cost = getattr(client, "last_cost_usd", None)
        if self.telemetry.tool_calls and isinstance(cost, (int, float)):
            self.telemetry.tool_calls[-1]["cost_usd"] = cost
