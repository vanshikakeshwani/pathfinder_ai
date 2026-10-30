# Pathfinder AI 3.2: decision-flip research agent (CLI)

Pathfinder is a single-agent LangGraph research CLI.

- **Comparison questions:** it builds an alternatives × criteria matrix from **verified, cited** web evidence, represents unknowns as score intervals, and spends each next search on the missing fact that could change, or make defensible, the recommendation.
- **List questions:** it tracks facet coverage instead.
- **Recommendations:** it states one only when the evidence supports it, and otherwise says why not.

Tools: Exa Search and Exa Get Contents for research; GPT-6 Luna (Experiential Labs gateway) for planning, extraction and verification. Every model output is schema-validated, and every finding cites a registered source excerpt.

## Requirements

- Windows 10/11 with **Python 3.11** (`py -0` must list `-V:3.11`) and Git.
- Offline use (tests and demo) needs **no API keys and no network** after installation.
- Live use needs an Experiential Labs key (`EXPLABS_API_KEY`) and an Exa key (`EXA_API_KEY`).

## Install (PowerShell, fresh folder)

```powershell
git clone <REPO-URL> pathfinder-ai
cd pathfinder-ai
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -c requirements-lock.txt -e ".[dev]"
```

`requirements-lock.txt` pins the exact versions tested on 2026-10-30 (langgraph 1.2.18, pydantic 2.14.2, openai 3.41.0, exa-py 2.26.0). Commands below call `.\.venv\Scripts\python.exe` directly, so no activation (and no execution-policy change) is needed.

## Offline check and demo (no keys)

```powershell
.\.venv\Scripts\python.exe -m pytest -q                             # expect: 232 passed
.\.venv\Scripts\ruff.exe check .                                     # expect: All checks passed!
.\.venv\Scripts\python.exe -m pathfinder.cli demo-fixture --case all # SYNTHETIC: flip, confirm, no-progress
```

The demo uses fictional vendors (labelled **SYNTHETIC**) to show the full loop:
- **flip:** the leader changes after the decisive fact is verified;
- **confirm:** the leader is confirmed;
- **no-progress:** an irrelevant page is rejected and the run stops honestly.

## Live use (optional; costs money)

```powershell
Copy-Item .env.example .env
notepad .env        # set EXPLABS_API_KEY=... and EXA_API_KEY=...  (.env is git-ignored; never commit it)
.\.venv\Scripts\python.exe -m pathfinder.cli smoke-gateway           # checks the key; recommended mode: json_schema
.\.venv\Scripts\python.exe -m pathfinder.cli run --question "Compare Qdrant, Weaviate, and Milvus for a small team building RAG; consider deployment, filtering and operational effort."
```

