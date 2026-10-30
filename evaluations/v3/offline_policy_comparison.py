"""Phase 9: OFFLINE POLICY COMPARISON on identical frozen inputs (no API calls, not live performance).

For every targeted decision point of the recorded V2 benchmark, the state before the action is rebuilt from
evidence verified in EARLIER rounds only (trace_replay.evidence_before). On that identical state:
  * the V2 policy is re-run (fidelity check: it must reproduce the action V2 actually took);
  * the V3 policy is run (what V3 would have chosen at that point).
This compares DECISIONS, not outcomes: what V3's choice would have found is unknown (it was never searched),
so no coverage or accuracy claim follows from this file.

It also re-evaluates the V3 COMMON stop rule on the same V2 trajectories (decisions unchanged), and re-scores
each run's final V2 evidence with the V3 dispute rule.

NOTE (v3.1): this analysis was produced with the V3 (pre-v3.1) aggregation; its saved output
(offline_policy_comparison.json / .md) is the historical record. Re-running it with the v3.1 package would mix
aggregation semantics (its `v2_cells` only widens disputes to [0, 2]); use the frozen pilot code for exact reruns.

Usage: python evaluations/v3/offline_policy_comparison.py outputs/eval_v2_E_20261030T045521_1e5cc3
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

from pathfinder.acquisition import POLICIES, choose_next, decision_relevant_open_cells
from pathfinder.matrix import build_cells
from pathfinder.models import OPEN_STATES, RESOLVED_STATES, Mode
from pathfinder.policy import choose_next_comparison
from pathfinder.readiness import assess
from pathfinder.trace_replay import cells_v3, evidence_before, history_before, load_run

NAME = re.compile(r"EVAL_(Q\d+)_r(\d+)_(static|adaptive)_")


def v3_cells(t, round_no):
    return cells_v3(t, round_no)


def v2_cells(t, round_no):
    """V2 matrix semantics: disputed is [0, 2] and there is no `insufficient` state."""
    cells = build_cells(t.plan, evidence_before(t, round_no), t.domains, t.published)
    return {k: (c.model_copy(update={"lower": 0, "upper": 2}) if c.state == "disputed" else c)
            for k, c in cells.items()}


def compare_decisions(runs) -> dict:
    rows = []
    fidelity = Counter()
    for (qid, rep, arm), t in sorted(runs.items()):
        if t.plan.mode != Mode.COMPARISON:
            continue
        for a in t.actions:
            r = a["round"]
            if r == 0:
                continue
            attempts, hist, issued = history_before(t, r)
            if arm == "adaptive":
                v2 = choose_next_comparison(t.plan, v2_cells(t, r), attempts, r + 1)
                fidelity["match" if v2 and v2.target_id == a["target_id"] else "mismatch"] += 1
            v3 = choose_next(t.plan, v3_cells(t, r), attempts, hist, issued, r + 1, POLICIES["v3"])
            prev = hist.last
            recorded_repeat = bool(prev and prev[1] == a["target_id"] and not prev[3])
            cells3 = v3_cells(t, r)
            relevant = set(decision_relevant_open_cells(t.plan, cells3))
            rec_base = a["target_id"].split("#", 1)[0]
            rows.append({
                "qid": qid, "rep": rep, "arm": arm, "round": r, "recorded": a["target_id"],
                "v3": v3.target_id if v3 else None, "same": bool(v3 and v3.target_id == a["target_id"]),
                "v3_kind": v3.action_kind if v3 else None,
                "v3_factor": (v3.analysis.get("chosen") or {}).get("decision_factor") if v3 else None,
                "v3_effects": (v3.analysis.get("chosen") or {}).get("effects") if v3 else None,
                "recorded_repeat_after_failure": recorded_repeat,
                "recorded_target_decision_relevant": rec_base in relevant,
                "v3_target_decision_relevant": bool(v3) and v3.target_id.split("#", 1)[0] in relevant,
                "v3_groups": len(v3.analysis.get("groups") or []) if v3 else 0,
                "open_cells": sum(1 for c in cells3.values() if c.state in OPEN_STATES),
            })
    return {"fidelity_v2_policy": dict(fidelity), "rows": rows}


def stop_rule_on_v2_trajectories(runs, settings_max_no_progress: int = 2) -> list[dict]:
    """Re-evaluate the V3 common stop rule round by round on the recorded V2 trajectories."""
    out = []
    for (qid, rep, arm), t in sorted(runs.items()):
        rounds = [m["round"] for m in t.round_metrics]
        last = rounds[-1]
        failed_rounds = {f["round"] for f in t.tool_failures}
        failed_rounds |= {x.get("round", 0) for x in t.rejected if "verifier unavailable" in x.get("reason", "")}
        counter = 0
        v3_stop = None
        for r in rounds:
            if t.plan.mode == Mode.COMPARISON:
                cb, ca = v3_cells(t, r), v3_cells(t, r + 1)
                progress = sum(1 for k in ca if (ca[k].state, ca[k].lower, ca[k].upper)
                               != (cb[k].state, cb[k].lower, cb[k].upper)
                               and {ca[k].state, cb[k].state} != {"unknown", "insufficient"})
            else:
                progress = t.round_metrics[rounds.index(r)]["new_units"]
            if progress > 0:
                counter = 0
            elif r == 0 or r in failed_rounds:
                pass
            else:
                counter += 1
            if r >= 1 and counter >= settings_max_no_progress:
                pending = []
                if t.plan.mode == Mode.COMPARISON:
                    attempts, _, _ = history_before(t, r + 1)
                    pending = [k for k in decision_relevant_open_cells(t.plan, v3_cells(t, r + 1))
                               if not attempts.get(k) and not attempts.get(f"{k}#conflict")]
                if not pending:
                    v3_stop = r
                    break
            if t.plan.mode == Mode.COMPARISON:
                ready = assess(t.plan, v3_cells(t, r + 1)).status == "ready"
                robust = assess(t.plan, v3_cells(t, r + 1)).stability == "robust"
                if ready and robust:
                    v3_stop = r
                    break
        v2_stop = next((m["round"] for m in t.round_metrics if m["would_stop"]), last)
        final = t.round_metrics[-1]["units_supported"]
        v3_round = v3_stop if v3_stop is not None else last
        by_round = {m["round"]: m for m in t.round_metrics}

        def units_at(r, by_round=by_round):
            return by_round[r]["units_supported"]

        def actions_at(r, by_round=by_round):
            return by_round[r]["actions"]
        out.append({"qid": qid, "rep": rep, "arm": arm, "v2_stop_round": v2_stop, "v3_stop_round": v3_round,
                    "v2_actions_saved": t.round_metrics[-1]["actions"] - actions_at(v2_stop),
                    "v3_actions_saved": t.round_metrics[-1]["actions"] - actions_at(v3_round),
                    "v2_premature": units_at(v2_stop) < final, "v3_premature": units_at(v3_round) < final,
                    "v2_units_at_stop": units_at(v2_stop), "v3_units_at_stop": units_at(v3_round),
                    "units_full": final})
    return out


def rescore_final(runs) -> dict:
    """Final V2 evidence under the V3 rule: disputed intervals narrowed, coverage definition unchanged."""
    res = Counter()
    for (_qid, _rep, _arm), t in runs.items():
        if t.plan.mode != Mode.COMPARISON:
            continue
        end = t.round_metrics[-1]["round"] + 1
        c2, c3 = v2_cells(t, end), v3_cells(t, end)
        res["supported_v2"] += sum(1 for c in c2.values() if c.state in RESOLVED_STATES)
        res["supported_v3"] += sum(1 for c in c3.values() if c.state in RESOLVED_STATES)
        res["disputed"] += sum(1 for c in c3.values() if c.state == "disputed")
        res["disputed_narrowed"] += sum(1 for c in c3.values() if c.state == "disputed" and c.upper - c.lower < 2)
        res["insufficient_v3"] += sum(1 for c in c3.values() if c.state == "insufficient")
        a2 = assess(t.plan, c2)
        a3 = assess(t.plan, c3)
        # both columns use the V3 readiness rules; they differ ONLY in the dispute interval ([0,2] vs [min,max])
        res[f"v2_dispute_interval_{a2.stability}"] += 1
        res[f"v3_dispute_interval_{a3.stability}"] += 1
        res[f"v2_dispute_interval_ready={a2.status == 'ready'}"] += 1
        res[f"v3_dispute_interval_ready={a3.status == 'ready'}"] += 1
        res["interval_leader_differs"] += a2.interval_leader != a3.interval_leader
    return dict(sorted(res.items()))


def main(record_dir: str) -> None:
    runs = {}
    for d in sorted(Path(record_dir).glob("EVAL_*")):
        m = NAME.match(d.name)
        if m:
            runs[(m.group(1), int(m.group(2)), m.group(3))] = load_run(d)
    dec = compare_decisions(runs)
    rows = dec["rows"]
    ad = [r for r in rows if r["arm"] == "adaptive"]
    summary = {
        "decision_points_adaptive": len(ad),
        "v2_policy_fidelity": dec["fidelity_v2_policy"],
        "v3_same_as_v2": sum(r["same"] for r in ad),
        "v2_repeats_after_failure": sum(r["recorded_repeat_after_failure"] for r in ad),
        "v3_at_those_points_repeats": sum(r["recorded_repeat_after_failure"] and r["same"] for r in ad),
        "v3_kinds": dict(Counter(r["v3_kind"] for r in ad)),
        "v2_choice_decision_relevant": sum(r["recorded_target_decision_relevant"] for r in ad),
        "v3_choice_decision_relevant": sum(r["v3_target_decision_relevant"] for r in ad),
        "points_with_any_relevant_open_cell": sum(r["v3_target_decision_relevant"] or r["recorded_target_decision_relevant"]
                                                  for r in ad),
        "v3_factor_distribution": dict(Counter(str(r["v3_factor"]) for r in ad)),
    }
    stops = stop_rule_on_v2_trajectories(runs)
    summary["stop_rule"] = {"runs": len(stops), "v2_rule_premature": sum(s["v2_premature"] for s in stops),
                            "v3_rule_premature": sum(s["v3_premature"] for s in stops),
                            "v3_rule_earlier_than_v2": sum(s["v3_stop_round"] < s["v2_stop_round"] for s in stops),
                            "v3_rule_later_than_v2": sum(s["v3_stop_round"] > s["v2_stop_round"] for s in stops),
                            "v2_rule_actions_saved": sum(s["v2_actions_saved"] for s in stops),
                            "v3_rule_actions_saved": sum(s["v3_actions_saved"] for s in stops),
                            "v2_rule_units_lost": sum(s["units_full"] - s["v2_units_at_stop"] for s in stops),
                            "v3_rule_units_lost": sum(s["units_full"] - s["v3_units_at_stop"] for s in stops)}
    summary["ready_under_v3_readiness_recorded_v2_ready_runs"] = [
        {"qid": q, "rep": r, "arm": a, "v3_status": assess(t.plan, v3_cells(t, t.round_metrics[-1]["round"] + 1)).status,
         "v3_reasons": assess(t.plan, v3_cells(t, t.round_metrics[-1]["round"] + 1)).reasons}
        for (q, r, a), t in sorted(runs.items())
        if t.plan.mode == Mode.COMPARISON and t.round_metrics[-1].get("recommendation") == "ready"]
    summary["rescore_final_v2_evidence"] = rescore_final(runs)
    out = {"label": "OFFLINE POLICY COMPARISON on frozen V2 inputs - decisions only, not live performance",
           "summary": summary, "decisions": rows, "stops": stops}
    dest = Path(__file__).with_name("offline_policy_comparison.json")
    dest.write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
