"""v3.1 source-family consensus aggregation, scope/dimension safeguards and reachable counterfactuals.

Fixtures are SYNTHETIC but mirror real V3-pilot patterns: two excerpts of one page scored 1 and 2 (Q1 Weaviate
deployment), four families against one (Q5 managed operational effort), a $20/month VPS against $9-18k of
engineering time (Q5 self-hosted startup cost)."""

from helpers import ev

from pathfinder.acquisition import POLICIES, TargetHistory, choose_next, pin_values, rank_candidates
from pathfinder.consensus import reachability
from pathfinder.matrix import build_cells
from pathfinder.models import RESOLVED_STATES, AlternativeDraft, Anchors, CriterionDraft, Direction, PlanDraft
from pathfinder.planner import normalize_plan
from pathfinder.readiness import assess

DOMAINS = {"P1": "blog-one.example", "P2": "blog-two.example", "P3": "blog-three.example", "P4": "blog-four.example",
           "P5": "blog-five.example", "GH1": "github.io", "GH2": "github.io", "SAME_A": "vendor-docs.example",
           "SAME_B": "vendor-docs.example", "OFF": "a-vendor.example", "COPY": "aggregator.example"}
URLS = {"GH1": "https://alice.github.io/post", "GH2": "https://bob.github.io/post",
        "SAME_A": "https://vendor-docs.example/v1/guide", "SAME_B": "https://vendor-docs.example/v2/guide"}


def plan_of(criteria=(("ops", 3), ("fit", 3)), official=("a-vendor.example",)):
    draft = PlanDraft(
        mode="comparison",
        alternatives=[AlternativeDraft(name="A", aliases=[], official_domains=list(official), kind="named",
                                       defining_features=[]),
                      AlternativeDraft(name="B", aliases=[], official_domains=[], kind="named", defining_features=[])],
        criteria=[CriterionDraft(criterion_id=c, description=f"{c} of the option", direction=Direction.HIGHER_IS_BETTER,
                                 weight=w, weight_source="user", anchors=Anchors(poor="p", plausible="m", strong="s"),
                                 thresholds=None, time_sensitive=False, scopes=[], preferred_scope=None)
                  for c, w in criteria],
        facets=[], target_entity_count=0, assumptions=["SYNTHETIC"], initial_queries=["q"], search_context="")
    return normalize_plan("[SYNTHETIC] consensus", draft, {c: w for c, w in criteria}, 2)[0]


def cells(plan, evidence, published=None):
    return build_cells(plan, evidence, DOMAINS, published or {}, source_urls=URLS)


def cell(evidence, target="A:ops", plan=None, published=None):
    plan = plan or plan_of()
    return cells(plan, evidence, published)[tuple(target.split(":"))]


def votes(spec, target="A:ops"):
    """spec: list of (source_id, score)."""
    return [ev(target, s, src) for src, s in spec]


# 1 -------------------------------------------------------------------------------------------- same page
def test_same_page_conflicting_excerpts_are_one_inconsistent_family_not_two_votes():
    c = cell(votes([("P1", 1), ("P1", 2)]))
    assert (c.state, c.dispute_kind, c.lower, c.upper, c.families) == ("disputed", "source_inconsistent", 1, 2, 1)
    rec = next(iter(c.consensus.values()))
    assert rec["family_count"] == 1 and len(rec["families"][0]["evidence_ids"]) == 2  # both excerpts kept
    assert "internally inconsistent" in " ".join(rec["families"][0]["notes"])


# 2 ----------------------------------------------------------------------------------- duplicates / hosts
def test_same_domain_pages_and_syndicated_copies_do_not_add_votes():
    c = cell(votes([("SAME_A", 2), ("SAME_B", 2), ("P1", 1)]))  # two pages of one publisher vs one dissent
    assert c.state == "disputed" and c.families == 2  # 1 vs 1 family, not 2 vs 1
    text = "Managed service handles upgrades and backups for you."
    copied = [ev("A:ops", 2, "P2", excerpt=text), ev("A:ops", 2, "COPY", excerpt=text), ev("A:ops", 1, "P3")]
    c2 = cell(copied)
    assert c2.families == 2 and c2.state == "disputed"  # the aggregator's copy merges into the original family
    rec = next(iter(c2.consensus.values()))
    assert any("copied/syndicated" in " ".join(f.get("notes", [])) for f in rec["families"])


