"""Query builders shared by BOTH evaluation arms.

The static baseline and the adaptive policy call the same functions with the same arguments for the same
target, so the arms can differ only in which target is researched next and when research stops.
"""

from __future__ import annotations

from pathfinder.grounding import registrable_domain
from pathfinder.models import Facet, ResearchPlan


def _words(identifier: str) -> str:
    return identifier.replace("_", " ").strip()


def build_query(plan: ResearchPlan, alternative: str, criterion_id: str, attempt: int,
                scope: str | None = None) -> tuple[str, list[str]]:
    """Comparison query for one cell. attempt 0 prefers official domains (named alternatives only);
    later attempts are open queries, which also lets independent sources appear."""
    alt = plan.alternative(alternative)
    crit = plan.criterion(criterion_id)
    scope = scope or crit.preferred_scope
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


def build_discovery_query(plan: ResearchPlan, facet: Facet | None, entity: str | None, attempt: int) -> str:
    """Discovery query: optional entity + facet keywords + the plan's topic context."""
    parts = []
    if entity:
        parts.append(entity)
    if facet is not None:
        parts.append(facet.search_terms or facet.description[:80])
    if plan.search_context:
        parts.append(plan.search_context)
    if attempt:
        parts.append("list overview")
    return " ".join(p for p in parts if p).strip() or plan.question[:200]
