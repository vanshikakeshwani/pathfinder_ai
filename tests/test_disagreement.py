"""Phase 4/5: disagreements stay visible without erasing information; readiness blockers (SYNTHETIC)."""

from conftest import run_xy
from helpers import DOMAINS, PUBLISHED, cells, ev, round0_evidence
from test_acquisition import cells_of, make_plan

from pathfinder.demo_fixtures import Y_PRICING, Y_REVIEW, item
from pathfinder.matrix import build_cells, insufficient_targets
from pathfinder.models import RESOLVED_STATES, RejectedCandidate
from pathfinder.readiness import assess


def test_valid_same_scope_disagreement_is_disputed_with_its_observed_range(plan):
    c = cells(plan, [*round0_evidence(), ev("VendorY:cost", 1, "SRC_3"), ev("VendorY:cost", 2, "SRC_4")])
    cell = c[("VendorY", "cost")]
    assert (cell.state, cell.lower, cell.upper, cell.observed_scores) == ("disputed", 1, 2, [1, 2])
    assert cell.state not in RESOLVED_STATES  # never awarded supported coverage
    assert cell.score is None and cell.factual_confidence == "low"  # not averaged, not resolved
    assert len(cell.evidence_ids) == 2  # neither credible source is discarded


def test_unsupported_contradiction_does_not_create_a_dispute():
    """A 'contradicts' verdict is rejected, so it cannot turn a supported cell into a dispute."""
    reseller = "A reseller lists VendorY at $400 per month for the same workload."
    price = "VendorY (SYNTHETIC) pricing: the Starter plan costs $9 per month for the expected workload."
    ctx = run_xy("flip", text_override={Y_PRICING: f"{price} {reseller}"},
                 items_override={Y_PRICING: [item("VendorY:cost", price, "y cost $9", 2, 9, "USD/month"),
                                             item("VendorY:cost", reseller, "y cost $400", 0, 400, "USD/month")]},
                 verifier_rules={"reseller": {"verdict": "contradicts"}})
    cell = ctx.cells()[("VendorY", "cost")]
    assert cell.state == "supported" and cell.score == 2
    assert any(r.target_id == "VendorY:cost" and "contradicts" in r.reason for r in ctx.rejected)


def test_repeated_copies_are_not_independent_support_even_inside_a_dispute(plan):
    same = "VendorY Starter is priced at nine dollars a month."
    c = cells(plan, [*round0_evidence(), ev("VendorY:cost", 2, "SRC_3", excerpt=same),
                     ev("VendorY:cost", 2, "SRC_4", excerpt=same), ev("VendorY:cost", 1, "SRC_5")])
    cell = c[("VendorY", "cost")]
    assert cell.state == "disputed" and cell.independent_sources == 2  # the copy is counted once
    single = cells(plan, [*round0_evidence(), ev("VendorY:cost", 2, "SRC_3", excerpt=same),
                          ev("VendorY:cost", 2, "SRC_4", excerpt=same)])[("VendorY", "cost")]
    assert single.state == "supported" and single.independent_sources == 1 and single.factual_confidence != "high"


def test_scope_difference_is_not_a_dispute_but_a_conflict_inside_a_scope_is():
    from test_readiness import q1_plan, q1_v1_evidence

    plan = q1_plan()
    scoped = build_cells(plan, [*q1_v1_evidence(), ev("Qdrant:operational_effort", 0, "BLOG2", scope="self_hosted")],
                         {**DOMAINS, "QD": "qdrant.tech", "WV": "weaviate.io", "MV": "milvus.io",
                          "BLOG": "blog.example.org", "BLOG2": "review.example.net"}, {})
    assert scoped[("Qdrant", "operational_effort")].state == "scope_dependent"
    conflict = build_cells(plan, [*q1_v1_evidence(), ev("Qdrant:operational_effort", 1, "BLOG2", scope="managed")],
                           {**DOMAINS, "QD": "qdrant.tech", "WV": "weaviate.io", "MV": "milvus.io",
                            "BLOG": "blog.example.org", "BLOG2": "review.example.net"}, {})
    c = conflict[("Qdrant", "operational_effort")]
    assert (c.state, c.lower, c.upper) == ("disputed", 1, 2)


def test_insufficient_only_for_unscorable_on_target_evidence(plan):
    def rej(reason, stage="acceptance"):
        return RejectedCandidate(candidate_id="C", target_id="VendorY:cost", stage=stage, reason=reason, round=1)

    assert insufficient_targets([rej("no derivable fit score (no thresholds+value, ...)")]) == {"VendorY:cost"}
    assert insufficient_targets([rej("verdict=partial: other tier", "verification")]) == {"VendorY:cost"}
    for wrong in (rej("lexical check: excerpt does not name VendorY"), rej("verdict=irrelevant: x", "verification"),
                  rej("excerpt not found in source text", "grounding")):
        assert insufficient_targets([wrong]) == set()  # wrong entity / irrelevant / ungrounded: still unknown
    c = build_cells(plan, round0_evidence(), DOMAINS, PUBLISHED, insufficient={"VendorY:cost"})
    assert (c[("VendorY", "cost")].state, c[("VendorY", "cost")].lower, c[("VendorY", "cost")].upper) == \
        ("insufficient", 0, 2)


