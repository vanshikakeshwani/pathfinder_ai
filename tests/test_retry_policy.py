"""Phase 3: failed-target handling. No immediate repeats by default, bounded broadened retries, no permanent
blacklist, near-duplicate queries avoided, recovery without wasting the budget (SYNTHETIC)."""

from conftest import build_ctx
from helpers import ev, round0_evidence
from test_acquisition import cells_of, choose, make_plan

from pathfinder.acquisition import POLICIES, TargetHistory
from pathfinder.config import Settings
from pathfinder.demo_fixtures import X_DOCS, X_REVIEW, Y_DOCS, Y_PRICING, Y_REVIEW, xy_scenario
from pathfinder.queries import build_query, near_duplicate
from pathfinder.runner import run
from pathfinder.tools.base import SearchHit
from pathfinder.tools.fixture_adapter import keyword_search


def test_failed_target_is_not_repeated_while_other_valuable_targets_exist():
    p = make_plan(["A", "B"], [("c1", 3), ("c2", 3)])
    cells = cells_of(p, [ev("A:c2", 2), ev("B:c2", 1)])  # open: A:c1, B:c1 (both decisive)
    h = TargetHistory()
    h.record(1, "A:c1", "A", success=False, decision_factor=2.0)
    a = choose(p, cells, history=h, attempts={"A:c1": 1})
    assert a.target_id == "B:c1"
    assert any(s["target_id"] == "A:c1" and "cool-down" in s["reason"] for s in a.analysis["skipped"])


def test_bounded_retry_only_for_a_uniquely_decisive_target_and_only_once(plan):
    cells = cells_of(plan, round0_evidence())  # Y:cost is the only open cell
    h = TargetHistory()
    q0, _ = build_query(plan, "VendorY", "cost", 0)
    h.record(1, "VendorY:cost", "VendorY", success=False, decision_factor=2.0)
    a = choose(plan, cells, history=h, attempts={"VendorY:cost": 1}, issued=[q0])
    assert a.target_id == "VendorY:cost" and a.action_kind == "bounded_retry"
    assert a.queries[0] != q0 and "independent review comparison" in a.queries[0]  # broadened, not repeated
    assert a.action_score == 5.0  # retry factor 0.5 after one failure
    assert "uniquely decisive" in a.why_selected
    # a second immediate failure: no second immediate retry; only the explicit fallback path remains
    h.record(2, "VendorY:cost", "VendorY", success=False, decision_factor=2.0, immediate_retry=True)
    b = choose(plan, cells, history=h, attempts={"VendorY:cost": 2}, issued=[q0, a.queries[0]])
    assert b.target_id == "VendorY:cost" and "fallback" in b.why_selected and b.action_score == 2.5
    assert b.queries[0] not in (q0, a.queries[0])
    assert choose(plan, cells, history=h, attempts={"VendorY:cost": 3}) is None  # bounded: 3 attempts


def test_failed_target_is_revisited_later_not_blacklisted():
    p = make_plan(["A", "B"], [("c1", 5), ("c2", 1)])
    cells = cells_of(p, [ev("A:c2", 2), ev("B:c2", 0)])  # open: A:c1 (w5), B:c1 (w5)
    h = TargetHistory()
    h.record(1, "A:c1", "A", success=False, decision_factor=2.0)
    h.record(2, "B:c1", "B", success=False, decision_factor=2.0)  # A:c1 is out of its cool-down now
    a = choose(p, cells, history=h, attempts={"A:c1": 1, "B:c1": 1})
    assert a.target_id == "A:c1" and a.analysis["chosen"]["retry_factor"] == 0.5
    assert a.action_kind == "fallback_exploration" and "Revisit after 1 failed attempt" in a.why_selected


def test_near_duplicate_queries_are_skipped(plan):
    cells = cells_of(plan, round0_evidence())
    q0, _ = build_query(plan, "VendorY", "cost", 0)
    q1, _ = build_query(plan, "VendorY", "cost", 1)
    assert near_duplicate(q0 + " ", [q0]) and not near_duplicate(q1, [q0])
    a = choose(plan, cells, issued=[q0])  # attempt-0 wording already used (e.g. by an earlier query)
    assert a.queries[0] == q1
    q2, _ = build_query(plan, "VendorY", "cost", 2)
    none = choose(plan, cells, issued=[q0, q1, q2])
    assert none is None or none.target_id != "VendorY:cost"


