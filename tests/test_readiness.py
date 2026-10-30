"""Phase-2 regressions: comparable scoring context and recommendation readiness. SYNTHETIC.

V1 Q1: Qdrant got operational effort 2 from managed-cloud docs while Weaviate (1) and Milvus (0) were scored
from self-hosting weaknesses; the interval engine declared Qdrant robust and it was reported as a winner.
"""

from helpers import ev

from pathfinder.matrix import bounds, build_cells
from pathfinder.models import AlternativeDraft, Anchors, CriterionDraft, Direction, PlanDraft
from pathfinder.planner import normalize_plan
from pathfinder.readiness import assess, comparability_issues, corroboration_targets

ALTS = ["Qdrant", "Weaviate", "Milvus"]
DOMAINS = {"QD": "qdrant.tech", "WV": "weaviate.io", "MV": "milvus.io", "BLOG": "blog.example.org",
           "BLOG2": "review.example.net", "BLOG3": "third.example.com"}


def q1_plan(preferred: str | None = None):
    def crit(cid, scopes=(), pref=None):
        return CriterionDraft(criterion_id=cid, description=cid, direction=Direction.HIGHER_IS_BETTER, weight=3,
                              weight_source="inferred", anchors=Anchors(poor="p", plausible="m", strong="s"),
                              thresholds=None, time_sensitive=False, scopes=list(scopes), preferred_scope=pref)

    draft = PlanDraft(mode="comparison",
                      alternatives=[AlternativeDraft(name=a, aliases=[], official_domains=[d], kind="named",
                                                     defining_features=[])
                                    for a, d in zip(ALTS, ["qdrant.tech", "weaviate.io", "milvus.io"], strict=True)],
                      criteria=[crit("deployment"), crit("filtering"),
                                crit("operational_effort", ("managed", "self_hosted"), preferred)],
                      facets=[], target_entity_count=0, assumptions=["SYNTHETIC"], initial_queries=["q"],
                      search_context="")
    return normalize_plan("[SYNTHETIC] Q1-like", draft, {}, 2)[0]


def q1_v1_evidence():
    """Mirror of the V1 Q1 run: equal deployment/filtering, asymmetric ops evidence."""
    out = []
    for a, src in zip(ALTS, ["QD", "WV", "MV"], strict=True):
        out += [ev(f"{a}:deployment", 2, src), ev(f"{a}:filtering", 2, src)]
    out += [ev("Qdrant:operational_effort", 2, "QD", scope="managed"),       # managed-cloud docs
            ev("Weaviate:operational_effort", 1, "BLOG", scope="self_hosted"),  # third-party weaknesses list
            ev("Milvus:operational_effort", 0, "BLOG", scope="self_hosted")]    # self-hosting complaint
    return out


def cells_for(plan, evidence):
    return build_cells(plan, evidence, DOMAINS, {})


def test_q1_asymmetric_scopes_interval_robust_but_recommendation_withheld():
    plan = q1_plan()
    cells = cells_for(plan, q1_v1_evidence())
    assert bounds(plan, cells) == {"Qdrant": (18, 18), "Weaviate": (15, 15), "Milvus": (12, 12)}
    r = assess(plan, cells)
    assert r.interval_leader == "Qdrant" and r.stability == "robust"  # the mathematics is unchanged...
    assert r.status == "withheld"  # ...but no authoritative recommendation
    assert any("not a like-for-like comparison" in x for x in r.reasons)
    assert "operational_effort" in comparability_issues(plan, cells)


def test_q1_corroboration_targets_competitors_in_the_comparable_scope():
    plan = q1_plan()
    targets = corroboration_targets(plan, cells_for(plan, q1_v1_evidence()))
    by_alt = {t["alternative"]: t for t in targets}
    assert by_alt["Weaviate"]["scope"] == "managed" and by_alt["Milvus"]["scope"] == "managed"
    assert by_alt["Weaviate"]["reason"] == "comparability"


def test_preferred_scope_excludes_other_context_evidence_from_scoring():
    plan = q1_plan(preferred="managed")
    cells = cells_for(plan, q1_v1_evidence())
    assert cells[("Weaviate", "operational_effort")].state == "unknown"
    assert cells[("Weaviate", "operational_effort")].excluded_evidence_ids  # kept, but not scored
    r = assess(plan, cells)
    assert r.stability != "robust" and r.status != "ready"


