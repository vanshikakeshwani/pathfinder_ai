"""F01, F03, F04, F05, F15 / V03 (disputed), S06 - interval arithmetic on SYNTHETIC X/Y."""

from helpers import cells, ev, round0_evidence

from pathfinder.matrix import bounds, decision_state, margin, robust_winner


def order(plan):
    return [a.name for a in plan.alternatives]


def test_F01_round0_intervals_no_robust_winner(plan):
    c = cells(plan, round0_evidence())
    b = bounds(plan, c)
    assert b == {"VendorX": (11, 11), "VendorY": (6, 16)}
    assert robust_winner(order(plan), b) is None
    st = decision_state(plan, c)
    # equal midpoints (11 vs 11): listed-order tie-break keeps X as leader, but stability is undetermined
    assert (st.recommended, st.stability) == ("VendorX", "undetermined")


def test_F03_y_cost_poor_makes_x_robust(plan):
    c = cells(plan, [*round0_evidence(), ev("VendorY:cost", 0, "SRC_2")])
    b = bounds(plan, c)
    assert b["VendorY"] == (6, 6)
    assert robust_winner(order(plan), b) == "VendorX"
    assert margin(order(plan), b, "VendorX") == 5


def test_F04_y_cost_strong_makes_y_robust(plan):
    c = cells(plan, [*round0_evidence(), ev("VendorY:cost", 2, "SRC_2")])
    assert bounds(plan, c)["VendorY"] == (16, 16)
    assert decision_state(plan, c).model_dump() == {"recommended": "VendorY", "stability": "robust"}


def test_F05_all_cells_supported_tie_is_not_robust(plan):
    c = cells(plan, [*round0_evidence(), ev("VendorY:cost", 1, "SRC_2")])
    b = bounds(plan, c)
    assert b == {"VendorX": (11, 11), "VendorY": (11, 11)}
    assert robust_winner(order(plan), b) is None
    assert decision_state(plan, c).stability == "undetermined"
    assert all(cell.state == "supported" for cell in c.values())


def test_F15_V03_conflicting_scores_are_disputed_full_interval(plan):
    c = cells(plan, [*round0_evidence(), ev("VendorY:cost", 2, "SRC_2"), ev("VendorY:cost", 0, "SRC_3")])
    cell = c[("VendorY", "cost")]
    assert (cell.state, cell.lower, cell.upper, cell.score) == ("disputed", 0, 2, None)
    assert cell.factual_confidence == "low"
    assert len(cell.evidence_ids) == 2


def test_S06_dispute_lower_bound_is_the_lowest_verified_score(plan):
    """V3 (deliberate change from V2's [0, 2]): a 1-vs-2 dispute keeps the verified range [1, 2]. The lower
    bound never exceeds the LOWEST verified score, the cell stays `disputed` (not supported coverage) and its
    factual confidence is low. 0 vs 2 still gives the full [0, 2]."""
    c = cells(plan, [*round0_evidence(), ev("VendorY:cost", 2, "SRC_2"), ev("VendorY:cost", 1, "SRC_3")])
    cell = c[("VendorY", "cost")]
    assert (cell.state, cell.lower, cell.upper, cell.observed_scores) == ("disputed", 1, 2, [1, 2])
    assert cell.factual_confidence == "low" and cell.score is None
    assert bounds(plan, c)["VendorY"] == (6 + 5 * 1, 6 + 5 * 2)  # LB from the lowest verified score only
    wide = cells(plan, [*round0_evidence(), ev("VendorY:cost", 2, "SRC_2"), ev("VendorY:cost", 0, "SRC_3")])
    assert (wide[("VendorY", "cost")].lower, wide[("VendorY", "cost")].upper) == (0, 2)


def test_unscored_evidence_does_not_support_a_cell(plan):
    c = cells(plan, [*round0_evidence(), ev("VendorY:cost", None, "SRC_2")])
    assert c[("VendorY", "cost")].state == "unknown"


def test_factual_confidence_rules(plan):
    # two distinct domains -> high
    c = cells(plan, [*round0_evidence(), ev("VendorY:cost", 2, "SRC_3"), ev("VendorY:cost", 2, "SRC_4")])
    assert c[("VendorY", "cost")].factual_confidence == "high"
    # official domain but undated + time-sensitive (pricing) -> moderate
    c = cells(plan, [*round0_evidence(), ev("VendorY:cost", 2, "SRC_2")])
    assert c[("VendorY", "cost")].factual_confidence == "moderate"
    # official, not time-sensitive -> high
    assert c[("VendorY", "deployment")].factual_confidence == "high"
    # single third-party source -> moderate
    c = cells(plan, [*round0_evidence(), ev("VendorY:cost", 2, "SRC_3")])
    assert c[("VendorY", "cost")].factual_confidence == "moderate"


def test_repeated_excerpt_is_not_independent_corroboration(plan):
    same = "VendorY Starter costs $9 per month for the workload"
    c = cells(plan, [*round0_evidence(), ev("VendorY:cost", 2, "SRC_3", excerpt=same),
                     ev("VendorY:cost", 2, "SRC_4", excerpt=same)])  # syndicated copy on a 2nd domain
    cell = c[("VendorY", "cost")]
    assert cell.independent_sources == 1 and cell.factual_confidence == "moderate"
    c = cells(plan, [*round0_evidence(), ev("VendorY:cost", 2, "SRC_3"), ev("VendorY:cost", 2, "SRC_4")])
    assert c[("VendorY", "cost")].independent_sources == 2 and c[("VendorY", "cost")].factual_confidence == "high"
