"""Thin entry point: `python evaluations/eval_runner.py --record` == `python -m pathfinder.cli evaluate --record`."""

import sys

from pathfinder.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["evaluate", *sys.argv[1:]]))
