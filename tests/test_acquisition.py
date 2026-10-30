"""V3 decision-aware acquisition policy: counterfactuals, groups, readiness, conflicts, exploration (SYNTHETIC)."""

from conftest import xy_plan
from helpers import DOMAINS, PUBLISHED, ev, round0_evidence

from pathfinder.acquisition import (
    POLICIES,
    TargetHistory,
    choose_next,
    decision_relevant_open_cells,
    minimal_groups,
    outcome,
    rank_candidates,
)
from pathfinder.matrix import build_cells
from pathfinder.models import AlternativeDraft, Anchors, CriterionDraft, Direction, PlanDraft
from pathfinder.planner import normalize_plan
from pathfinder.policy import flip_relevant


def make_plan(alternatives, criteria):
    """criteria: list of (criterion_id, weight)."""
    draft = PlanDraft(
        mode="comparison",
        alternatives=[AlternativeDraft(name=a, aliases=[], official_domains=[], kind="approach",
                                       defining_features=[]) for a in alternatives],
        criteria=[CriterionDraft(criterion_id=c, description=f"{c} of the option", direction=Direction.HIGHER_IS_BETTER,
                                 weight=w, weight_source="user", anchors=Anchors(poor="p", plausible="m", strong="s"),
                                 thresholds=None, time_sensitive=False, scopes=[], preferred_scope=None)
                  for c, w in criteria],
        facets=[], target_entity_count=0, assumptions=["SYNTHETIC"], initial_queries=["q"], search_context="")
    return normalize_plan("[SYNTHETIC] policy test", draft, {c: w for c, w in criteria}, 2)[0]


def cells_of(plan, evidence):
    return build_cells(plan, evidence, DOMAINS, PUBLISHED)


def choose(plan, cells, history=None, attempts=None, issued=None, policy="v3"):
    return choose_next(plan, cells, attempts or {}, history or TargetHistory(), issued or [], 1, POLICIES[policy])


def ranked(plan, cells, history=None, attempts=None, policy="v3"):
    return rank_candidates(plan, cells, attempts or {}, history or TargetHistory(), [], POLICIES[policy])


# ----------------------------------------------------------------------------------- one decisive cell


def test_one_cell_can_change_the_winner_xy_priority_preserved(plan):
    """PF-1: X [11,11], Y [6,16]. Y:cost is the only open cell; pinning it 0/1/2 gives X robust / tie / Y robust."""
    cells = cells_of(plan, round0_evidence())
    a = choose(plan, cells)
    assert a.target_id == "VendorY:cost" and a.action_kind == "targeted"
    assert a.action_score == 10.0  # 5 (weight) x 2 (width) x 2.0 (decisive) / 2: same number as V2
    cf = a.analysis["chosen"]["counterfactual"]
    assert [(v["score"], v["leader"], v["stability"]) for v in cf["values"]] == [
        (0, "VendorX", "robust"), (1, None, "tie"), (2, "VendorY", "robust")]
    assert cf["breaks_tie"] and cf["makes_robust"]
    assert "could break the tie" in a.why_selected and "Priority 5 x 2 x 2.00" in a.why_selected


def test_S04_weight_one_lowers_priority_but_stays_decisive():
    p = xy_plan(cost_weight=1)
    a = choose(p, cells_of(p, round0_evidence()))
    assert a.target_id == "VendorY:cost" and a.action_score == 2.0 and a.analysis["chosen"]["decision_factor"] == 2.0


# ------------------------------------------------------------------------------- jointly relevant cells


