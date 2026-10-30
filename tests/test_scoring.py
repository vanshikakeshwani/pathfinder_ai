"""S01-S03, S05 and confidence separation."""

import pytest

from pathfinder.demo_fixtures import XY_QUESTION, xy_plan_draft
from pathfinder.models import CriterionDraft, ExtractionCandidate, SupportVerdict
from pathfinder.planner import normalize_plan
from pathfinder.scoring import (
    comparison_confidence,
    derive_score,
    discovery_confidence,
    parse_weights,
    threshold_score,
)


def cand(raw=None, proposed=None):
    return ExtractionCandidate(candidate_id="C1", source_id="SRC_1", excerpt="x" * 20, target_id="VendorY:cost",
                               entity="VendorY", claim="c", raw_value=raw, proposed_score=proposed)


def verdict(justifies=True):
    return SupportVerdict(candidate_id="C1", verdict="supports", mentions_alternative=True,
                          addresses_criterion=True, justifies_proposed_score=justifies)


def test_S01_threshold_scoring_overrides_llm_proposal(plan):
    cost = plan.criterion("cost")  # lower_is_better, strong<=20, plausible<=100
    assert [threshold_score(cost, v) for v in (9, 20, 21, 100, 101)] == [2, 2, 1, 1, 0]
    # The LLM proposed 2 for a $400 price; code computes 0 from the verified raw value.
    assert derive_score(cost, cand(raw=400, proposed=2), verdict()) == (0, "threshold")


def test_higher_is_better_thresholds(plan):
    from pathfinder.models import Anchors, Criterion, Thresholds

    c = Criterion(criterion_id="uptime", description="uptime", weight=3, direction="higher_is_better",
                  anchors=Anchors(poor="a", plausible="b", strong="c"),
                  thresholds=Thresholds(strong=99.9, plausible=99.0))
    assert [threshold_score(c, v) for v in (99.95, 99.5, 98)] == [2, 1, 0]


def test_proposal_needs_verifier_justification(plan):
    deploy = plan.criterion("deployment")  # no thresholds
    assert derive_score(deploy, cand(proposed=2), verdict(True)) == (2, "verified_proposal")
    assert derive_score(deploy, cand(proposed=2), verdict(False)) is None


def test_S02_user_weights_override_and_are_labelled():
    draft = xy_plan_draft()
    plan, _ = normalize_plan(XY_QUESTION, draft, parse_weights("cost=2,deployment=4"), 2)
    assert [(c.criterion_id, c.weight, c.weight_source) for c in plan.criteria] == \
        [("cost", 2, "user"), ("deployment", 4, "user")]


def test_S03_missing_weights_default_to_3_with_assumption():
    draft = xy_plan_draft()
    draft.criteria = [c.model_copy(update={"weight": None, "weight_source": "default"}) for c in draft.criteria]
    plan, _ = normalize_plan(XY_QUESTION, draft, {}, 2)
    assert {c.weight for c in plan.criteria} == {3}
    assert {c.weight_source for c in plan.criteria} == {"default"}
    assert any("default weight 3" in a for a in plan.assumptions)


def test_invalid_inferred_weight_falls_back_to_default():
    draft = xy_plan_draft()
    draft.criteria[0] = CriterionDraft(**{**draft.criteria[0].model_dump(), "weight": 9,
                                          "weight_source": "inferred"})
    plan, _ = normalize_plan(XY_QUESTION, draft, {}, 2)
    assert plan.criteria[0].weight == 3 and plan.criteria[0].weight_source == "default"


def test_parse_weights_rejects_out_of_range():
    with pytest.raises(ValueError):
        parse_weights("cost=7")


def test_S05_robust_but_moderate_facts_gives_moderate_confidence():
    assert comparison_confidence("robust", ["high", "moderate"]) == "moderate"
    assert comparison_confidence("robust", ["high", "high"]) == "high"
    assert comparison_confidence("provisional", ["high"]) == "moderate"
    assert comparison_confidence("undetermined", ["high"]) == "low"
    assert comparison_confidence("robust", []) == "low"


def test_S05_end_to_end_fields_are_separate():
    from conftest import run_xy

    from pathfinder.demo_fixtures import Y_REVIEW

    # Without an independent source, Y:cost rests on one undated official pricing page: the interval is
    # robust but factual confidence is moderate and the recommendation is withheld.
    r = run_xy("flip", items_override={Y_REVIEW: []}).report
    assert r.decision_stability == "robust" and r.factual_confidence == "moderate"
    assert r.recommendation_status == "withheld" and r.recommended is None and r.interval_leader == "VendorY"
    assert r.confidence == "moderate"
    # With the independent review, the same interval outcome becomes a ready, high-confidence recommendation.
    r = run_xy("flip").report
    assert r.decision_stability == "robust" and r.factual_confidence == "high"
    assert r.recommendation_status == "ready" and r.recommended == "VendorY" and r.confidence == "high"


def test_discovery_confidence():
    assert discovery_confidence(1.0, ["high"]) == "high"
    assert discovery_confidence(1.0, ["moderate", "high"]) == "moderate"
    assert discovery_confidence(0.6, ["high"]) == "moderate"
    assert discovery_confidence(0.4, ["high"]) == "low"
