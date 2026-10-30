# Submission readiness (2026-10-30)

Legend:
- **DONE**: verified in this repo
- **PARTIAL**: exists, with a known gap
- **YOU**: only the author can do it

| Item | Status | Evidence |
|---|---|---|
| Fresh install on Windows / Python 3.11 | DONE | Clean copy of the submission file set, new venv, `pip install -c requirements-lock.txt -e ".[dev]"`; see `docs/RELEASE_CHECKLIST.md` |
| Offline tests and lint | DONE | 232 tests pass, Ruff clean (also in the fresh copy) |
| Offline demo without keys | DONE | `demo-fixture --case all`: flip, confirm, no-progress (SYNTHETIC) |
| Live workflow (GPT-6 Luna + Exa) | DONE | 36 V2 runs plus 2 × 9 pilot runs and the V3.2 benchmark runs, all with recorded provider responses; `smoke-gateway` passed (`docs/gateway-compat.md`) |
| Plan, trace and tool decisions visible | DONE | `decision_trace.jsonl`; every V3 action records its calculation (`analysis`) |
| Search and Contents as separate tools | DONE | `tool_usage.json` |
| Citations validated | DONE | 0 invalid cited IDs across all evaluated runs |
| Bounded loops; explicit stop reasons | DONE | All runs end with a stated reason |
| ≥ 5 real questions evaluated | DONE | V2: 6 questions × 3 repetitions (replayed exactly). V3/V3.1 pilots. V3.2 benchmark partial (stopped for the deadline). |
| Honest evaluation write-up | DONE | `evaluations/v2/EVALUATION_ANALYSIS.md`, `evaluations/v3/pilot*/`, `evaluations/v3/benchmark_v32/` |
| 2–3 real sample outputs | DONE | `samples/` (V2 runs with caveats) |
| Secrets excluded | DONE | `.env` git-ignored; key scan of the submission set: 0 hits |
| Human review scores | YOU (optional) | Blank worksheets in the `review/` folders; AI-provisional reviews are labelled as such |
| Demo video (3–5 min) | YOU | `docs/demo-script.md` |
| GitHub repository and push | YOU | Commands in `docs/GIT_PUBLISH.md`; nothing has been committed or pushed |
| AI-assistance disclosure | DONE (confirm policy) | Last line of `README.md` |

**Known limitations** (`docs/tradeoffs.md`):
- adaptive targeting has not been shown to beat the fair baseline;
- scores are rubric judgements by the same model family;
- source and cost-dimension heuristics;
- no human review.