def test_multiple_cells_collectively_matter_where_v2_saw_none():
    """A [15,15]; B and C each have two open cells ([6,18]). No single cell can change the leader or make it
    robust, so V2 scored every cell 'not flip-relevant'. V3 finds the minimal groups of 2."""
    p = make_plan(["A", "B", "C"], [("c1", 3), ("c2", 3), ("c3", 3)])
    evidence = [ev("A:c1", 2), ev("A:c2", 2), ev("A:c3", 1), ev("B:c1", 2), ev("C:c1", 2)]
    cells = cells_of(p, evidence)
    assert not any(flip_relevant(p, cells, a, c) for (a, c), cell in cells.items() if cell.state == "unknown")
    groups = minimal_groups(p, cells, outcome(p, cells))
    goals = {g["goal"]: g for g in groups}
    assert goals["A becomes interval-robust"]["size"] == 2
    assert goals["B overtakes A"]["size"] == 2 and goals["C overtakes A"]["size"] == 2
    eligible, _, _ = ranked(p, cells)
    assert {r["decision_factor"] for r in eligible} == {1.5}
    assert all(any("jointly matters" in e for e in r["effects"]) for r in eligible)
    assert set(decision_relevant_open_cells(p, cells)) == {"B:c2", "B:c3", "C:c2", "C:c3"}


# ------------------------------------------------------------------------------------- readiness-aware


def test_critical_missing_cell_prevents_readiness_and_is_targeted():
    """A is interval-robust, but its critical criterion (weight 5) has no support: withheld, and that cell is
    the readiness target (factor 2) even though it cannot change the leader."""
    from pathfinder.readiness import assess

    p = make_plan(["A", "B"], [("c1", 5), ("c2", 3), ("c3", 3)])
    two = [("SRC_3", "SRC_4")]  # differentiating cells have two independent sources: no other blocker
    cells = cells_of(p, [ev(t, s, src) for t, s in [("A:c2", 2), ("A:c3", 2), ("B:c2", 0), ("B:c3", 0)]
                         for src in two[0]] + [ev("B:c1", 0)])
    r = assess(p, cells)
    assert r.stability == "robust" and r.status == "withheld"
    assert any(b.kind == "critical_unsupported" and b.criterion_id == "c1" for b in r.blockers)
    a = choose(p, cells)
    assert a.target_id == "A:c1" and a.analysis["chosen"]["decision_factor"] == 2.0
    assert "readiness blocker" in a.why_selected and not a.analysis["chosen"]["counterfactual"]["changes_leader"]


def test_readiness_aware_targeting_before_robustness():
    """V2 corroborated only once robust. V3 sees a single-source differentiating cell of a PROVISIONAL leader
    as a (weaker) readiness target; with readiness_aware off it is ignored."""
    p = make_plan(["A", "B"], [("c1", 3), ("c2", 3)])
    cells = cells_of(p, [ev("A:c1", 2, "SRC_3"), ev("B:c1", 0, "SRC_4")])  # both single-source, c2 unknown
    on = {r["target_id"] for r in ranked(p, cells)[0]}
    off = {r["target_id"] for r in ranked(p, cells, policy="no_readiness")[0]}
    assert "A:c1#corroborate" in on and "A:c1#corroborate" not in off


# ------------------------------------------------------------------------------------ conflict-directed


def test_important_disagreement_beats_low_impact_empty_cell():
    p = make_plan(["A", "B"], [("c1", 5), ("c2", 1)])
    evidence = [ev("A:c1", 1, "SRC_3"), ev("A:c1", 2, "SRC_4"), ev("A:c2", 2), ev("B:c1", 1)]
    cells = cells_of(p, evidence)
    assert (cells[("A", "c1")].state, cells[("A", "c1")].lower, cells[("A", "c1")].upper) == ("disputed", 1, 2)
    a = choose(p, cells)
    assert a.target_id == "A:c1#conflict" and a.action_kind == "conflict_resolution"
    assert "detailed evidence version differences" in a.queries[0]
    assert a.action_score > next(c["priority"] for c in a.analysis["candidates"] if c["target_id"] == "B:c2")
    # with conflict-directed research off, the disputed cell is an ordinary open target with a plain query
    b = choose(p, cells, policy="no_conflict")
    assert not b.target_id.endswith("#conflict")


# --------------------------------------------------------------------------------------- low-value skip