def test_coverage_counts_supported_disputed_unknown_separately():
    reseller = "A reseller lists VendorY at $400 per month for the same workload."
    price = "VendorY (SYNTHETIC) pricing: the Starter plan costs $9 per month for the expected workload."
    ctx = run_xy("flip", text_override={Y_PRICING: f"{price} {reseller}"}, items_override={
        Y_PRICING: [item("VendorY:cost", price, "y cost $9", 2, 9, "USD/month"),
                    item("VendorY:cost", reseller, "y cost $400", 0, 400, "USD/month")], Y_REVIEW: []})
    last = ctx.round_metrics[-1]
    assert last["units_disputed"] == 1 and last["units_supported"] == 3
    assert last["units_evidenced"] == 4 and last["units_unknown"] == 0
    assert last["units_supported"] + last["units_disputed"] + last["units_unknown"] + last["units_insufficient"] \
        == last["units_total"]  # units_supported already includes scope-dependent cells

# ------------------------------------------------------------------------------------- readiness blockers


def _robust_two_alt(extra=()):
    p = make_plan(["A", "B"], [("c1", 3), ("c2", 3)])
    base = [ev("A:c1", 2, "SRC_3"), ev("A:c1", 2, "SRC_4"), ev("B:c1", 0, "SRC_3"), ev("B:c1", 0, "SRC_4"),
            ev("A:c2", 2, "SRC_3"), ev("A:c2", 2, "SRC_4"), ev("B:c2", 0, "SRC_3"), ev("B:c2", 0, "SRC_4")]
    return p, [*base, *extra]


def test_like_for_like_two_source_evidence_is_ready():
    p, evidence = _robust_two_alt()
    assert assess(p, cells_of(p, evidence)).status == "ready"


def test_leader_disputed_cell_blocks_readiness():
    """v3.1: two families say 2, one says 1 -> a WEAK qualified consensus (still blocks readiness); with only
    one supporting family against one dissenting family the leader's own cell is disputed (blocks)."""
    p, evidence = _robust_two_alt([ev("A:c2", 1, "SRC_5")])
    c = cells_of(p, evidence)
    assert (c[("A", "c2")].state, c[("A", "c2")].dispute_kind, c[("A", "c2")].score) == ("consensus", "weak", 2)
    r = assess(p, c)
    assert r.stability == "robust" and r.status == "withheld"
    assert any(b.kind == "weak_consensus" and b.criterion_id == "c2" for b in r.blockers)
    one_each = [e for e in evidence if not (e.target_id == "A:c2" and e.source_id == "SRC_4")]
    r2 = assess(p, cells_of(p, one_each))
    assert r2.status == "withheld" and any(b.kind == "leader_disputed" and b.criterion_id == "c2" for b in r2.blockers)


def test_corroboration_can_disagree_and_is_reported_honestly():
    """Single-source differentiating cell -> withheld; a 'corroborating' search that finds a different score
    makes the cell disputed, and the recommendation stays withheld (no confidence is manufactured)."""
    p = make_plan(["A", "B"], [("c1", 3), ("c2", 3)])
    weak = [ev("A:c1", 2, "SRC_3"), ev("B:c1", 0, "SRC_3"), ev("B:c1", 0, "SRC_4"),
            ev("A:c2", 2, "SRC_3"), ev("A:c2", 2, "SRC_4"), ev("B:c2", 0, "SRC_3"), ev("B:c2", 0, "SRC_4")]
    before = assess(p, cells_of(p, weak))
    assert before.status == "withheld" and any(b.kind == "weak_support" for b in before.blockers)
    after = assess(p, cells_of(p, [*weak, ev("A:c1", 1, "SRC_5")]))
    assert after.status == "withheld" and any(b.kind == "leader_disputed" for b in after.blockers)


def test_self_reported_evaluative_claim_blocks_readiness_but_measured_facts_do_not():
    from pathfinder.models import AlternativeDraft, Anchors, CriterionDraft, Direction, PlanDraft
    from pathfinder.planner import normalize_plan

    draft = PlanDraft(mode="comparison", alternatives=[
        AlternativeDraft(name="A", aliases=[], official_domains=["a-vendor.example"], kind="named", defining_features=[]),
        AlternativeDraft(name="B", aliases=[], official_domains=["b-vendor.example"], kind="named", defining_features=[])],
        criteria=[CriterionDraft(criterion_id=cid, description=cid, direction=Direction.HIGHER_IS_BETTER, weight=3,
                                 weight_source="default", anchors=Anchors(poor="p", plausible="m", strong="s"),
                                 thresholds=None, time_sensitive=False, scopes=[], preferred_scope=None)
                  for cid in ("ease", "fit")],
        facets=[], target_entity_count=0, assumptions=["SYNTHETIC"], initial_queries=["q"], search_context="")
    p = normalize_plan("[SYNTHETIC]", draft, {}, 2)[0]
    domains = {"OA": "a-vendor.example", "R1": "review-one.example", "R2": "review-two.example"}
    same = [ev(f"{a}:fit", 1, src) for a in ("A", "B") for src in ("R1", "R2")]  # equal: not differentiating
    evidence = [ev("A:ease", 2, "OA"), ev("B:ease", 0, "R1"), ev("B:ease", 0, "R2"), *same]
    c = build_cells(p, evidence, domains, {k: None for k in domains})
    assert c[("A", "ease")].self_reported_only and c[("A", "ease")].factual_confidence == "high"
    r = assess(p, c)
    assert r.status == "withheld" and any(b.kind == "self_reported" for b in r.blockers)
    measured = ev("A:ease", 2, "OA")
    measured = measured.model_copy(update={"score_basis": "threshold"})
    c2 = build_cells(p, [measured, *evidence[1:]], domains, {k: None for k in domains})
    assert not c2[("A", "ease")].self_reported_only and assess(p, c2).status == "ready"
