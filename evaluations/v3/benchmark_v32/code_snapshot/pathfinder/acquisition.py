"""V3 decision-aware acquisition policy (comparison mode).

Question answered each round: which missing or weak piece of evidence, if researched next, could most improve
our ability to make a DEFENSIBLE decision under the disclosed rubric and weights?

For every candidate target (an open cell, a disputed cell, or a supported cell that blocks readiness) the
policy computes and records:

    priority = weight x uncertainty x decision_factor x exploration_factor x retry_factor / cost_units

  weight             criterion importance (1-5; user > inferred > default)
  uncertainty        interval width of the cell (unknown/insufficient 2; disputed max-min); 1 for a
                     corroboration target (the score is known, its support is weak)
  decision_factor    from deterministic counterfactuals over the cell's possible rubric scores:
                       2.0      resolving this cell ALONE can change the leader, break a tie or make the
                                leader interval-robust, or it is the only readiness blocker of a robust leader
                       1 + 1/k  it belongs to a minimal group of k >= 2 cells that can JOINTLY change the
                                leader or make it robust, or it is one of k readiness blockers
                       1.25     resolving it can rule out another alternative (no leader change)
                       1.0      coverage only: no counterfactual effect on the decision
                       0.5      coverage only, and its alternative is already ruled out (low value)
  exploration_factor 1 / (1 + 0.5 n), n = how many of the last 2 targeted rounds went to this
                     alternative while other alternatives still have targets with decision value; x 1.2 if the
                     alternative has never been targeted yet
  retry_factor       0.5 ** (failed attempts on this target)
  cost_units         2 (one search + its content pages): an estimate, not billing

None of these factors is a probability: a counterfactual says what COULD change if the evidence came out a
certain way, never how likely that is. Ties are broken deterministically (priority, decision factor, weight,
then plan order).

Reachable counterfactuals (v3.1): a disputed cell is pinned only to scores that more evidence can actually
establish under the aggregation rules (pathfinder.consensus.reachability), and its decision factor is divided
by k, the minimum number of new agreeing independent families needed (assumption: one search adds at most one;
agreement is never assumed). A dispute that no amount of agreeing evidence can resolve (material, authoritative
or version-specific dissent) or that needs more families than the remaining searches is valued 0.5 and
labelled. Corroboration of a single-source or weak-consensus cell is likewise divided by its k.

Retry policy (retry_handling):
  - a target that just failed (no new verified evidence for it) is not repeated in the next round, unless it
    is the uniquely decisive target (factor 2, no other eligible target with factor >= 1.5) and has not been
    retried immediately before: a bounded retry with a different (broadened) query;
  - a failed target can be revisited later (no permanent blacklist), but each failure halves its priority;
  - at most 3 attempts per target, each with a query variant that is not a near-duplicate of an issued query.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from pathfinder.consensus import reachability
from pathfinder.matrix import Bounds, Cells, cell_key, robust_winner
from pathfinder.models import OPEN_STATES, RESOLVED_STATES, ActionKind, ResearchAction, ResearchPlan
from pathfinder.queries import MAX_QUERY_VARIANTS, build_query, near_duplicate
from pathfinder.readiness import Blocker, assess, corroboration_targets

COST_UNITS = 2.0
MAX_ATTEMPTS = 3
RETRY_PENALTY = 0.5
DECISIVE = 2.0
RULE_OUT = 1.25
DOMINATED = 0.5
UNEXPLORED_BONUS = 1.2
CONCENTRATION_STEP = 0.5
FORMULA = ("priority = weight x uncertainty x decision_factor x exploration_factor x retry_factor / cost_units "
           "(cost_units = 2); factors are disclosed heuristics, not probabilities")


@dataclass(frozen=True)
class PolicyConfig:
    """Which V3 components are active. Ablations switch one component off; `legacy_v2` runs the unchanged
    V2 policy (policy.choose_next_comparison) under the current scoring and stop rule."""
    name: str = "v3"
    decision_aware: bool = True
    readiness_aware: bool = True
    conflict_directed: bool = True
    retry_handling: bool = True
    exploration: bool = True
    legacy_v2: bool = False


POLICIES: dict[str, PolicyConfig] = {
    "v3": PolicyConfig(),
    "v2_policy": PolicyConfig(name="v2_policy", legacy_v2=True),
    "no_retry": PolicyConfig(name="no_retry", retry_handling=False),
    "no_decision": PolicyConfig(name="no_decision", decision_aware=False),
    "no_readiness": PolicyConfig(name="no_readiness", readiness_aware=False),
    "no_conflict": PolicyConfig(name="no_conflict", conflict_directed=False),
    "no_exploration": PolicyConfig(name="no_exploration", exploration=False),
}


@dataclass
class TargetHistory:
    """What the policy remembers about its own past actions (never about future evidence)."""
    failures: dict[str, int] = field(default_factory=dict)
    last_failed_round: dict[str, int] = field(default_factory=dict)
    immediate_retries: dict[str, int] = field(default_factory=dict)
    factor_at_failure: dict[str, float] = field(default_factory=dict)
    targeted: list[tuple[int, str, str | None, bool]] = field(default_factory=list)  # round, target, alt, ok

    @property
    def last(self) -> tuple[int, str, str | None, bool] | None:
        return self.targeted[-1] if self.targeted else None

    def recent_alternatives(self, n: int = 2) -> list[str]:
        return [alt for _, _, alt, _ in self.targeted[-n:] if alt]

    def record(self, round_no: int, target: str, alternative: str | None, success: bool,
               decision_factor: float | None = None, immediate_retry: bool = False) -> None:
        self.targeted.append((round_no, target, alternative, success))
        if immediate_retry:
            self.immediate_retries[target] = self.immediate_retries.get(target, 0) + 1
        if not success:
            self.failures[target] = self.failures.get(target, 0) + 1
            self.last_failed_round[target] = round_no
            if decision_factor is not None:
                self.factor_at_failure[target] = decision_factor


# ---------------------------------------------------------------------------- counterfactual arithmetic


def pinned_bounds(plan: ResearchPlan, cells: Cells, pins: dict[tuple[str, str], int] | None = None) -> Bounds:
    pins = pins or {}
    out: Bounds = {}
    for alt in plan.alternatives:
        lo_sum = hi_sum = 0
        for crit in plan.criteria:
            key = (alt.name, crit.criterion_id)
            lo, hi = (pins[key], pins[key]) if key in pins else (cells[key].lower, cells[key].upper)
            lo_sum += crit.weight * lo
            hi_sum += crit.weight * hi
        out[alt.name] = (lo_sum, hi_sum)
    return out


def outcome(plan: ResearchPlan, cells: Cells, pins: dict | None = None) -> tuple[str | None, str, Bounds]:
    """(leader, stability, bounds) from bounds alone: robust winner; else the unique top midpoint
    ('provisional'); else no leader ('tie')."""
    order = [a.name for a in plan.alternatives]
    b = pinned_bounds(plan, cells, pins)
    win = robust_winner(order, b)
    if win:
        return win, "robust", b
    mids = {a: (b[a][0] + b[a][1]) / 2 for a in order}
    best = max(mids.values())
    top = [a for a in order if mids[a] == best]
    return (top[0], "provisional", b) if len(top) == 1 else (None, "tie", b)


def dominated(b: Bounds) -> set[str]:
    """Alternatives ruled out: some other alternative's lower bound exceeds their upper bound."""
    return {a for a in b if any(b[o][0] > b[a][1] for o in b if o != a)}