def test_low_value_target_of_a_ruled_out_alternative_is_skipped():
    p = make_plan(["A", "B", "C"], [("c1", 3), ("c2", 3)])
    evidence = [ev("A:c1", 2), ev("A:c2", 2), ev("B:c1", 2), ev("C:c1", 0)]  # C [0,6] < A 12: ruled out
    cells = cells_of(p, evidence)
    eligible, _, ctx = ranked(p, cells)
    c_cell = next(r for r in eligible if r["target_id"] == "C:c2")
    assert c_cell["decision_factor"] == 0.5 and "C is already ruled out" in c_cell["effects"]
    assert "C" in ctx["ruled_out"]
    assert choose(p, cells).target_id == "B:c2"


# --------------------------------------------------------------------- empty start and exploration balance


def test_initial_searches_found_nothing_then_failure_moves_to_another_alternative():
    p = make_plan(["A", "B"], [("c1", 3), ("c2", 3)])
    cells = cells_of(p, [])  # empty shared round 0: every cell is a tie-breaker
    first = choose(p, cells)
    assert first.target_id == "A:c1" and first.analysis["chosen"]["decision_factor"] == 2.0
    h = TargetHistory()
    h.record(1, "A:c1", "A", success=False, decision_factor=2.0)
    second = choose(p, cells, history=h, attempts={"A:c1": 1})
    assert second.target_id.startswith("B:")  # cool-down for A:c1, concentration penalty for A, bonus for B
    skipped = {s["target_id"]: s["reason"] for s in second.analysis["skipped"]}
    assert "cool-down" in skipped["A:c1"]


def test_agent_must_explore_another_alternative():
    """A's open cell has the higher raw value (5x2x2=20 vs 3x2x2=12), but the last two rounds both went to A
    while B was never researched: 20 x 0.5 = 10 < 12 x 1.2 = 14.4, so B is researched next."""
    p = make_plan(["A", "B"], [("c1", 5), ("c2", 3)])
    cells = cells_of(p, [ev("A:c2", 1), ev("B:c1", 1)])  # open: A:c1 (w5) and B:c2 (w3), both decisive
    h = TargetHistory()
    h.record(1, "A:x", "A", True)
    h.record(2, "A:y", "A", True)
    a = choose(p, cells, history=h)
    assert a.target_id == "B:c2"
    a_row = next(c for c in a.analysis["candidates"] if c["target_id"] == "A:c1")
    assert a_row["exploration_factor"] == 0.5 and a.analysis["chosen"]["exploration_factor"] == 1.2
    assert choose(p, cells, history=h, policy="no_exploration").target_id == "A:c1"


def test_every_remaining_target_is_low_value_or_exhausted():
    p = make_plan(["A", "B"], [("c1", 3), ("c2", 3)])
    evidence = [ev("A:c1", 2, "SRC_3"), ev("A:c1", 2, "SRC_4"), ev("A:c2", 2, "SRC_3"), ev("A:c2", 2, "SRC_4"),
                ev("B:c1", 0, "SRC_3"), ev("B:c1", 0, "SRC_4")]  # A robust and ready; only B:c2 open
    cells = cells_of(p, evidence)
    a = choose(p, cells)  # nothing can change the decision: an explicit, labelled fallback
    assert a.target_id == "B:c2" and a.action_kind == "fallback_exploration"
    assert a.analysis["chosen"]["decision_factor"] == 0.5  # B is already ruled out
    assert choose(p, cells, attempts={"B:c2": 3}) is None  # exhausted -> the graph stops


# ------------------------------------------------------------------------------------- determinism / trace


def test_selection_is_deterministic_and_records_its_calculations(plan):
    cells = cells_of(plan, round0_evidence())
    a1, a2 = choose(plan, cells), choose(plan, cells)
    assert a1 == a2
    for key in ("formula", "bounds", "groups", "candidates", "skipped", "readiness_blockers", "chosen"):
        assert key in a1.analysis
    assert "not probabilities" in a1.analysis["formula"]
