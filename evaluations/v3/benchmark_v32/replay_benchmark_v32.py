"""Replay the V3.2 benchmark (repetition 1) with the FROZEN V3.2 code (evaluations/v3/benchmark_v32/code_snapshot), offline.

The live package now includes later verification fixes; pilot results must stay reproducible with the code that produced them.
Usage (from the repo root):  python evaluations/v3/benchmark_v32/replay_benchmark_v32.py
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SNAPSHOT = ROOT / "evaluations" / "v3" / "benchmark_v32" / "code_snapshot"
sys.path.insert(0, str(SNAPSHOT))
for name in [m for m in sys.modules if m == "pathfinder" or m.startswith("pathfinder.")]:
    del sys.modules[name]
os.chdir(ROOT)  # .env (budget settings) and relative snapshot paths resolve from the repo root

import pathfinder  # noqa: E402
from pathfinder.cli import main  # noqa: E402

if Path(pathfinder.__file__).resolve().parent != SNAPSHOT / "pathfinder":
    raise SystemExit(f"refusing to run: imported {pathfinder.__file__}, not the frozen pilot snapshot")

if __name__ == "__main__":
    print(f"V3.2 benchmark code snapshot: {Path(pathfinder.__file__).parent}")
    raise SystemExit(main(["evaluate", "--replay", "--repeat", "1", "--arms", "static,v2_policy,adaptive", "--plans-dir", "evaluations/v3/plans", "--snapshots", "evaluations/snapshots_v32_benchmark", *sys.argv[1:]]))
