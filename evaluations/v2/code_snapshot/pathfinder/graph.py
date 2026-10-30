"""The single-agent LangGraph: 8 nodes + a `decide` router on the edge after update_state.

START -> plan -> choose_action -> search -> retrieve -> extract -> verify -> update_state -(decide)->
         choose_action ... | report -> END

Python guards every edge: research budgets, round counts, no-progress and cancellation are checked
explicitly; the LangGraph recursion limit is only a backstop.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Literal, TypedDict

from langgraph.errors import GraphRecursionError
from langgraph.graph import END, START, StateGraph

from pathfinder import coverage as cov_mod
from pathfinder.config import Settings
from pathfinder.extraction import extract
from pathfinder.grounding import Registry
from pathfinder.llm import StructuredLLM
from pathfinder.matrix import Cells, bounds, build_cells, decision_state, robust_winner
from pathfinder.models import (
    RESOLVED_STATES,
    DecisionChange,
    Evidence,
    ExtractionCandidate,
    Mode,
    RejectedCandidate,
    ResearchAction,
    ResearchPlan,
    ResearchReport,
    Source,
    StopReason,
)
from pathfinder.planner import make_plan, static_queue
from pathfinder.policy import choose_next_comparison, detect_decision_change
from pathfinder.readiness import assess
from pathfinder.retry import Cancelled, CancelToken, ToolError
from pathfinder.telemetry import Budget, Telemetry
from pathfinder.tools.base import SearchHit, ToolRunner
from pathfinder.verification import rejection, verify

Strategy = Literal["adaptive", "static"]


@dataclass
class RunContext:
    run_id: str
    question: str
    settings: Settings
    llm: StructuredLLM
    tools: ToolRunner
    budget: Budget
    telemetry: Telemetry
    cancel: CancelToken
    registry: Registry = field(default_factory=Registry)
    strategy: Strategy = "adaptive"
    user_weights: dict[str, int] = field(default_factory=dict)
    preset_plan: ResearchPlan | None = None
    synthetic: bool = False
    # False: ignore the stable/no_progress stops and run to the research budget (evaluation mode). The
    # common stop rule is still evaluated every round and logged as `would_stop`, so the stopped
    # trajectory is an exact prefix of this one.
    early_stop: bool = True

    plan: ResearchPlan | None = None
    plan_notes: list[str] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)
    rejected: list[RejectedCandidate] = field(default_factory=list)
    rounds_done: int = 0  # round 0 is the initial (shared) round
    action: ResearchAction | None = None
    action_counter: int = 0
    hits: list[SearchHit] = field(default_factory=list)
    new_sources: list[Source] = field(default_factory=list)
    candidates: list[ExtractionCandidate] = field(default_factory=list)
    round_new_evidence: list[Evidence] = field(default_factory=list)
    attempts: dict[str, int] = field(default_factory=dict)
    no_progress_rounds: int = 0
    decision_changes: list[DecisionChange] = field(default_factory=list)
    queries_issued: list[str] = field(default_factory=list)
    static_queue: list[tuple[str, str, list[str]]] = field(default_factory=list)
    stop_reason: StopReason | None = None
    stop_note: str = ""
    round0_hash: str | None = None
    report: ResearchReport | None = None
    round_metrics: list[dict] = field(default_factory=list)

    # helpers ---------------------------------------------------------------
    def stop(self, reason: StopReason, note: str = "") -> None:
        if self.stop_reason is None:
            self.stop_reason = reason
            self.stop_note = note
            self.telemetry.event("stop", reason=reason, note=note, budget=self.budget.snapshot())

    def cells(self, evidence: list[Evidence] | None = None, plan: ResearchPlan | None = None) -> Cells:
        reg = self.registry
        return build_cells(plan or self.plan, self.evidence if evidence is None else evidence,  # type: ignore[arg-type]
                           {k: s.domain for k, s in reg.sources.items()},
                           {k: s.published_at for k, s in reg.sources.items()})

    def coverage(self, evidence: list[Evidence] | None = None) -> cov_mod.Coverage:
        return cov_mod.compute_coverage(self.plan, self.evidence if evidence is None else evidence)  # type: ignore[arg-type]

    def is_robust(self) -> bool:
        if self.plan is None or self.plan.mode != Mode.COMPARISON:
            return False
        order = [a.name for a in self.plan.alternatives]
        return robust_winner(order, bounds(self.plan, self.cells())) is not None

    def is_stable(self) -> bool:
        """Common `stable` stop: comparison = interval-robust AND recommendation ready; discovery = complete."""
        if self.plan is None:
            return False
        if self.plan.mode == Mode.COMPARISON:
            return self.is_robust() and assess(self.plan, self.cells()).status == "ready"
        return self.coverage().complete

    def requirement_units(self) -> tuple[int, int]:
        """(supported, total): comparison cells, or discovery coverage units."""
        if self.plan is None:
            return 0, 0
        if self.plan.mode == Mode.COMPARISON:
            cells = self.cells()
            return sum(1 for c in cells.values() if c.state in RESOLVED_STATES), len(cells)
        cov = self.coverage()
        return cov.verified_units, cov.required_units


class GraphState(TypedDict):
    ctx: RunContext


def _handle_tool_error(ctx: RunContext, where: str, err: ToolError) -> None:
    ctx.telemetry.event("tool_failure", node=where, error_kind=err.kind, status=err.status,
                        message=str(err)[:200])
    if err.kind == "auth":
        ctx.stop("error", f"authentication/configuration failure in {where}; not retried")


def _guarded(name: str, fn):
    def node(state: GraphState) -> GraphState:
        ctx = state["ctx"]
        if ctx.stop_reason is None and ctx.cancel.is_set():
            ctx.stop("cancelled", f"cancel requested before {name}")
        if ctx.stop_reason is None or name == "report":
            try:
                fn(ctx)
            except Cancelled:
                ctx.stop("cancelled", f"cancelled during {name}")
        return {"ctx": ctx}

    return node


# ----------------------------------------------------------------------- nodes


def node_plan(ctx: RunContext) -> None:
    if ctx.preset_plan is not None:
        ctx.plan = ctx.preset_plan
        ctx.plan_notes.append("frozen plan supplied (evaluation)")
    else:
        try:
            ctx.plan, notes = make_plan(ctx.llm, ctx.question, ctx.user_weights,
                                        ctx.settings.max_initial_queries)
            ctx.plan_notes.extend(notes)
        except ToolError as err:
            ctx.telemetry.event("plan_failed", error_kind=err.kind, message=str(err)[:200])
            ctx.stop("error", f"planning failed ({err.kind})")
            return
        except ValueError as err:  # cross-field validation of the normalized plan
            ctx.telemetry.event("plan_failed", error_kind="malformed", message=str(err)[:300])
            ctx.stop("error", "planner output failed plan validation")
            return
    ctx.static_queue = static_queue(ctx.plan)
    ctx.telemetry.event("plan", mode=ctx.plan.mode.value, strategy=ctx.strategy,
                        plan=ctx.plan.model_dump(mode="json"), notes=ctx.plan_notes)


def node_choose_action(ctx: RunContext) -> None:
    plan = ctx.plan
    assert plan is not None
    ctx.action_counter += 1
    n = ctx.action_counter
    if ctx.rounds_done == 0:
        ctx.action = ResearchAction(action_id=f"ACT_{n}", target_id="initial", queries=plan.initial_queries,
                                    predicted_gain=0.0, estimated_cost_units=float(len(plan.initial_queries) * 2),
                                    action_score=0.0, why_selected="Initial planned queries (round 0, shared by "
                                    "static and adaptive strategies).")
    elif ctx.strategy == "static":
        if not ctx.static_queue:
            ctx.stop("no_progress", "static query plan exhausted")
            return
        target, query, domains = ctx.static_queue.pop(0)
        ctx.action = ResearchAction(action_id=f"ACT_{n}", target_id=target, queries=[query],
                                    include_domains=domains, predicted_gain=0.0,
                                    estimated_cost_units=2.0, action_score=0.0,
                                    why_selected="Static baseline: next target in the fixed round-robin schedule "
                                                 "(computed from the plan before retrieval; no adaptation).")
    elif plan.mode == Mode.COMPARISON:
        ctx.action = choose_next_comparison(plan, ctx.cells(), ctx.attempts, n)
        if ctx.action is None:
            if ctx.is_stable():
                ctx.stop("stable", "interval-robust winner with recommendation ready")
            elif ctx.is_robust():
                ctx.stop("stable", "interval-robust, but the recommendation stays withheld after all "
                                   "corroboration attempts")
            elif all(c.state in RESOLVED_STATES for c in ctx.cells().values()):
                ctx.stop("stable", "all cells supported; remaining tie cannot be changed by more research")
            else:
                ctx.stop("no_progress", "every open target already attempted the maximum number of times")
            return
    else:
        cov = ctx.coverage()
        ctx.action = cov_mod.choose_next_discovery(plan, cov, ctx.attempts, n)
        if ctx.action is None:
            if cov.complete:
                ctx.stop("stable", "all required facets/entities covered")
            else:
                ctx.stop("no_progress", "every open target already attempted the maximum number of times")
            return
    ctx.telemetry.event("action_selected", round=ctx.rounds_done, target_id=ctx.action.target_id,
                        action_score=ctx.action.action_score, flip_relevant=ctx.action.flip_relevant,
                        queries=ctx.action.queries, include_domains=ctx.action.include_domains,
                        reason=ctx.action.why_selected,
                        budget_remaining={"search": ctx.budget.search_remaining,
                                          "contents": ctx.budget.content_remaining})


def node_search(ctx: RunContext) -> None:
    assert ctx.action is not None
    ctx.hits, ctx.new_sources, ctx.candidates, ctx.round_new_evidence = [], [], [], []
    ctx.attempts[ctx.action.target_id] = ctx.attempts.get(ctx.action.target_id, 0) + 1
    seen: set[str] = set()
    for query in ctx.action.queries:
        if ctx.budget.search_remaining <= 0:
            ctx.telemetry.event("budget_skip", tool="exa_search", query=query)
            break
        ctx.queries_issued.append(query)
        try:
            hits = ctx.tools.search(query, ctx.settings.results_per_search, ctx.action.include_domains or None)
        except ToolError as err:
            _handle_tool_error(ctx, "search", err)
            if ctx.stop_reason:
                return
            continue
        fresh = [h for h in hits if not ctx.registry.known_url(h.url) and h.url not in seen]
        dup = len(hits) - len(fresh)
        seen.update(h.url for h in fresh)
        ctx.hits.extend(fresh[: ctx.settings.pages_per_search])
        ctx.telemetry.event("search_result", query=query, hits=len(hits), new=len(fresh),
                            duplicates_skipped=dup, urls=[h.url for h in fresh[: ctx.settings.pages_per_search]])


def node_retrieve(ctx: RunContext) -> None:
    urls = [h.url for h in ctx.hits]
    try:
        pages = ctx.tools.get_contents(urls)
    except ToolError as err:
        _handle_tool_error(ctx, "retrieve", err)
        return
    returned = {p.url for p in pages}
    for p in pages:
        src, status = ctx.registry.add_page(p)
        if status == "new" and src is not None:
            ctx.new_sources.append(src)
        ctx.telemetry.event("content", url=p.url, status=status, chars=len(p.text or ""),
                            source_id=src.source_id if src else None)
    for u in urls:
        if u not in returned and u in urls[: ctx.budget.max_content_pages]:
            ctx.telemetry.event("content", url=u, status="missing_in_response")


def node_extract(ctx: RunContext) -> None:
    assert ctx.plan is not None
    try:
        cands, rejected = extract(ctx.llm, ctx.plan, ctx.registry, ctx.new_sources,
                                  ctx.action.target_id if ctx.action else None, ctx.rounds_done,
                                  ctx.settings.max_evidence_per_round)
    except ToolError as err:
        _handle_tool_error(ctx, "extract", err)
        return
    grounded: list[ExtractionCandidate] = []
    for c in cands:
        g, status = ctx.registry.ground(c)
        if g is None:
            rejected.append(rejection(c, "grounding", status))
        else:
            grounded.append(g)
            if status == "offsets_corrected":
                ctx.telemetry.event("offsets_corrected", candidate_id=c.candidate_id)
    for r in rejected:
        ctx.telemetry.event("candidate_rejected", **r.model_dump())
    ctx.rejected.extend(rejected)
    ctx.candidates = grounded


def node_verify(ctx: RunContext) -> None:
    assert ctx.plan is not None
    result = verify(ctx.llm, ctx.plan, ctx.registry, ctx.candidates)
    for r in result.rejected:
        ctx.telemetry.event("candidate_rejected", **r.model_dump())
    for e in result.accepted:
        ctx.telemetry.event("evidence_verified", evidence_id=e.evidence_id, target_id=e.target_id,
                            source_id=e.source_id, score=e.score, score_basis=e.score_basis)
    ctx.rejected.extend(result.rejected)
    ctx.round_new_evidence = result.accepted


def node_update_state(ctx: RunContext) -> None:
    plan = ctx.plan
    assert plan is not None
    new = list(ctx.round_new_evidence)
    before_ev = list(ctx.evidence)
    ctx.evidence.extend(new)
    round_no = ctx.rounds_done
    if plan.mode == Mode.COMPARISON:
        cb, ca = ctx.cells(before_ev), ctx.cells()
        progress = sum(1 for k in ca if (ca[k].state, ca[k].lower, ca[k].upper)
                       != (cb[k].state, cb[k].lower, cb[k].upper))
        change, note = detect_decision_change(plan, plan, cb, ca, ctx.cells(before_ev), [e.evidence_id for e in new],
                                              round_no)
        if change:
            ctx.decision_changes.append(change)
            ctx.telemetry.event("decision_change", **change.model_dump(mode="json"))
        state = decision_state(plan, ca)
        b = bounds(plan, ca)
        ctx.telemetry.event("cell_update", round=round_no, progress_units=progress, decision_note=note,
                            decision=state.model_dump(), bounds={k: list(v) for k, v in b.items()},
                            cells={f"{a}:{c}": [cell.state, cell.lower, cell.upper] for (a, c), cell in ca.items()})
    else:
        before, after = ctx.coverage(before_ev), ctx.coverage()
        progress = cov_mod.progress_units(before, after, plan)
        ctx.telemetry.event("coverage_update", round=round_no, progress_units=progress,
                            verified_units=after.verified_units, required_units=after.required_units,
                            facet_status=after.facet_status)
    ctx.no_progress_rounds = 0 if progress > 0 else ctx.no_progress_rounds + 1
    ctx.rounds_done += 1
    if round_no == 0:
        ctx.round0_hash = round_hash(ctx)
        ctx.telemetry.event("round0_snapshot", hash=ctx.round0_hash)
    snapshot = round_snapshot(ctx, round_no, progress)
    ctx.round_metrics.append(snapshot)
    ctx.telemetry.event("round_metrics", **snapshot)


def round_snapshot(ctx: RunContext, round_no: int, progress: int) -> dict:
    """Cumulative state after a round, plus whether the common stop rule would end the run here."""
    b, t = ctx.budget, ctx.telemetry
    supported, total = ctx.requirement_units()
    tokens = sum(c["usage"]["total_tokens"] for c in t.llm_calls
                 if isinstance(c.get("usage"), dict) and isinstance(c["usage"].get("total_tokens"), int))
    llm_cost = sum(c["usage"]["cost"] for c in t.llm_calls
                   if isinstance(c.get("usage"), dict) and isinstance(c["usage"].get("cost"), (int, float)))
    exa_cost = sum(c["cost_usd"] for c in t.tool_calls if isinstance(c.get("cost_usd"), (int, float)))
    snap = {"round": round_no, "search_calls": b.search_calls, "content_pages": b.content_pages,
            "actions": b.research_actions_spent, "llm_requests": b.llm_calls, "llm_tokens": tokens,
            "llm_cost_usd": round(llm_cost, 6), "exa_cost_usd": round(exa_cost, 6),
            "units_supported": supported, "units_total": total, "new_units": progress,
            "accepted": len(ctx.evidence), "rejected": len(ctx.rejected),
            "distinct_domains": len({ctx.registry.sources[e.source_id].domain for e in ctx.evidence}),
            "tool_errors": sum(1 for c in t.tool_calls if not c["ok"]),
            "llm_errors": sum(1 for c in t.llm_calls if not c["ok"]),
            "flips": sum(1 for c in ctx.decision_changes if c.kind == "leader_changed"),
            "status_changes": sum(1 for c in ctx.decision_changes if c.kind != "leader_changed")}
    if ctx.plan is not None and ctx.plan.mode == Mode.COMPARISON:
        r = assess(ctx.plan, ctx.cells())
        snap.update(stability=r.stability, interval_leader=r.interval_leader, recommendation=r.status)
    else:
        snap.update(stability="n/a", interval_leader=None, recommendation="not_applicable")
    reason, _ = early_stop_reason(ctx)
    if reason is None:
        budget_reason, _ = _budget_reason(ctx)
        reason = budget_reason
    snap["would_stop"] = reason
    return snap


def _budget_reason(ctx: RunContext) -> tuple[StopReason | None, str]:
    s, b = ctx.settings, ctx.budget
    if ctx.rounds_done - 1 >= s.max_research_rounds or b.search_remaining <= 0 or b.content_remaining <= 0:
        return "budget_exhausted", ""
    return None, ""


def round_hash(ctx: RunContext) -> str:
    payload = {
        "sources": sorted((str(s.url), hashlib.sha256(s.content.encode()).hexdigest())
                          for s in ctx.registry.sources.values()),
        "evidence": sorted((e.target_id, e.excerpt, e.score) for e in ctx.evidence),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()[:16]


def node_report(ctx: RunContext) -> None:
    from pathfinder.reports import build_report

    if ctx.stop_reason is None:
        ctx.stop("error", "reached report without a stop reason")
    ctx.report = build_report(ctx)


# --------------------------------------------------------------------- routers


def _stopped(state: GraphState) -> bool:
    return state["ctx"].stop_reason is not None


def route_after_plan(state: GraphState) -> str:
    return "report" if _stopped(state) else "choose_action"


def route_after_choose(state: GraphState) -> str:
    return "report" if _stopped(state) else "search"


def route_after_search(state: GraphState) -> str:
    if _stopped(state):
        return "report"
    return "retrieve" if state["ctx"].hits and state["ctx"].budget.content_remaining > 0 else "update_state"


def route_after_retrieve(state: GraphState) -> str:
    if _stopped(state):
        return "report"
    return "extract" if state["ctx"].new_sources else "update_state"


def route_after_extract(state: GraphState) -> str:
    if _stopped(state):
        return "report"
    return "verify" if state["ctx"].candidates else "update_state"


def route_after_verify(state: GraphState) -> str:
    return "report" if _stopped(state) else "update_state"


def decide(state: GraphState) -> str:
    """Router after update_state: continue research or stop with an explicit reason."""
    ctx = state["ctx"]
    if ctx.stop_reason is None:
        reason, note = stop_check(ctx)
        if reason:
            if reason in ("no_progress", "budget_exhausted") and not ctx.evidence:
                reason, note = "insufficient_evidence", f"{note}; no verified evidence was found"
            ctx.stop(reason, note)
    return "report" if ctx.stop_reason else "choose_action"


def early_stop_reason(ctx: RunContext) -> tuple[StopReason | None, str]:
    """The COMMON stopping policy (identical for static and adaptive): stable or no-progress."""
    if ctx.is_stable():
        return "stable", ("interval-robust winner with recommendation ready"
                          if ctx.plan and ctx.plan.mode == Mode.COMPARISON
                          else "all required facets/entities covered")
    if ctx.rounds_done - 1 >= 1 and ctx.no_progress_rounds >= ctx.settings.max_no_progress:
        return "no_progress", f"{ctx.no_progress_rounds} consecutive round(s) without newly verified evidence"
    return None, ""


def stop_check(ctx: RunContext) -> tuple[StopReason | None, str]:
    s, b = ctx.settings, ctx.budget
    if ctx.cancel.is_set():
        return "cancelled", "cancel requested"
    targeted_done = ctx.rounds_done - 1
    if ctx.early_stop:
        reason, note = early_stop_reason(ctx)
        if reason:
            return reason, note
    if targeted_done >= s.max_research_rounds:
        return "budget_exhausted", f"MAX_RESEARCH_ROUNDS={s.max_research_rounds} reached"
    if b.search_remaining <= 0:
        return "budget_exhausted", "search budget exhausted"
    if b.content_remaining <= 0:
        return "budget_exhausted", "content-page budget exhausted"
    cap = b.optional_cap_hit()
    if cap:
        return "budget_exhausted", f"optional cap {cap} reached"
    return None, ""


# ----------------------------------------------------------------------- build


def build_graph():
    g = StateGraph(GraphState)
    for name, fn in [("plan", node_plan), ("choose_action", node_choose_action), ("search", node_search),
                     ("retrieve", node_retrieve), ("extract", node_extract), ("verify", node_verify),
                     ("update_state", node_update_state), ("report", node_report)]:
        g.add_node(name, _guarded(name, fn))
    g.add_edge(START, "plan")
    g.add_conditional_edges("plan", route_after_plan, ["choose_action", "report"])
    g.add_conditional_edges("choose_action", route_after_choose, ["search", "report"])
    g.add_conditional_edges("search", route_after_search, ["retrieve", "update_state", "report"])
    g.add_conditional_edges("retrieve", route_after_retrieve, ["extract", "update_state", "report"])
    g.add_conditional_edges("extract", route_after_extract, ["verify", "update_state", "report"])
    g.add_conditional_edges("verify", route_after_verify, ["update_state", "report"])
    g.add_conditional_edges("update_state", decide, ["choose_action", "report"])
    g.add_edge("report", END)
    return g.compile()


def run_graph(ctx: RunContext) -> RunContext:
    """Run to completion. KeyboardInterrupt is converted into a `cancelled` partial report."""
    graph = build_graph()
    limit = 20 + 8 * (ctx.settings.max_research_rounds + 2)
    try:
        graph.invoke({"ctx": ctx}, config={"recursion_limit": limit})
    except KeyboardInterrupt:
        ctx.cancel.cancel()
        ctx.stop("cancelled", "interrupted by user (Ctrl+C)")
    except GraphRecursionError:
        ctx.stop("error", "graph recursion backstop reached (should be unreachable: budgets bound the loop)")
    if ctx.report is None:  # interrupted, or recursion backstop hit
        node_report(ctx)
    return ctx
