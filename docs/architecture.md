# Architecture (V2, with V3 changes marked)

> V3 changes are implemented and tested offline; no live V3 evaluation has been run yet. Details: `evaluations/v3/V3_CHANGES.md`.

## Data flow

| Stage | Module | Trusts the LLM? | Output |
|---|---|---|---|
| Plan | `planner.py` | Drafts only. Ids slugified; weights user > inferred > default 3; alternatives typed `named` or `approach`; criterion `scopes` / `preferred_scope`; fewer than 2 alternatives → coverage mode | `ResearchPlan` |
| Choose action | V3: `acquisition.py` (adaptive comparison; V2 policy kept in `policy.py` as the `v2_policy` arm), `coverage.py` (discovery), `planner.static_queue` (static) | No | `ResearchAction` with score, `action_kind`, reason and the recorded `analysis` |
| Query text | `queries.py`, shared by both arms | No | Query string and official-domain filter |
| Search / Retrieve | `tools/exa_adapter.py` via `ToolRunner` | n/a | `SearchHit[]` → `Source` (app-allocated `SRC_n`) |
| Extract | `extraction.py` | Proposes candidates with `scope` and `rubric_rationale` | `ExtractionCandidate[]` |
| Ground | `grounding.Registry.ground` | No | Verbatim excerpt, checked offsets |
| Verify | `verification.py` | Gives a verdict; **acceptance is decided by code** | `Evidence` or `RejectedCandidate` (excerpt kept) |
| Update | `matrix.py`, `coverage.py`, `policy.detect_decision_change` | No | Cells/intervals or coverage, decision changes, round snapshot |
| Readiness | `readiness.py` | No | Interval leader, recommendation `ready` / `withheld` / `none`, reasons |
| Report | `reports.py` | Optional prose; citations validated | `ResearchReport` + files |

## Identity checks by alternative kind (verification.py)

- **Named** (product/company): the verifier must say the excerpt is about this entity, **and** the name or an alias must appear in the excerpt context (lexical).
- **Approach** (conceptual option): the verifier must attribute the excerpt to *this* approach. `applies_to` must be its name, not another alternative, `multiple` or `none`, and the identification quote it gives must be found verbatim in the source by code. The planner's label itself need not appear. Instruction-like text in an excerpt is rejected regardless of the verdict.

## Cells, scopes and corroboration (matrix.py)

| State | Meaning | Interval |
|---|---|---|
| unknown | no scorable verified evidence | [0, 2] |
| supported | consistent evidence | [s, s] |
| insufficient (V3) | researched; on-target candidates could not justify a score | [0, 2] |
| scope_dependent | consistent within each context, but contexts differ (e.g. managed 2, self-hosted 0) and the user chose none | [min, max] |
| consensus (v3.1) | qualified consensus of independent source families, dissent disclosed (`pathfinder/consensus.py`) | [s, s] |
| disputed | conflicting evidence within one context without qualified consensus; kind recorded | V3: [min, max] of the verified scores (V2: [0, 2]); never supported |

- With a `preferred_scope`, only that context (and `general`) scores. Other-context evidence is kept and listed as excluded.
- `independent_sources` counts distinct domains among *distinct* excerpts, so a repeated passage is not corroboration.

## Recommendation readiness (readiness.py)

The interval outcome (`robust` / `provisional` / `undetermined`) is always computed and traced. A recommendation is **ready** only if:
- the leader is interval-robust;
- the differentiating cells (where the leader's and a competitor's supported scores differ) all have high factual confidence;
- no differentiating criterion compares different scopes.

Otherwise the report says "Interval result: X … Recommendation withheld: <reasons>". Adaptive then researches the blocking cells (`#corroborate` targets: open queries, in the comparable scope).

V3 adds named blockers (`readiness.Blocker`): the leader's own score disputed, a critical criterion (weight ≥ 4) unsupported for the leader, and an evaluative advantage resting only on the leader's own domain. The V3 policy targets blockers at any stability, not only once robust.

## Graph

`graph.py` builds a `StateGraph` with a single state key `ctx` (`RunContext`). There are 8 nodes, plus the `decide` router after `update_state`.

- Every node is guarded: it skips work once a stop reason is set, turns cancellation into `cancelled`, and lets `report` always run.
- **Common stopping rule** (`early_stop_reason`), identical for both strategies:
  - `stable`: robust with the recommendation ready, or discovery complete;
  - `no_progress`: `MAX_NO_PROGRESS` targeted rounds without newly verified units. V3: round 0 and provider-failure rounds are not counted, and the stop is deferred while a decision-relevant cell has never been attempted;
  - budget and round caps.
- `RunContext.early_stop=False` (evaluation) skips stable/no_progress but still evaluates the rule each round and logs it as `would_stop` in a `round_metrics` snapshot.

## Static baseline (evaluation)

`planner.static_queue(plan)` is a fixed schedule computed from the plan before any retrieval:
- comparison: **diagonal round-robin** over alternatives and criteria, e.g. 3×3 → (0,0) (1,1) (2,2) (0,1) …;
- discovery: facets in plan order.

Queries come from `queries.py` with the same arguments the adaptive arm would use for that target. **The only policy differences are which target is researched next** (fixed schedule vs flip-relevance and corroboration ranking), **and, in the common_stop view, nothing else**. The stopping rule is shared.

## Evaluation protocol V3 (evaluation.py)

- One frozen plan per question, reused by every repetition and arm (`--plans-dir evaluations/v3/plans`).
- Arms by name: `static`, `adaptive` (V3), `v2_policy`, and ablations (`--arms`). All share round 0 and every component except target selection.
- Protocol `v3` fingerprint. V2 is replayed with its frozen code (`evaluations/v2/replay_v2.py`).

## Evaluation protocol V2 (evaluation.py, historical)

- **Pairs:** one frozen plan and one shared round 0 per repetition. Arms are separate after that. Repetitions are independent: separate `plan_rep{k}` / `rep{k}` snapshot stores.
- **Two views of each arm's single trajectory:** `common_stop` (an exact prefix up to `would_stop`) and `full_budget`.
- **Snapshots** are keyed by a fingerprint of the budget/provider settings plus the protocol version, so V1 recordings are never reused.
- **Spend guard:** `--max-usd` stops before a pair if provider-reported spend plus the largest observed pair cost would exceed the cap.