def test_multi_tenant_hosts_are_separate_families_with_uncertain_independence():
    c = cell(votes([("GH1", 2), ("GH2", 2), ("P1", 1)]))
    assert c.families == 3 and c.certain_families == 1
    assert c.state == "disputed"  # 2:1 by count, but fewer than two families of certain independence (C1)
    assert "C1" in next(iter(c.consensus.values()))["decision"]


# 3 / 9 ---------------------------------------------------------------------------- qualified consensus
def test_independent_two_to_one_majority_is_a_weak_consensus_with_dissent_retained():
    c = cell(votes([("P1", 2), ("P2", 2), ("P3", 1)]))
    assert (c.state, c.score, c.lower, c.upper, c.dispute_kind) == ("consensus", 2, 2, 2, "weak")
    assert c.factual_confidence == "moderate" and c.state in RESOLVED_STATES
    rec = next(iter(c.consensus.values()))
    assert rec["supporting"] == ["blog-one.example", "blog-two.example"] and rec["dissenting"] == ["blog-three.example"]
    assert rec["disagreement"] == "rubric_interpretation" and "dissent" in rec["remaining_uncertainty"]
    assert set(c.evidence_ids) == {e for f in rec["families"] for e in f["evidence_ids"]}  # nothing dropped


def test_case_a_three_to_one_is_a_strong_consensus_but_still_discloses_dissent():
    c = cell(votes([("P1", 2), ("P2", 2), ("P3", 2), ("P4", 1)]))
    assert (c.state, c.dispute_kind, c.factual_confidence) == ("consensus", "strong", "high")
    assert next(iter(c.consensus.values()))["dissenting"] == ["blog-four.example"]


# 4 ---------------------------------------------------------------------------------- unresolved disputes
def test_case_c_one_to_one_and_two_to_two_stay_unresolved():
    one = cell(votes([("P1", 2), ("P2", 1)]))
    two = cell(votes([("P1", 2), ("P2", 2), ("P3", 1), ("P4", 1)]))
    for c in (one, two):
        assert (c.state, c.dispute_kind, c.lower, c.upper) == ("disputed", "independent_disagreement", 1, 2)


# 5 ------------------------------------------------------------------------------------- authoritative
def test_material_and_authoritative_dissent_block_majority_voting():
    opposite = cell(votes([("P1", 2), ("P2", 2), ("P3", 2), ("P4", 0)]))
    assert (opposite.state, opposite.dispute_kind) == ("disputed", "material_contradiction")
    against_self = cell(votes([("P1", 2), ("P2", 2), ("P3", 2), ("OFF", 1)]))  # vendor rates itself lower
    assert (against_self.state, against_self.dispute_kind) == ("disputed", "authoritative_dissent")
    in_own_favour = cell(votes([("P1", 1), ("P2", 1), ("P3", 1), ("OFF", 2)]))  # vendor rates itself higher
    assert in_own_favour.state == "consensus" and in_own_favour.score == 1
    measured = votes([("P1", 2), ("P2", 2), ("P3", 2)]) + [ev("A:ops", 1, "P4").model_copy(update={"score_basis": "threshold"})]
    assert cell(measured).dispute_kind == "authoritative_dissent"  # a measured value outranks judgements


# 6 -------------------------------------------------------------------------------- version-specific
def test_case_d_version_specific_dissent_is_not_outvoted():
    evidence = votes([("P1", 2), ("P2", 2), ("P3", 2), ("P4", 2)]) + [
        ev("A:ops", 1, "P5", excerpt="In version 2.3 this capability is only partly available.")]
    c = cell(evidence)
    assert (c.state, c.dispute_kind) == ("disputed", "version_specific")
    assert "version" in next(iter(c.consensus.values()))["decision"]


# 8 ------------------------------------------------------------------- unresolved inconsistency / supersession
def test_case_e_newer_document_is_noted_as_possible_supersession_not_assumed():
    pub = {"SAME_A": "2024-01-10", "SAME_B": "2026-05-02"}
    c = cell(votes([("SAME_A", 0), ("SAME_B", 2)]), published=pub)
    assert (c.state, c.dispute_kind, c.lower, c.upper) == ("disputed", "source_inconsistent", 0, 2)
    notes = " ".join(next(iter(c.consensus.values()))["families"][0]["notes"])
    assert "may supersede" in notes and "not assumed" in notes


