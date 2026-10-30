"""Record/replay wrappers for frozen, repeatable evaluations.

record: reuse a stored response for an identical call; otherwise call the real client and store the
        response (including classified errors). Reuse is what gives both evaluation arms an identical
        round 0 even though the live LLM is not deterministic.
replay: never touch the network; return the stored response or raise ToolError("replay_miss").
Keys hash the operation and its normalized parameters, so both strategies share identical responses
for identical calls (e.g. the round-0 queries and their extraction prompts).
"""

from __future__ import annotations

import hashlib
import json
import threading
from pathlib import Path
from typing import Literal

from pathfinder.llm import LLMRequest, LLMTransport, RawCompletion
from pathfinder.retry import ToolError
from pathfinder.tools.base import ContentsClient, PageContent, SearchClient, SearchHit

ReplayMode = Literal["record", "replay"]


def _key(*parts) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()


class SnapshotStore:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._lock = threading.Lock()
        self.data: dict[str, dict] = json.loads(self.path.read_text("utf-8")) if self.path.exists() else {}

    def get(self, key: str) -> dict | None:
        return self.data.get(key)

    def put(self, key: str, value: dict) -> None:
        with self._lock:
            self.data[key] = value
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(self.data, indent=1, ensure_ascii=False), encoding="utf-8")


def _replay_error(entry: dict) -> ToolError:
    return ToolError(entry["error"], entry.get("message", ""), entry.get("status"), None)


class _Base:
    def __init__(self, store: SnapshotStore, mode: ReplayMode) -> None:
        self.store = store
        self.mode = mode
        self.last_cost_usd: float | None = None

    def _lookup(self, key: str) -> dict:
        entry = self.store.get(key)
        if entry is None:
            raise ToolError("replay_miss", "no recorded response for this call")
        if "error" in entry:
            raise _replay_error(entry)
        return entry

    def _use_store(self, key: str) -> bool:
        """Replay always reads the store; record reads it when this exact call was already made."""
        return self.mode == "replay" or self.store.get(key) is not None

    def _record_error(self, key: str, err: ToolError) -> None:
        self.store.put(key, {"error": err.kind, "message": str(err)[:300], "status": err.status})


class RecordingSearch(_Base):
    name = "exa_search"

    def __init__(self, inner: SearchClient | None, store: SnapshotStore, mode: ReplayMode) -> None:
        super().__init__(store, mode)
        self.inner = inner

    def search(self, query, num_results, include_domains, timeout) -> list[SearchHit]:
        key = _key("search", query, num_results, include_domains)
        self.last_cost_usd = None
        if self._use_store(key):
            entry = self._lookup(key)
            self.last_cost_usd = entry.get("cost_usd")  # cost as recorded for this call
            return [SearchHit(**h) for h in entry["hits"]]
        assert self.inner is not None
        try:
            hits = self.inner.search(query, num_results, include_domains, timeout)
        except ToolError as err:
            self._record_error(key, err)
            raise
        self.last_cost_usd = getattr(self.inner, "last_cost_usd", None)
        self.store.put(key, {"hits": [h.model_dump() for h in hits], "cost_usd": self.last_cost_usd})
        return hits


class RecordingContents(_Base):
    name = "exa_get_contents"

    def __init__(self, inner: ContentsClient | None, store: SnapshotStore, mode: ReplayMode) -> None:
        super().__init__(store, mode)
        self.inner = inner

    def get_contents(self, urls, max_chars, timeout) -> list[PageContent]:
        key = _key("contents", sorted(urls), max_chars)
        self.last_cost_usd = None
        if self._use_store(key):
            entry = self._lookup(key)
            self.last_cost_usd = entry.get("cost_usd")
            return [PageContent(**p) for p in entry["pages"]]
        assert self.inner is not None
        try:
            pages = self.inner.get_contents(urls, max_chars, timeout)
        except ToolError as err:
            self._record_error(key, err)
            raise
        self.last_cost_usd = getattr(self.inner, "last_cost_usd", None)
        self.store.put(key, {"pages": [p.model_dump() for p in pages], "cost_usd": self.last_cost_usd})
        return pages


class RecordingLLM(_Base):
    def __init__(self, inner: LLMTransport | None, store: SnapshotStore, mode: ReplayMode,
                 model_id: str) -> None:
        super().__init__(store, mode)
        self.inner = inner
        self.model_id = f"{model_id} ({mode})"

    def complete(self, request: LLMRequest) -> RawCompletion:
        key = _key("llm", request.task, request.system, request.payload, request.schema.__name__,
                   request.feedback)
        if self._use_store(key):
            entry = self._lookup(key)
            return RawCompletion(entry["text"], entry.get("usage"))
        assert self.inner is not None
        try:
            raw = self.inner.complete(request)
        except ToolError as err:
            self._record_error(key, err)
            raise
        self.store.put(key, {"text": raw.text, "usage": raw.usage})
        return raw
