"""Decision-Flip policy (comparison mode) and decision-change detection.

priority = weight x width x flip_factor / cost_units
  width       = upper - lower of the cell (2 for unknown/disputed)
  flip_factor = 2 if pinning the cell to 0 vs 2 changes the outcome leader, else 1
  cost_units  = 2 (one search + contents); an estimate, not billing
This is a transparent priority heuristic, not a probability or Bayesian value of information.
"""

from __future__ import annotations

from collections.abc import Mapping

from pathfinder.matrix import Cells, bounds, cell_key, decision_state, outcome_leader, robust_winner
from pathfinder.models import RESOLVED_STATES, DecisionChange, DecisionState, ResearchAction, ResearchPlan
from pathfinder.queries import build_query
from pathfinder.readiness import corroboration_targets

COST_UNITS = 2.0
MAX_ATTEMPTS_PER_TARGET = 2


def flip_relevant(plan: ResearchPlan, cells: Cells, alternative: str, criterion_id: str) -> bool:
    low = outcome_leader(plan, cells, (alternative, criterion_id, 0))
    high = outcome_leader(plan, cells, (alternative, criterion_id, 2))
    return low != high


def rank_targets(plan: ResearchPlan, cells: Cells) -> list[dict]:
    """All unknown/disputed cells with their priority, sorted (deterministic tie-break)."""
    out = []
    for alt in plan.alternatives:
        for crit in plan.criteria:
            cell = cells[(alt.name, crit.criterion_id)]
            if cell.state in RESOLVED_STATES:  # scope_dependent: more research cannot pick the user's context
                continue
            width = cell.upper - cell.lower
            relevant = flip_relevant(plan, cells, alt.name, crit.criterion_id)
            factor = 2 if relevant else 1
            gain = crit.weight * width * factor
            out.append({"alternative": alt.name, "criterion_id": crit.criterion_id, "weight": crit.weight,
                        "width": width, "flip_relevant": relevant, "flip_factor": factor,
                        "predicted_gain": float(gain), "priority": gain / COST_UNITS,
                        "state": cell.state})
    return sorted(out, key=lambda t: (-t["priority"], t["alternative"], t["criterion_id"]))


def choose_corroboration(plan: ResearchPlan, cells: Cells, attempts: Mapping[str, int],
                         action_no: int) -> ResearchAction | None:
    """Interval is robust but the recommendation is withheld: research the weakest differentiating cell,
    in the comparable scope where a scope mismatch exists. Open query (attempt >= 1) so that an
    independent source can appear. Priority = criterion weight (no flip factor: the leader is fixed)."""
    for t in corroboration_targets(plan, cells):
        key = f"{cell_key(t['alternative'], t['criterion_id'])}#corroborate"
        tried = attempts.get(key, 0)
        if tried >= MAX_ATTEMPTS_PER_TARGET:
            continue
        query, domains = build_query(plan, t["alternative"], t["criterion_id"], 1 + tried, scope=t["scope"])
        why = (f"Interval winner is robust but the recommendation is withheld ({t['reason']}): corroborate "
               f"{t['alternative']}:{t['criterion_id']}" + (f" in the '{t['scope']}' context" if t["scope"] else "")
               + f" (weight {t['weight']}).")
        return ResearchAction(action_id=f"ACT_{action_no}", target_id=key, queries=[query],
                              include_domains=domains, predicted_gain=float(t["weight"]),
                              estimated_cost_units=COST_UNITS, action_score=t["weight"] / COST_UNITS,
                              flip_relevant=False, why_selected=why)
    return None


def choose_next_comparison(plan: ResearchPlan, cells: Cells, attempts: Mapping[str, int],
                           action_no: int) -> ResearchAction | None:
    order = [a.name for a in plan.alternatives]
    if robust_winner(order, bounds(plan, cells)):
        return choose_corroboration(plan, cells, attempts, action_no)
    for t in rank_targets(plan, cells):
        key = cell_key(t["alternative"], t["criterion_id"])
        tried = attempts.get(key, 0)
        if tried >= MAX_ATTEMPTS_PER_TARGET:
            continue
        query, domains = build_query(plan, t["alternative"], t["criterion_id"], tried)
        others_known = [c.criterion_id for (a, _), c in cells.items()
                        if a == t["alternative"] and c.state in RESOLVED_STATES]
        why = (f"{key} is {t['state']} (width {t['width']}, weight {t['weight']}"
               f"{', flip-relevant x2' if t['flip_relevant'] else ', not flip-relevant x1'}); "
               f"resolving it {'could change' if t['flip_relevant'] else 'cannot alone change'} the leader."
               + (f" Already supported for {t['alternative']}: {', '.join(others_known)}." if others_known else "")
               + (" Retry with an open query." if tried else ""))
        return ResearchAction(action_id=f"ACT_{action_no}", target_id=key, queries=[query],
                              include_domains=domains, predicted_gain=t["predicted_gain"],
                              estimated_cost_units=COST_UNITS, action_score=t["priority"],
                              flip_relevant=t["flip_relevant"], why_selected=why)
    return None


def classify_change(before: DecisionState, after: DecisionState) -> str | None:
    """Leader changes count only between two real leaders; a leader that appears or moves while the
    state stays `undetermined` is a tie-break artifact, not a decision change."""
    if before == after or before.stability == after.stability == "undetermined":
        return None
    if before.recommended != after.recommended and before.recommended and after.recommended:
        return "leader_changed"
    if after.stability == "robust" and before.stability != "robust":
        return "became_robust"
    if before.stability == "robust" and after.stability != "robust":
        return "lost_robustness"
    if before.stability != after.stability:
        return "stability_changed"
    return None


def detect_decision_change(plan_before: ResearchPlan, plan_after: ResearchPlan, cells_before: Cells,
                           cells_after: Cells, cells_without_new: Cells, new_evidence_ids: list[str],
                           round_no: int) -> tuple[DecisionChange | None, str]:
    """Return (change, note). A change is recorded only when attributable to newly verified evidence.

    cells_without_new: the after-state recomputed WITHOUT this round's new evidence (counterfactual).
    """
    before = decision_state(plan_before, cells_before)
    after = decision_state(plan_after, cells_after)
    kind = classify_change(before, after)
    if kind is None:
        return None, "no change in recommendation or its supported status"
    if [(c.criterion_id, c.weight) for c in plan_before.criteria] != \
            [(c.criterion_id, c.weight) for c in plan_after.criteria] or plan_before.criteria != plan_after.criteria:
        return None, "change caused by a criteria/weight/rubric edit; not counted"
    if not new_evidence_ids:
        return None, "no newly verified evidence this round; not counted"
    if decision_state(plan_after, cells_without_new) != before:
        return None, "counterfactual without new evidence does not restore previous state; not counted"
    return DecisionChange(round=round_no, kind=kind, before=before, after=after,  # type: ignore[arg-type]
                          evidence_ids=new_evidence_ids), "attributed to newly verified evidence"