# 7 ------------------------------------------------------------------------------------- cost dimensions
def test_infrastructure_cost_and_engineering_labour_are_not_pooled():
    plan = plan_of(criteria=(("startup_cost", 3), ("fit", 3)))
    infra = ev("B:startup_cost", 2, "P1", excerpt="Self-hosted Qdrant runs on a $20 per month VPS for 1M vectors.")
    infra = infra.model_copy(update={"raw_value": 20.0, "raw_unit": "USD/month"})
    labour = ev("B:startup_cost", 0, "P2", excerpt="That is $9,000-$18,000 in upfront engineering cost before launch.")
    labour = labour.model_copy(update={"raw_unit": "USD upfront engineering cost"})
    c = cells(plan, [infra, labour])
    cc = c[("B", "startup_cost")]
    assert cc.state == "scope_dependent" and cc.dimension_mismatch and cc.dispute_kind == "dimension_mismatch"
    assert set(cc.dimensions) == {"recurring_infrastructure", "engineering_labour"} and cc.score is None
    assert (cc.lower, cc.upper) == (0, 2)  # no unsupported conversion into one score
    # the same two facts are neither a false consensus nor a false contradiction
    assert cc.state not in ("consensus", "disputed")
    # and a leader whose own cost evidence mixes dimensions is not recommendable on that criterion
    plan2 = plan_of(criteria=(("startup_cost", 3), ("fit", 3)))
    mixed = [infra.model_copy(update={"target_id": "A:startup_cost", "entity": "A"}),
             labour.model_copy(update={"target_id": "A:startup_cost", "entity": "A"})]
    strong = [ev(t, s, src) for t, s in (("A:fit", 2), ("B:fit", 0), ("B:startup_cost", 0)) for src in ("P3", "P4")]
    r = assess(plan2, cells(plan2, mixed + strong))
    assert any(b.kind == "incomparable_dimensions" for b in r.blockers) and r.status != "ready"


def test_different_cost_dimensions_across_alternatives_are_a_comparability_issue():
    plan = plan_of(criteria=(("startup_cost", 3), ("fit", 3)))
    a = [ev("A:startup_cost", 2, s, excerpt=f"Runs on a $20 per month instance ({s}).") for s in ("P1", "P2")]
    b = [ev("B:startup_cost", 0, s, excerpt=f"Needs 0.5 FTE of engineering time ({s}).") for s in ("P3", "P4")]
    fit = [ev(t, 1, s) for t in ("A:fit", "B:fit") for s in ("P1", "P2")]
    r = assess(plan, cells(plan, a + b + fit))
    assert any("different cost dimensions" in x for x in r.comparability_issues) and r.status != "ready"


# 10 ------------------------------------------------------------------------------ consensus vs readiness
def test_a_weak_consensus_never_makes_a_recommendation_ready():
    plan = plan_of()
    two = ("P1", "P2")
    evidence = votes([("P1", 2), ("P2", 2), ("P3", 1)]) + [ev(t, s, src) for t, s in
                                                           (("B:ops", 0), ("A:fit", 2), ("B:fit", 0)) for src in two]
    c = cells(plan, evidence)
    r = assess(plan, c)
    assert r.stability == "robust" and r.status == "withheld"
    assert any(b.kind == "weak_consensus" and b.criterion_id == "ops" for b in r.blockers)


# 11 / 12 / 13 ------------------------------------------------------------------ reachable counterfactuals
def test_a_one_to_one_dispute_is_reachable_with_one_more_independent_source():
    c = cell(votes([("P1", 2), ("P2", 1)]))
    reach = reachability(c, 3)
    assert reach["class"] == "resolvable_by_one_source" and reach["reachable"] == {1: 1, 2: 1}
    assert pin_values(c, 3) == [1, 2]


def test_two_to_two_needs_multiple_sources_and_is_unreachable_with_one_search_left():
    c = cell(votes([("P1", 2), ("P2", 2), ("P3", 1), ("P4", 1)]))
    assert reachability(c, 3)["class"] == "needs_multiple_sources" and reachability(c, 3)["k"] == 2
    assert reachability(c, 1)["class"] == "unlikely_within_budget" and pin_values(c, 1) == []


