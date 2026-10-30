"""Offline reconstruction of a recorded run's state at each decision point (no network, no LLM).

Used for the V2 failure diagnosis and the offline V2-vs-V3 policy comparison. The state before the action of
round r is rebuilt ONLY from evidence verified in rounds < r (`evidence_before`), so a policy evaluated on
it cannot see evidence that was recorded later in the run.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from pathfinder.grounding import registrable_domain
from pathfinder.matrix import Cells, build_cells
from pathfinder.models import Evidence, ResearchPlan


@dataclass
class RunTrace:
    run_dir: Path
    run_id: str
    plan: ResearchPlan
    evidence: list[Evidence]
    rejected: list[dict]
    domains: dict[str, str]
    published: dict[str, str | None]
    actions: list[dict]  # action_selected events (round, target_id, queries, reason, ...)
    round_metrics: list[dict]
    tool_failures: list[dict] = field(default_factory=list)  # each with the round it happened in
    stop: dict | None = None
    strategy: str = ""


def _events(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line.strip()]


def load_run(run_dir: Path) -> RunTrace:
    run_dir = Path(run_dir)
    events = _events(run_dir / "decision_trace.jsonl")
    plan_ev = next(e for e in events if e["event"] == "plan")
    plan = ResearchPlan.model_validate(plan_ev["plan"])
    domains: dict[str, str] = {}
    actions, metrics, failures = [], [], []
    stop = None
    current_round = 0
    for e in events:
        kind = e["event"]
        if kind == "action_selected":
            current_round = e["round"]
            actions.append(e)
        elif kind == "content" and e.get("source_id"):
            domains[e["source_id"]] = registrable_domain(e["url"])
        elif kind == "round_metrics":
            metrics.append(e)
        elif kind == "tool_failure":
            failures.append({**e, "round": current_round})
        elif kind == "stop":
            stop = e
    evidence, rejected = [], []
    for rec in _events(run_dir / "verification_log.jsonl"):
        if rec.get("type") == "accepted":
            evidence.append(Evidence.model_validate({k: v for k, v in rec.items() if k != "type"}))
        else:
            rejected.append(rec)
    published: dict[str, str | None] = {}
    report = run_dir / "report.json"
    if report.exists():
        for s in json.loads(report.read_text("utf-8")).get("sources", []):
            published[s["source_id"]] = s.get("published_at")
    for sid in domains:
        published.setdefault(sid, None)
    t = RunTrace(run_dir=run_dir, run_id=plan_ev["run_id"], plan=plan, evidence=evidence, rejected=rejected,
                 domains=domains, published=published, actions=actions, round_metrics=metrics,
                 tool_failures=failures, stop=stop, strategy=plan_ev.get("strategy", ""))
    return t


def evidence_before(trace: RunTrace, round_no: int) -> list[Evidence]:
    """Evidence available to the policy when it chose the action of `round_no` (verified in earlier rounds)."""
    return [e for e in trace.evidence if e.round < round_no]


def rejected_before(trace: RunTrace, round_no: int) -> list[dict]:
    return [r for r in trace.rejected if r.get("round", 0) < round_no]


def cells_before(trace: RunTrace, round_no: int, builder=build_cells, **kwargs) -> Cells:
    return builder(trace.plan, evidence_before(trace, round_no), trace.domains, trace.published, **kwargs)


def new_evidence_in_round(trace: RunTrace, round_no: int) -> list[Evidence]:
    return [e for e in trace.evidence if e.round == round_no]


def cells_v3(trace: RunTrace, round_no: int) -> Cells:
    """Current (V3) matrix semantics, including `insufficient` from rejections in earlier rounds."""
    from pathfinder.matrix import insufficient_targets

    return build_cells(trace.plan, evidence_before(trace, round_no), trace.domains, trace.published,
                       insufficient_targets(rejected_before(trace, round_no)))


def history_before(trace: RunTrace, round_no: int):
    """(attempts, TargetHistory, issued queries) of the run's OWN actions in rounds < round_no, with each
    action's success judged exactly as the live graph does (new verified evidence for its target)."""
    from pathfinder.acquisition import TargetHistory
    from pathfinder.models import Mode

    attempts: dict[str, int] = {}
    issued: list[str] = []
    hist = TargetHistory()
    for a in trace.actions:
        r = a["round"]
        if r >= round_no:
            break
        attempts[a["target_id"]] = attempts.get(a["target_id"], 0) + 1
        issued += a.get("queries") or []
        if r == 0:
            continue
        tid = a["target_id"]
        base = tid.split("#", 1)[0]
        if trace.plan.mode == Mode.COMPARISON:
            key = tuple(base.split(":", 1))
            if tid.endswith("#corroborate"):
                before, after = cells_v3(trace, r)[key], cells_v3(trace, r + 1)[key]
                ok = (after.independent_sources > before.independent_sources
                      or (after.state, after.lower, after.upper) != (before.state, before.lower, before.upper))
            else:
                ok = any(e.target_id == base for e in new_evidence_in_round(trace, r))
            alt = key[0]
        else:
            ok = bool(new_evidence_in_round(trace, r))
            alt = None
        prev = hist.last
        factor = ((a.get("analysis") or {}).get("chosen") or {}).get("decision_factor")
        hist.record(r, tid, alt, ok, factor, immediate_retry=bool(prev and prev[1] == tid and not prev[3]))
    return attempts, hist, issued