def test_like_for_like_strong_evidence_makes_recommendation_ready():
    plan = q1_plan()
    evidence = [e for e in q1_v1_evidence() if "operational_effort" not in e.target_id]
    evidence += [ev("Qdrant:operational_effort", 2, "QD", scope="managed"),
                 ev("Qdrant:operational_effort", 2, "BLOG2", scope="managed"),
                 ev("Weaviate:operational_effort", 1, "BLOG", scope="managed"),
                 ev("Weaviate:operational_effort", 1, "BLOG3", scope="managed"),
                 ev("Milvus:operational_effort", 0, "BLOG", scope="managed"),
                 ev("Milvus:operational_effort", 0, "BLOG2", scope="managed")]
    r = assess(plan, cells_for(plan, evidence))
    assert not r.comparability_issues
    assert r.status == "ready" and r.interval_leader == "Qdrant"


def test_single_source_is_disclosed_and_blocks_only_differentiating_cells():
    plan = q1_plan()
    evidence = [e for e in q1_v1_evidence() if "operational_effort" not in e.target_id]
    evidence += [ev("Qdrant:operational_effort", 2, "BLOG", scope="managed"),     # single third-party source
                 ev("Weaviate:operational_effort", 1, "BLOG2", scope="managed"),
                 ev("Weaviate:operational_effort", 1, "BLOG3", scope="managed"),
                 ev("Milvus:operational_effort", 0, "BLOG2", scope="managed"),
                 ev("Milvus:operational_effort", 0, "BLOG3", scope="managed")]
    r = assess(plan, cells_for(plan, evidence))
    assert "Qdrant:deployment" in r.single_source_cells  # disclosed even though it is not differentiating
    assert r.weak_differentiating_cells == [("Qdrant", "operational_effort")]
    assert r.status == "withheld"


def test_repeated_excerpt_does_not_upgrade_a_differentiating_cell():
    plan = q1_plan()
    evidence = [e for e in q1_v1_evidence() if "operational_effort" not in e.target_id]
    same = "Managed cloud handles scaling, backups and upgrades for you."
    evidence += [ev("Qdrant:operational_effort", 2, "BLOG", scope="managed", excerpt=same),
                 ev("Qdrant:operational_effort", 2, "BLOG2", scope="managed", excerpt=same),
                 ev("Weaviate:operational_effort", 1, "BLOG", scope="managed"),
                 ev("Weaviate:operational_effort", 1, "BLOG3", scope="managed"),
                 ev("Milvus:operational_effort", 0, "BLOG", scope="managed"),
                 ev("Milvus:operational_effort", 0, "BLOG2", scope="managed")]
    cells = cells_for(plan, evidence)
    assert cells[("Qdrant", "operational_effort")].independent_sources == 1
    assert assess(plan, cells).status == "withheld"


def test_different_contexts_in_one_cell_are_scope_dependent_not_disputed():
    """Regression from the V2 pilot: Qdrant ops had managed=2 and self_hosted=0 evidence and was labelled
    'disputed', misreporting a context difference as a factual conflict."""
    from pathfinder.policy import rank_targets

    plan = q1_plan()
    evidence = q1_v1_evidence() + [ev("Qdrant:operational_effort", 0, "BLOG2", scope="self_hosted")]
    cells = cells_for(plan, evidence)
    cell = cells[("Qdrant", "operational_effort")]
    assert (cell.state, cell.lower, cell.upper) == ("scope_dependent", 0, 2)
    assert cell.scope_scores == {"managed": 2, "self_hosted": 0}
    assert ("Qdrant", "operational_effort") not in {(t["alternative"], t["criterion_id"])
                                                    for t in rank_targets(plan, cells)}
    # a real conflict within ONE context is still a dispute
    evidence = q1_v1_evidence() + [ev("Qdrant:operational_effort", 0, "BLOG2", scope="managed")]
    assert cells_for(plan, evidence)[("Qdrant", "operational_effort")].state == "disputed"
    # 'general' evidence applies to every context
    evidence = [e for e in q1_v1_evidence() if e.target_id != "Weaviate:operational_effort"]
    evidence += [ev("Weaviate:operational_effort", 1, "BLOG", scope="managed"),
                 ev("Weaviate:operational_effort", 1, "BLOG2", scope="self_hosted"),
                 ev("Weaviate:operational_effort", 1, "BLOG3", scope="general")]
    c = cells_for(plan, evidence)[("Weaviate", "operational_effort")]
    assert (c.state, c.score) == ("supported", 1)


def test_report_keeps_interval_outcome_but_withholds_recommendation():
    from conftest import run_xy

    from pathfinder.demo_fixtures import Y_REVIEW

    ctx = run_xy("flip", items_override={Y_REVIEW: []})
    r = ctx.report
    assert r.interval_leader == "VendorY" and r.decision_stability == "robust"
    assert r.recommendation_status == "withheld" and r.recommended is None
    assert "Recommendation withheld" in r.short_answer
    trace = [e for e in ctx.telemetry.events if e["event"] == "round_metrics"]
    assert trace[-1]["interval_leader"] == "VendorY" and trace[-1]["recommendation"] == "withheld"
