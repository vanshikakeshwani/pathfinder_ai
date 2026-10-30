"""Phase 8: conservative improvements to the COMMON stopping rule (identical for every arm) (SYNTHETIC)."""

from conftest import build_ctx, run_xy

from pathfinder.config import Settings
from pathfinder.demo_fixtures import xy_scenario
from pathfinder.graph import early_stop_reason, unattempted_relevant
from pathfinder.retry import ToolError
from pathfinder.runner import run
from pathfinder.tools.fixture_adapter import keyword_search


def _nothing_found():
    llm, search, contents = xy_scenario("flip")
    search.handler = keyword_search([])  # every search returns no hits
    return llm, search, contents


def test_empty_shared_round0_is_not_counted_as_no_progress():
    """V2 premature stop Q1r1/static: round 0 found nothing, then ONE empty targeted round stopped the run."""
    ctx = build_ctx(*_nothing_found(), Settings(max_no_progress=2))
    ctx.early_stop = False
    run(ctx)
    traj = ctx.round_metrics
    assert traj[0]["new_units"] == 0 and traj[1]["new_units"] == 0
    assert traj[1]["would_stop"] is None  # V2 rule would have said no_progress here
    assert ctx.no_progress_rounds == len(traj) - 1  # only targeted rounds are counted


def test_provider_failure_round_is_not_counted_as_no_progress():
    """V2 premature stop Q4r3/adaptive: a provider timeout looked like 'research exhausted'."""
    calls = {"n": 0}
    llm, search, contents = xy_scenario("flip")
    extract = llm.handlers["extract"]

    def flaky(req):
        calls["n"] += 1
        if calls["n"] == 2:  # round 1's extraction times out (after retries the round fails)
            return ToolError("timeout", "slow")
        return extract(req)

    llm.handlers["extract"] = flaky
    ctx = build_ctx(llm, search, contents, Settings(llm_max_retries=0))
    ctx.early_stop = False
    run(ctx)
    failure_rounds = [e["round"] for e in ctx.telemetry.events if e["event"] == "provider_failure_round"]
    assert failure_rounds == [1]
    assert ctx.round_metrics[1]["provider_failure_round"] and ctx.round_metrics[1]["would_stop"] is None


def test_no_progress_deferred_while_a_decision_relevant_cell_was_never_attempted():
    ctx = build_ctx(*_nothing_found(), Settings(max_no_progress=1))
    run(ctx)  # early_stop=True: the normal CLI path
    # every cell stayed unknown; no_progress only fires once no unattempted decision-relevant cell remains
    assert ctx.stop_reason in ("insufficient_evidence", "budget_exhausted")
    deferred = [m for m in ctx.round_metrics if m["round"] >= 1 and m["would_stop"] is None]
    assert deferred, "at least one round must have been deferred by the unattempted-relevant check"


def test_the_stop_rule_is_identical_for_static_and_adaptive():
    """The rule reads only the run's own state (evidence, counters, attempts), never its strategy: with the
    same state, a static and an adaptive run get the same answer."""
    s = build_ctx(*_nothing_found(), Settings(), strategy="static")
    a = build_ctx(*_nothing_found(), Settings(), strategy="adaptive")
    for c in (s, a):
        c.early_stop = False
        run(c)
    assert s.no_progress_rounds == a.no_progress_rounds  # identical (empty) evidence in both runs
    a.attempts = dict(s.attempts)  # give both the same attempt history
    assert unattempted_relevant(a) == unattempted_relevant(s)
    assert early_stop_reason(a) == early_stop_reason(s)


def test_stable_stop_still_needs_a_ready_recommendation():
    ctx = run_xy("flip")
    assert ctx.stop_reason == "stable" and ctx.report.recommendation_status == "ready"
