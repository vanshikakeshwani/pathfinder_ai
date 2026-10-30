"""D01-D06: a decision change counts only when newly verified evidence changes the recommendation
or its supported status (SYNTHETIC X/Y)."""

from conftest import run_xy, xy_plan
from helpers import cells, ev, round0_evidence

from pathfinder.policy import detect_decision_change


def change(plan, before_ev, new_ev, plan_after=None):
    plan_after = plan_after or plan
    cb = cells(plan, before_ev)
    ca = cells(plan_after, before_ev + new_ev)
    cw = cells(plan_after, before_ev)
    return detect_decision_change(plan, plan_after, cb, ca, cw, [e.evidence_id for e in new_ev], 1)


def test_D01_leader_change_counted(plan):
    new = [ev("VendorY:cost", 2, "SRC_2")]
    c, _ = change(plan, round0_evidence(), new)
    assert c is not None and c.kind == "leader_changed"
    assert c.before.recommended == "VendorX" and c.after.recommended == "VendorY"
    assert c.evidence_ids == [new[0].evidence_id]


def test_D01_end_to_end_flip_count():
    r = run_xy("flip").report
    assert r.decision_flip_count == 1 and r.status_change_count == 0
    assert r.recommended == "VendorY" and r.stop_reason == "stable"


def test_D02_same_leader_becomes_robust_is_status_change(plan):
    c, _ = change(plan, round0_evidence(), [ev("VendorY:cost", 0, "SRC_2")])
    assert c is not None and c.kind == "became_robust"
    r = run_xy("confirm").report
    assert (r.decision_flip_count, r.status_change_count, r.recommended) == (0, 1, "VendorX")


def test_D03_new_criterion_narrowing_without_status_change_not_counted(plan):
    # Start: X cost=2, X deploy=2 (X=[16,16]); Y deploy=0 -> Y=[0,10]; X robust.
    before = [ev("VendorX:cost", 2), ev("VendorX:deployment", 2), ev("VendorY:deployment", 0)]
    c, note = change(plan, before, [ev("VendorY:cost", 1)])  # narrows Y to [5,5]; X still robust
    assert c is None and "no change" in note


def test_D04_score_change_without_recommendation_change_not_counted(plan):
    # X robust (11 vs 6). A dispute on Y:deployment (2 vs 1 -> [1, 2]) changes Y's interval but not the
    # recommendation or its status: not a decision change.
    before = [*round0_evidence(), ev("VendorY:cost", 0, "SRC_2")]
    c, _ = change(plan, before, [ev("VendorY:deployment", 1, "SRC_3")])
    assert c is None


def test_D04b_tie_to_leader_counts_under_v2_rule_but_is_not_a_strong_flip(plan):
    """Y:cost 1 makes a tie (X 11 = Y 11). A 2-vs-1 dispute ([1, 2]) makes Y the provisional leader. The
    preserved V2 definition counts this as `leader_changed` (as for D01); the stricter V3 metric does not,
    because the previous state was a tie, not a real leader."""
    from pathfinder.policy import is_strong_flip

    before = [*round0_evidence(), ev("VendorY:cost", 1)]
    c, _ = change(plan, before, [ev("VendorY:cost", 2, "SRC_3")])
    assert c is not None and c.kind == "leader_changed" and c.before.stability == "undetermined"
    assert not is_strong_flip(c)


def test_D05_weight_edit_not_counted(plan):
    edited = xy_plan(cost_weight=1)  # X=[7,7], Y=[6,8] with Y:cost unknown; with Y:cost=2 -> Y=[8,8]
    c, note = change(plan, round0_evidence(), [ev("VendorY:cost", 2)], plan_after=edited)
    assert c is None and "weight" in note


def test_D06_conflict_removes_robustness(plan):
    before = [*round0_evidence(), ev("VendorY:cost", 0, "SRC_2")]  # X robust
    c, _ = change(plan, before, [ev("VendorY:cost", 2, "SRC_3")])  # dispute -> Y back to [6,16]
    assert c is not None and c.kind == "lost_robustness"


def test_no_new_evidence_never_counts(plan):
    after = cells(plan, [*round0_evidence(), ev("VendorY:cost", 0)])  # X robust, but nothing new this round
    c, note = detect_decision_change(plan, plan, cells(plan, round0_evidence()), after,
                                     cells(plan, round0_evidence()), [], 1)
    assert c is None and "no newly verified" in note


def test_leader_appearing_while_undetermined_is_not_a_change(plan):
    c, note = change(plan, [], round0_evidence())  # (None, undetermined) -> (X by tie-break, undetermined)
    assert c is None and "no change" in note