- **Cost:** a live `run` makes up to 6 Exa searches, 12 page fetches and about 9 model calls, roughly **$0.05–0.08** provider-reported.
- **Outputs:** written to `outputs\<RUN_ID>\`:
  - `report.md` / `report.json`: answer, cited findings, matrix, readiness, limitations;
  - `decision_trace.jsonl`: every tool decision and its reason;
  - `matrix.json` or `coverage.json`;
  - `tool_usage.json`;
  - `verification_log.jsonl`: accepted and rejected evidence.
- **Other commands:** `--strategy static` runs the fixed baseline; `--weights operational_effort=5` sets weights; `evaluate --help` shows the benchmark harness.

## Deep-research mode (optional, one question at a time)

> **Warning:** more research does **not** guarantee a better answer. It costs more (up to about $0.10–0.12 per run) and often surfaces more disagreement between sources. The same verification and recommendation-readiness rules apply, so a deeper run can still end with the recommendation withheld.

Deep mode only raises the budget limits, through process environment variables that take precedence over `.env`. The values are in `.env.deep.example`. Nothing else changes:
- request timeouts and retries;
- the no-progress stop;
- verification;
- readiness.

The variables affect only the current PowerShell window:

```powershell
$env:MAX_RESEARCH_ROUNDS="5"; $env:MAX_SEARCH_CALLS="8"; $env:MAX_CONTENT_PAGES="16"
$env:MAX_LLM_CALLS="20"; $env:MAX_SECONDS="360"; $env:MAX_NO_PROGRESS="2"
.\.venv\Scripts\python.exe -m pathfinder.cli run --question "<your question>" --output-dir outputs\deep
# back to the normal limits:
Remove-Item Env:MAX_RESEARCH_ROUNDS, Env:MAX_SEARCH_CALLS, Env:MAX_CONTENT_PAGES, Env:MAX_LLM_CALLS, Env:MAX_SECONDS, Env:MAX_NO_PROGRESS
```

- **How the time and call caps work:** `MAX_SECONDS` and `MAX_LLM_CALLS` are checked between research steps. A request already in flight is still bounded by its own timeout (60 s for the model, 20 s for Exa) and retries.
- **Stopping:** the run stops with an explicit reason, as usual.
- **Not for evaluations:** do **not** run `evaluate` in a window with these variables set. The recorded evaluations use frozen budgets, and different limits produce a different, non-comparable configuration fingerprint.

## Results so far (honest summary; each version labelled)

| Version | What was run | Result |
|---|---|---|
| V1 | 6 questions, 1 repetition | Superseded: confounded baseline and a verification flaw (`evaluations/v1/`) |
| **V2** | 6 questions × 3 paired repetitions, static vs adaptive (`evaluations/v2/`) | **Adaptive did not beat a fair static baseline** (69 vs 70 supported cells). Replayed exactly. |
| V3 pilot | Q1, Q4, Q5 × static / V2 policy / V3 (`evaluations/v3/pilot/`) | Found that evidence disputes could never be resolved (scoring defect) |
| V3.1 pilot | same three questions and arms (`evaluations/v3/pilot_v31/`) | All 8 correctness checks passed; supported cells V3.1 22, V2 policy 21, static 18 (n = 3, descriptive) |
| V3.2 benchmark | pre-registered 18-pair, 3-arm run; **stopped for the submission deadline after repetition 1 of all 6 questions** (`evaluations/v3/benchmark_v32/BENCHMARK_V32_PARTIAL.md`) | Supported cells: V3.2 32, V2 policy 28, static 28 (of 45). At matched actions the paired median is 0, so **mixed / not supported** under the pre-registered rule. Replayed exactly; $0.61 spent. |

No version produced a "ready" recommendation on the live questions. The readiness gate is deliberately strict, and the reasons are printed in every report. There is no human review yet; AI-provisional review sheets and a blank human worksheet are in each `review/` folder.

## How it works (short)

- **Graph:** `plan → choose_action → search → retrieve → extract → verify → update_state → (decide) → … → report`, as 8 nodes. Budgets, rounds and cancellation are guarded in Python.
- **Grounding is not support:** an excerpt must exist verbatim (grounding) **and** pass a separate fail-closed verification before it can score a cell.
- **Cells:** cells are unknown, insufficient, supported, qualified consensus (independent source families, dissent disclosed), scope-dependent (incl. different cost dimensions), or disputed. Scores are intervals; a leader is *robust* only when its lower bound beats every rival's upper bound.
- **Target selection (V3.2):** priority = weight × uncertainty × decision factor × exploration × retry ÷ 2. The decision factor comes from counterfactuals restricted to outcomes that more evidence can actually reach. Every choice is logged with its numbers. These are heuristics, not probabilities.
- **Details:**
  - `docs/design.md`: mechanics, scoring and flips;
  - `docs/architecture.md`;
  - `docs/tradeoffs.md`;
  - `evaluations/v3/V3_CHANGES.md`, `V31_DISPUTE_AGGREGATION.md` and `V32_CHANGES.md`.

## Project layout

```
pathfinder/    agent package: graph, planner, extraction, verification, consensus, matrix, readiness,
               acquisition (V3 policy), policy (V2), coverage, reports, evaluation, cli, tools/ (Exa + fixtures)
tests/         offline test suite (232 tests; no keys, no network)
samples/       real run outputs (V2) and samples/v1
evaluations/   queries.json, rubric.md, v1/ v2/ v3/ (reports, analyses, pre-registrations, frozen code for replay)
docs/          design, architecture, tradeoffs, demo-script, RELEASE_CHECKLIST, submission-readiness
```

Recorded API responses (`evaluations/snapshots*`) and run outputs (`outputs/`) contain third-party page text and are not committed. The derived reports, CSVs and analyses are committed.

AI assistance: this repository was implemented with an AI coding assistant (Claude Code) from the author's specification and decisions.
