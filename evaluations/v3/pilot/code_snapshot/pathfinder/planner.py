"""Planner: intent (comparison vs discovery), alternatives + scoring rules or facets, initial queries.

The LLM drafts; this module normalizes and validates. Weights: user-specified (--weights or explicit
in the question) > inferred from stated priorities > default 3. Every default is logged as an assumption.
"""

from __future__ import annotations

import re

from pathfinder.llm import StructuredLLM
from pathfinder.models import (
    Alternative,
    Criterion,
    Facet,
    Mode,
    PlanDraft,
    ResearchPlan,
)
from pathfinder.queries import build_discovery_query, build_query
from pathfinder.scoring import DEFAULT_WEIGHT

PLAN_SYSTEM = """You plan a bounded web research task. Return a JSON plan.
mode: "comparison" when the user must choose between or compare 2-4 options/approaches;
"discovery" when the user wants a list of entities, an overview, or coverage of topics.
Comparison: list 2-4 alternatives. For each alternative set kind:
 - "named" for a specific product, company or project (give aliases and official website domains
   if known; leave the domain list empty if unsure);
 - "approach" for a conceptual option or architecture pattern (e.g. "managed vector database",
   "multi-agent automation"); give 2-4 defining_features that distinguish it from the other
   alternatives in ordinary text, and leave official_domains empty.
Give 2-5 criteria. For each criterion give: snake_case criterion_id, description, direction of the RAW
attribute (lower_is_better for cost/effort/latency), anchors that define fit scores poor(0)/
plausible(1)/strong(2) for THIS user's constraints, numeric thresholds only if the user stated
numeric limits (else null), time_sensitive=true for prices/plans.
scopes: if alternatives can be evaluated in materially different contexts for this criterion
(e.g. ["managed", "self_hosted"] for operational effort of databases), list them as snake_case
labels so evidence is compared like-for-like; else []. preferred_scope: one of scopes only if the
user's constraints clearly select it, else null.
weight 1-5 and weight_source="user" only if the user stated priorities explicitly, "inferred" if
clearly implied by stated constraints, else weight=null and weight_source="default".
Discovery: facets are predicates every entity must satisfy (target_entity_count = number requested)
or topics to cover (target_entity_count = 0); snake_case facet_id; importance 1-5; required_count;
search_terms = 2-5 search keywords for the facet. search_context: a short topic phrase
(e.g. "India HR SaaS companies") used in follow-up searches; "" for comparisons.
assumptions: every assumption you make about missing requirements (never empty).
initial_queries: 2-3 concise web search queries; for a comparison, together they must name every
alternative (e.g. combine two alternatives in one query). Do not answer the question."""


