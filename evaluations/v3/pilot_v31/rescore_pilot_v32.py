"""Post-fix (v3.2) retrospective offline re-scoring of the V3.1 pilot evidence - NOT a new live benchmark.

Compares each of the 9 V3.1 pilot runs' FINAL cells under the v3.1 rules (`rescoring_baseline_v31_rules.json`,
saved before the fix from the frozen V3.1 code's behaviour) with the v3.2 rules, using only saved evidence.
Writes RESCORING_V32.md and rescoring_v32.json next to this file; the original pilot artifacts are untouched.
Usage: python evaluations/v3/pilot_v31/rescore_pilot_v32.py
"""

from __future__ import annotations

import glob
import json
from pathlib import Path

from pathfinder.consensus import cost_dimension, is_cost_like
from pathfinder.matrix import bounds
from pathfinder.models import RESOLVED_STATES
from pathfinder.readiness import assess
from pathfinder.trace_replay import cells_v3, load_run

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
RECORD = ROOT / "outputs" / "eval_v3.1_E_20261030T080154_a99d87"
ORDER = ["static", "v2_policy", "adaptive"]


def main() -> None:
    base = json.loads((HERE / "rescoring_baseline_v31_rules.json").read_text("utf-8"))
    out = {"label": "Post-fix (v3.2) retrospective offline re-scoring of V3.1 pilot evidence - NOT a new live "
                    "benchmark", "runs": {}}
    for d in sorted(glob.glob(str(RECORD / "EVAL_*"))):
        t = load_run(Path(d))
        name = Path(d).name.split("_2026")[0][5:]
        cells = cells_v3(t, t.round_metrics[-1]["round"] + 1)
        r = assess(t.plan, cells)
        old = base[name]
        dims = []
        for e in t.evidence:
            crit = t.plan.criterion(e.target_id.split(":", 1)[1])
            if is_cost_like(crit.criterion_id, crit.description):
                before, after = old["evidence_dimensions"].get(e.evidence_id), cost_dimension(e)
                if before != after:
                    dims.append({"evidence": e.evidence_id, "cell": e.target_id, "score": e.score,
                                 "before": before, "after": after, "excerpt": e.excerpt[:120]})
        changed = {}
        for (a, k), c in cells.items():
            key = f"{a}:{k}"
            o = old["cells"][key]
            after = {"state": c.state, "kind": c.dispute_kind, "interval": [c.lower, c.upper],
                     "factual_confidence": c.factual_confidence, "heterogeneous": c.heterogeneous,
                     "ambiguous_dimension": c.ambiguous_dimension, "dimensions": c.dimensions}
            before = {"state": o["state"], "kind": o["kind"], "interval": [o["lower"], o["upper"]],
                      "factual_confidence": o["factual_confidence"], "dimensions": o["dimensions"]}
            if any(before[x] != after[x] for x in before) or c.heterogeneous or c.ambiguous_dimension:
                rec = c.consensus.get("summary") or next(iter(c.consensus.values()), {})
                changed[key] = {"before": before, "after": after, "decision": rec.get("decision"),
                                "products": next((x.get("heterogeneous_products") for x in c.consensus.values()
                                                  if x.get("heterogeneous_products")), None)}

        def supported(cs):
            return sum(1 for c in cs.values() if c["state"] in RESOLVED_STATES and not c.get("dimension_mismatch"))

        out["runs"][name] = {
            "old": {"supported": supported(old["cells"]),
                    "strict": sum(1 for c in old["cells"].values() if c["state"] == "supported"),
                    "consensus": sum(1 for c in old["cells"].values() if c["state"] == "consensus"),
                    "leader": old["leader"], "stability": old["stability"], "recommendation": old["recommendation"],
                    "bounds": old["bounds"], "reasons": old["reasons"]},
            "new": {"supported": sum(1 for c in cells.values() if c.state in RESOLVED_STATES and not c.dimension_mismatch),
                    "strict": sum(1 for c in cells.values() if c.state == "supported"),
                    "consensus": sum(1 for c in cells.values() if c.state == "consensus"),
                    "leader": r.interval_leader, "stability": r.stability, "recommendation": r.status,
                    "bounds": {a: list(v) for a, v in bounds(t.plan, cells).items()}, "reasons": r.reasons},
            "dimension_changes": dims, "changed_cells": changed}
    (HERE / "rescoring_v32.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    write_md(out)


def write_md(out: dict) -> None:
    L = ["# Post-fix (v3.2) retrospective re-scoring of the V3.1 pilot evidence", "",
         "> **NOT a new controlled live benchmark.** The 9 V3.1 pilot runs' saved, verified evidence is re-aggregated "
         "with the v3.2 rules (cost-dimension classification of the scored quantity, word-bounded patterns, "
         "product-heterogeneity flags) and compared with the v3.1 result of the same evidence. No API call; the pilot's "
         "own artifacts are unchanged (`V31_PILOT_ARTIFACTS_SHA256.txt`). Trajectories were chosen under v3.1.", "",
         "## Per run", "",
         "| Q | arm | strict old → new | consensus old → new | total supported old → new | leader old → new | "
         "stability old → new | recommendation old → new |", "|---|---|---|---|---|---|---|---|"]
    for q in ("Q1", "Q4", "Q5"):
        for arm in ORDER:
            r = out["runs"][f"{q}_r1_{arm}"]
            o, n = r["old"], r["new"]
            L.append(f"| {q} | {arm} | {o['strict']} → {n['strict']} | {o['consensus']} → {n['consensus']} | "
                     f"{o['supported']} → {n['supported']} | {o['leader']} → {n['leader']} | {o['stability']} → "
                     f"{n['stability']} | {o['recommendation']} → {n['recommendation']} |")
    L += ["", "## Cost-dimension changes (evidence level)", ""]
    any_dim = False
    for name, r in out["runs"].items():
        for x in r["dimension_changes"]:
            any_dim = True
            L.append(f"- {name} `{x['evidence']}` {x['cell']} (score {x['score']}): {x['before']} → **{x['after']}** — "
                     f"\"{x['excerpt']}\"")
    if not any_dim:
        L.append("- none")
    L += ["", "## Changed or flagged cells", ""]
    for name, r in out["runs"].items():
        for key, x in r["changed_cells"].items():
            b, a = x["before"], x["after"]
            L.append(f"- **{name} `{key}`**: {b['state']} ({b['kind']}) {b['interval']} conf {b['factual_confidence']} "
                     f"dims {b['dimensions']} → **{a['state']} ({a['kind']}) {a['interval']}** conf "
                     f"{a['factual_confidence']} dims {a['dimensions']}"
                     + (f"; heterogeneous products {x['products']}" if x["products"] else "")
                     + ("; ambiguous dimension" if a["ambiguous_dimension"] else "")
                     + (f". {x['decision']}" if x["decision"] else ""))
        if r["new"]["bounds"] != r["old"]["bounds"]:
            L.append(f"  - {name} utility intervals: {r['old']['bounds']} → {r['new']['bounds']}")
    L += ["", "## Readiness reasons after the fix", ""]
    for q in ("Q1", "Q4", "Q5"):
        for arm in ORDER:
            n = out["runs"][f"{q}_r1_{arm}"]["new"]
            L.append(f"- {q} {arm}: {n['recommendation']} — " + "; ".join(n["reasons"]))
    (HERE / "RESCORING_V32.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
