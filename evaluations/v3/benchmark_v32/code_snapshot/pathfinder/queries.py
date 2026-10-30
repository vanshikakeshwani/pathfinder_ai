"""Query builders shared by BOTH evaluation arms.

The static baseline and the adaptive policy call the same functions with the same arguments for the same
target, so the arms can differ only in which target is researched next and when research stops.
"""

from __future__ import annotations

from pathfinder.grounding import registrable_domain
from pathfinder.models import Facet, ResearchPlan


def _words(identifier: str) -> str:
    return identifier.replace("_", " ").strip()


_STOP = {"the", "a", "an", "and", "or", "of", "to", "for", "in", "on", "with", "is", "are", "be", "by", "it",
         "its", "that", "this", "how", "much", "what", "which", "as", "at", "from"}
MAX_QUERY_VARIANTS = 3  # attempt 0, 1, 2


def build_query(plan: ResearchPlan, alternative: str, criterion_id: str, attempt: int,
                scope: str | None = None, purpose: str | None = None) -> tuple[str, list[str]]:
    """Comparison query for one cell.

    attempt 0: prefers official domains (named alternatives only); the static baseline always uses this.
    attempt 1: open query ("independent review comparison"), which also lets independent sources appear.
    attempt 2: broadened query from the criterion's description keywords (V3 retry ladder).
    purpose "conflict": looks for evidence that distinguishes competing claims (versions, scope, detail).
    Attempts 0 and 1 without a purpose are byte-identical to V2.
    """
    alt = plan.alternative(alternative)
    crit = plan.criterion(criterion_id)
    scope = scope or crit.preferred_scope
    if purpose == "conflict":
        parts = [alt.name, _words(criterion_id)]
        if scope:
            parts.append(_words(scope))
        parts.append("detailed evidence version differences" if attempt == 0 else "independent measured comparison")
        return " ".join(parts), []
    if attempt >= 2:
        words = [w for w in "".join(ch if ch.isalnum() or ch == " " else " " for ch in crit.description.lower()).split()
                 if w not in _STOP][:6]
        parts = [alt.name, *words]
        if scope:
            parts.append(_words(scope))
        parts.append("experience report")
        return " ".join(parts), []
    parts = [alt.name, _words(criterion_id)]
    if scope:
        parts.append(_words(scope))
    if crit.time_sensitive:
        parts.append("pricing plans")
    if attempt == 0:
        parts.append("official documentation" if alt.kind == "named" else "trade-offs")
    else:
        parts.append("independent review comparison")
    domains = ([registrable_domain(d) for d in alt.official_domains]
               if attempt == 0 and alt.kind == "named" else [])
    return " ".join(parts), domains


def _tokens(query: str) -> set[str]:
    return {w for w in query.lower().split() if w not in _STOP}


def near_duplicate(query: str, issued: list[str], threshold: float = 0.8) -> bool:
    """True if `query` shares >= threshold of its tokens (Jaccard) with an already issued query."""
    t = _tokens(query)
    for q in issued:
        u = _tokens(q)
        if t and u and len(t & u) / len(t | u) >= threshold:
            return True
    return False


def build_discovery_query(plan: ResearchPlan, facet: Facet | None, entity: str | None, attempt: int) -> str:
    """Discovery query: optional entity + facet keywords + the plan's topic context."""
    parts = []
    if entity:
        parts.append(entity)
    if facet is not None:
        parts.append(facet.search_terms or facet.description[:80])
    if plan.search_context:
        parts.append(plan.search_context)
    if attempt == 1:
        parts.append("list overview")
    elif attempt >= 2:
        parts.append("directory companies examples")
    return " ".join(p for p in parts if p).strip() or plan.question[:200]
