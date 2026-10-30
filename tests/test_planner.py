"""Planner normalization (offline, scripted drafts)."""

from pathfinder.config import Settings
from pathfinder.llm import FixtureLLM, StructuredLLM
from pathfinder.models import Mode, PlanDraft
from pathfinder.planner import make_plan, normalize_plan, static_queue
from pathfinder.retry import CancelToken
from pathfinder.telemetry import Budget, Telemetry


def q7_draft():
    """What a planner might return for the underspecified Q7 (SYNTHETIC draft)."""
    def alt(name, domains=()):
        return {"name": name, "aliases": [], "official_domains": list(domains), "kind": "named",
                "defining_features": []}

    return PlanDraft.model_validate({
        "mode": "comparison",
        "alternatives": [alt("Qdrant", ["qdrant.tech"]), alt("Weaviate"), alt("Milvus"), alt("pgvector"),
                         alt("Chroma")],
        "criteria": [{"criterion_id": "Ops Effort!", "description": "operational effort",
                      "direction": "lower_is_better", "weight": None, "weight_source": "default",
                      "anchors": {"poor": "a", "plausible": "b", "strong": "c"}, "thresholds": None,
                      "time_sensitive": False, "scopes": ["Managed", "self-hosted", "general"],
                      "preferred_scope": None},
                     {"criterion_id": "filtering", "description": "metadata filtering",
                      "direction": "higher_is_better", "weight": None, "weight_source": "default",
                      "anchors": {"poor": "a", "plausible": "b", "strong": "c"}, "thresholds": None,
                      "time_sensitive": False, "scopes": [], "preferred_scope": None}],
        "facets": [], "target_entity_count": 0,
        "assumptions": ["No workload, scale or budget was given; assuming a small RAG team."],
        "initial_queries": ["vector database comparison", "qdrant vs weaviate", "milvus review"],
        "search_context": "",
    })


def test_Q7_underspecified_question_states_assumptions_and_caps():
    plan, _ = normalize_plan("Which vector database is best?", q7_draft(), {}, 2)
    assert plan.mode == Mode.COMPARISON
    assert len(plan.alternatives) == 4 and any("first 4 alternatives" in a for a in plan.assumptions)
    assert any("assuming a small RAG team" in a for a in plan.assumptions)
    assert any("default weight 3" in a for a in plan.assumptions)
    assert [c.criterion_id for c in plan.criteria] == ["ops_effort", "filtering"]
    assert len(plan.initial_queries) == 2


def test_initial_query_cap_keeps_alternative_coverage():
    """Regression from the first live Q1 run: the 2-query cap dropped the only Milvus query."""
    from pathfinder.planner import select_initial_queries

    live = ["Qdrant official deployment filtering documentation",
            "Weaviate official deployment metadata filtering documentation",
            "Milvus official deployment filtering documentation"]
    assert select_initial_queries(live, ["Qdrant", "Weaviate", "Milvus"], 2) == live[:2]  # only 2 fit
    combined = [*live, "Qdrant vs Milvus operational effort"]
    picked = select_initial_queries(combined, ["Qdrant", "Weaviate", "Milvus"], 2)
    assert picked == ["Qdrant vs Milvus operational effort", live[1]]  # all three alternatives covered
    assert select_initial_queries(["a", "b", "c"], [], 2) == ["a", "b"]  # discovery keeps planner order


def test_uncovered_alternative_is_noted():
    draft = q7_draft()
    draft.initial_queries = ["qdrant docs", "weaviate docs"]
    _, notes = normalize_plan("q", draft, {}, 2)
    assert any("do not mention" in n and "Milvus" in n for n in notes)


def test_unknown_user_weight_keys_are_reported():
    _, notes = normalize_plan("q", q7_draft(), {"latency": 5}, 2)
    assert any("latency" in n for n in notes)


def test_make_plan_passes_weights_to_model():
    seen = {}

    def handler(req):
        seen.update(req.payload)
        return q7_draft()

    s = Settings()
    llm = StructuredLLM(FixtureLLM({"plan": handler}), s, Budget.from_settings(s), Telemetry("T"), CancelToken())
    plan, _ = make_plan(llm, "Which vector database is best?", {"filtering": 5}, 2)
    assert seen["user_weights"] == {"filtering": 5}
    assert plan.criterion("filtering").weight_source == "user"


def test_static_queue_uses_same_query_builder_as_adaptive():
    """Regression: static used different query wording/no domain filter, confounding the evaluation."""
    from pathfinder.queries import build_query

    plan, _ = normalize_plan("q", q7_draft(), {}, 2)
    queue = static_queue(plan)
    assert len(queue) == 4 * 2
    for target, query, domains in queue:
        alt, crit = target.split(":")
        assert (query, domains) == build_query(plan, alt, crit, 0)
    assert queue[0][2] == ["qdrant.tech"]


def test_static_schedule_is_round_robin_not_alternative_major():
    """Regression from V1: static spent all targeted rounds on the first alternative."""
    from pathfinder.planner import round_robin_cells

    assert round_robin_cells(3, 3) == [(0, 0), (1, 1), (2, 2), (0, 1), (1, 2), (2, 0), (0, 2), (1, 0), (2, 1)]
    for a, c in ((4, 2), (2, 3), (3, 5), (1, 4)):
        cells = round_robin_cells(a, c)
        assert sorted(cells) == [(i, j) for i in range(a) for j in range(c)]  # every pair exactly once
        first = cells[:min(a, 3)]
        assert len({i for i, _ in first}) == len(first)  # first rounds touch distinct alternatives
    plan, _ = normalize_plan("q", q7_draft(), {}, 2)
    assert [t for t, _, _ in static_queue(plan)][:3] == ["Qdrant:ops_effort", "Weaviate:filtering",
                                                          "Milvus:ops_effort"]


def test_alternative_kinds_and_scopes_are_normalized():
    draft = q7_draft()
    draft.alternatives[1].kind = "approach"
    draft.alternatives[1].official_domains = ["should-be-dropped.example"]
    draft.alternatives[1].defining_features = ["runs as a managed service", " "]
    plan, _ = normalize_plan("q", draft, {}, 2)
    weav = plan.alternative("Weaviate")
    assert weav.kind == "approach" and weav.official_domains == [] and weav.defining_features == [
        "runs as a managed service"]
    ops = plan.criterion("ops_effort")
    assert ops.scopes == ["managed", "self_hosted"] and ops.preferred_scope is None  # "general" is implicit
    draft.criteria[0].preferred_scope = "managed"
    plan, _ = normalize_plan("q", draft, {}, 2)
    assert plan.criterion("ops_effort").preferred_scope == "managed"
    assert any("'managed' context only" in a for a in plan.assumptions)