def test_attempt_0_and_1_queries_are_unchanged_from_v2(plan):
    """The static baseline uses attempt 0; V2 adaptive used 0 and 1. Their wording must not drift."""
    assert build_query(plan, "VendorY", "cost", 0)[0] == "VendorY cost pricing plans official documentation"
    assert build_query(plan, "VendorY", "cost", 1)[0] == "VendorY cost pricing plans independent review comparison"


def _failing_first_search():
    """Fixture where the first targeted search for Y:cost (official-docs wording) finds nothing."""
    llm, search, contents = xy_scenario("flip")
    search.handler = keyword_search([
        (("vendory", "official"), []),  # attempt-0 query fails
        (("vendory", "independent"), [SearchHit(url=Y_REVIEW)]),
        (("vendorx", "independent"), [SearchHit(url=X_REVIEW)]),
        (("vendory", "pricing"), [SearchHit(url=Y_PRICING)]),
        (("vendory",), [SearchHit(url=Y_DOCS)]),
        (("vendorx",), [SearchHit(url=X_DOCS)]),
    ])
    return llm, search, contents


def test_recovery_from_a_failed_search_without_wasting_the_budget():
    ctx = build_ctx(*_failing_first_search(), Settings())
    run(ctx)
    kinds = [e["action_kind"] for e in ctx.telemetry.events if e["event"] == "action_selected"]
    outcomes = [e["success"] for e in ctx.telemetry.events if e["event"] == "target_outcome"]
    assert kinds[:3] == ["first_exploration", "targeted", "bounded_retry"]
    assert outcomes[:2] == [False, True]  # the broadened retry found the independent review
    assert ctx.report.decision_flip_count == 1 and ctx.report.interval_leader == "VendorY"
    queries = [q for e in ctx.telemetry.events if e["event"] == "action_selected" for q in e["queries"]]
    assert len(queries) == len(set(queries))  # no query issued twice
    assert sum(1 for k in kinds if k == "bounded_retry") <= 1


def test_v2_policy_arm_retries_the_same_target_like_v2():
    """The legacy-V2 arm (used as a controlled ablation) keeps V2's retry behaviour and labels it."""
    ctx = build_ctx(*_failing_first_search(), Settings())
    ctx.policy = POLICIES["v2_policy"]
    run(ctx)
    targets = [e["target_id"] for e in ctx.telemetry.events if e["event"] == "action_selected"]
    kinds = [e["action_kind"] for e in ctx.telemetry.events if e["event"] == "action_selected"]
    assert targets[1] == targets[2] == "VendorY:cost" and kinds[2] == "bounded_retry"


def test_known_unusable_page_is_not_fetched_again():
    llm, search, contents = xy_scenario("flip")
    contents.pages[Y_PRICING] = contents.pages[Y_PRICING].model_copy(update={"text": "302 Found"})  # unusable stub
    search.handler = keyword_search([(("vendory",), [SearchHit(url=Y_PRICING)]), (("vendorx",), [SearchHit(url=X_DOCS)])])
    ctx = build_ctx(llm, search, contents, Settings())
    run(ctx)
    fetched = [u for call in ctx.tools.contents_client.calls for u in call]
    assert fetched.count(Y_PRICING) == 1


def test_v2_policy_arm_uses_v2_discovery_behaviour():
    """Fairness: in discovery mode the `v2_policy` arm must not inherit V3's retry policy."""
    from pathfinder.coverage import choose_next_discovery, compute_coverage
    from pathfinder.models import Facet, Mode, ResearchPlan

    plan = ResearchPlan(question="[SYNTHETIC] discovery", mode=Mode.DISCOVERY, alternatives=[], criteria=[],
                        facets=[Facet(facet_id="hq", description="HQ", importance=5, required_count=1,
                                      search_terms="headquarters")],
                        target_entity_count=0, assumptions=["SYNTHETIC"], initial_queries=["q"], search_context="")
    cov = compute_coverage(plan, [])
    h = TargetHistory()
    h.record(1, "hq", None, success=False)
    v2 = choose_next_discovery(plan, cov, {"hq": 1}, 2, h, [], POLICIES["v2_policy"])
    v3 = choose_next_discovery(plan, cov, {"hq": 1}, 2, h, [], POLICIES["v3"])
    assert v2.target_id == "hq" and v2.action_kind == "bounded_retry" and not v2.analysis  # V2: plain retry
    assert v3.analysis.get("policy") == "v3"  # V3: failure-aware path (records its candidates)
