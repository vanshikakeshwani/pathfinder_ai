"""v3.2: cost-dimension classification of the SCORED quantity, and product heterogeneity inside conceptual
(approach) alternatives. Excerpts are copied from the V3.1 live pilot (Q5); the scenarios are SYNTHETIC."""

import pytest
from helpers import ev

from pathfinder.consensus import classify_cost_text, cost_dimension, reachability
from pathfinder.matrix import build_cells
from pathfinder.models import AlternativeDraft, Anchors, CriterionDraft, Direction, PlanDraft
from pathfinder.planner import normalize_plan
from pathfinder.readiness import assess

REAL_COST = "The infrastructure is $530/month. The real cost is $3,530/month. That's what the pricing comparisons miss."
PINECONE = ("Cost. The s1.x1 pod sufficient for our index ran ~$70/mo per pod, and we needed 2 for redundancy. "
            "Add metadata filtering and we ended up at ~$280/mo just for vectors.")
HETZNER = "Self-hosting on a Hetzner CX33 is $9.99/month if you will operate Qdrant, Milvus, or pgvector."
BUILD = ("Initial build: 4 engineer-weeks cost $16,188 in-house, $10,800 nearshore or $7,200 offshore, once. At pilot "
         "scale the managed bill is close to its minimum.")
QDRANT_CLOUD = "Qdrant Cloud: $25 to $65 per month. Managed Qdrant pricing is based on cluster size rather than vector count."
ZILLIZ = "For low-query-volume agents (experimental systems, pilot projects), Zilliz Cloud is cheaper; you pay only for what you use."
WEAVIATE = "Weaviate Flex: 1,536M dimensions x $0.00465 = $7.14 plus under $1 of storage, so the $45 minimum applies."


def priced(target, score, src, excerpt, raw=None, unit=None, claim="synthetic claim"):
    return ev(target, score, src, excerpt=excerpt).model_copy(update={"raw_value": raw, "raw_unit": unit, "claim": claim})


# ------------------------------------------------------------------------------------------ dimensions
def test_pilot_real_cost_example_classifies_the_scored_quantity():
    total = priced("X:cost", 0, "S1", REAL_COST, 3530.0, "USD/month",
                   "Including operational overhead materially increases the monthly cost beyond infrastructure.")
    infra = priced("X:cost", 1, "S1", REAL_COST, 530.0, "USD/month", "Infrastructure is $530 per month.")
    assert cost_dimension(total) == "total_cost_of_ownership"  # v3.1 said recurring_infrastructure
    assert cost_dimension(infra) == "recurring_infrastructure"  # the same passage, a different scored amount


def test_word_boundaries_no_substring_false_positives():
    """v3.1 matched 'fte' inside 'after' and labelled a pod price as engineering labour."""
    e = priced("X:cost", 1, "S1", PINECONE, 280.0, "USD/month", "The deployment cost about $280 per month after filtering.")
    assert cost_dimension(e) == "recurring_infrastructure"


@pytest.mark.parametrize("text", [
    "The real cost is $3,530/month.", "The true cost is far higher.", "Total cost: $900 per month.",
    "Total cost of ownership over a year", "Our TCO came to $40k.", "about $500/month including engineering time",
    "infrastructure plus engineering comes to $2,100 a month", "a managed service is cheaper once engineering time is priced in",
    "It shifts costs from the vendor bill to infrastructure spend and staff time.", "the all-in cost per month",
])
def test_total_cost_wording_is_recognised(text):
    assert classify_cost_text(text) == "total_cost_of_ownership"


def test_a_monthly_amount_is_not_assumed_to_be_infrastructure():
    assert classify_cost_text("0.15 FTE costs $2,428 a month in-house") == "engineering_labour"
    assert classify_cost_text("$1,200 per month in staff time") == "engineering_labour"
    assert classify_cost_text("Hetzner CX33 is $9.99/month") == "recurring_infrastructure"


def test_engineering_build_amount_is_labour():
    e = priced("X:cost", 0, "S1", BUILD, 16188.0, "USD one-time initial build, in-house estimate")
    assert cost_dimension(e) == "engineering_labour"


# ------------------------------------------------------------------------------ plans for cell tests
def plan_of(kind="approach", names=("Managed vector database", "Self-hosted vector database")):
    crit = [CriterionDraft(criterion_id=c, description=f"{c} for a startup", direction=Direction.HIGHER_IS_BETTER,
                           weight=3, weight_source="default", anchors=Anchors(poor="p", plausible="m", strong="s"),
                           thresholds=None, time_sensitive=False, scopes=[], preferred_scope=None)
            for c in ("startup_cost", "control")]
    draft = PlanDraft(mode="comparison", alternatives=[
        AlternativeDraft(name=n, aliases=[], official_domains=[], kind=kind, defining_features=[]) for n in names],
        criteria=crit, facets=[], target_entity_count=0, assumptions=["SYNTHETIC"], initial_queries=["q"],
        search_context="")
    return normalize_plan("[SYNTHETIC] v3.2", draft, {}, 2)[0]


DOMAINS = {"A": "adaptiverecall.com", "Z": "zilliz.com", "W": "weaviate-blog.example", "C": "c17.io",
           "V": "vecstore.app", "R1": "review-one.example", "R2": "review-two.example", "R3": "review-three.example"}


def cells(plan, evidence):
    return build_cells(plan, evidence, DOMAINS, {k: None for k in DOMAINS})


M, S = "Managed vector database", "Self-hosted vector database"


