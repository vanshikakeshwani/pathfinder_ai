"""F07, F16 and discovery-mode behaviour (SYNTHETIC companies)."""

from conftest import build_ctx

from pathfinder.coverage import choose_next_discovery, compute_coverage, entity_key
from pathfinder.demo_fixtures import ScriptedExtractor, ScriptedVerifier, evidence_report
from pathfinder.llm import FixtureLLM
from pathfinder.models import AlternativeDraft, Anchors, CriterionDraft, Direction, FacetDraft, PlanDraft
from pathfinder.runner import run
from pathfinder.tools.base import PageContent, SearchHit
from pathfinder.tools.fixture_adapter import FixtureContents, FixtureSearch

COMPANIES = ["Alphahire", "Betapay HR", "Gammateam"]  # fictional


def discovery_draft(target=5):
    return PlanDraft(mode="discovery", alternatives=[], criteria=[],
                     facets=[FacetDraft(facet_id="india_hq", description="headquartered in India", importance=5,
                                        required_count=1, search_terms="headquarters India"),
                             FacetDraft(facet_id="b2b_hr_saas", description="B2B SaaS for HR", importance=4,
                                        required_count=1, search_terms="B2B HR SaaS")],
                     target_entity_count=target, assumptions=["SYNTHETIC companies"],
                     initial_queries=["synthetic india hr saas companies"], search_context="India HR SaaS companies")


def discovery_world():
    pages, by_url, hits = {}, {}, []
    for name in COMPANIES:
        url = f"https://{entity_key(name)}.example/about"
        hq = f"{name} is headquartered in Bengaluru, India."
        prod = f"{name} sells B2B SaaS software for HR teams."
        pages[url] = PageContent(url=url, title=name, text=f"{hq} {prod}")
        hits.append(SearchHit(url=url, title=name))
        by_url[url] = [
            {"target_id": "india_hq", "excerpt": hq, "claim": f"{name} HQ in India", "entity": name,
             "proposed_score": None, "raw_value": None, "raw_unit": None, "start": None, "end": None,
             "scope": None, "rubric_rationale": None},
            {"target_id": "b2b_hr_saas", "excerpt": prod, "claim": f"{name} B2B HR SaaS", "entity": name,
             "proposed_score": None, "raw_value": None, "raw_unit": None, "start": None, "end": None,
             "scope": None, "rubric_rationale": None},
        ]
    return pages, by_url, hits


def run_discovery(target=5, **settings_kw):
    from pathfinder.config import Settings

    pages, by_url, hits = discovery_world()
    llm = FixtureLLM({"plan": lambda r: discovery_draft(target), "extract": ScriptedExtractor(by_url),
                      "verify": ScriptedVerifier(), "report": evidence_report})
    search = FixtureSearch(lambda q, d: list(hits))
    ctx = build_ctx(llm, search, FixtureContents(pages), Settings(pages_per_search=5, **settings_kw),
                    question="[SYNTHETIC] five India HR SaaS companies")
    run(ctx)
    return ctx


def test_F07_three_of_five_verified_is_not_complete():
    ctx = run_discovery(5)
    r = ctx.report
    cov = ctx.coverage()
    assert (cov.verified_units, cov.required_units) == (3, 5)
    assert r.status == "partial" and r.stop_reason != "stable"
    assert any("Only 3 of 5" in lim for lim in r.limitations)
    assert r.recommended is None and r.decision_stability is None  # discovery never invents a winner


def test_discovery_complete_when_target_met():
    ctx = run_discovery(3)
    assert ctx.report.stop_reason == "stable" and ctx.report.status == "complete"


def test_entity_needs_every_facet_and_names_merge():
    plan = __import__("pathfinder.planner", fromlist=["normalize_plan"]).normalize_plan(
        "q", discovery_draft(2), {}, 2)[0]
    from helpers import ev

    evidence = [ev("india_hq", None, entity="Alphahire Pvt Ltd"), ev("b2b_hr_saas", None, entity="AlphaHire"),
                ev("india_hq", None, entity="Gammateam")]
    cov = compute_coverage(plan, evidence)
    assert cov.verified_units == 1  # Alphahire (merged) complete; Gammateam missing a facet
    action = choose_next_discovery(plan, cov, {}, 1)
    assert action.target_id == "Gammateam|b2b_hr_saas"


def test_F16_single_alternative_falls_back_to_coverage():
    draft = PlanDraft(mode="comparison",
                      alternatives=[AlternativeDraft(name="Qdrant", aliases=[], official_domains=[], kind="named",
                                                     defining_features=[])],
                      criteria=[CriterionDraft(criterion_id="filtering", description="metadata filtering",
                                               direction=Direction.HIGHER_IS_BETTER, weight=None,
                                               weight_source="default",
                                               anchors=Anchors(poor="a", plausible="b", strong="c"),
                                               thresholds=None, time_sensitive=False, scopes=[], preferred_scope=None)],
                      facets=[], target_entity_count=0, assumptions=[], initial_queries=["qdrant filtering"],
                      search_context="")
    llm = FixtureLLM({"plan": lambda r: draft, "extract": lambda r: {"items": []},
                      "verify": ScriptedVerifier(), "report": evidence_report})
    ctx = build_ctx(llm, FixtureSearch(lambda q, d: []), FixtureContents({}), question="Is Qdrant good?")
    run(ctx)  # must not crash on an empty competitor set
    assert ctx.plan.mode.value == "discovery" and ctx.plan.facets[0].facet_id == "filtering"
    assert ctx.report.stop_reason == "insufficient_evidence" and ctx.report.status == "failed"
    assert any("switched to coverage mode" in a for a in ctx.plan.assumptions)
