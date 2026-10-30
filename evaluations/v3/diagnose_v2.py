"""Phase 1 diagnosis of the V2 benchmark from the recorded decision traces (offline, no API calls).

Reads outputs/<V2 record dir>/EVAL_*; rebuilds the state before every action from evidence verified in
earlier rounds only; writes evaluations/v3/diagnosis_v2.json (numbers) used by DIAGNOSIS_V2.md.
Usage: python evaluations/v3/diagnose_v2.py outputs/eval_v2_E_20261030T045521_1e5cc3
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from pathfinder.matrix import decision_state, outcome_leader, robust_winner
from pathfinder.models import RESOLVED_STATES, Mode
from pathfinder.policy import flip_relevant
from pathfinder.readiness import assess
from pathfinder.trace_replay import cells_before, load_run, new_evidence_in_round

NAME = re.compile(r"EVAL_(Q\d+)_r(\d+)_(static|adaptive)_")


def base_target(target_id: str) -> str:
    return target_id.split("#", 1)[0]


def pinned_leader(plan, cells, pins: dict) -> str:
    """Outcome leader with several cells pinned (group counterfactual; used only for this diagnosis)."""
    order = [a.name for a in plan.alternatives]
    b = {}
    for alt in plan.alternatives:
        lo = hi = 0
        for crit in plan.criteria:
            key = (alt.name, crit.criterion_id)
            if key in pins:
                c_lo = c_hi = pins[key]
            else:
                c_lo, c_hi = cells[key].lower, cells[key].upper
            lo += crit.weight * c_lo
            hi += crit.weight * c_hi
        b[alt.name] = (lo, hi)
    win = robust_winner(order, b)
    if win:
        return win
    mids = {a: sum(b[a]) / 2 for a in order}
    best = max(mids.values())
    return next(a for a in order if mids[a] == best)


def group_relevant(plan, cells) -> bool:
    """Can SOME pair of open cells, pinned to extremes, change the outcome leader (when no single cell can)?"""
    open_cells = [k for k, c in cells.items() if c.state not in RESOLVED_STATES]
    leader = outcome_leader(plan, cells)
    for i, a in enumerate(open_cells):
        for b in open_cells[i + 1:]:
            for va in (0, 2):
                for vb in (0, 2):
                    if pinned_leader(plan, cells, {a: va, b: vb}) != leader:
                        return True
    return False


def main(record_dir: str) -> None:
    rec = Path(record_dir)
    runs = {}
    for d in sorted(rec.glob("EVAL_*")):
        m = NAME.match(d.name)
        if m:
            runs[(m.group(1), int(m.group(2)), m.group(3))] = load_run(d)
    out: dict = {"record_dir": str(rec), "runs": len(runs)}

    # A. reconstruction fidelity -------------------------------------------------------------------
    checked = mismatched = 0
    for t in runs.values():
        if t.plan.mode != Mode.COMPARISON:
            continue
        for m in t.round_metrics:
            cells = cells_before(t, m["round"] + 1)
            r = assess(t.plan, cells)
            got = (sum(1 for c in cells.values() if c.state in RESOLVED_STATES), r.interval_leader, r.stability,
                   r.status)
            want = (m["units_supported"], m["interval_leader"], m["stability"], m["recommendation"])
            checked += 1
            mismatched += got != want
    out["fidelity"] = {"comparison_rounds_checked": checked, "mismatches": mismatched}

    # B/C. targeting: repeats, flip relevance, availability of alternatives -------------------------
    rounds = []
    for (qid, rep, arm), t in runs.items():
        prev = None
        for a in t.actions:
            r = a["round"]
            if r == 0:
                continue
            tid = a["target_id"]
            new = new_evidence_in_round(t, r - 1) if prev else []
            prev_failed = prev is not None and not any(base_target(e.target_id) == base_target(prev) or
                                                       (t.plan.mode != Mode.COMPARISON) for e in new)
            row = {"qid": qid, "rep": rep, "arm": arm, "round": r, "target": tid, "mode": t.plan.mode.value,
                   "repeat_prev": tid == prev, "prev_failed": prev_failed,
                   "success": any(base_target(e.target_id) == base_target(tid) or t.plan.mode != Mode.COMPARISON
                                  for e in new_evidence_in_round(t, r)),
                   "flip_relevant": bool(a.get("flip_relevant")), "corroborate": "#corroborate" in tid}
            if t.plan.mode == Mode.COMPARISON:
                cells = cells_before(t, r)
                open_cells = [k for k, c in cells.items() if c.state not in RESOLVED_STATES]
                single = [k for k in open_cells if flip_relevant(t.plan, cells, *k)]
                row.update(open_cells=len(open_cells), single_flip_cells=len(single),
                           target_state=cells[tuple(base_target(tid).split(":", 1))].state
                           if ":" in base_target(tid) else None,
                           group_relevant=(not single and group_relevant(t.plan, cells)),
                           state=decision_state(t.plan, cells).stability,
                           target_already_supported=(":" in base_target(tid) and "#" not in tid and
                                                     cells[tuple(base_target(tid).split(":", 1))].state
                                                     in RESOLVED_STATES))
            rounds.append(row)
            prev = tid
    out["targeted_rounds"] = rounds

    def summ(rows):
        return {"rounds": len(rows), "repeat_prev": sum(r["repeat_prev"] for r in rows),
                "repeat_after_failure": sum(r["repeat_prev"] and r["prev_failed"] for r in rows),
                "repeat_succeeded": sum(r["repeat_prev"] and r["success"] for r in rows),
                "success": sum(r["success"] for r in rows)}

    out["summary_targeting"] = {}
    for arm in ("adaptive", "static"):
        rows = [r for r in rounds if r["arm"] == arm]
        comp = [r for r in rows if r["mode"] == "comparison"]
        out["summary_targeting"][arm] = {
            "all": summ(rows), "comparison": summ(comp), "discovery": summ([r for r in rows if r["mode"] != "comparison"]),
            "comparison_flip_relevant_chosen": sum(r["flip_relevant"] for r in comp),
            "comparison_corroborate": sum(r["corroborate"] for r in comp),
            "comparison_rounds_with_any_single_flip_cell": sum(r["single_flip_cells"] > 0 for r in comp),
            "comparison_rounds_group_only_relevant": sum(r["group_relevant"] for r in comp),
            "comparison_rounds_no_relevance_at_all": sum(r["single_flip_cells"] == 0 and not r["group_relevant"]
                                                         and not r["corroborate"] for r in comp),
            "target_already_supported": sum(bool(r.get("target_already_supported")) for r in comp),
            "repeat_with_other_open_cells": sum(r["repeat_prev"] and r.get("open_cells", 0) > 1 for r in comp),
        }

    # D. disputes ----------------------------------------------------------------------------------
    disputes = []
    coverage_drops = []
    for (qid, rep, arm), t in runs.items():
        if t.plan.mode != Mode.COMPARISON:
            continue
        last = max(m["round"] for m in t.round_metrics)
        cells = cells_before(t, last + 1)
        for k, c in cells.items():
            if c.state == "disputed":
                evs = [e for e in t.evidence if e.target_id == f"{k[0]}:{k[1]}"]
                disputes.append({"qid": qid, "rep": rep, "arm": arm, "cell": f"{k[0]}:{k[1]}",
                                 "scores": sorted({e.score for e in evs}),
                                 "scopes": sorted({e.scope for e in evs}),
                                 "sources": len({t.domains.get(e.source_id) for e in evs})})
        prev_units = None
        for m in t.round_metrics:
            if prev_units is not None and m["units_supported"] < prev_units:
                coverage_drops.append({"qid": qid, "rep": rep, "arm": arm, "round": m["round"],
                                       "from": prev_units, "to": m["units_supported"]})
            prev_units = m["units_supported"]
    out["disputes_final"] = disputes
    out["disputes_summary"] = {
        "cells": len(disputes),
        "by_arm": dict(Counter(d["arm"] for d in disputes)),
        "score_sets": dict(Counter(str(d["scores"]) for d in disputes)),
        "adjacent_1_2": sum(d["scores"] == [1, 2] for d in disputes),
        "adjacent_0_1": sum(d["scores"] == [0, 1] for d in disputes),
        "spanning_0_2": sum(0 in d["scores"] and 2 in d["scores"] for d in disputes)}
    out["coverage_drops"] = coverage_drops

    # E. premature stops (common_stop view lost units the full budget later found) -----------------
    stops = []
    for (qid, rep, arm), t in runs.items():
        traj = t.round_metrics
        ws = next((m for m in traj if m["would_stop"]), traj[-1])
        final = traj[-1]
        if ws["round"] < final["round"] and final["units_supported"] > ws["units_supported"]:
            stops.append({"qid": qid, "rep": rep, "arm": arm, "stop_round": ws["round"], "would_stop": ws["would_stop"],
                          "units_at_stop": ws["units_supported"], "units_full": final["units_supported"],
                          "new_units_per_round": [m["new_units"] for m in traj],
                          "tool_or_llm_failures_by_round": dict(Counter(f["round"] for f in t.tool_failures)),
                          "round0_new_units": traj[0]["new_units"]})
    out["premature_stops"] = stops

    # F. readiness ---------------------------------------------------------------------------------
    reasons = Counter()
    statuses = Counter()
    for t in runs.values():
        rp = json.loads((t.run_dir / "report.json").read_text("utf-8"))
        if t.plan.mode != Mode.COMPARISON:
            continue
        statuses[rp.get("recommendation_status")] += 1
        for r in rp.get("recommendation_withheld_reasons") or []:
            reasons[r.split(":")[0].split("(")[0].strip()] += 1
    out["readiness"] = {"status": dict(statuses), "withheld_reasons": dict(reasons)}

    # G. plan variance -----------------------------------------------------------------------------
    plans = defaultdict(dict)
    for (qid, rep, arm), t in runs.items():
        if arm == "static":
            plans[qid][rep] = {"alternatives": [a.name for a in t.plan.alternatives],
                               "criteria": [c.criterion_id for c in t.plan.criteria],
                               "facets": [f.facet_id for f in t.plan.facets],
                               "units": t.round_metrics[0]["units_total"]}
    out["plans"] = plans

    # H. counted flips -----------------------------------------------------------------------------
    flips = []
    for (qid, rep, arm), t in runs.items():
        for e in (json.loads((t.run_dir / "report.json").read_text("utf-8")).get("decision_changes") or []):
            if e["kind"] == "leader_changed":
                flips.append({"qid": qid, "rep": rep, "arm": arm, **e})
    out["flips"] = flips

    dest = Path(__file__).with_name("diagnosis_v2.json")
    dest.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(json.dumps({k: out[k] for k in ("fidelity", "summary_targeting", "disputes_summary", "readiness")},
                     indent=1))
    print("coverage drops", coverage_drops)
    print("premature", json.dumps(stops, indent=0))
    print("plans", {q: {r: v["units"] for r, v in p.items()} for q, p in plans.items()})


if __name__ == "__main__":
    main(sys.argv[1])