def test_pilot_false_dispute_becomes_a_dimension_split():
    c = cells(plan_of(), [priced(f"{S}:startup_cost", 1, "C", HETZNER, 9.99, "USD/month"),
                          priced(f"{S}:startup_cost", 0, "V", REAL_COST, 3530.0, "USD/month",
                                 "Including operational overhead the monthly cost is far beyond infrastructure.")])
    cell = c[(S, "startup_cost")]
    assert cell.state == "scope_dependent" and cell.dimension_mismatch  # v3.1: disputed (false contradiction)
    assert set(cell.dimensions) == {"recurring_infrastructure", "total_cost_of_ownership"}


# ------------------------------------------------------------------------------- product heterogeneity
def test_category_cost_consensus_over_different_products_is_flagged_not_merged():
    """Pilot Q5 static: Zilliz (1), Qdrant Cloud (1) vs Weaviate Flex (2) -> v3.1 weak consensus at 1."""
    evidence = [priced(f"{M}:startup_cost", 1, "Z", ZILLIZ, None, None, "cheaper at low volume"),
                priced(f"{M}:startup_cost", 1, "A", QDRANT_CLOUD, None, "USD/month", "$25-65 per month"),
                priced(f"{M}:startup_cost", 2, "W", WEAVIATE, 45.0, "USD/month", "$45 monthly minimum")]
    cell = cells(plan_of(), evidence)[(M, "startup_cost")]
    assert (cell.state, cell.score, cell.dispute_kind) == ("consensus", 1, "heterogeneous")
    assert cell.heterogeneous and cell.factual_confidence == "moderate"
    rec = next(r for r in cell.consensus.values() if r.get("heterogeneous_products"))
    assert rec["heterogeneous_products"]["zilliz.com"] == ["Zilliz"]
    assert "Weaviate" in rec["heterogeneous_products"]["weaviate-blog.example"]
    assert set(cell.evidence_ids) == {e.evidence_id for e in evidence}  # nothing merged away or suppressed
    assert reachability(cell, 3)["class"] == "needs_scope_or_authority_clarification"


def test_several_sources_about_the_same_product_are_not_heterogeneous():
    evidence = [priced(f"{M}:startup_cost", 1, src, f"Qdrant Cloud starts at $25 per month ({src}).", 25.0, "USD/month")
                for src in ("R1", "R2")]
    cell = cells(plan_of(), evidence)[(M, "startup_cost")]
    assert cell.state == "supported" and not cell.heterogeneous and cell.factual_confidence == "high"


def test_approach_level_property_examples_from_different_products_are_not_flagged():
    """Non-cost criterion: Pinecone and Qdrant Cloud each illustrating 'managed limits control' are legitimate
    independent examples of an approach-level property."""
    evidence = [ev(f"{M}:control", 1, "R1", excerpt="Pinecone limits low-level index tuning."),
                ev(f"{M}:control", 1, "R2", excerpt="Qdrant Cloud restricts some network topology choices.")]
    cell = cells(plan_of(), evidence)[(M, "control")]
    assert cell.state == "supported" and not cell.heterogeneous


def test_named_alternatives_are_not_product_checked():
    plan = plan_of("named", ("Qdrant", "Weaviate"))
    evidence = [priced("Qdrant:startup_cost", 1, "R1", "Qdrant Cloud costs $25 per month; Pinecone costs more.", 25.0,
                       "USD/month"),
                priced("Qdrant:startup_cost", 1, "R2", "Hetzner hosting for Qdrant is $25 per month.", 25.0, "USD/month")]
    assert not cells(plan, evidence)[("Qdrant", "startup_cost")].heterogeneous


# ----------------------------------------------------------------------------------------- readiness
def _robust(cost_evidence):
    plan = plan_of()
    strong = [ev(t, s, src) for t, s in ((f"{M}:control", 2), (f"{S}:control", 0)) for src in ("R1", "R2")]
    self_cost = [priced(f"{S}:startup_cost", 0, src, f"Self-hosting runs $900 per month in servers ({src}).", 900.0,
                        "USD/month") for src in ("R1", "R2")]
    return plan, assess(plan, cells(plan, [*cost_evidence, *strong, *self_cost]))


def test_heterogeneous_cost_consensus_cannot_make_a_recommendation_ready():
    het = [priced(f"{M}:startup_cost", 2, "Z", ZILLIZ, None, "USD/month", "cheaper at low volume, $30 per month"),
           priced(f"{M}:startup_cost", 2, "A", QDRANT_CLOUD, None, "USD/month", "$25-65 per month"),
           priced(f"{M}:startup_cost", 1, "W", WEAVIATE, 45.0, "USD/month", "$45 monthly minimum")]
    _, r = _robust(het)
    assert r.stability == "robust" and r.status == "withheld"
    assert any(b.kind == "heterogeneous_products" for b in r.blockers)


def test_ambiguous_cost_dimension_cannot_make_a_recommendation_ready():
    vague = [priced(f"{M}:startup_cost", 2, src, f"It is cheap ({src}).", None, None, "inexpensive")
             for src in ("R1", "R2")]
    _, r = _robust(vague)
    assert r.status == "withheld" and any(b.kind == "ambiguous_cost_dimension" for b in r.blockers)


def test_clean_same_dimension_cost_evidence_can_still_be_ready():
    clean = [priced(f"{M}:startup_cost", 2, src, f"Managed plans start at $25 per month ({src}).", 25.0, "USD/month")
             for src in ("R1", "R2")]
    _, r = _robust(clean)
    assert r.status == "ready", r.reasons