def slug(text: str, fallback: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")[:40]
    return s or fallback


def select_initial_queries(queries: list[str], alternatives: list[str], limit: int) -> list[str]:
    """Keep at most `limit` queries, greedily maximising how many alternatives they mention, so a
    cap can never silently drop an alternative from round 0 when another query covers it.
    Ties keep the planner's order."""
    chosen: list[str] = []
    covered: set[str] = set()
    remaining = list(queries)
    while remaining and len(chosen) < limit:
        def gain(q: str) -> int:
            return sum(1 for a in alternatives if a not in covered and a.lower() in q.lower())

        best = max(remaining, key=gain)  # max() returns the first maximum -> planner order on ties
        chosen.append(best)
        remaining.remove(best)
        covered.update(a for a in alternatives if a.lower() in best.lower())
    return chosen


def normalize_plan(question: str, draft: PlanDraft, user_weights: dict[str, int],
                   max_initial_queries: int) -> tuple[ResearchPlan, list[str]]:
    notes: list[str] = []
    assumptions = [a for a in draft.assumptions if a.strip()]
    mode = draft.mode
    alternatives = [Alternative(name=a.name.strip()[:80], aliases=a.aliases,
                                official_domains=a.official_domains if a.kind == "named" else [],
                                kind=a.kind, defining_features=[f for f in a.defining_features if f.strip()][:4])
                    for a in draft.alternatives[:4] if a.name.strip()]
    if mode == Mode.COMPARISON and len(draft.alternatives) > 4:
        assumptions.append(f"Only the first 4 alternatives were compared: {', '.join(a.name for a in alternatives)}.")
    for a in alternatives:
        if a.kind == "approach" and not a.defining_features:
            notes.append(f"approach '{a.name}' has no defining features; identification relies on the verifier")

    criteria: list[Criterion] = []
    defaults: list[str] = []
    for i, c in enumerate(draft.criteria[:5]):
        cid = slug(c.criterion_id or c.description, f"criterion_{i + 1}")
        if cid in user_weights:
            weight, source = user_weights[cid], "user"
        elif c.weight_source in ("user", "inferred") and c.weight is not None and 1 <= c.weight <= 5:
            weight, source = c.weight, c.weight_source
        else:
            weight, source = DEFAULT_WEIGHT, "default"
            defaults.append(cid)
        scopes = list(dict.fromkeys(slug(s, "") for s in c.scopes if slug(s, "") and slug(s, "") != "general"))[:4]
        preferred = slug(c.preferred_scope, "") if c.preferred_scope else None
        if preferred and preferred not in scopes:
            notes.append(f"{cid}: preferred_scope '{preferred}' not in scopes; ignored")
            preferred = None
        criteria.append(Criterion(criterion_id=cid, description=c.description, direction=c.direction,
                                  weight=weight, weight_source=source, anchors=c.anchors,
                                  thresholds=c.thresholds, time_sensitive=c.time_sensitive,
                                  scopes=scopes, preferred_scope=preferred))
    unknown_user = sorted(set(user_weights) - {c.criterion_id for c in criteria})
    if unknown_user:
        notes.append(f"--weights keys not in plan, ignored: {', '.join(unknown_user)}")
    if defaults:
        assumptions.append(f"No stated priority for {', '.join(defaults)}: equal default weight {DEFAULT_WEIGHT}.")
    for c in criteria:
        if c.preferred_scope:
            assumptions.append(f"{c.criterion_id} is compared in the '{c.preferred_scope}' context only "
                               "(selected by the stated constraints).")

    facets = [Facet(facet_id=slug(f.facet_id or f.description, f"facet_{i + 1}"), description=f.description,
                    importance=min(5, max(1, f.importance)), required_count=min(10, max(1, f.required_count)),
                    search_terms=f.search_terms.strip()[:80])
              for i, f in enumerate(draft.facets[:6])]
    target_count = min(10, max(0, draft.target_entity_count))

    if mode == Mode.COMPARISON and len(alternatives) < 2:
        # F16: a single option cannot be compared; research its criteria as coverage facets instead.
        name = alternatives[0].name if alternatives else "the subject"
        facets = [Facet(facet_id=c.criterion_id, description=f"{name}: {c.description}",
                        importance=c.weight, required_count=1, search_terms=f"{name} {c.criterion_id.replace('_', ' ')}")
                  for c in criteria] or facets
        mode, criteria, alternatives, target_count = Mode.DISCOVERY, [], [], 0
        assumptions.append("Fewer than two alternatives: switched to coverage mode; no winner is ranked.")
        notes.append("comparison -> discovery fallback (fewer than two alternatives)")

    queries = select_initial_queries([q.strip() for q in draft.initial_queries if q.strip()],
                                     [a.name for a in alternatives] if mode == Mode.COMPARISON else [],
                                     max_initial_queries) or [question[:200]]
    if mode == Mode.COMPARISON:
        missed = [a.name for a in alternatives if not any(a.name.lower() in q.lower() for q in queries)]
        if missed:
            notes.append(f"round-0 queries do not mention: {', '.join(missed)} (left to targeted rounds)")
    if not assumptions:
        assumptions = ["Interpreted the question literally; no additional constraints were assumed."]
    plan = ResearchPlan(question=question, mode=mode, alternatives=alternatives, criteria=criteria,
                        facets=facets, target_entity_count=target_count, assumptions=assumptions,
                        initial_queries=queries,
                        search_context=draft.search_context.strip()[:80] if mode == Mode.DISCOVERY else "")
    return plan, notes


def make_plan(llm: StructuredLLM, question: str, user_weights: dict[str, int],
              max_initial_queries: int) -> tuple[ResearchPlan, list[str]]:
    draft = llm.call("plan", PLAN_SYSTEM, {"question": question,
                                           "user_weights": user_weights or None}, PlanDraft)
    return normalize_plan(question, draft, user_weights, max_initial_queries)


def round_robin_cells(n_alternatives: int, n_criteria: int) -> list[tuple[int, int]]:
    """Diagonal round-robin over (alternative, criterion) index pairs: consecutive targets rotate through
    BOTH alternatives and criteria, and every pair appears exactly once.
    e.g. 3x3 -> (0,0) (1,1) (2,2) (0,1) (1,2) (2,0) (0,2) (1,0) (2,1)."""
    # For a fixed alternative i, (i + offset) % n_criteria takes every criterion once as offset varies.
    return [(i, (i + offset) % n_criteria) for offset in range(n_criteria) for i in range(n_alternatives)]


def static_queue(plan: ResearchPlan) -> list[tuple[str, str, list[str]]]:
    """Static-baseline follow-ups: a fixed schedule computed from the plan alone, before any retrieval.

    Comparison: diagonal round-robin across alternatives and criteria. Discovery: facets in plan order.
    Queries come from the SAME builders the adaptive policy uses (pathfinder.queries), with attempt 0,
    so the arms differ only in which target is researched next.
    """
    if plan.mode == Mode.COMPARISON:
        out = []
        for ai, ci in round_robin_cells(len(plan.alternatives), len(plan.criteria)):
            a, c = plan.alternatives[ai], plan.criteria[ci]
            query, domains = build_query(plan, a.name, c.criterion_id, 0)
            out.append((f"{a.name}:{c.criterion_id}", query, domains))
        return out
    return [(f.facet_id, build_discovery_query(plan, f, None, 0), []) for f in plan.facets]
