"""Static-vs-adaptive evaluation, protocol V3 (V2 results are replayed with the frozen V2 code).

Pairing: within each repetition, ONE frozen plan and ONE shared round 0 (identical recorded responses) feed
every arm; after divergence each arm has its own RunContext, trace and output folder.
V3 planning: ONE fixed plan per question, frozen before the evaluation and reused for every repetition
(`--plans-dir`, or frozen once per question into the `plan_fixed` store). Retrieval still varies
independently across repetitions (separate snapshot store per repetition).
Arms: `static` (fixed round-robin) and adaptive policies by name (`adaptive` = V3; ablations from
acquisition.POLICIES). All arms share plan, round 0, budgets, query builder, verifier, scoring and stop rule.

Targeting vs stopping: both arms run with early_stop=False to the full research budget. Every round logs
`would_stop` under the COMMON stopping rule (identical for both arms). Each arm is then reported in two
views of the same trajectory:
  * common_stop: the prefix up to the round where the common rule fires (an exact prefix, because stopping
    only ends a run - it never changes earlier decisions);
  * full_budget: the whole trajectory.
Static vs adaptive within a view isolates TARGET SELECTION; common_stop vs full_budget within an arm
isolates the STOPPING rule.

Costs are provider-reported (Exa cost_dollars, gateway usage.cost), never estimated. Per-arm numbers are
attributed (the shared round 0 counts for both arms); actual spend is summed once per recorded call.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from pathfinder.config import Settings
from pathfinder.graph import RunContext
from pathfinder.llm import LLMTransport, StructuredLLM
from pathfinder.models import ResearchPlan
from pathfinder.planner import make_plan
from pathfinder.retry import CancelToken
from pathfinder.runner import make_context, new_run_id, run
from pathfinder.telemetry import Budget, Telemetry, utc_now

PROTOCOL_VERSION = "v3.1"  # v3.1: source-family consensus aggregation, reachable counterfactuals
VIEWS = ("common_stop", "full_budget")

FIELDS = ["protocol", "qid", "mode", "repeat", "arm", "view", "run_id", "timestamp", "llm_model", "config_fp",
          "plan_hash", "round0_hash", "rounds", "search_calls", "content_pages", "actions", "llm_requests",
          "llm_tokens", "llm_cost_usd", "exa_cost_usd", "units_supported", "units_total", "coverage",
          "new_units_after_round0", "accepted", "rejected", "acceptance_rate", "distinct_domains",
          "relevant_retrieval_yield", "stability", "interval_leader", "recommendation", "flips",
          "status_changes", "tool_errors", "llm_errors", "stop_reason", "targeted_actions",
          # V3 additions
          "policy", "units_disputed", "units_unknown", "units_insufficient", "units_evidenced",
          "high_confidence_cells", "strong_flips", "tie_flips", "repeat_prev_target", "failed_targeted_rounds",
          "action_kinds", "disputes_seen", "disputes_resolved", "consequential_disputes",
          "consequential_disputes_resolved", "readiness_changes", "became_ready", "provider_failure_rounds",
          # v3.1 additions
          "units_consensus", "units_dimension_mismatch", "source_inconsistent_cells"]

# Settings that change what a run can do; any change produces a different snapshot folder.
FINGERPRINT_FIELDS = ["llm_provider", "llm_model", "llm_base_url", "llm_structured_mode", "llm_temperature",
                      "llm_max_retries", "exa_max_retries", "max_search_calls", "max_content_pages",
                      "max_research_rounds", "max_no_progress", "max_evidence_per_round", "max_initial_queries",
                      "results_per_search", "pages_per_search", "max_llm_calls", "max_seconds"]


def config_fingerprint(settings: Settings) -> tuple[str, dict]:
    cfg = {k: getattr(settings, k) for k in FINGERPRINT_FIELDS}
    cfg["protocol"] = PROTOCOL_VERSION
    return hashlib.sha256(json.dumps(cfg, sort_keys=True, default=str).encode()).hexdigest()[:10], cfg


def plan_hash(plan: ResearchPlan) -> str:
    return hashlib.sha256(plan.model_dump_json().encode()).hexdigest()[:16]


def freeze_plan(llm: LLMTransport, settings: Settings, question: str, weights: dict[str, int]) -> ResearchPlan:
    budget = Budget.from_settings(settings)
    structured = StructuredLLM(llm, settings, budget, Telemetry("PLAN_FREEZE"), CancelToken())
    plan, _ = make_plan(structured, question, weights, settings.max_initial_queries)
    return plan


def stop_index(trajectory: list[dict]) -> int:
    """Index of the round where the common stopping rule fires (last round if it never fires)."""
    for i, snap in enumerate(trajectory):
        if snap.get("would_stop"):
            return i
    return len(trajectory) - 1


def view_row(ctx: RunContext, qid: str, arm: str, repeat: int, view: str, config_fp: str = "") -> dict:
    assert ctx.plan is not None and ctx.round_metrics
    traj = ctx.round_metrics
    snap = traj[stop_index(traj)] if view == "common_stop" else traj[-1]
    if view == "common_stop":
        reason = traj[stop_index(traj)].get("would_stop") or "budget_exhausted"
    else:
        reason = ctx.report.stop_reason if ctx.report else "error"
    if reason in ("no_progress", "budget_exhausted") and snap["accepted"] == 0:
        reason = "insufficient_evidence"
    targeted = [e["target_id"] for e in ctx.telemetry.events
                if e["event"] == "action_selected" and e["target_id"] != "initial" and e["round"] <= snap["round"]]
    cand = snap["accepted"] + snap["rejected"]
    upto = traj[: traj.index(snap) + 1]
    targeted_rounds = [s for s in upto if s["round"] > 0]
    kinds: dict[str, int] = {}
    for s in targeted_rounds:
        kinds[s.get("action_kind") or "?"] = kinds.get(s.get("action_kind") or "?", 0) + 1
    recs = [s.get("recommendation") for s in upto]
    extra = {
        "policy": "static" if arm == "static" else ctx.policy.name,
        **{k: snap.get(k, "") for k in ("units_disputed", "units_unknown", "units_insufficient", "units_evidenced",
                                        "high_confidence_cells", "disputes_seen", "disputes_resolved",
                                        "consequential_disputes", "consequential_disputes_resolved",
                                        "units_consensus", "units_dimension_mismatch", "source_inconsistent_cells")},
        "strong_flips": snap.get("strong_flips", 0), "tie_flips": snap["flips"] - snap.get("strong_flips", 0),
        "repeat_prev_target": sum(1 for s in targeted_rounds if s.get("repeat_prev")),
        "failed_targeted_rounds": sum(1 for s in targeted_rounds if s.get("target_success") is False),
        "action_kinds": " ".join(f"{k}={v}" for k, v in sorted(kinds.items())),
        "readiness_changes": sum(1 for a, b in zip(recs, recs[1:], strict=False) if a != b),
        "became_ready": int(recs[-1] == "ready" and recs[0] != "ready"),
        "provider_failure_rounds": sum(1 for s in upto if s.get("provider_failure_round")),
    }
    return {
        "protocol": PROTOCOL_VERSION, "qid": qid, "mode": ctx.plan.mode.value, "repeat": repeat, "arm": arm,
        "view": view, "run_id": ctx.run_id, "timestamp": utc_now(), "llm_model": ctx.llm.model_id,
        "config_fp": config_fp, "plan_hash": plan_hash(ctx.plan), "round0_hash": ctx.round0_hash or "",
        "rounds": snap["round"], "search_calls": snap["search_calls"], "content_pages": snap["content_pages"],
        "actions": snap["actions"], "llm_requests": snap["llm_requests"], "llm_tokens": snap["llm_tokens"],
        "llm_cost_usd": snap["llm_cost_usd"], "exa_cost_usd": snap["exa_cost_usd"],
        "units_supported": snap["units_supported"], "units_total": snap["units_total"],
        "coverage": round(snap["units_supported"] / snap["units_total"], 3) if snap["units_total"] else "n/a",
        "new_units_after_round0": snap["units_supported"] - traj[0]["units_supported"],
        "accepted": snap["accepted"], "rejected": snap["rejected"],
        "acceptance_rate": round(snap["accepted"] / cand, 3) if cand else "n/a",
        "distinct_domains": snap["distinct_domains"],
        "relevant_retrieval_yield": round(snap["units_supported"] / snap["actions"], 3) if snap["actions"] else "n/a",
        "stability": snap["stability"], "interval_leader": snap["interval_leader"] or "",
        "recommendation": snap["recommendation"], "flips": snap["flips"], "status_changes": snap["status_changes"],
        "tool_errors": snap["tool_errors"], "llm_errors": snap["llm_errors"], "stop_reason": reason,
        "targeted_actions": " | ".join(targeted), **extra,
    }


DEFAULT_ARMS = ("static", "adaptive")


def arm_policy(arm: str):
    """'static' -> None; 'adaptive' -> the V3 policy; otherwise a named policy from acquisition.POLICIES."""
    from pathfinder.acquisition import POLICIES

    if arm == "static":
        return None
    name = "v3" if arm == "adaptive" else arm
    if name not in POLICIES:
        raise ValueError(f"unknown arm {arm!r}; choose static, adaptive or one of {sorted(POLICIES)}")
    return POLICIES[name]


def run_pair(question: str, qid: str, plan: ResearchPlan, settings: Settings, clients_factory, repeat: int,
             out_dir: Path, synthetic: bool = False, config_fp: str = "",
             arms: tuple[str, ...] = DEFAULT_ARMS) -> list[dict]:
    """One paired repetition: every arm on the same frozen plan and shared round 0 (static first)."""
    from pathfinder.reports import write_outputs

    rows, traces = [], []
    hashes = {}
    for arm in arms:
        policy = arm_policy(arm)
        llm, search, contents = clients_factory()
        ctx = make_context(question, settings, llm, search, contents,
                           strategy="static" if policy is None else "adaptive", preset_plan=plan,
                           run_id=new_run_id(f"EVAL_{qid}_r{repeat}_{arm}"), synthetic=synthetic)
        if policy is not None:
            ctx.policy = policy
        ctx.early_stop = False
        run(ctx)
        write_outputs(ctx, out_dir)
        hashes[arm] = ctx.round0_hash
        if not ctx.round_metrics:  # failed before any round (e.g. auth): nothing comparable
            continue
        rows += [view_row(ctx, qid, arm, repeat, v, config_fp) for v in VIEWS]
        traces.append({"qid": qid, "repeat": repeat, "arm": arm, "run_id": ctx.run_id,
                       "trajectory": ctx.round_metrics,
                       "actions": [{k: e.get(k) for k in ("round", "target_id", "action_score", "flip_relevant",
                                                          "reason", "queries", "action_kind")}
                                   for e in ctx.telemetry.events if e["event"] == "action_selected"],
                       "decision_changes": [c.model_dump(mode="json") for c in ctx.decision_changes],
                       "final_stop": ctx.stop_reason})
    if len(set(hashes.values())) != 1:
        for row in rows:
            row["stop_reason"] += " (ROUND0 MISMATCH: pair not comparable)"
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "trajectories.jsonl").open("a", encoding="utf-8") as fh:
        for t in traces:
            fh.write(json.dumps(t, ensure_ascii=False, default=str) + "\n")
    return rows


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def load_frozen_plan(path: str | Path) -> ResearchPlan:
    """A plan frozen before the evaluation: either a bare ResearchPlan JSON or {"plan": ..., provenance}."""
    data = json.loads(Path(path).read_text("utf-8"))
    return ResearchPlan.model_validate(data.get("plan", data) if isinstance(data, dict) else data)


def load_queries(path: str | Path) -> list[dict]:
    return json.loads(Path(path).read_text("utf-8"))["questions"]


def store_spend(paths: list[Path]) -> dict:
    """Actual provider-reported spend: each recorded call counted once, however many arms reused it."""
    exa, llm, tokens, calls = 0.0, 0.0, 0, 0
    priced_tokens, unpriced_tokens, unpriced_calls = 0, 0, 0
    for p in paths:
        if not p.exists():
            continue
        for entry in json.loads(p.read_text("utf-8")).values():
            calls += 1
            if isinstance(entry.get("cost_usd"), (int, float)):
                exa += entry["cost_usd"]
            usage = entry.get("usage") or {}
            used = usage.get("total_tokens") if isinstance(usage.get("total_tokens"), int) else 0
            tokens += used
            if isinstance(usage.get("cost"), (int, float)) and usage["cost"] > 0:
                llm += usage["cost"]
                priced_tokens += used
            elif used:  # the gateway reported cost 0 or nothing for a call that consumed tokens
                unpriced_calls += 1
                unpriced_tokens += used
    # Estimate for unpriced calls at the observed average rate of priced calls (not provider-reported).
    estimate = llm / priced_tokens * unpriced_tokens if priced_tokens else None
    return {"recorded_calls": calls, "exa_cost_usd": round(exa, 6), "llm_reported_cost_usd": round(llm, 6),
            "total_reported_usd": round(exa + llm, 6), "llm_total_tokens": tokens,
            "llm_unpriced_calls": unpriced_calls, "llm_unpriced_tokens": unpriced_tokens,
            "llm_unpriced_estimate_usd": round(estimate, 6) if estimate is not None else None,
            "total_estimated_usd": round(exa + llm + (estimate or 0.0), 6)}


def evaluate(args, settings: Settings | None = None) -> int:
    from pathfinder.config import load_settings
    from pathfinder.replay import RecordingContents, RecordingLLM, RecordingSearch, SnapshotStore
    from pathfinder.retry import ToolError
    from pathfinder.runner import live_clients
    from pathfinder.scoring import parse_weights

    settings = settings or load_settings()
    fp, cfg = config_fingerprint(settings)
    queries = load_queries(args.queries)
    ids = args.ids.split(",") if args.ids else [q["id"] for q in queries if q.get("required")]
    mode = "replay" if args.replay else "record" if args.record else None
    max_usd = getattr(args, "max_usd", None)
    arms = tuple(a.strip() for a in (getattr(args, "arms", None) or ",".join(DEFAULT_ARMS)).split(",") if a.strip())
    try:
        for a in arms:
            arm_policy(a)  # validate before any call
    except ValueError as err:
        print(f"Configuration error: {err}")
        return 2
    plans_dir = Path(args.plans_dir) if getattr(args, "plans_dir", None) else None
    live = None
    if mode != "replay":
        try:
            live = live_clients(settings)
        except ToolError as err:
            print(f"Configuration error: {err}. Use --replay with existing snapshots, or set keys.")
            return 2
    out_dir = Path(args.output_dir or settings.output_dir) / f"eval_{PROTOCOL_VERSION}_{new_run_id('E')}"
    out_dir.mkdir(parents=True, exist_ok=True)
    meta = {"protocol": PROTOCOL_VERSION, "mode": mode or "live-unrecorded", "config_fp": fp, "settings": cfg,
            "question_ids": ids, "repeat": args.repeat, "max_usd": max_usd, "started": utc_now(),
            "guard_stop": None, "arms": list(arms), "plans_dir": str(plans_dir) if plans_dir else None,
            "plans": {}}
    print(f"config fingerprint {fp}: {json.dumps(cfg, default=str)}")
    rows: list[dict] = []
    stores: list[Path] = []
    pair_costs: list[float] = []

    def spent() -> float:
        return store_spend(sorted(set(stores)))["total_estimated_usd"]  # unpriced LLM calls are not free

    fixed_plans: dict[str, ResearchPlan] = {}
    for k in range(1, max(1, args.repeat) + 1):
        for q in queries:
            if q["id"] not in ids:
                continue
            snap = Path(args.snapshots) / q["id"] / fp
            weights = parse_weights(q.get("weights"))

            def clients_for(sub: str, _snap=snap):
                if mode is None:
                    assert live is not None
                    return live
                stores.append(_snap / f"{sub}.json")
                store = SnapshotStore(_snap / f"{sub}.json")
                inner = live or (None, None, None)
                return (RecordingLLM(inner[0], store, mode, settings.llm_model),
                        RecordingSearch(inner[1], store, mode), RecordingContents(inner[2], store, mode))

            if mode == "record" and max_usd is not None:
                projected = max(pair_costs) if pair_costs else 0.0
                if spent() + projected > max_usd:
                    meta["guard_stop"] = (f"stopped before {q['id']} repeat {k}: spent ${spent():.4f} + projected "
                                          f"${projected:.4f} > cap ${max_usd}")
                    print(meta["guard_stop"])
                    break
            before = spent() if mode == "record" else 0.0
            if q["id"] not in fixed_plans:  # ONE plan per question, reused by every repetition
                source = plans_dir / f"{q['id']}.json" if plans_dir else None
                try:
                    if source is not None and source.exists():
                        fixed_plans[q["id"]] = load_frozen_plan(source)
                        origin = str(source)
                    else:
                        print(f"[{q['id']}] freezing the question's plan ...")
                        fixed_plans[q["id"]] = freeze_plan(clients_for("plan_fixed")[0], settings, q["question"],
                                                           weights)
                        origin = "plan_fixed store"
                except (ToolError, ValueError) as err:
                    print(f"[{q['id']}] plan failed: {err}")
                    continue
                (out_dir / "plans").mkdir(exist_ok=True)
                (out_dir / "plans" / f"{q['id']}.json").write_text(
                    fixed_plans[q["id"]].model_dump_json(indent=2), encoding="utf-8")
                meta["plans"][q["id"]] = {"source": origin, "plan_hash": plan_hash(fixed_plans[q["id"]])}
            plan = fixed_plans[q["id"]]
            print(f"[{q['id']}] repeat {k}: arms {', '.join(arms)} (plan {plan_hash(plan)})")
            new = run_pair(q["question"], q["id"], plan, settings, lambda k=k: clients_for(f"rep{k}"), k,
                           out_dir, config_fp=fp, arms=arms)
            if mode == "record":
                pair_costs.append(spent() - before)
            for row in new:
                if row["view"] == "common_stop":
                    print(f"   {row['arm']:14} cover {row['units_supported']}/{row['units_total']} actions "
                          f"{row['actions']} stop {row['stop_reason']} rec {row['recommendation']} "
                          f"({row['interval_leader'] or '-'}/{row['stability']})")
            rows += new
            write_csv(rows, out_dir / "results.csv")  # incremental, so an interrupted run keeps finished pairs
        if meta["guard_stop"]:
            break
    write_csv(rows, out_dir / "results.csv")
    if mode is not None:
        spend = store_spend(sorted(set(stores)))
        spend["note"] = ("provider-reported values (Exa cost_dollars, gateway usage.cost); not an invoice. "
                         "Each recorded call counted once.")
        (out_dir / "spend.json").write_text(json.dumps(spend, indent=2), encoding="utf-8")
        print(f"recorded spend: {spend}")
    meta["finished"] = utc_now()
    (out_dir / "config.json").write_text(json.dumps(meta, indent=2, default=str), encoding="utf-8")
    print(f"Wrote {len(rows)} rows to {out_dir / 'results.csv'}")
    return 0 if rows else 1
