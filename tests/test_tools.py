"""Tool layer: X01-X04, G02, G03, URL safety, Exa error classification."""

import pytest

from pathfinder.config import Settings
from pathfinder.retry import CancelToken, RetryPolicy, ToolError, call_with_retry
from pathfinder.telemetry import Budget, Telemetry
from pathfinder.tools.base import MAX_QUERY_CHARS, PageContent, SearchHit, ToolRunner, is_safe_url
from pathfinder.tools.fixture_adapter import FixtureContents, FixtureSearch

HIT = SearchHit(url="https://docs.example.com/a", title="a")


def runner(search, contents=None, **budget_kw):
    s = Settings(**budget_kw)
    t = Telemetry("T")
    r = ToolRunner(search, contents or FixtureContents({}), Budget.from_settings(s), t, CancelToken(),
                   RetryPolicy(max_retries=2), 5.0, sleeper=lambda _s: False)
    return r, t


def test_X01_429_then_success_bounded_and_logged():
    r, t = runner(FixtureSearch(lambda q, d: [HIT], faults=[ToolError("rate_limited", "429", 429, 1.0)]))
    assert r.search("q", 5) == [HIT]
    assert [(c["attempt"], c["ok"], c["error_kind"]) for c in t.tool_calls] == \
        [(1, False, "rate_limited"), (2, True, None)]
    assert r.budget.search_calls == 1  # one logical search, two attempts


def test_X02_permanent_503_fails_after_bounded_retries():
    faults = [ToolError("transient", "503", 503)] * 10
    r, t = runner(FixtureSearch(lambda q, d: [HIT], faults=list(faults)))
    with pytest.raises(ToolError) as e:
        r.search("q", 5)
    assert e.value.kind == "transient" and len(t.tool_calls) == 3


def test_auth_error_not_retried():
    r, t = runner(FixtureSearch(lambda q, d: [HIT], faults=[ToolError("auth", "401", 401)]))
    with pytest.raises(ToolError):
        r.search("q", 5)
    assert len(t.tool_calls) == 1


def test_X04_malformed_tool_output_fails_safely():
    r, _ = runner(FixtureSearch(lambda q, d: [{"url": "https://x.example"}]))
    with pytest.raises(ToolError) as e:
        r.search("q", 5)
    assert e.value.kind == "malformed"
    r, _ = runner(FixtureSearch(lambda q, d: [HIT]), FixtureContents({}, raw_override="not a list"))
    with pytest.raises(ToolError):
        r.get_contents([HIT.url])


def test_G02_retry_after_is_honoured_with_ceiling():
    waits = []
    calls = iter([ToolError("rate_limited", "429", 429, retry_after=3.0),
                  ToolError("rate_limited", "429", 429, retry_after=999.0), "ok"])

    def fn():
        v = next(calls)
        if isinstance(v, Exception):
            raise v
        return v

    assert call_with_retry(fn, RetryPolicy(max_retries=2), CancelToken(),
                           sleeper=lambda s: waits.append(s) or False) == "ok"
    assert waits == [3.0, 60.0]


def test_G03_timeouts_count_as_attempts():
    r, t = runner(FixtureSearch(lambda q, d: [HIT], faults=[ToolError("timeout", "t")] * 2))
    assert r.search("q", 5) == [HIT]
    assert [c["error_kind"] for c in t.tool_calls] == ["timeout", "timeout", None]


def test_cancel_during_backoff_raises_cancelled():
    from pathfinder.retry import Cancelled

    token = CancelToken()

    def fn():
        token.cancel()
        raise ToolError("transient", "x")

    with pytest.raises(Cancelled):
        call_with_retry(fn, RetryPolicy(max_retries=3), token)


@pytest.mark.parametrize("url,ok", [
    ("https://docs.example.com/a", True), ("http://docs.example.com/a", False),
    ("https://localhost/x", False), ("https://127.0.0.1/x", False), ("https://10.0.0.5/x", False),
    ("https://169.254.169.254/latest", False), ("https://[::1]/x", False), ("https://intranet/x", False),
    ("https://printer.local/x", False), ("https://user:pw@example.com/", False), ("file:///etc/passwd", False),
])
def test_url_safety(url, ok):
    assert is_safe_url(url) is ok


def test_unsafe_hits_dropped_and_query_capped():
    s = FixtureSearch(lambda q, d: [HIT, SearchHit(url="https://192.168.1.1/admin")])
    r, t = runner(s)
    assert r.search("x" * 1000, 50) == [HIT]
    assert len(s.queries[0]) == MAX_QUERY_CHARS
    assert any(e["event"] == "unsafe_urls_dropped" for e in t.events)


def test_budgets_enforced():
    r, _ = runner(FixtureSearch(lambda q, d: [HIT]), max_search_calls=1)
    r.search("q", 5)
    with pytest.raises(ToolError, match="budget"):
        r.search("q2", 5)
    pages = {HIT.url: PageContent(url=HIT.url, text="hello world text")}
    r, _ = runner(FixtureSearch(lambda q, d: [HIT]), FixtureContents(pages), max_content_pages=1)
    assert len(r.get_contents([HIT.url, "https://other.example/b"])) == 1
    assert r.budget.content_pages == 1


def test_exa_error_classification():
    from pathfinder.tools.exa_adapter import _classify

    assert _classify(ValueError("Request failed with status code 429: slow down")).kind == "rate_limited"
    assert _classify(ValueError("Request failed with status code 401: bad key")).kind == "auth"
    assert _classify(ValueError("Request failed with status code 503")).kind == "transient"
    assert _classify(ValueError("Expected a JSON response but received a non-JSON body")).kind == "malformed"
