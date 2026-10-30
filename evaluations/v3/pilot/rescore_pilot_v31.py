"""Retrospective offline re-scoring of V3 pilot evidence under v3.1 aggregation - NOT a new controlled live benchmark.

Recomputes each pilot run's FINAL cells from its saved verified evidence (no API calls) and compares them with
the cells the pilot rules produced (`rescoring_baseline_pilot_rules.json`, saved before the code changed).
The research trajectories were chosen under the pilot rules; live v3.1 trajectories could differ.

Usage: python evaluations/v3/pilot/rescore_pilot_v31.py
Writes: evaluations/v3/pilot/rescoring_v31.json and RESCORING_V31.md (original artifacts untouched).
"""

from __future__ import annotations

import glob
import json
from collections import Counter
from pathlib import Path

from pathfinder.matrix import bounds
from pathfinder.models import RESOLVED_STATES
from pathfinder.readiness import assess
from pathfinder.trace_replay import cells_v3, load_run

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
RECORD = ROOT / "outputs" / "eval_v3_E_20261030T071515_43c018"
ORDER = ["static", "v2_policy", "adaptive"]


def main() -> None:
    base = json.loads((HERE / "rescoring_baseline_pilot_rules.json").read_text("utf-8"))
    out: dict = {"label": "Retrospective offline re-scoring of V3 pilot evidence - NOT a new controlled live benchmark",
                 "runs": {}}
    for d in sorted(glob.glob(str(RECORD / "EVAL_*"))):
        t = load_run(Path(d))
        name = Path(d).name.split("_2026")[0][5:]
        end = t.round_metrics[-1]["round"] + 1
        cells = cells_v3(t, end)
        r = assess(t.plan, cells)
        old = base[name]
        rows = {}
        for (a, k), c in cells.items():
            key = f"{a}:{k}"
            o = old["cells"][key]
            rows[key] = {"old_state": o["state"], "old_interval": [o["lower"], o["upper"]], "old_observed": o["observed"],
                         "new_state": c.state, "new_kind": c.dispute_kind, "new_interval": [c.lower, c.upper],
                         "new_score": c.score, "families": c.families, "certain_families": c.certain_families,
                         "dimension_mismatch": c.dimension_mismatch, "factual_confidence": c.factual_confidence,
                         "decision": (c.consensus.get("summary") or next(iter(c.consensus.values()), {})).get("decision")}
        old_supported = sum(1 for x in old["cells"].values() if x["state"] in ("supported", "scope_dependent"))
        new_supported = sum(1 for c in cells.values() if c.state in RESOLVED_STATES and not c.dimension_mismatch)
        out["runs"][name] = {
            "old": {"supported": old_supported, "leader": old["leader"], "stability": old["stability"],
                    "recommendation": old["recommendation"], "bounds": old["bounds"],
                    "disputed": sum(1 for x in old["cells"].values() if x["state"] == "disputed")},
            "new": {"supported": new_supported, "leader": r.interval_leader, "stability": r.stability,
                    "recommendation": r.status, "reasons": r.reasons,
                    "bounds": {a: list(v) for a, v in bounds(t.plan, cells).items()},
                    "consensus": sum(1 for c in cells.values() if c.state == "consensus"),
                    "disputed": sum(1 for c in cells.values() if c.state == "disputed")},
            "newly_supported": [k for k, v in rows.items() if v["new_state"] == "supported" and v["old_state"] != "supported"],
            "newly_consensus": [f"{k} ({v['new_kind']})" for k, v in rows.items() if v["new_state"] == "consensus"],
            "still_disputed": [f"{k} ({v['new_kind']})" for k, v in rows.items() if v["new_state"] == "disputed"],
            "source_inconsistent": [k for k, v in rows.items() if v["new_kind"] == "source_inconsistent"],
            "dimension_mismatch": [k for k, v in rows.items() if v["dimension_mismatch"]],
            "changed_cells": {k: v for k, v in rows.items()
                              if (v["old_state"], v["old_interval"]) != (v["new_state"], v["new_interval"])
                              or v["new_kind"] in ("source_inconsistent",)},
        }
    (HERE / "rescoring_v31.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    write_md(out)
    print((HERE / "RESCORING_V31.md").read_text("utf-8"))


def write_md(out: dict) -> None:
    L = ["# Retrospective offline re-scoring of V3 pilot evidence (v3.1 aggregation)", "",
         "> **NOT a new controlled live benchmark.** Each pilot run's saved, verified evidence is re-aggregated with "
         "the v3.1 rules; no API call is made and no original artifact is modified "
         "(`HISTORICAL_ARTIFACTS_SHA256.txt` verifies this). The research trajectories were chosen under the pilot "
         "rules, so live v3.1 runs could follow different paths. Nothing here shows that V3 performs better.", "",
         "Supported = cells with a single comparable score or a scope-dependent split (v3.1 excludes cells whose cost "
         "evidence measures incompatible dimensions). Old figures are the pilot's own (`rescoring_baseline_pilot_rules.json`).",
         "", "## Per run", "",
         "| Q | arm | supported old → new | consensus (new) | disputed old → new | leader old → new | stability old → new | recommendation old → new |",
         "|---|---|---|---|---|---|---|---|"]
    tot = Counter()
    for q in ("Q1", "Q4", "Q5"):
        for arm in ORDER:
            r = out["runs"][f"{q}_r1_{arm}"]
            o, n = r["old"], r["new"]
            tot[f"{arm}_old"] += o["supported"]
            tot[f"{arm}_new"] += n["supported"]
            L.append(f"| {q} | {arm} | {o['supported']} → {n['supported']} | {n['consensus']} | {o['disputed']} → "
                     f"{n['disputed']} | {o['leader']} → {n['leader']} | {o['stability']} → {n['stability']} | "
                     f"{o['recommendation']} → {n['recommendation']} |")
    L += ["", "Totals, supported cells (old → new): " + "; ".join(
        f"{a} {tot[a + '_old']} → {tot[a + '_new']}" for a in ORDER), "", "## Changed cells", ""]
    for q in ("Q1", "Q4", "Q5"):
        for arm in ORDER:
            r = out["runs"][f"{q}_r1_{arm}"]
            if not r["changed_cells"]:
                L.append(f"- **{q} {arm}:** no cell changed state or interval.")
                continue
            L.append(f"- **{q} {arm}:**")
            for k, v in r["changed_cells"].items():
                L.append(f"  - `{k}`: {v['old_state']} {v['old_observed']} [{v['old_interval'][0]},{v['old_interval'][1]}] → "
                         f"**{v['new_state']}** ({v['new_kind']}) [{v['new_interval'][0]},{v['new_interval'][1]}]; "
                         f"families {v['families']} ({v['certain_families']} certain). {v['decision'] or ''}")
            if r["new"]["bounds"] != r["old"]["bounds"]:
                L.append(f"  - utility intervals: {r['old']['bounds']} → {r['new']['bounds']}")
    L += ["", "## Readiness after re-scoring", ""]
    for q in ("Q1", "Q4", "Q5"):
        for arm in ORDER:
            n = out["runs"][f"{q}_r1_{arm}"]["new"]
            L.append(f"- {q} {arm}: {n['recommendation']} — " + "; ".join(n["reasons"]))
    (HERE / "RESCORING_V31.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
