"""Replay the historical V2 benchmark with the FROZEN V2 code (evaluations/v2/code_snapshot), offline.

The live package keeps evolving (V3); V2 results must stay reproducible with the code that produced them.
Usage (from the repo root):  python evaluations/v2/replay_v2.py [--output-dir outputs]
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOT = ROOT / "evaluations" / "v2" / "code_snapshot"
sys.path.insert(0, str(SNAPSHOT))
for name in [m for m in sys.modules if m == "pathfinder" or m.startswith("pathfinder.")]:
    del sys.modules[name]
os.chdir(ROOT)  # .env (budget settings) and relative snapshot paths resolve from the repo root

import pathfinder  # noqa: E402
from pathfinder.cli import main  # noqa: E402

if Path(pathfinder.__file__).resolve().parent != SNAPSHOT / "pathfinder":
    raise SystemExit(f"refusing to run: imported {pathfinder.__file__}, not the frozen V2 snapshot")

if __name__ == "__main__":
    print(f"V2 code snapshot: {Path(pathfinder.__file__).parent}")
    raise SystemExit(main(["evaluate", "--replay", "--repeat", "3", *sys.argv[1:]]))
