"""Exa adapters: two distinct operations, Search (no contents) and Get Contents.

Signatures verified against exa-py 2.26.0:
  Exa.search(query, *, contents=False, num_results, include_domains, type, timeout) -> SearchResponse
  Exa.get_contents(urls, text={"max_characters": N}, timeout=...) -> SearchResponse (results carry .text)
The SDK raises ValueError("...status code N...") for HTTP errors and ExaTimeoutError for timeouts.
"""

from __future__ import annotations

import re

from pydantic import ValidationError

from pathfinder.retry import ToolError, classify_status
from pathfinder.tools.base import PageContent, SearchHit

_STATUS = re.compile(r"status(?: code)?\D{0,3}(\d{3})", re.IGNORECASE)


def _classify(err: Exception) -> ToolError:
    from exa_py.errors import ExaTimeoutError

    if isinstance(err, ExaTimeoutError):
        return ToolError("timeout", str(err)[:300])
    msg = str(err)
    m = _STATUS.search(msg)
    if m:
        status = int(m.group(1))
        return ToolError(classify_status(status), msg[:300], status)
    if isinstance(err, ValueError):
        return ToolError("malformed", msg[:300])
    return ToolError("transient", f"{type(err).__name__}: {msg[:250]}")


class _ExaBase:
    def __init__(self, api_key: str) -> None:
        from exa_py import Exa

        self._exa = Exa(api_key=api_key)
        self.last_cost_usd: float | None = None  # provider-reported cost of the last successful call

    def _record_cost(self, resp) -> None:
        cost = getattr(resp, "cost_dollars", None)
        total = getattr(cost, "total", None)
        self.last_cost_usd = float(total) if isinstance(total, (int, float)) else None


class ExaSearch(_ExaBase):
    name = "exa_search"

    def search(self, query: str, num_results: int, include_domains: list[str] | None,
               timeout: float) -> list[SearchHit]:
        try:
            resp = self._exa.search(query, contents=False, num_results=num_results,
                                    include_domains=include_domains, type="auto", timeout=timeout)
        except Exception as e:  # classified below; never swallowed
            raise _classify(e) from e
        self._record_cost(resp)
        try:
            return [SearchHit(url=r.url, title=r.title or "", published_date=r.published_date,
                              result_id=r.id) for r in resp.results]
        except (AttributeError, ValidationError, TypeError) as e:
            raise ToolError("malformed", f"unexpected search payload: {e}") from e


class ExaContents(_ExaBase):
    name = "exa_get_contents"

    def get_contents(self, urls: list[str], max_chars: int, timeout: float) -> list[PageContent]:
        try:
            resp = self._exa.get_contents(urls, text={"max_characters": max_chars}, timeout=timeout)
        except Exception as e:
            raise _classify(e) from e
        self._record_cost(resp)
        try:
            return [PageContent(url=r.url, title=r.title or "", text=getattr(r, "text", None) or "",
                                published_date=r.published_date) for r in resp.results]
        except (AttributeError, ValidationError, TypeError) as e:
            raise ToolError("malformed", f"unexpected contents payload: {e}") from e