DEFAULT_REMAINING = 3


def pin_values(cell, remaining: int = DEFAULT_REMAINING) -> list[int]:
    """Scores research could still establish for an open cell: the whole interval for unknown/insufficient
    cells; for a disputed cell only the scores reachable within the remaining searches."""
    if cell.state in ("unknown", "insufficient"):
        return list(range(cell.lower, cell.upper + 1))
    if cell.state == "disputed":
        reach = reachability(cell, remaining)
        return sorted(s for s, k in reach["reachable"].items() if k <= remaining)
    return []


def cell_counterfactual(plan: ResearchPlan, cells: Cells, key: tuple[str, str],
                        current: tuple[str | None, str, Bounds], values: list[int] | None = None) -> dict:
    """Pin the cell to each score it can reach and record what the decision would become."""
    leader, stability, b = current
    cell = cells[key]
    ruled_now = dominated(b)
    values_out = []
    for v in (values if values is not None else range(cell.lower, cell.upper + 1)):
        lv, sv, bv = outcome(plan, cells, {key: v})
        values_out.append({"score": v, "leader": lv, "stability": sv,
                           "ruled_out": sorted(dominated(bv) - ruled_now),
                           "bounds": {a: list(x) for a, x in bv.items()}})
    real = [x for x in values_out if x["leader"] is not None]
    return {
        "values": values_out,
        "changes_leader": leader is not None and any(x["leader"] != leader for x in real),
        "breaks_tie": stability == "tie" and bool(real),
        "makes_robust": stability != "robust" and any(x["stability"] == "robust" for x in values_out),
        "rules_out": any(x["ruled_out"] for x in values_out),
    }


