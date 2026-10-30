"""F02, S04 and policy determinism (SYNTHETIC X/Y)."""

from conftest import xy_plan
from helpers import cells, ev, round0_evidence

from pathfinder.policy import choose_next_comparison, flip_relevant, rank_targets


def test_F02_targets_y_cost_not_known_deployment(plan):
    c = cells(plan, round0_evidence())
    action = choose_next_comparison(plan, c, {}, 1)
    assert action is not None
    assert action.target_id == "VendorY:cost"
    assert action.flip_relevant is True
    assert action.action_score == 10.0  # 5 (weight) x 2 (width) x 2 (flip) / 2 (cost units)
    assert "deployment" in action.why_selected  # explains deployment is already supported
    assert action.include_domains == ["vendory.example"]  # official pricing first


def test_flip_relevance_two_extremes(plan):
    c = cells(plan, round0_evidence())
    assert flip_relevant(plan, c, "VendorY", "cost")


def test_robust_but_weak_differentiating_cells_get_corroborated(plan):
    # X robust after Y:cost=0, but the differentiating cost cells are single third-party sources
    c = cells(plan, [*round0_evidence(), ev("VendorY:cost", 0, "SRC_3")])
    a = choose_next_comparison(plan, c, {}, 1)
    assert a is not None and a.target_id.endswith("#corroborate") and a.include_domains == []
    assert "withheld" in a.why_selected


def test_no_action_when_robust_and_ready(plan):
    c = cells(plan, [*round0_evidence(), ev("VendorX:cost", 1, "SRC_3"), ev("VendorY:cost", 0, "SRC_3"),
                     ev("VendorY:cost", 0, "SRC_4")])
    assert choose_next_comparison(plan, c, {}, 1) is None


def test_S04_weight_one_changes_priority_and_outcome():
    plan = xy_plan(cost_weight=1)
    c = cells(plan, round0_evidence())
    t = rank_targets(plan, c)[0]
    # X = 1*1 + 3*2 = 7; Y = [0+6, 2+6] = [6, 8]: Y:cost is still flip-relevant but priority drops to 2
    assert (t["alternative"], t["criterion_id"], t["priority"], t["flip_relevant"]) == ("VendorY", "cost", 2.0, True)
    from pathfinder.matrix import bounds

    assert bounds(plan, c) == {"VendorX": (7, 7), "VendorY": (6, 8)}


def test_non_flip_relevant_cells_get_factor_one(plan):
    # X cost unknown but X can never lose to Y's ceiling? Construct: Y fully poor, X deploy strong, X cost unknown
    c = cells(plan, [ev("VendorX:deployment", 2), ev("VendorY:cost", 0), ev("VendorY:deployment", 0)])
    targets = {(t["alternative"], t["criterion_id"]): t for t in rank_targets(plan, c)}
    t = targets[("VendorX", "cost")]
    # X = [6, 16] vs Y = [0, 0]: X wins whether X:cost is 0 or 2 -> not flip-relevant
    assert t["flip_relevant"] is False and t["flip_factor"] == 1


def test_attempt_limit_and_retry_query(plan):
    c = cells(plan, round0_evidence())
    second = choose_next_comparison(plan, c, {"VendorY:cost": 1}, 2)
    assert second is not None and second.include_domains == [] and "Retry" in second.why_selected
    assert choose_next_comparison(plan, c, {"VendorY:cost": 2}, 3) is None


def test_deterministic_tie_break(plan):
    c = cells(plan, [])
    first = [(t["alternative"], t["criterion_id"]) for t in rank_targets(plan, c)]
    assert first == [(t["alternative"], t["criterion_id"]) for t in rank_targets(plan, c)]
    assert first[0] == ("VendorX", "cost")  # highest weight, then alternative name
