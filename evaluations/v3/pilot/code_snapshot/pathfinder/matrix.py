"""Alternatives x criteria matrix built ONLY from verified evidence, with interval arithmetic.

unknown         -> [0, 2]          (no verified evidence)
insufficient    -> [0, 2]          (researched; on-target candidates could not justify a score)
supported       -> [s, s]          (all verified evidence implies the same score s)
scope_dependent -> [min, max]      (consistent per context, contexts differ, no preferred context)
disputed        -> [min, max]      (comparable verified evidence implies different scores; V2 used [0, 2])

A dispute keeps the range of the verified scores (1 vs 2 -> [1, 2]): every verified source says "at least 1",
so the lower bound is justified by the evidence, while the conflict stays visible (state `disputed`, never
counted as supported, factual confidence `low`). 0 vs 2 is still [0, 2].

The midpoint is only an investigation priority; it is never presented as a score.
"""

from __future__ import annotations

from collections.abc import Mapping

from pathfinder.grounding import registrable_domain
from pathfinder.models import (
    RESOLVED_STATES,
    DecisionState,
    Evidence,
    MatrixCell,
    RejectedCandidate,
    ResearchPlan,
)
from pathfinder.scoring import factual_confidence

Cells = dict[tuple[str, str], MatrixCell]
Bounds = dict[str, tuple[int, int]]


def cell_key(alternative: str, criterion_id: str) -> str:
    return f"{alternative}:{criterion_id}"


def scorable(crit_preferred_scope: str | None, evidence_scope: str) -> bool:
    """With a preferred scope, only that context (or scope-free 'general' evidence) can score the cell."""
    return crit_preferred_scope is None or evidence_scope in (crit_preferred_scope, "general")


def independent_sources(evidence: list[Evidence], source_domains: Mapping[str, str]) -> int:
    """Distinct domains, counting each distinct (normalized) excerpt once: the same passage repeated, or
    quoted twice from one site, is not independent corroboration."""
    seen_excerpts: set[str] = set()
    domains: set[str] = set()
    for e in evidence:
        norm = " ".join(e.excerpt.lower().split())
        if norm in seen_excerpts:
            continue
        seen_excerpts.add(norm)
        domains.add(source_domains[e.source_id])
    return len(domains)


INSUFFICIENT_REASONS = ("no derivable fit score", "verdict=partial")


def insufficient_targets(rejected: list[RejectedCandidate] | list[dict]) -> set[str]:
    """Cell keys with on-target candidates that verification judged unable to justify a score."""
    out = set()
    for r in rejected:
        stage, reason, target = ((r["stage"], r["reason"], r["target_id"]) if isinstance(r, dict)
                                 else (r.stage, r.reason, r.target_id))
        if stage in ("verification", "acceptance") and reason.startswith(INSUFFICIENT_REASONS):
            out.add(target)
    return out


def build_cells(plan: ResearchPlan, evidence: list[Evidence], source_domains: Mapping[str, str],
                source_published: Mapping[str, str | None], insufficient: set[str] | None = None) -> Cells:
    cells: Cells = {}
    insufficient = insufficient or set()
    for alt in plan.alternatives:
        official = [registrable_domain(d) for d in alt.official_domains]
        for crit in plan.criteria:
            key = cell_key(alt.name, crit.criterion_id)
            verified = [e for e in evidence if e.target_id == key and e.score is not None]
            evs = [e for e in verified if scorable(crit.preferred_scope, e.scope)]
            excluded = [e.evidence_id for e in verified if e not in evs]
            state, lo, hi, score, scope_scores = cell_state(evs, scoped=bool(crit.scopes) and not crit.preferred_scope)
            if state == "unknown" and key in insufficient:
                state = "insufficient"
            self_only = bool(evs) and bool(official) and all(
                source_domains[e.source_id] in official and e.score_basis == "verified_proposal" for e in evs)
            cells[(alt.name, crit.criterion_id)] = MatrixCell(
                alternative=alt.name, criterion_id=crit.criterion_id, state=state, lower=lo, upper=hi,
                score=score, evidence_ids=[e.evidence_id for e in evs],
                factual_confidence=factual_confidence(state, evs, dict(source_domains),
                                                      dict(source_published), official,
                                                      crit.time_sensitive),
                independent_sources=independent_sources(evs, source_domains),
                scopes=sorted({e.scope for e in evs}), scope_scores=scope_scores, excluded_evidence_ids=excluded,
                observed_scores=sorted({e.score for e in evs if e.score is not None}), self_reported_only=self_only)
    return cells