MAX_GROUP = 4  # joint analysis looks at groups of 2..4 cells (exact search; plans have <= 20 cells)


def minimal_groups(plan: ResearchPlan, cells: Cells, current: tuple[str | None, str, Bounds],
                   remaining: int = DEFAULT_REMAINING) -> list[dict]:
    """Smallest groups (2 <= k <= 4) of open cells that could JOINTLY change the leader or make it robust.

    Exact search in increasing size: each cell is pinned to the extreme that favours the goal (challenger
    cells up / leader cells down for an overtake; leader cells up / other cells down for robustness). For each
    goal the result lists one example group and `members`: every cell that appears in ANY minimal group.
    Single-cell effects are handled by cell_counterfactual. A group is a possibility, not a prediction.
    """
    from itertools import combinations

    leader, stability, b = current
    if leader is None:
        return []
    order = [a.name for a in plan.alternatives]
    crit_order = [c.criterion_id for c in plan.criteria]
    allowed = {k: pin_values(c, remaining) for k, c in cells.items() if c.state in OPEN_STATES and c.upper > c.lower}
    open_cells = sorted((k for k, v in allowed.items() if v),  # only cells research can still move
                        key=lambda k: (order.index(k[0]), crit_order.index(k[1])))
    ruled = dominated(b)

    def search(goal: str, relevant: list[tuple[str, str]], pin_value, done) -> dict | None:
        for size in range(1, min(MAX_GROUP, len(relevant)) + 1):
            hits = []
            for combo in combinations(relevant, size):
                pins = {k: pin_value(k) for k in combo}
                if done(outcome(plan, cells, pins)):
                    hits.append(pins)
            if hits and size == 1:
                return None  # one cell suffices: a single-cell effect, so no larger group is minimal
            if hits:
                members = sorted({cell_key(*k) for h in hits for k in h},
                                 key=lambda x: (order.index(x.split(":", 1)[0]), x))
                return {"goal": goal, "cells": [cell_key(*k) for k in hits[0]],
                        "pins": {cell_key(*k): v for k, v in hits[0].items()}, "size": size,
                        "members": members, "minimal_groups_found": len(hits)}
        return None

    groups: list[dict] = []
    for comp in order:
        if comp == leader or comp in ruled:
            continue
        relevant = [k for k in open_cells if k[0] in (comp, leader)]
        g = search(f"{comp} overtakes {leader}", relevant,
                   lambda k, comp=comp: max(allowed[k]) if k[0] == comp else min(allowed[k]),
                   lambda o, comp=comp: o[0] == comp)
        if g:
            groups.append(g)
    if stability != "robust":
        g = search(f"{leader} becomes interval-robust", open_cells,
                   lambda k: max(allowed[k]) if k[0] == leader else min(allowed[k]),
                   lambda o: o[0] == leader and o[1] == "robust")
        if g:
            groups.append(g)
    return groups


def decision_relevant_open_cells(plan: ResearchPlan, cells: Cells, remaining: int = DEFAULT_REMAINING) -> list[str]:
    """Open cells whose REACHABLE resolution could, alone or within a minimal group, change the leader, break a
    tie or make the leader robust. Strategy-independent: also used by the COMMON stopping rule."""
    current = outcome(plan, cells)
    out = []
    for k, c in cells.items():
        if c.state not in OPEN_STATES:
            continue
        values = pin_values(c, remaining)
        if not values:
            continue
        cf = cell_counterfactual(plan, cells, k, current, values)
        if cf["changes_leader"] or cf["breaks_tie"] or cf["makes_robust"]:
            out.append(cell_key(*k))
    for g in minimal_groups(plan, cells, current, remaining):
        out += [k for k in g["members"] if k not in out]
    return out


