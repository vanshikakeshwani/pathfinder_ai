"""Graph routing and stop policy: PF-1..PF-3, F06, F11, F14, X09, X10, G04, G05 (SYNTHETIC)."""

from conftest import build_ctx, run_xy

from pathfinder.config import Settings
from pathfinder.demo_fixtures import Y_PRICING, Y_REVIEW, xy_scenario
from pathfinder.graph import build_graph
from pathfinder.retry import ToolError
from pathfinder.runner import run

VALID_STOPS = {"stable", "budget_exhausted", "no_progress", "insufficient_evidence", "error", "cancelled"}


def events(ctx, name):
    return [e for e in ctx.telemetry.events if e["event"] == name]


def test_graph_has_eight_nodes():
    nodes = set(build_graph().get_graph().nodes) - {"__start__", "__end__"}
    assert nodes == {"plan", "choose_action", "search", "retrieve", "extract", "verify", "update_state", "report"}


def test_PF1_PF2_trace_shows_round0_intervals_then_targeted_y_cost():
    ctx = run_xy("flip")
    updates = events(ctx, "cell_update")
    assert updates[0]["bounds"] == {"VendorX": [11, 11], "VendorY": [6, 16]}
    actions = events(ctx, "action_selected")
    assert [a["target_id"] for a in actions][:2] == ["initial", "VendorY:cost"]
    assert actions[1]["action_score"] == 10.0
    assert updates[1]["bounds"]["VendorY"] == [16, 16]
    # robust after round 1, but the decisive cost cells are single undated official pages: withheld,
    # so adaptive corroborates them (open queries) until the recommendation is ready
    assert events(ctx, "round_metrics")[1]["recommendation"] == "withheld"
    assert [a["target_id"] for a in actions][2:] == ["VendorX:cost#corroborate", "VendorY:cost#corroborate"]
    r = ctx.report
    assert r.stop_reason == "stable" and r.status == "complete" and r.recommendation_status == "ready"
    assert r.recommended == "VendorY" and r.interval_leader == "VendorY"


def test_PF3_F06_irrelevant_targeted_evidence_stops_no_progress():
    ctx = run_xy("irrelevant")
    assert ctx.report.stop_reason == "no_progress"
    assert ctx.cells()[("VendorY", "cost")].state == "unknown"
    assert events(ctx, "cell_update")[-1]["progress_units"] == 0
    assert ctx.report.status == "partial"


def test_F11_all_searches_fail_reports_insufficient_evidence_without_looping():
    llm, search, contents = xy_scenario("flip")
    search.faults = [ToolError("transient", "503", 503)] * 100
    ctx = build_ctx(llm, search, contents)
    run(ctx)
    assert ctx.report.stop_reason in {"insufficient_evidence", "budget_exhausted", "no_progress"}
    assert ctx.report.status == "failed" and not ctx.report.findings
    assert ctx.budget.search_calls <= ctx.settings.max_search_calls


def test_auth_failure_stops_with_error_immediately():
    llm, search, contents = xy_scenario("flip")
    search.faults = [ToolError("auth", "401", 401)]
    ctx = build_ctx(llm, search, contents)
    run(ctx)
    assert ctx.report.stop_reason == "error" and ctx.budget.search_calls == 1


def test_F14_X10_round_and_search_budgets_bound_the_run():
    ctx = run_xy("irrelevant", settings=Settings(max_research_rounds=0))
    assert ctx.report.stop_reason == "budget_exhausted"
    assert ctx.rounds_done == 1
    ctx = run_xy("flip", settings=Settings(max_search_calls=2))
    assert ctx.report.stop_reason == "budget_exhausted" and ctx.budget.search_calls == 2


def test_optional_caps_stop_with_budget_exhausted():
    ctx = run_xy("irrelevant", settings=Settings(max_llm_calls=2, max_no_progress=5))
    assert ctx.report.stop_reason in {"budget_exhausted", "insufficient_evidence"}
    assert ctx.budget.llm_calls <= 2


def test_X09_only_one_criterion_has_content_targets_the_gap():
    ctx = run_xy("flip", items_override={Y_PRICING: [], Y_REVIEW: []}, settings=Settings(max_no_progress=2))
    assert ctx.cells()[("VendorY", "cost")].state == "unknown"
    targets = [a["target_id"] for a in events(ctx, "action_selected")]
    assert targets.count("VendorY:cost") == 2  # targeted recovery, then an open-query retry
    assert any("Unknown" in lim for lim in ctx.report.limitations)


def test_G04_cancel_during_retrieve_gives_partial_report_without_more_calls():
    llm, search, contents = xy_scenario("flip")
    ctx = build_ctx(llm, search, contents)

    def cancel_on_pricing(urls):
        if Y_PRICING in urls:
            ctx.cancel.cancel()
            raise ToolError("transient", "connection dropped while cancelling")

    contents.on_call = cancel_on_pricing
    run(ctx)
    r = ctx.report
    assert r.stop_reason == "cancelled" and r.status == "partial"
    assert not [x for x in llm.requests if x.task == "report"]  # deterministic report, no further API calls


def test_G05_no_global_caps_still_terminates_within_derived_bound():
    calls = {"n": 0}

    def always_bad(req):
        calls["n"] += 1
        return "{bad json"

    s = Settings()
    assert s.max_llm_calls is None and s.max_seconds is None
    ctx = run_xy("irrelevant", settings=s, llm_overrides={"extract": always_bad, "verify": always_bad,
                                                          "report": always_bad})
    # 1 plan + (round 0 + R targeted rounds) x (extract + verify) + 1 report, each with bounded retries
    bound = (1 + (s.max_research_rounds + 1) * 2 + 1) * (1 + s.llm_max_retries)
    assert ctx.report.stop_reason in VALID_STOPS
    assert ctx.budget.llm_calls <= bound


def test_every_fixture_run_has_explicit_stop_reason():
    for variant in ("flip", "confirm", "irrelevant"):
        assert run_xy(variant).report.stop_reason in VALID_STOPS


def test_trace_contains_no_chain_of_thought_fields():
    ctx = run_xy("flip")
    for e in ctx.telemetry.events:
        assert "reasoning" not in e and "chain_of_thought" not in e
