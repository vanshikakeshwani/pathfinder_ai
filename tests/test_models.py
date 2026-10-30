import pytest
from pydantic import ValidationError

from pathfinder.models import (
    Anchors,
    Criterion,
    Direction,
    Evidence,
    ExtractionBatch,
    ResearchPlan,
    Thresholds,
)

A = Anchors(poor="p", plausible="m", strong="s")


def crit(cid="cost", **kw):
    return Criterion(criterion_id=cid, description=cid, weight=kw.pop("weight", 3), anchors=A, **kw)


def test_weight_must_be_1_to_5():
    with pytest.raises(ValidationError):
        crit(weight=6)
    with pytest.raises(ValidationError):
        crit(weight=0)


def test_threshold_order_respects_direction():
    crit(direction=Direction.LOWER_IS_BETTER, thresholds=Thresholds(strong=20, plausible=100))
    with pytest.raises(ValidationError):
        crit(direction=Direction.LOWER_IS_BETTER, thresholds=Thresholds(strong=100, plausible=20))
    with pytest.raises(ValidationError):
        crit(direction=Direction.HIGHER_IS_BETTER, thresholds=Thresholds(strong=1, plausible=5))


def test_comparison_requires_two_alternatives():
    with pytest.raises(ValidationError, match="2-4 alternatives"):
        ResearchPlan(question="q", mode="comparison", alternatives=[{"name": "A"}],
                     criteria=[crit("a"), crit("b")], assumptions=["x"], initial_queries=["q"])


def test_plan_requires_assumptions_and_queries():
    with pytest.raises(ValidationError):
        ResearchPlan(question="q", mode="discovery", facets=[{"facet_id": "f", "description": "d",
                                                               "importance": 3}],
                     assumptions=[], initial_queries=["q"])


def test_evidence_offsets_validated():
    with pytest.raises(ValidationError):
        Evidence(evidence_id="EV_1", candidate_id="C", source_id="SRC_1", excerpt="x", start=5, end=5,
                 target_id="t", entity="e", claim="c")


def test_llm_output_rejects_unexpected_fields():
    """An injected 'tool' instruction smuggled into model output is a schema violation, not an action."""
    with pytest.raises(ValidationError):
        ExtractionBatch.model_validate({"items": [], "tool": "shell", "command": "cat .env"})