# ----------------------------------------------------------------------------------- candidate scoring


def _blocker_cells(blockers: list[Blocker]) -> dict[tuple[str, str], list[Blocker]]:
    out: dict[tuple[str, str], list[Blocker]] = {}
    for bl in blockers:
        out.setdefault((bl.alternative, bl.criterion_id), []).append(bl)
    return out


def _query_for(plan, purpose, alt, crit, attempts, scope, issued, cfg) -> tuple[str, list[str], int] | None:
    start = attempts + (1 if purpose == "corroboration" else 0)  # corroboration needs an open query
    last = MAX_QUERY_VARIANTS if cfg.retry_handling else start + 1
    for variant in range(start, max(last, start + 1)):
        q, domains = build_query(plan, alt, crit, variant, scope=scope,
                                 purpose="conflict" if purpose == "conflict" and variant < 2 else None)
        if not cfg.retry_handling or not near_duplicate(q, issued):
            return q, domains, variant
    return None


def rank_candidates(plan: ResearchPlan, cells: Cells, attempts: dict[str, int], history: TargetHistory,
                    issued: list[str], cfg: PolicyConfig = POLICIES["v3"],
                    remaining: int = DEFAULT_REMAINING) -> tuple[list[dict], list[dict], dict]:
    """(eligible candidates sorted best-first, skipped targets with reasons, context) - all deterministic."""
    order = [a.name for a in plan.alternatives]
    crit_order = [c.criterion_id for c in plan.criteria]
    current = outcome(plan, cells)
    leader, stability, b = current
    ruled = dominated(b)
    readiness = assess(plan, cells)
    blockers = readiness.blockers if cfg.readiness_aware else []
    bcells = _blocker_cells(blockers)
    groups = minimal_groups(plan, cells, current, remaining) if cfg.decision_aware else []
    group_factor: dict[str, tuple[float, str]] = {}
    for g in groups:
        f = 1 + 1 / g["size"]
        for k in g["members"]:
            if f > group_factor.get(k, (0, ""))[0]:
                group_factor[k] = (f, g["goal"])

    raw: list[dict] = []
    for alt in plan.alternatives:
        for crit in plan.criteria:
            k = (alt.name, crit.criterion_id)
            cell = cells[k]
            if cell.state in OPEN_STATES:
                purpose = "conflict" if cell.state == "disputed" and cfg.conflict_directed else "uncertainty"
                raw.append({"key": k, "purpose": purpose, "uncertainty": cell.upper - cell.lower, "scope": None})
            elif k in bcells and cell.state in RESOLVED_STATES:
                scope = next((bl.scope for bl in bcells[k] if bl.scope), None)
                raw.append({"key": k, "purpose": "corroboration", "uncertainty": 1, "scope": scope})
    if not cfg.readiness_aware:  # V2 behaviour: corroborate only once the interval is robust
        for t in (corroboration_targets(plan, cells) if stability == "robust" else []):
            k = (t["alternative"], t["criterion_id"])
            if not any(r["key"] == k and r["purpose"] == "corroboration" for r in raw):
                raw.append({"key": k, "purpose": "corroboration", "uncertainty": 1, "scope": t["scope"]})

    for r in raw:
        k = r["key"]
        ck = cell_key(*k)
        effects: list[str] = []
        factor = 1.0
        cf = None
        reach = reachability(cells[k], remaining)
        k_needed = reach.get("k") or 1
        unreachable = reach["class"] in ("unresolvable_by_more_evidence", "needs_scope_or_authority_clarification",
                                         "unlikely_within_budget", "not_applicable")
        if r["purpose"] != "corroboration":
            values = pin_values(cells[k], remaining)
            cf = cell_counterfactual(plan, cells, k, current, values) if values else None
        if cfg.decision_aware and cf is not None:
            if cf["changes_leader"]:
                effects.append("could change the leader")
            if cf["breaks_tie"]:
                effects.append("could break the tie")
            if cf["makes_robust"]:
                effects.append("could make the leader interval-robust")
            if effects:
                factor = DECISIVE
            elif ck in group_factor:
                factor = group_factor[ck][0]
                effects.append(f"jointly matters: {group_factor[ck][1]} needs a group of "
                               f"{round(1 / (factor - 1))} cells")
            elif cf["rules_out"]:
                factor = RULE_OUT
                effects.append("could rule out another alternative")
        if k in bcells:
            n = len(bcells)
            rf = (DECISIVE if n == 1 else 1 + 1 / n) if stability == "robust" else 1 + 1 / (n + 1)
            effects.append("readiness blocker: " + "; ".join(bl.reason for bl in bcells[k]))
            factor = max(factor, rf)
        elif r["purpose"] == "corroboration":  # no_readiness ablation: V2 corroboration weight
            effects.append("corroborate a differentiating cell of the robust leader")
        if factor == 1.0 and cfg.decision_aware and k[0] in ruled:
            factor = DOMINATED
            effects.append(f"{k[0]} is already ruled out")
        if cells[k].state in ("disputed", "consensus") or r["purpose"] == "corroboration":
            if unreachable:
                factor = min(factor, DOMINATED)
                effects.append(f"more research cannot change this cell under the aggregation rules "
                               f"({reach['class']})")
            elif k_needed > 1:
                factor = factor / k_needed
                effects.append(f"needs {k_needed} more agreeing independent source families ({reach['class']})")
        r.update(alternative=k[0], criterion_id=k[1], cell=ck, state=cells[k].state,
                 weight=plan.criterion(k[1]).weight, decision_factor=round(factor, 4), effects=effects,
                 counterfactual=cf, reach={"class": reach["class"], "k": reach.get("k"),
                                           "reachable_scores": sorted(reach.get("reachable", {}))})
        r["target_id"] = ck + {"uncertainty": "", "conflict": "#conflict", "corroboration": "#corroborate"}[r["purpose"]]

    others_valuable = {a: any(x["alternative"] != a and x["decision_factor"] >= 1.0 for x in raw) for a in order}
    targeted_alts = {alt for _, _, alt, _ in history.targeted if alt}
    recent = history.recent_alternatives(2)
    eligible, skipped = [], []
    last = history.last
    for r in raw:
        tid = r["target_id"]
        tried = attempts.get(tid, 0)
        fails = history.failures.get(tid, 0)
        explore = 1.0
        if cfg.exploration:
            n = recent.count(r["alternative"])
            if n and others_valuable[r["alternative"]]:
                explore /= 1 + CONCENTRATION_STEP * n
            if history.targeted and r["alternative"] not in targeted_alts:
                explore *= UNEXPLORED_BONUS
        retry = RETRY_PENALTY ** fails if cfg.retry_handling else 1.0
        max_attempts = MAX_ATTEMPTS if cfg.retry_handling else 2
        if tried >= max_attempts:
            skipped.append({"target_id": tid, "reason": f"maximum attempts ({max_attempts}) reached"})
            continue
        q = _query_for(plan, r["purpose"], r["alternative"], r["criterion_id"], tried, r["scope"], issued, cfg)
        if q is None:
            skipped.append({"target_id": tid, "reason": "no query variant left that is not a near-duplicate"})
            continue
        r["query"], r["domains"], r["query_variant"] = q
        r["immediate"] = bool(last and last[1] == tid and not last[3])
        r["attempts"], r["failures"] = tried, fails
        r["exploration_factor"], r["retry_factor"] = round(explore, 4), retry
        value = r["weight"] * r["uncertainty"] * r["decision_factor"]
        r["value"] = value
        r["priority"] = round(value * explore * retry / COST_UNITS, 4)
        eligible.append(r)

    purpose_rank = {"uncertainty": 0, "conflict": 1, "corroboration": 2}
    eligible.sort(key=lambda r: (-r["priority"], -r["decision_factor"], -r["weight"], order.index(r["alternative"]),
                                 crit_order.index(r["criterion_id"]), purpose_rank[r["purpose"]]))
    if cfg.retry_handling:  # cool-down after a failure, except one bounded retry of a uniquely decisive target
        kept = []
        for r in eligible:
            if not r["immediate"]:
                kept.append(r)
                continue
            rivals = [x for x in eligible if x is not r and not x["immediate"] and x["decision_factor"] >= 1.5]
            if (r["decision_factor"] >= DECISIVE and not rivals
                    and history.immediate_retries.get(r["target_id"], 0) == 0):
                r["bounded_retry_reason"] = ("uniquely decisive target and no other target with decision "
                                             "value >= 1.5; one bounded retry with a different query")
                kept.append(r)
            else:
                skipped.append({"target_id": r["target_id"],
                                "reason": "cool-down: failed in the previous round; other targets available"})
        if not kept and eligible:  # every remaining target is in cool-down: explicit fallback
            kept = [dict(eligible[0], bounded_retry_reason="fallback: only cool-down targets remain")]
        eligible = kept
    context = {"leader": leader, "stability": stability, "bounds": {a: list(x) for a, x in b.items()},
               "ruled_out": sorted(ruled), "groups": groups,
               "readiness_blockers": [bl.reason for bl in blockers], "formula": FORMULA, "policy": cfg.name}
    return eligible, skipped, context