def cell_state(evs: list[Evidence], scoped: bool) -> tuple[str, int, int, int | None, dict[str, int]]:
    """(state, lower, upper, score, per-scope scores) from scorable verified evidence.

    Scoped criterion without a preferred scope: evidence about different contexts is not a dispute. If each
    context is internally consistent but the contexts differ (managed 2, self_hosted 0), the cell is
    `scope_dependent` with interval [min, max]. 'general' evidence applies to every context.
    """
    scores = {e.score for e in evs}
    if not scores:
        return "unknown", 0, 2, None, {}
    contexts = sorted({e.scope for e in evs} - {"general"})
    if scoped and len(contexts) >= 2:
        per = {c: {e.score for e in evs if e.scope in (c, "general")} for c in contexts}
        if any(len(v) > 1 for v in per.values()):  # a real conflict inside one context
            return "disputed", min(scores), max(scores), None, {}  # type: ignore[type-var]
        vals = {c: next(iter(v)) for c, v in per.items()}  # type: ignore[misc]
        if len(set(vals.values())) == 1:
            s = next(iter(vals.values()))
            return "supported", s, s, s, vals
        return "scope_dependent", min(vals.values()), max(vals.values()), None, vals  # type: ignore[type-var]
    if len(scores) == 1:
        s = next(iter(scores))
        return "supported", s, s, s, {}  # type: ignore[return-value]
    return "disputed", min(scores), max(scores), None, {}  # type: ignore[type-var]


def interval(cell: MatrixCell) -> tuple[int, int]:
    return cell.lower, cell.upper


def bounds(plan: ResearchPlan, cells: Cells,
           override: tuple[str, str, int] | None = None) -> Bounds:
    """LB/UB per alternative. `override=(alt, criterion_id, score)` pins one cell (flip-relevance test)."""
    out: Bounds = {}
    for alt in plan.alternatives:
        lo_sum = hi_sum = 0
        for crit in plan.criteria:
            if override and override[0] == alt.name and override[1] == crit.criterion_id:
                lo = hi = override[2]
            else:
                lo, hi = interval(cells[(alt.name, crit.criterion_id)])
            lo_sum += crit.weight * lo
            hi_sum += crit.weight * hi
        out[alt.name] = (lo_sum, hi_sum)
    return out


def robust_winner(order: list[str], b: Bounds) -> str | None:
    """The unique alternative whose LB is strictly greater than every other UB."""
    winners = [a for a in order if all(b[a][0] > b[o][1] for o in order if o != a)]
    return winners[0] if len(winners) == 1 else None


def midpoint_leader(order: list[str], b: Bounds) -> tuple[str, bool]:
    """(leader by midpoint with listed-order tie-break, whether the top midpoint is tied)."""
    mids = {a: (b[a][0] + b[a][1]) / 2 for a in order}
    best = max(mids.values())
    top = [a for a in order if mids[a] == best]
    return top[0], len(top) > 1


def margin(order: list[str], b: Bounds, leader: str) -> int:
    return b[leader][0] - max(b[o][1] for o in order if o != leader)


def decision_state(plan: ResearchPlan, cells: Cells) -> DecisionState:
    """recommended = robust winner, else midpoint leader (listed-order tie-break), else None when no
    cell has verified support. stability: robust | provisional (unique top midpoint) | undetermined."""
    order = [a.name for a in plan.alternatives]
    b = bounds(plan, cells)
    winner = robust_winner(order, b)
    if winner:
        return DecisionState(recommended=winner, stability="robust")
    if not any(c.state in RESOLVED_STATES for c in cells.values()):
        return DecisionState(recommended=None, stability="undetermined")
    leader, tied = midpoint_leader(order, b)
    return DecisionState(recommended=leader, stability="undetermined" if tied else "provisional")


def outcome_leader(plan: ResearchPlan, cells: Cells, override: tuple[str, str, int] | None = None) -> str:
    """Robust winner, else provisional leader (listed-order tie-break). Used for flip relevance."""
    order = [a.name for a in plan.alternatives]
    b = bounds(plan, cells, override)
    return robust_winner(order, b) or midpoint_leader(order, b)[0]
