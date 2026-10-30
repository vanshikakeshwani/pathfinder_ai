"""Offline reconstruction used by the V2-vs-V3 policy comparison: no future evidence, exact fidelity (SYNTHETIC)."""

from conftest import build_ctx
from test_retry_policy import _failing_first_search

from pathfinder.acquisition import POLICIES, choose_next
from pathfinder.config import Settings
from pathfinder.reports import write_outputs
from pathfinder.runner import run
from pathfinder.trace_replay import cells_v3, evidence_before, history_before, load_run


def _recorded_v3_run(tmp_path):
    ctx = build_ctx(*_failing_first_search(), Settings())
    ctx.early_stop = False  # run every round, as in evaluation
    run(ctx)
    write_outputs(ctx, tmp_path)
    return ctx, load_run(next(p for p in tmp_path.iterdir() if p.is_dir()))


def test_state_before_a_round_contains_no_later_evidence(tmp_path):
    ctx, trace = _recorded_v3_run(tmp_path)
    assert len(trace.evidence) == len(ctx.evidence)
    for r in range(1, len(trace.actions)):
        before = evidence_before(trace, r)
        assert all(e.round < r for e in before)
        assert len(before) == sum(1 for e in ctx.evidence if e.round < r)  # nothing from round r or later


def test_reconstruction_reproduces_every_live_v3_decision(tmp_path):
    """If the rebuilt state (earlier rounds only) gives the SAME choice as the live run at every round, the
    live policy provably used no information beyond what the reconstruction contains."""
    ctx, trace = _recorded_v3_run(tmp_path)
    live = [e for e in ctx.telemetry.events if e["event"] == "action_selected" and e["round"] > 0]
    assert len(live) >= 2
    for e in live:
        r = e["round"]
        attempts, hist, issued = history_before(trace, r)
        again = choose_next(trace.plan, cells_v3(trace, r), attempts, hist, issued, r + 1, POLICIES["v3"])
        assert again is not None and again.target_id == e["target_id"] and again.queries == e["queries"]
        assert again.action_kind == e["action_kind"]