def _kind(r: dict, history: TargetHistory) -> ActionKind:
    if r.get("immediate"):  # the decisive reason for the action is the retry, whatever its purpose
        return "bounded_retry"
    if r["purpose"] == "corroboration":
        return "corroboration"
    if r["purpose"] == "conflict":
        return "conflict_resolution"
    if r["failures"]:
        before = history.factor_at_failure.get(r["target_id"], 0.0)
        return "targeted" if r["decision_factor"] > before else "fallback_exploration"
    return "targeted" if r["decision_factor"] > 1.0 else "fallback_exploration"


def explain(r: dict, kind: str) -> str:
    what = {"uncertainty": "is " + r["state"], "conflict": f"is disputed (interval width {r['uncertainty']})",
            "corroboration": "is supported but blocks readiness"}[r["purpose"]]
    effect = "; ".join(r["effects"]) if r["effects"] else "no counterfactual effect on the decision (coverage only)"
    text = (f"Researching {r['cell']} (weight {r['weight']}) because it {what}: {effect}. "
            f"Priority {r['weight']} x {r['uncertainty']} x {r['decision_factor']:.2f} (decision) x "
            f"{r['exploration_factor']:.2f} (exploration) x {r['retry_factor']:.2f} (retry) / 2 = {r['priority']:.2f}.")
    if kind == "bounded_retry" or r.get("bounded_retry_reason"):
        text += f" Retry: {r.get('bounded_retry_reason', '')}."
    elif r["failures"]:
        text += (f" Revisit after {r['failures']} failed attempt(s): "
                 + ("its decision value increased since the failure." if kind == "targeted"
                    else "fallback, no untried target ranks higher."))
    return text


