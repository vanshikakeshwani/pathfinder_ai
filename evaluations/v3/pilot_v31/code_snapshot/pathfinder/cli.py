"""Command line interface.

  python -m pathfinder.cli run --question "..." [--weights cost=5,ops=3] [--strategy adaptive|static]
  python -m pathfinder.cli demo-fixture --case decision-flip|confirm|no-progress|all
  python -m pathfinder.cli evaluate --queries evaluations/queries.json [--record | --replay]
  python -m pathfinder.cli smoke-gateway
"""

from __future__ import annotations

import argparse
import sys

from pathfinder.config import load_settings
from pathfinder.graph import RunContext
from pathfinder.models import Mode
from pathfinder.reports import write_outputs
from pathfinder.retry import ToolError
from pathfinder.scoring import parse_weights

DEMO_CASES = {"decision-flip": "flip", "confirm": "confirm", "no-progress": "irrelevant"}


def _print_run(ctx: RunContext, out_path) -> None:
    r = ctx.report
    assert r is not None
    if r.synthetic:
        print("=== SYNTHETIC FIXTURE RUN (fictional vendors/data) ===")
    plan = ctx.plan
    if plan is not None:
        if plan.mode == Mode.COMPARISON:
            crit = ", ".join(f"{c.criterion_id}(w{c.weight},{c.weight_source})" for c in plan.criteria)
            print(f"Plan: comparison of {', '.join(a.name for a in plan.alternatives)} on {crit}")
        else:
            print(f"Plan: discovery, facets {', '.join(f.facet_id for f in plan.facets)}"
                  f"{f', {plan.target_entity_count} entities' if plan.target_entity_count else ''}")
    for e in ctx.telemetry.events:
        if e["event"] == "action_selected":
            print(f"  [round {e['round']}] target {e['target_id']} score={e['action_score']:.1f}: {e['reason']}")
        elif e["event"] == "cell_update":
            print(f"    bounds {e['bounds']} -> {e['decision']['recommended']} ({e['decision']['stability']})")
        elif e["event"] == "coverage_update":
            print(f"    coverage {e['verified_units']}/{e['required_units']}")
        elif e["event"] == "decision_change":
            print(f"    DECISION CHANGE: {e['kind']} via {', '.join(e['evidence_ids'])}")
        elif e["event"] == "candidate_rejected":
            print(f"    rejected {e['candidate_id']} ({e['stage']}): {e['reason']}")
    print(f"\nAnswer: {r.short_answer}")
    print(f"Status={r.status} stop={r.stop_reason} confidence={r.confidence} "
          f"(factual={r.factual_confidence}, stability={r.decision_stability or 'n/a'}) "
          f"flips={r.decision_flip_count} status_changes={r.status_change_count}")
    print(f"Outputs: {out_path}")


def cmd_run(args) -> int:
    from pathfinder.runner import live_clients, make_context, run

    settings = load_settings()
    try:
        llm, search, contents = live_clients(settings)
    except ToolError as err:
        print(f"Configuration error: {err}. Set keys in .env (see .env.example) or use demo-fixture.",
              file=sys.stderr)
        return 2
    ctx = make_context(args.question, settings, llm, search, contents, strategy=args.strategy,
                       user_weights=parse_weights(args.weights))
    run(ctx)
    _print_run(ctx, write_outputs(ctx, args.output_dir or settings.output_dir))
    return 0 if ctx.report and ctx.report.status != "failed" else 1


def cmd_demo(args) -> int:
    from pathfinder.config import Settings
    from pathfinder.demo_fixtures import XY_QUESTION, xy_scenario
    from pathfinder.runner import make_context, new_run_id, run

    cases = list(DEMO_CASES) if args.case == "all" else [args.case]
    settings = Settings(output_dir=args.output_dir or "outputs")
    for case in cases:
        llm, search, contents = xy_scenario(DEMO_CASES[case])
        ctx = make_context(XY_QUESTION, settings, llm, search, contents, synthetic=True,
                           run_id=new_run_id(f"SYNTH_{case.upper().replace('-', '_')}"))
        run(ctx)
        print(f"\n##### demo case: {case} #####")
        _print_run(ctx, write_outputs(ctx, settings.output_dir))
    return 0


def cmd_evaluate(args) -> int:
    from pathfinder.evaluation import evaluate

    return evaluate(args)


def cmd_smoke(args) -> int:
    from pathfinder.smoke import main as smoke_main

    return smoke_main()


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="pathfinder", description="Pathfinder AI 2.0 decision-flip research agent")
    sub = p.add_subparsers(dest="command", required=True)
    r = sub.add_parser("run", help="live research run (needs EXPLABS_API_KEY and EXA_API_KEY)")
    r.add_argument("--question", required=True)
    r.add_argument("--weights", help="criterion weights 1-5, e.g. cost=5,deployment=3")
    r.add_argument("--strategy", choices=["adaptive", "static"], default="adaptive")
    r.add_argument("--output-dir")
    r.set_defaults(func=cmd_run)
    d = sub.add_parser("demo-fixture", help="offline SYNTHETIC decision-flip demonstration")
    d.add_argument("--case", choices=[*DEMO_CASES, "all"], default="decision-flip")
    d.add_argument("--output-dir")
    d.set_defaults(func=cmd_demo)
    e = sub.add_parser("evaluate", help="static vs adaptive evaluation")
    e.add_argument("--queries", default="evaluations/queries.json")
    e.add_argument("--ids", help="comma-separated question ids (default: required ones)")
    e.add_argument("--snapshots", default="evaluations/snapshots")
    mode = e.add_mutually_exclusive_group()
    mode.add_argument("--record", action="store_true", help="live calls, cache every response")
    mode.add_argument("--replay", action="store_true", help="no network; replay cached responses")
    e.add_argument("--repeat", type=int, default=1)
    e.add_argument("--max-usd", type=float, default=None,
                   help="record mode: stop before a pair if provider-reported spend + projected pair cost exceeds this")
    e.add_argument("--output-dir")
    e.add_argument("--arms", help="comma-separated arms: static, adaptive (V3) or a policy/ablation name "
                                  "(v2_policy, no_retry, no_decision, no_readiness, no_conflict, no_exploration)")
    e.add_argument("--plans-dir", help="folder of frozen plans <QID>.json reused for every repetition")
    e.set_defaults(func=cmd_evaluate)
    s = sub.add_parser("smoke-gateway", help="authenticated gateway compatibility checks")
    s.set_defaults(func=cmd_smoke)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
