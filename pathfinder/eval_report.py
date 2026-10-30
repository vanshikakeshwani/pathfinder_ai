"""Build the evaluation report (V3; any set of arms), AI-provisional review sheet and human-review worksheet.

Every number comes from files written by `evaluate` (results.csv, trajectories.jsonl, spend.json, config.json
and per-run outputs). Nothing is estimated, and no human score is ever pre-filled.

  python -m pathfinder.eval_report <record_dir> [--replay <replay_dir>] [--out ...] [--review-dir ...]
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

VOLATILE = {"run_id", "timestamp", "llm_model"}
KEY_METRICS = ["coverage", "units_supported", "actions", "accepted", "rejected", "relevant_retrieval_yield",
               "distinct_domains", "llm_tokens", "exa_cost_usd", "llm_cost_usd"]


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def load_rows(eval_dir: Path) -> list[dict]:
    with (eval_dir / "results.csv").open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def load_trajectories(eval_dir: Path) -> dict[tuple, dict]:
    out = {}
    path = eval_dir / "trajectories.jsonl"
    if path.exists():
        for line in path.read_text("utf-8").splitlines():
            if line.strip():
                t = json.loads(line)
                out[(t["qid"], int(t["repeat"]), t["arm"])] = t
    return out


def replay_diff(rec: list[dict], rep: list[dict]) -> list[str]:
    """Differences in decisions/metrics between record and replay (volatile fields excluded)."""
    diffs = []
    by_key = {(r["qid"], r["repeat"], r["arm"], r.get("view", "")): r for r in rep}
    for r in rec:
        other = by_key.get((r["qid"], r["repeat"], r["arm"], r.get("view", "")))
        if other is None:
            diffs.append(f"{r['qid']}/r{r['repeat']}/{r['arm']}/{r.get('view')}: missing in replay")
            continue
        for k in r:
            if k not in VOLATILE and r[k] != other.get(k):
                diffs.append(f"{r['qid']}/r{r['repeat']}/{r['arm']}/{r.get('view')}: {k} record={r[k]!r} "
                             f"replay={other.get(k)!r}")
    return diffs


def coverage_at(trajectory: list[dict], actions: float) -> tuple[int, int]:
    """(units_supported, actions used) at the last round whose cumulative actions <= `actions`."""
    best = trajectory[0]
    for snap in trajectory:
        if snap["actions"] <= actions:
            best = snap
    return best["units_supported"], best["actions"]


def classify(s: dict, a: dict) -> str:
    """Static vs adaptive in the same view. Equal-but-incomplete coverage is never called a benefit."""
    cs, ca = _num(s["coverage"]), _num(a["coverage"])
    xs, xa = int(s["actions"]), int(a["actions"])
    if cs is None or ca is None:
        return "n/a"
    if ca > cs:
        return "adaptive better coverage"
    if ca < cs:
        return "adaptive WORSE coverage"
    if ca < 1.0:
        return "NO coverage benefit (equal, incomplete)" + ("; adaptive fewer actions" if xa < xs else
                                                            "; adaptive MORE actions" if xa > xs else "")
    if xa < xs:
        return "equal full coverage, adaptive fewer actions"
    if xa > xs:
        return "equal full coverage, adaptive MORE actions"
    return "no difference"


def _stat(values: list[float]) -> str:
    vals = [v for v in values if v is not None]
    if not vals:
        return "n/a"
    med = statistics.median(vals)
    lo, hi = min(vals), max(vals)
    fmt = (lambda x: f"{x:.3g}") if any(v != int(v) for v in vals) else (lambda x: f"{int(x)}")
    return f"{fmt(med)} [{fmt(lo)}-{fmt(hi)}]"


V3_METRICS = ["units_strict_supported", "units_consensus", "units_disputed", "units_unknown", "units_insufficient", "units_evidenced", "high_confidence_cells",
              "repeat_prev_target", "failed_targeted_rounds"]
AGG_KEYS = ["units_strict_supported", "units_consensus", "units_supported", "units_evidenced", "units_disputed",
            "units_unknown", "units_insufficient", "units_dimension_mismatch", "source_inconsistent_cells",
            "units_heterogeneous", "units_ambiguous_dimension",
            "units_total", "high_confidence_cells", "actions", "accepted", "rejected", "distinct_domains",
            "repeat_prev_target", "failed_targeted_rounds", "disputes_seen", "disputes_resolved",
            "consequential_disputes", "consequential_disputes_resolved", "readiness_changes", "became_ready",
            "flips", "strong_flips", "tie_flips", "status_changes", "provider_failure_rounds", "llm_tokens",
            "exa_cost_usd", "llm_cost_usd", "tool_errors", "llm_errors"]
V2_AGG_KEYS = ["units_supported", "units_total", "actions", "accepted", "rejected", "flips", "status_changes",
               "llm_tokens", "exa_cost_usd", "llm_cost_usd", "tool_errors", "llm_errors"]


def _paired(values: list[float]) -> str:
    if not values:
        return "n/a"
    better = sum(1 for v in values if v > 0)
    equal = sum(1 for v in values if v == 0)
    worse = sum(1 for v in values if v < 0)
    return (f"median {statistics.median(values):+g} [{min(values):+g} to {max(values):+g}]; "
            f"{better} better / {equal} equal / {worse} worse")


def build(eval_dir: Path, replay_dir: Path | None, out: Path, review_dir: Path) -> None:
    rows = load_rows(eval_dir)
    trajs = load_trajectories(eval_dir)
    cfg = json.loads((eval_dir / "config.json").read_text("utf-8"))
    spend = json.loads((eval_dir / "spend.json").read_text("utf-8")) if (eval_dir / "spend.json").exists() else {}
    idx = {(r["qid"], int(r["repeat"]), r["arm"], r["view"]): r for r in rows}
    qids = list(dict.fromkeys(r["qid"] for r in rows))
    reps = sorted({int(r["repeat"]) for r in rows})
    arms = cfg.get("arms") or list(dict.fromkeys(r["arm"] for r in rows))
    others = [a for a in arms if a != "static"]
    v3 = bool(rows) and "units_disputed" in rows[0]
    metrics = KEY_METRICS + (V3_METRICS if v3 else [])
    proto = str(cfg.get("protocol", "")).upper()

    L = [f"# Evaluation report {proto}: {' vs '.join(arms)} (live, paired, {len(reps)} repetition(s))", "",
         f"- Folder: `{eval_dir.as_posix()}` (protocol {cfg.get('protocol')}, mode {cfg['mode']}, "
         f"started {cfg['started']}, finished {cfg.get('finished')})",
         f"- Config fingerprint `{cfg['config_fp']}`: "
         + ", ".join(f"{k}={v}" for k, v in cfg["settings"].items()),
         f"- Questions {', '.join(cfg['question_ids'])}; repetitions completed: {reps}; arms: {', '.join(arms)}; "
         f"spend cap: {cfg.get('max_usd')} USD; guard stop: {cfg.get('guard_stop') or 'not triggered'}"]
    if cfg.get("plans"):
        L.append("- Fixed plans (one per question, reused by every repetition and arm): "
                 + "; ".join(f"{q} `{p['plan_hash']}` from {p['source']}" for q, p in cfg["plans"].items()))
    L += ["- Views: **common_stop** = trajectory prefix up to where the common stopping rule fires (same rule for "
          "every arm); **full_budget** = the whole run. Arms compared *within a view* measure target selection; "
          "common_stop vs full_budget *within an arm* measures stopping.",
          f"- Descriptive only: {len(reps)} repetition(s) per arm, no significance claims.", ""]
    if replay_dir is not None:
        diffs = replay_diff(rows, load_rows(replay_dir))
        L += ["## Replay check", "",
              f"Offline replay `{replay_dir.as_posix()}`: " + (
                  f"**all {len(rows)} rows identical** (decisions and metrics; run id, timestamp and model label "
                  "excluded). Replay is a reproducibility check, not an additional repetition."
                  if not diffs else f"**{len(diffs)} differences**:"), ""]
        L += [f"- {d}" for d in diffs[:40]] + ([""] if diffs else [])

    # per question / repetition --------------------------------------------------------------
    extra_head = " strict / consensus | disputed / unknown / insufficient | kinds |" if v3 else ""
    L += ["## Results per question and repetition", "",
          "| Q | rep | arm | view | supported | searches | pages | accepted / rejected | domains | stability | "
          "interval leader | recommendation | flips (strong) / status chg | stop | tokens | Exa $ | LLM $ | "
          "errors t/l |" + extra_head,
          "|" + "---|" * (18 + (3 if v3 else 0))]
    for q in qids:
        for k in reps:
            for arm in arms:
                for view in ("common_stop", "full_budget"):
                    r = idx.get((q, k, arm, view))
                    if not r:
                        continue
                    extra = (f" {r.get('units_strict_supported', '-')} / {r.get('units_consensus', '-')} | "
                             f"{r['units_disputed']} / {r['units_unknown']} / {r['units_insufficient']} | "
                             f"{r['action_kinds']} |" if v3 else "")
                    strong = f" ({r['strong_flips']})" if v3 else ""
                    L.append(f"| {q} | {k} | {arm} | {view} | {r['units_supported']}/{r['units_total']} | "
                             f"{r['search_calls']} | {r['content_pages']} | {r['accepted']} / {r['rejected']} | "
                             f"{r['distinct_domains']} | {r['stability']} | {r['interval_leader'] or '-'} | "
                             f"{r['recommendation']} | {r['flips']}{strong} / {r['status_changes']} | "
                             f"{r['stop_reason']} | {r['llm_tokens']} | {r['exa_cost_usd']} | {r['llm_cost_usd']} | "
                             f"{r['tool_errors']}/{r['llm_errors']} |" + extra)

    # distributions ---------------------------------------------------------------------------
    L += ["", "## Distribution across repetitions: median [min-max]", "",
          "| Q | arm | view | " + " | ".join(metrics) + " |", "|---|---|---|" + "---|" * len(metrics)]
    for q in qids:
        for arm in arms:
            for view in ("common_stop", "full_budget"):
                rs = [idx[(q, k, arm, view)] for k in reps if (q, k, arm, view) in idx]
                if rs:
                    L.append(f"| {q} | {arm} | {view} | "
                             + " | ".join(_stat([_num(r.get(m)) for r in rs]) for m in metrics) + " |")

    # targeting value (each non-static arm vs static) ---------------------------------------------
    for other in others:
        L += ["", f"## Targeting value: static vs {other} (same stopping rule)", "",
              "Matched-actions compares coverage when each arm has spent no more than the other arm's common-stop "
              "actions, so neither arm gets credit just for spending more.", "",
              f"| Q | rep | common_stop outcome | supported static → {other} | actions static → {other} | "
              "matched-actions supported static vs arm (at ≤ k actions) | full_budget outcome | "
              "full supported static → arm |",
              "|---|---|---|---|---|---|---|---|"]
        tally_common, tally_full = defaultdict(list), defaultdict(list)
        diffs_c, diffs_f, diffs_m, diffs_e, diffs_s = [], [], [], [], []
        for q in qids:
            for k in reps:
                s, a = idx.get((q, k, "static", "common_stop")), idx.get((q, k, other, "common_stop"))
                sf, af = idx.get((q, k, "static", "full_budget")), idx.get((q, k, other, "full_budget"))
                if not (s and a and sf and af):
                    continue
                oc, of = classify(s, a), classify(sf, af)
                tally_common[oc].append(f"{q}r{k}")
                tally_full[of].append(f"{q}r{k}")
                diffs_c.append(int(a["units_supported"]) - int(s["units_supported"]))
                diffs_f.append(int(af["units_supported"]) - int(sf["units_supported"]))
                if v3:  # cell-level metrics exist only for comparison questions (blank for discovery)
                    if _num(af.get("units_evidenced")) is not None and _num(sf.get("units_evidenced")) is not None:
                        diffs_e.append(int(af["units_evidenced"]) - int(sf["units_evidenced"]))
                    if _num(af.get("units_strict_supported")) is not None and                             _num(sf.get("units_strict_supported")) is not None:
                        diffs_s.append(int(af["units_strict_supported"]) - int(sf["units_strict_supported"]))
                matched = ""
                ts, ta = trajs.get((q, k, "static")), trajs.get((q, k, other))
                if ts and ta:
                    kk = min(int(s["actions"]), int(a["actions"]))
                    us, xs = coverage_at(ts["trajectory"], kk)
                    ua, xa = coverage_at(ta["trajectory"], kk)
                    diffs_m.append(ua - us)
                    matched = f"{us} vs {ua} (k={kk}; used {xs}/{xa})"
                L.append(f"| {q} | {k} | {oc} | {s['units_supported']} → {a['units_supported']} | "
                         f"{s['actions']} → {a['actions']} | {matched} | {of} | "
                         f"{sf['units_supported']} → {af['units_supported']} |")
        L += ["", f"**Paired differences ({other} − static), units supported:**",
              f"- common_stop: {_paired(diffs_c)}", f"- full_budget: {_paired(diffs_f)}",
              f"- matched actions: {_paired(diffs_m)}"]
        if v3:
            L.append(f"- full_budget units with verified evidence (supported + disputed): {_paired(diffs_e)}")
            if diffs_s:
                L.append(f"- full_budget STRICTLY supported units (no consensus, no scope split): {_paired(diffs_s)}")
        L += ["", "**Tally, common_stop view:** " + "; ".join(f"{k}: {len(v)} ({', '.join(v)})"
                                                              for k, v in sorted(tally_common.items())),
              "", "**Tally, full_budget view:** " + "; ".join(f"{k}: {len(v)} ({', '.join(v)})"
                                                             for k, v in sorted(tally_full.items())), ""]

    # stopping value --------------------------------------------------------------------------
    L += ["## Stopping value (common_stop vs full_budget, same trajectory)", "",
          "| Q | rep | arm | stop rule fired | round | actions saved | coverage lost | premature? |",
          "|---|---|---|---|---|---|---|---|"]
    premature = []
    for q in qids:
        for k in reps:
            for arm in arms:
                c, f = idx.get((q, k, arm, "common_stop")), idx.get((q, k, arm, "full_budget"))
                if not (c and f):
                    continue
                saved = int(f["actions"]) - int(c["actions"])
                lost = int(f["units_supported"]) - int(c["units_supported"])
                if lost > 0:
                    premature.append(f"{q}r{k}/{arm} (lost {lost} unit(s))")
                L.append(f"| {q} | {k} | {arm} | {c['stop_reason']} | {c['rounds']} | {saved} | {lost} | "
                         f"{'YES' if lost > 0 else 'no'} |")
    L += ["", "Premature stops (the common rule stopped before units that the full budget later found): "
          + ("; ".join(premature) if premature else "none"), ""]

    # aggregates ------------------------------------------------------------------------------
    def total(arm, view, key):
        return sum(v for v in (_num(r.get(key)) for r in rows if r["arm"] == arm and r["view"] == view)
                   if v is not None)

    cols = [(a, v) for v in ("common_stop", "full_budget") for a in arms]
    L += ["## Aggregate (sums over all questions and repetitions; descriptive)", "",
          "| metric | " + " | ".join(f"{a} {v.split('_')[0]}" for a, v in cols) + " |",
          "|---|" + "---|" * len(cols)]
    for key in (AGG_KEYS if v3 else V2_AGG_KEYS):
        L.append(f"| {key} | " + " | ".join(str(round(total(a, v, key), 4)) for a, v in cols) + " |")
    ready = {a: sum(1 for r in rows if r["arm"] == a and r["view"] == "full_budget" and r["recommendation"] == "ready")
             for a in arms}
    L += ["", "Ready recommendations (full_budget): " + ", ".join(f"{a} {n}" for a, n in ready.items()) + "."]
    flips = []
    for r in rows:
        if r["view"] == "full_budget" and int(r["flips"]) > 0:
            label = ("strong" if int(r["strong_flips"]) else "tie-related") if v3 else ""
            flips.append(f"{r['qid']}r{r['repeat']}/{r['arm']}" + (f" ({label})" if label else ""))
    L += ["", "Counted leader changes, preserved V2 definition (full_budget): "
          + (", ".join(flips) if flips else "none") + ". A *strong* flip replaces a real leader with a different "
          "real leader; tie-related changes move into or out of a tie.", ""]
    if spend:
        L += ["## Recorded spend (each provider call counted once)", "",
              f"- Recorded calls: {spend['recorded_calls']}; Exa (provider-reported): ${spend['exa_cost_usd']}; "
              f"gateway `usage.cost`: ${spend['llm_reported_cost_usd']}; total reported: "
              f"${spend.get('total_reported_usd')}; tokens: {spend['llm_total_tokens']}",
              f"- {spend.get('note', '')}",
              *([f"- **Under-reported LLM cost:** {spend['llm_unpriced_calls']} gateway calls "
                 f"({spend['llm_unpriced_tokens']} tokens) reported `usage.cost` 0. At the average rate of the priced "
                 f"calls they would cost about ${spend['llm_unpriced_estimate_usd']}, giving an estimated total of "
                 f"${spend['total_estimated_usd']} (an estimate, not provider-reported)."]
                if spend.get("llm_unpriced_calls") else []),
              "- Per-arm figures above are attributed (the shared round 0 counts for every arm).", ""]

    # actions -----------------------------------------------------------------------------------
    L += ["## Research actions and selection reasons", ""]
    for q in qids:
        for k in reps:
            for arm in arms:
                t = trajs.get((q, k, arm))
                if not t:
                    continue
                stop_round = next((s["round"] for s in t["trajectory"] if s.get("would_stop")), None)
                L.append(f"**{q} r{k} {arm}** (common stop after round {stop_round}; final {t['final_stop']})")
                for act in t["actions"]:
                    kind = f" [{act['action_kind']}]" if act.get("action_kind") else ""
                    L.append(f"- round {act['round']} `{act['target_id']}`{kind} score {act['action_score']}"
                             f"{' flip-relevant' if act.get('flip_relevant') else ''}: {act['reason']}")
                for c in t["decision_changes"]:
                    L.append(f"- decision change round {c['round']}: {c['kind']} {c['before']['recommended']}/"
                             f"{c['before']['stability']} → {c['after']['recommended']}/{c['after']['stability']}")
                L.append("")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    build_review(eval_dir, rows, review_dir, proto or "V3")


def build_review(eval_dir: Path, rows: list[dict], review_dir: Path, version: str = "V3") -> None:
    """AI-provisional review sheet (mechanical checks + every accepted excerpt) and a blank human worksheet."""
    runs = {}
    for r in rows:
        if r["view"] == "full_budget":
            runs[r["run_id"]] = r
    L = [f"# AI-provisional review materials ({version})", "",
         "> **AI-PROVISIONAL, NOT HUMAN EVALUATION.** These are mechanical checks computed from the run files, "
         "plus flags raised by the AI assistant. No score here is a human judgement. Human scores go in "
         "`HUMAN_REVIEW_WORKSHEET.csv`.", ""]
    for run_id, r in runs.items():
        d = eval_dir / run_id
        report = json.loads((d / "report.json").read_text("utf-8"))
        log = [json.loads(x) for x in (d / "verification_log.jsonl").read_text("utf-8").splitlines() if x]
        accepted = [x for x in log if x["type"] == "accepted"]
        rejected = [x for x in log if x["type"] == "rejected"]
        valid = {x["evidence_id"] for x in accepted}
        cited = [i for f in report["findings"] for i in f["evidence_ids"]]
        bad = [i for i in cited if i not in valid]
        flags = []
        if r["mode"] == "comparison":
            m = json.loads((d / "matrix.json").read_text("utf-8"))
            for a in {c["alternative"] for c in m["cells"]}:
                cs = [c for c in m["cells"] if c["alternative"] == a]
                if cs and all(c["score"] == 2 for c in cs):
                    flags.append(f"score saturation: {a} scored 2 on every criterion")
            if report.get("comparability_issues"):
                flags += [f"comparability: {x}" for x in report["comparability_issues"]]
        by_source = defaultdict(set)
        for x in accepted:
            by_source[x["source_id"]].add(x["target_id"])
        multi = {s: t for s, t in by_source.items() if len(t) >= 3}
        if multi:
            flags.append("one source supports 3+ targets: " + "; ".join(f"{s} ({len(t)})" for s, t in multi.items()))
        lex = sum(1 for x in rejected if "lexical" in x["reason"])
        ident = sum(1 for x in rejected if "approach identity" in x["reason"])
        L += [f"## {r['qid']} r{r['repeat']} {r['arm']} - `{run_id}`", "",
              f"- Status `{report['status']}`, stop `{report['stop_reason']}`, interval leader "
              f"`{report.get('interval_leader')}` ({report['decision_stability']}), recommendation "
              f"`{report.get('recommendation_status')}`" + (f" - withheld: {'; '.join(report['recommendation_withheld_reasons'])}"
                                                            if report.get("recommendation_withheld_reasons") else ""),
              f"- Mechanical: {len(cited)} cited evidence IDs, **{len(bad)} invalid**; {len(accepted)} accepted / "
              f"{len(rejected)} rejected (lexical {lex}, approach-identity {ident}); single-source cells: "
              f"{', '.join(report.get('single_source_cells') or []) or 'none'}",
              "- AI-provisional flags: " + ("; ".join(flags) if flags else "none"), "",
              "| EV | target | score | scope | identification quote | rubric rationale | excerpt |",
              "|---|---|---|---|---|---|---|"]
        for x in accepted:
            def cut(s, n):
                s = (s or "").replace("|", "/").replace("\n", " ")
                return s if len(s) <= n else s[:n] + "..."
            L.append(f"| {x['evidence_id']} | {x['target_id']} | {x['score'] if x['score'] is not None else '-'} | "
                     f"{x.get('scope', '')} | {cut(x.get('identification_quote'), 60)} | "
                     f"{cut(x.get('rubric_rationale'), 120)} | {cut(x['excerpt'], 200)} |")
        L += ["", "Rejected candidates:", ""]
        L += [f"- {x['candidate_id']} `{x['target_id']}` ({x['stage']}): {x['reason'][:170]}" for x in rejected] \
            or ["- none"]
        L.append("")
    review_dir.mkdir(parents=True, exist_ok=True)
    (review_dir / "AI_PROVISIONAL_REVIEW.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    with (review_dir / "HUMAN_REVIEW_WORKSHEET.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["run_id", "qid", "repeat", "arm", "reviewer_initials", "review_date",
                    "d1_answers_question", "d2_covers_requirements", "d3_inspectable_sources",
                    "d4_excerpts_support_claims", "d5_uncertainty_stated", "d6_tool_choices_useful",
                    "d7_no_fabrication", "d8_next_steps_structure", "wrongly_accepted_evidence_ids",
                    "wrongly_rejected_candidate_ids", "recommendation_justified_yes_no_na", "notes"])
        for run_id, r in runs.items():
            w.writerow([run_id, r["qid"], r["repeat"], r["arm"]] + [""] * 14)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("eval_dir")
    p.add_argument("--replay")
    p.add_argument("--out", default="evaluations/v3/EVALUATION_REPORT.md")
    p.add_argument("--review-dir", default="evaluations/v3/review")
    a = p.parse_args(argv)
    build(Path(a.eval_dir), Path(a.replay) if a.replay else None, Path(a.out), Path(a.review_dir))
    print(f"wrote {a.out} and {a.review_dir}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
