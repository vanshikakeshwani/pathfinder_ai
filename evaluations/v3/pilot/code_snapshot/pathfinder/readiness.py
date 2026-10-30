"""Recommendation readiness: separates the mathematical interval outcome from an authoritative recommendation.

Four things are reported separately:
1. requirement coverage   - how many cells have verified support;
2. evidence quality        - factual confidence and independent sources per cell;
3. interval stability      - robust / provisional / undetermined (matrix.py, unchanged);
4. recommendation readiness - "ready" only if the interval winner is robust AND the cells that
   differentiate it from each competitor are comparable and well supported. Otherwise the interval
   outcome is still reported and traced, but the recommendation is withheld, with reasons.

V3 names every readiness blocker explicitly (`blockers`), so the adaptive policy can research what stands
between the interval outcome and a defensible recommendation:
- weak_support: a differentiating cell lacks high factual confidence (one source family, or non-official);
- comparability: a differentiating criterion compares different contexts (managed vs self-hosted);
- self_reported: the leader's advantage on a differentiating criterion is an evaluative judgement taken
  only from the leader's own domain (marketing-style claim; threshold-scored facts such as prices exempt);
- leader_disputed: the leader's own score on a criterion is disputed (comparable sources disagree);
- critical_unsupported: a critical criterion (weight >= 4) has no supported score for the leader.
Corroboration is never assumed to succeed: a new source can disagree, which makes the cell disputed.

Comparability: when a criterion declares scopes (e.g. managed / self_hosted) and has no preferred scope,
alternatives whose scores rest on DIFFERENT scopes are not compared like-for-like (Q1 v1: Qdrant scored from
managed-cloud docs, competitors from self-hosting complaints). Single-source support is disclosed, not
forbidden; but a consequential comparative recommendation requires each differentiating cell to have
high factual confidence (two independent sources, or an official source for a non-time-sensitive fact).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from pathfinder.matrix import Cells, decision_state
from pathfinder.models import RESOLVED_STATES, ResearchPlan

CRITICAL_WEIGHT = 4


@dataclass(frozen=True)
class Blocker:
    kind: str  # weak_support | comparability | self_reported | leader_disputed | critical_unsupported
    alternative: str
    criterion_id: str
    reason: str
    scope: str | None = None  # comparable context to research (comparability blockers)


@dataclass
class Readiness:
    status: str  # ready | withheld | none
    interval_leader: str | None
    stability: str
    reasons: list[str] = field(default_factory=list)
    comparability_issues: list[str] = field(default_factory=list)
    single_source_cells: list[str] = field(default_factory=list)
    differentiating_cells: list[tuple[str, str]] = field(default_factory=list)
    weak_differentiating_cells: list[tuple[str, str]] = field(default_factory=list)
    blockers: list[Blocker] = field(default_factory=list)


def comparability_issues(plan: ResearchPlan, cells: Cells) -> dict[str, str]:
    """criterion_id -> description, for criteria whose supported cells rest on disjoint scopes."""
    issues: dict[str, str] = {}
    for crit in plan.criteria:
        if not crit.scopes or crit.preferred_scope:
            continue
        scoped = {a.name: set(cells[(a.name, crit.criterion_id)].scopes) - {"general"}
                  for a in plan.alternatives if cells[(a.name, crit.criterion_id)].state == "supported"}
        scoped = {a: s for a, s in scoped.items() if s}
        names = list(scoped)
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                if scoped[a].isdisjoint(scoped[b]):
                    issues[crit.criterion_id] = (
                        f"{crit.criterion_id}: {a} scored from {sorted(scoped[a])} evidence but {b} from "
                        f"{sorted(scoped[b])}; not a like-for-like comparison")
                    break
            if crit.criterion_id in issues:
                break
    return issues


def differentiating_cells(plan: ResearchPlan, cells: Cells, leader: str) -> list[tuple[str, str]]:
    """Cells whose known scores differ between the leader and some competitor on the same criterion."""
    out: list[tuple[str, str]] = []
    for crit in plan.criteria:
        lc = cells[(leader, crit.criterion_id)]
        for alt in plan.alternatives:
            if alt.name == leader:
                continue
            oc = cells[(alt.name, crit.criterion_id)]
            if lc.state == oc.state == "supported" and lc.score != oc.score:
                for key in ((leader, crit.criterion_id), (alt.name, crit.criterion_id)):
                    if key not in out:
                        out.append(key)
    return out


def _blockers(plan: ResearchPlan, cells: Cells, leader: str, diff: list[tuple[str, str]],
              issues: dict[str, str]) -> list[Blocker]:
    out: list[Blocker] = []
    for a, c in diff:
        if cells[(a, c)].factual_confidence != "high":
            out.append(Blocker("weak_support", a, c, f"{a}:{c} has one source family or no official source"))
    for a, c in diff:
        if c in issues:
            lead_scopes = set(cells[(leader, c)].scopes) - {"general"}
            scope = sorted(lead_scopes)[0] if (a != leader and lead_scopes) else None
            out.append(Blocker("comparability", a, c, issues[c], scope))
    for a, c in diff:
        cell = cells[(a, c)]
        if a == leader and cell.self_reported_only and cell.factual_confidence == "high":
            out.append(Blocker("self_reported", a, c,
                               f"{a}'s advantage on {c} rests only on {a}'s own (self-reported) claims"))
    for crit in plan.criteria:
        cell = cells[(leader, crit.criterion_id)]
        if cell.state == "disputed":
            out.append(Blocker("leader_disputed", leader, crit.criterion_id,
                               f"{leader}'s own score on {crit.criterion_id} is disputed "
                               f"(verified scores {cell.observed_scores})"))
        elif cell.state in ("unknown", "insufficient") and crit.weight >= CRITICAL_WEIGHT:
            out.append(Blocker("critical_unsupported", leader, crit.criterion_id,
                               f"critical criterion {crit.criterion_id} (weight {crit.weight}) has no supported "
                               f"score for {leader}"))
    return out


def assess(plan: ResearchPlan, cells: Cells) -> Readiness:
    st = decision_state(plan, cells)
    single = [f"{a}:{c}" for (a, c), cell in cells.items() if cell.state in RESOLVED_STATES and cell.independent_sources <= 1]
    issues = comparability_issues(plan, cells)
    r = Readiness(status="none", interval_leader=st.recommended, stability=st.stability,
                  comparability_issues=list(issues.values()), single_source_cells=single)
    if st.recommended is None or st.stability == "undetermined":
        r.reasons.append("no unique interval leader")
        return r
    diff = differentiating_cells(plan, cells, st.recommended)
    r.differentiating_cells = diff
    r.weak_differentiating_cells = [k for k in diff if cells[k].factual_confidence != "high"]
    r.blockers = _blockers(plan, cells, st.recommended, diff, issues)
    if st.stability != "robust":
        r.reasons.append("score intervals overlap (provisional leader only)")
    blocking = [msg for cid, msg in issues.items() if any(c == cid for _, c in diff)]
    r.reasons += blocking
    if r.weak_differentiating_cells:
        r.reasons.append("differentiating cells lack strong support (single source or non-official): "
                         + ", ".join(f"{a}:{c}" for a, c in r.weak_differentiating_cells))
    for kind in ("self_reported", "leader_disputed", "critical_unsupported"):
        r.reasons += [b.reason for b in r.blockers if b.kind == kind]
    if st.stability == "robust" and not diff:
        r.reasons.append("robust only through unknown/undifferentiated cells; no supported difference")
    r.status = "ready" if not r.reasons else "withheld"
    return r


def corroboration_targets(plan: ResearchPlan, cells: Cells) -> list[dict]:
    """Supported cells that block readiness (weak differentiating cells, or cells on a criterion with a
    comparability issue), ranked by criterion weight. Used by the adaptive policy once the interval is
    robust but the recommendation is withheld."""
    r = assess(plan, cells)
    if r.interval_leader is None or r.stability != "robust" or r.status == "ready":
        return []
    issue_criteria = {c for c in comparability_issues(plan, cells)}
    targets = list(r.weak_differentiating_cells)
    for a, c in r.differentiating_cells:
        if c in issue_criteria and (a, c) not in targets:
            targets.append((a, c))
    out = []
    for a, c in targets:
        crit = plan.criterion(c)
        # research the comparable context: the leader's scope if the competitor used a different one
        lead_scopes = set(cells[(r.interval_leader, c)].scopes) - {"general"}
        scope = sorted(lead_scopes)[0] if (c in issue_criteria and a != r.interval_leader and lead_scopes) else None
        out.append({"alternative": a, "criterion_id": c, "weight": crit.weight, "scope": scope,
                    "reason": "comparability" if c in issue_criteria else "single-source/weak support"})
    return sorted(out, key=lambda t: (-t["weight"], t["alternative"], t["criterion_id"]))