def choose_next(plan: ResearchPlan, cells: Cells, attempts: dict[str, int], history: TargetHistory,
                issued: list[str], action_no: int, cfg: PolicyConfig = POLICIES["v3"],
                remaining: int = DEFAULT_REMAINING) -> ResearchAction | None:
    eligible, skipped, context = rank_candidates(plan, cells, attempts, history, issued, cfg, remaining)
    if not eligible:
        return None
    r = eligible[0]
    kind = _kind(r, history)

    def brief(x: dict) -> dict:
        return {k: x.get(k) for k in ("target_id", "purpose", "state", "weight", "uncertainty", "decision_factor",
                                      "exploration_factor", "retry_factor", "priority", "effects", "attempts",
                                      "failures", "query", "reach")}

    analysis = {**context, "chosen": {**brief(r), "counterfactual": r["counterfactual"],
                                      "bounded_retry_reason": r.get("bounded_retry_reason")},
                "candidates": [brief(x) for x in eligible[:6]], "skipped": skipped}
    return ResearchAction(action_id=f"ACT_{action_no}", target_id=r["target_id"], queries=[r["query"]],
                          include_domains=r["domains"], predicted_gain=float(r["value"]),
                          estimated_cost_units=COST_UNITS, action_score=float(r["priority"]),
                          flip_relevant=r["decision_factor"] >= DECISIVE and r["purpose"] != "corroboration",
                          why_selected=explain(r, kind), action_kind=kind, analysis=analysis)