def test_blocked_dispute_is_valued_low_and_labelled_not_pinned():
    plan = plan_of()
    evidence = votes([("P1", 2), ("P2", 2), ("P3", 2), ("P4", 0)]) + votes([("P5", 1)], "B:ops")
    c = cells(plan, evidence)
    reach = reachability(c[("A", "ops")], 3)
    # 2 and 0 are blocked by the opposite-end contradiction; 1 would need 8 new agreeing families
    assert reach["class"] == "unlikely_within_budget" and reach["reachable"] == {1: 8} and set(reach["why"]) == {0, 2}
    eligible, _, _ = rank_candidates(plan, c, {}, TargetHistory(), [], POLICIES["v3"], 3)
    row = next(r for r in eligible if r["target_id"] == "A:ops#conflict")
    assert row["decision_factor"] <= 0.5 and row["counterfactual"] is None
    assert any("cannot change this cell" in e for e in row["effects"])


def test_readiness_corroboration_needing_two_families_is_discounted():
    """A single github.io page cannot establish independence: two more certain families are needed."""
    plan = plan_of()
    strong = [ev(t, s, src) for t, s in (("B:ops", 0), ("A:fit", 2), ("B:fit", 0)) for src in ("P1", "P2")]
    c = cells(plan, [ev("A:ops", 2, "GH1"), *strong])
    assert c[("A", "ops")].certain_families == 0 and reachability(c[("A", "ops")], 3)["k"] == 2
    a = choose_next(plan, c, {}, TargetHistory(), [], 1, POLICIES["v3"], 3)
    assert a.target_id == "A:ops#corroborate"
    assert any("needs 2 more agreeing independent source families" in e for e in a.analysis["chosen"]["effects"])


# 15 / 16 ------------------------------------------------------------------- fairness and provenance
def test_aggregation_is_identical_for_every_arm():
    from conftest import build_ctx

    from pathfinder.acquisition import POLICIES as P
    from pathfinder.config import Settings
    from pathfinder.demo_fixtures import xy_scenario
    from pathfinder.runner import run

    results = []
    for strategy, policy in (("static", None), ("adaptive", P["v3"]), ("adaptive", P["v2_policy"])):
        ctx = build_ctx(*xy_scenario("flip"), Settings(), strategy=strategy)
        if policy:
            ctx.policy = policy
        ctx.early_stop = False
        run(ctx)
        # rebuild each arm's cells from the SAME evidence set: identical output, whatever the arm
        results.append(ctx)
    base = results[0]
    shared = [e for e in base.evidence if e.round == 0]
    assert shared and all(r.round0_hash == base.round0_hash for r in results)
    assert all(r.cells(shared) == base.cells(shared) for r in results)  # identical round 0 -> identical cells


def test_consensus_preserves_exact_provenance():
    evidence = votes([("P1", 2), ("P2", 2), ("P3", 1)])
    c = cell(evidence)
    rec = next(iter(c.consensus.values()))
    ids = {e for f in rec["families"] for e in f["evidence_ids"]}
    assert ids == {e.evidence_id for e in evidence} == set(c.evidence_ids)
    assert {d for f in rec["families"] for d in f["documents"]} == {"P1", "P2", "P3"}
    assert all((e.start, e.end) == (0, 10) for e in evidence)  # aggregation never edits evidence


def test_audit_cell_passes_on_every_pilot_pattern_and_catches_double_counting():
    from pathfinder.consensus import audit_cell

    for spec in ([("P1", 1), ("P1", 2)], [("SAME_A", 2), ("SAME_B", 2), ("P1", 1)], [("P1", 2), ("P2", 2), ("P3", 1)],
                 [("GH1", 2), ("GH2", 2), ("P1", 1)]):
        assert audit_cell(cell(votes(spec))) == []
    c = cell(votes([("P1", 2), ("P2", 2), ("P3", 1)]))
    rec = next(iter(c.consensus.values()))
    rec["families"].append(dict(rec["families"][0], family="blog-one.example"))  # tamper: count a family twice
    assert audit_cell(c)
