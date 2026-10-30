# Release checklist: fresh install on Windows (Python 3.11)

Run each command in **PowerShell**, in a **new, empty folder**, in order. The *Expected* column was verified on 2026-10-30 in a clean copy of the submission file set (a new venv, no `.env`, no outputs, no snapshots).

## A. Install

| # | Command | Expected |
|---|---|---|
| A1 | `py -0` | Lists `-V:3.11` |
| A2 | `git clone <REPO-URL> pathfinder-ai` then `cd pathfinder-ai` | Folder contains `pathfinder\`, `tests\`, `README.md`, `pyproject.toml`, `requirements-lock.txt`, `.env.example`. **No `.env`, no `outputs\`, no `.venv\`.** |
| A3 | `py -3.11 -m venv .venv` | Creates `.venv\` (no output) |
| A4 | `.\.venv\Scripts\python.exe --version` | `Python 3.11.x` (tested with 3.11.9) |
| A5 | `.\.venv\Scripts\python.exe -m pip install --upgrade pip` | `Successfully installed pip-…` or `Requirement already satisfied` |
| A6 | `.\.venv\Scripts\python.exe -m pip install -c requirements-lock.txt -e ".[dev]"` | Ends with `Successfully installed … pathfinder-ai-3.2.0 …`; no `ERROR` lines (needs internet, about 1–3 minutes) |

## B. Offline verification (no keys, no network)

| # | Command | Expected |
|---|---|---|
| B1 | `.\.venv\Scripts\python.exe -m pytest -q` | `232 passed` |
| B2 | `.\.venv\Scripts\ruff.exe check .` | `All checks passed!` |
| B3 | `.\.venv\Scripts\python.exe -m pathfinder.cli demo-fixture --case all` | Three blocks labelled `=== SYNTHETIC FIXTURE RUN ===`, ending in this order:<br>• `Status=complete stop=stable … flips=1 status_changes=0` (Recommendation: VendorY)<br>• `Status=complete stop=stable … flips=0 status_changes=1` (Recommendation: VendorX)<br>• `Status=partial stop=no_progress … flips=0` |
| B4 | `.\.venv\Scripts\pathfinder.exe --help` | `usage: pathfinder [-h] {run,demo-fixture,evaluate,smoke-gateway} ...` and `Pathfinder AI 3.2 …` |
| B5 | `.\.venv\Scripts\python.exe -m pathfinder.cli run --question "Compare Qdrant and Weaviate"` (still without `.env`) | `Configuration error: EXA_API_KEY is not set. Set keys in .env …`, exit code 2. This confirms nothing is called without keys. |

## C. Live (optional; uses your keys and money)

| # | Command | Expected |
|---|---|---|
| C1 | `Copy-Item .env.example .env` then `notepad .env` | Fill in `EXPLABS_API_KEY=` and `EXA_API_KEY=` only |
| C2 | `.\.venv\Scripts\python.exe -m pathfinder.cli smoke-gateway` | Table with `basic_completion yes`, `strict_json_schema yes`, and `Recommended LLM_STRUCTURED_MODE: **json_schema**`. `json_object_mode NO` is a known gateway quirk and is not used. This overwrites `docs\gateway-compat.md`; restore it with `git checkout docs/gateway-compat.md` if you don't want the change. |
| C3 | `.\.venv\Scripts\python.exe -m pathfinder.cli run --question "Compare Qdrant, Weaviate, and Milvus for a small team building RAG; consider deployment, filtering and operational effort."` | Prints the plan, `[round N] target … score=…` lines with reasons, `Answer: …` and a `Status=… stop=…` line. Creates `outputs\RUN_…\` with `report.md`, `report.json`, `decision_trace.jsonl`, `matrix.json`, `tool_usage.json`, `verification_log.jsonl`. About 2–4 minutes and about $0.05–0.08. A `withheld` recommendation is a normal, honest outcome. |
| C4 (optional) | Deep-research mode for one question: see README, "Deep-research mode" (sets 6 environment variables in the current window, runs `run`, then removes them) | Same output files as C3 under `outputs\deep\RUN_…\`. Up to 5 targeted rounds, 8 searches, 16 pages and 20 model calls, about $0.10–0.12. A deeper run is not guaranteed to be better. |

## D. Before publishing

| # | Command | Expected |
|---|---|---|
| D1 | `git status --short` | No `.env`, `outputs/`, `.venv/` or `evaluations/snapshots*` entries |
| D2 | `git check-ignore .env outputs evaluations/snapshots_v32_benchmark` | Prints all three paths (they are ignored) |
| D3 | `git ls-files \| Select-String "\.env$"` | No output (only `.env.example` is tracked) |
| D4 | `Select-String -Path (git ls-files) -Pattern "sk-[A-Za-z0-9]{20,}" -List` | No output |

## E. Demo video (3–5 min)

Follow `docs/demo-script.md`. Use the offline demo (B3) for the guaranteed part, and one live `run` (C3) or a saved sample in `samples\` for the real part.
