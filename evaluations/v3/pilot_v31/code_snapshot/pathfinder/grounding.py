"""Source/evidence registry and the deterministic grounding gate.

Grounding only proves an excerpt exists verbatim in a retrieved page. It does NOT prove the excerpt
supports a claim; that is the job of verification.py.
"""

from __future__ import annotations

import re
import unicodedata
from urllib.parse import urlparse, urlunparse

from pathfinder.models import ExtractionCandidate, Source
from pathfinder.telemetry import utc_now
from pathfinder.tools.base import PageContent

MIN_EXCERPT_CHARS = 12
MIN_SOURCE_CHARS = 60
# Providers sometimes return HTTP error/redirect stubs or bot walls as "successful" page text
# (seen live: milvus.io returned "302 Found nginx/1.22.1").
_STUB_PAGE = re.compile(r"^\W*(\d{3}\s+(found|moved|moved permanently|not found|forbidden|bad gateway|"
                        r"service unavailable|internal server error)\b|access denied|just a moment|"
                        r"attention required|enable javascript)", re.IGNORECASE)
_SECOND_LEVEL = {"co", "com", "org", "net", "ac", "gov", "edu"}


def unusable_reason(text: str) -> str | None:
    if len(text) < MIN_SOURCE_CHARS:
        return f"too short ({len(text)} chars)"
    if _STUB_PAGE.match(text):
        return "HTTP error/redirect or bot-check stub"
    return None


def normalize(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).split())


def normalize_url(url: str) -> str:
    p = urlparse(url.strip())
    host = (p.hostname or "").lower()
    path = p.path.rstrip("/") or "/"
    return urlunparse((p.scheme.lower(), host, path, "", p.query, ""))


def registrable_domain(url_or_host: str) -> str:
    host = (urlparse(url_or_host).hostname or url_or_host).lower().rstrip(".")
    host = host.removeprefix("www.")
    labels = host.split(".")
    if len(labels) >= 3 and labels[-2] in _SECOND_LEVEL and len(labels[-1]) == 2:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])


class Registry:
    """App-allocated SRC_n / EV_n / CAND_n identifiers. The LLM never invents IDs that are accepted."""

    def __init__(self) -> None:
        self.sources: dict[str, Source] = {}
        self._by_url: dict[str, str] = {}
        self._unusable: dict[str, str] = {}  # normalized URL -> status; never re-fetched
        self._ev = 0
        self._cand = 0

    # sources ---------------------------------------------------------------
    def known_url(self, url: str) -> bool:
        """True for registered sources AND for URLs already fetched but found empty/unusable."""
        key = normalize_url(url)
        return key in self._by_url or key in self._unusable

    def add_page(self, page: PageContent) -> tuple[Source | None, str]:
        """Register a page. Returns (source, status), status in {"new", "duplicate", "empty", "unusable: ..."}."""
        key = normalize_url(page.url)
        if key in self._by_url:
            return self.sources[self._by_url[key]], "duplicate"
        if key in self._unusable:
            return None, self._unusable[key]
        content = normalize(page.text or "")
        reason = unusable_reason(content)
        if reason:
            status = "empty" if len(content) < MIN_EXCERPT_CHARS else f"unusable: {reason}"
            self._unusable[key] = status
            return None, status
        sid = f"SRC_{len(self.sources) + 1}"
        src = Source(source_id=sid, url=page.url, domain=registrable_domain(page.url),
                     title=normalize(page.title or "")[:200], retrieved_at=utc_now(), content=content,
                     published_at=page.published_date)
        self.sources[sid] = src
        self._by_url[key] = sid
        return src, "new"

    # ids -------------------------------------------------------------------
    def next_candidate_id(self) -> str:
        self._cand += 1
        return f"CAND_{self._cand}"

    def next_evidence_id(self) -> str:
        self._ev += 1
        return f"EV_{self._ev}"

    # grounding -------------------------------------------------------------
    def ground(self, cand: ExtractionCandidate) -> tuple[ExtractionCandidate | None, str]:
        """Check the excerpt exists in the cited source. Offsets are corrected once if needed."""
        src = self.sources.get(cand.source_id)
        if src is None:
            return None, f"unknown source id {cand.source_id}"
        excerpt = normalize(cand.excerpt)
        if len(excerpt) < MIN_EXCERPT_CHARS:
            return None, "excerpt too short"
        content = src.content
        s, e = cand.start, cand.end
        if s is not None and e is not None and 0 <= s < e <= len(content) and content[s:e] == excerpt:
            return cand.model_copy(update={"excerpt": excerpt}), "ok"
        idx = content.find(excerpt)
        if idx < 0:
            low = content.lower().find(excerpt.lower())
            if low < 0:
                return None, "excerpt not found in source text"
            idx = low
            excerpt = content[idx: idx + len(excerpt)]
        return cand.model_copy(update={"excerpt": excerpt, "start": idx, "end": idx + len(excerpt)}), \
            "offsets_corrected"

    def context_window(self, source_id: str, start: int, end: int, chars: int = 300) -> str:
        content = self.sources[source_id].content
        return content[max(0, start - chars): min(len(content), end + chars)]
