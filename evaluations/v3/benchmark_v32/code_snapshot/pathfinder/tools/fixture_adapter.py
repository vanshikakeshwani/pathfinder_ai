"""Offline, clearly synthetic tool clients with injectable faults (429s, 503s, empty or malformed data)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from pathfinder.tools.base import PageContent, SearchHit

SearchHandler = Callable[[str, list[str] | None], Any]


@dataclass
class FixtureSearch:
    """`handler(query, include_domains)` returns hits or an Exception (raised).

    `faults` is consumed first: each entry is an Exception to raise or None to fall through.
    """

    handler: SearchHandler
    faults: list[Exception | None] = field(default_factory=list)
    name: str = "exa_search"
    queries: list[str] = field(default_factory=list)

    def search(self, query: str, num_results: int, include_domains: list[str] | None,
               timeout: float) -> list[SearchHit]:
        self.queries.append(query)
        if self.faults:
            fault = self.faults.pop(0)
            if fault is not None:
                raise fault
        out = self.handler(query, include_domains)
        if isinstance(out, Exception):
            raise out
        return out


@dataclass
class FixtureContents:
    pages: dict[str, PageContent]
    faults: list[Exception | None] = field(default_factory=list)
    on_call: Callable[[list[str]], None] | None = None
    raw_override: Any = None  # return this instead (malformed-output tests)
    name: str = "exa_get_contents"
    calls: list[list[str]] = field(default_factory=list)

    def get_contents(self, urls: list[str], max_chars: int, timeout: float) -> list[PageContent]:
        self.calls.append(list(urls))
        if self.on_call:
            self.on_call(urls)
        if self.faults:
            fault = self.faults.pop(0)
            if fault is not None:
                raise fault
        if self.raw_override is not None:
            return self.raw_override
        return [self.pages[u].model_copy(update={"text": self.pages[u].text[:max_chars]})
                for u in urls if u in self.pages]


def keyword_search(index: list[tuple[tuple[str, ...], list[SearchHit]]]) -> SearchHandler:
    """Return the hits of the first entry whose keywords all appear in the query (case-insensitive)."""

    def handler(query: str, include_domains: list[str] | None):
        q = query.lower()
        for keywords, hits in index:
            if all(k.lower() in q for k in keywords):
                return list(hits)
        return []

    return handler
