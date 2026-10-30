# Phase 1: diagnosis of the V2 failures (from decision traces)

> **Source:** `outputs/eval_v2_E_20261030T045521_1e5cc3` (V2 record, 36 runs).
> **Method:** the state before every action was rebuilt offline from evidence verified in *earlier* rounds only (`pathfinder/trace_replay.py`). All numbers come from `evaluations/v3/diagnose_v2.py` (output `diagnosis_v2.json`).
> **Fidelity check:** the rebuilt state matches the recorded `round_metrics` in **93 of 93** comparison rounds (units, leader, stability, readiness). V2 itself still replays identically with the frozen V2 code (`evaluations/v2/replay_v2.py`: 0 differences in 72 rows).
> No evaluation definition was changed for this diagnosis.

## Measured facts

| Measure | Adaptive | Static |
|---|---|---|
| Targeted rounds (comparison / discovery) | 33 / 18 | 36 / 18 |
| Comparison rounds that found new evidence for the chosen target | **11 / 33 (33%)** | 23 / 36 (64%) |
| Comparison rounds that repeated the previous target | 11 (10 right after a failure; 3 of them succeeded) | 0 |
| Of those repeats, other open cells were available | 10 | — |
| Rounds where at least one single-cell flip-relevant target existed | 11, and adaptive chose it every time | 14 (not used) |
| Rounds where only a *pair* of cells could change the leader (no single cell could) | 8, all treated as "not flip-relevant x1" | 7 |
| Rounds where nothing could change the leader and no corroboration was pending | 9 | 15 |
| Corroboration rounds | 5 | — |
| Static rounds spent on cells that were already supported | — | 17 / 36 |

**Final disputed cells:** 19 (adaptive 7, static 12). By score set:

| Score set | Cells |
|---|---|
| {1, 2} | 10 |
| {0, 1} | 8 |
| {0, 2} | 1 |

**Rounds where supported coverage fell:** 6 (static: Q3r2, Q5r1 twice, Q5r3; adaptive: Q5r2, Q5r3).

**Readiness**, over 24 comparison runs:

| Status | Runs |
|---|---|
| ready | 1 |
| withheld | 18 |
| none | 5 |

Withheld reasons: "intervals overlap" 16, "differentiating cells lack strong support" 11.

**Plans:** criteria counts differed between repetitions only for Q4 (12, 15 and 16 cells). Criterion *names* also differed between repetitions (e.g. `implementation_complexity` vs `implementation_and_operational_complexit`).

**Premature stops** (5; the common rule stopped before units that the full budget later found):

| Run | New units per round (r0, r1, r2, r3) | Cause |
|---|---|---|
| Q1 r1 static | 0, 0, 1, 2 | The empty shared round 0 counted toward `no_progress`, so one empty targeted round stopped it |
| Q4 r3 adaptive | 0, 0, 0, 1 | Provider timeout in round-0 extraction (1 tool failure) counted as "no progress", plus one failed round |
| Q3 r3 adaptive | 2, 0, 0, 1 | Two rounds on the same failed target (an immediate retry) |
| Q4 r1 static | 8, 0, 0, 1 | Two consecutive empty targeted rounds. The schedule still had unresearched cells that could matter. |
| Q4 r2 static | 4, 0, 0, 1 | Same as Q4 r1 |

**Counted flip:** Q1 r2 adaptive, round 2: Weaviate/provisional → Qdrant/**undetermined**, via EV_9–EV_16. It moved into a tie.

## Root-cause table

| # | Failure | Code path | Policy decision behind it | Supporting trace |
|---|---|---|---|---|
| R1 | Budget spent on immediate retries | `policy.choose_next_comparison`: takes the top of `rank_targets` unless `attempts ≥ MAX_ATTEMPTS_PER_TARGET (2)`. A failed target keeps its rank, because it is still unknown with the same priority. | No memory of *failure*, only of attempt counts. There is no cool-down, and no comparison with other targets after a miss. | 11 of 33 comparison rounds repeated the previous target; 10 followed a failure, and other open cells existed in 10. Only 3 of 10 retries after failure succeeded. Examples: Q4r2 round 2 (11 other open cells, all flip-relevant), Q3r3 round 2 (premature stop). |
| R2 | Flip relevance does not discriminate | `policy.flip_relevant`: pins **one** cell to 0 and to 2 and compares the outcome leader | The single-cell test is all-or-nothing: early on every cell can flip a near-tie (Q1r1 round 2: 8 of 8 open cells), later none can alone. Cells that matter only *jointly* get the same x1 as irrelevant cells. | Single-flip cells were available in 11 rounds and absent in 22. In 8 of the absent rounds a pair of cells could change the leader. In the other 9 (plus 5 corroboration rounds), priority reduced to weight × width, which is weighted missing-cell selection. |
| R3 | Adaptive chooses hard targets with no fallback | `rank_targets` ranks only by weight × width × flip factor. There is no notion of how researchable a target is, or that it was already searched. | Cells still unknown after round 0 are often the hard ones (no page addresses them). Adaptive keeps returning to them. | Adaptive found new target evidence in 33% of comparison rounds vs 64% for static. Static's rate includes 17 rounds on cells that were already supported, where new evidence can only confirm or dispute. |
| R4 | Close disagreements erase coverage | `matrix.cell_state`: any two different scores in one context give `disputed` [0, 2] | Maximally conservative: a 1-vs-2 disagreement is treated as total ignorance, and the cell stops counting as covered | 18 of 19 final disputes were adjacent ({1,2}: 10, {0,1}: 8). Coverage fell in 6 rounds; Q5r1 static went 5 → 3 → 2 units while accepting 21 items. Static accepted 266 items vs 213 and was penalised for the extra sources. |
| R5 | Readiness rarely reachable, and blockers not targeted before robustness | `readiness.assess` plus `policy.choose_next_comparison`. Corroboration only starts once the interval is **robust**, so readiness blockers on a provisional leader are invisible to targeting. The "high confidence" test also accepts a vendor's own page as strong support for an evaluative claim. | Readiness is a gate, not a goal of the policy before robustness | 1 ready in 24 comparison runs. Withheld for overlap 16 times and for weak differentiating cells 11 times. |
| R6 | Premature stops from non-research failures | `graph.node_update_state` adds 1 to `no_progress_rounds` for **every** empty round, including round 0 and rounds where the provider failed. `early_stop_reason` only exempts round 0 from *stopping*, not from *counting*. | Provider failure and an empty shared round are treated as evidence that research is exhausted | Q1r1 static (empty round 0) and Q4r3 adaptive (round-0 timeout) |
| R7 | No-progress stop ignores remaining consequential targets | `early_stop_reason` uses only the count of empty rounds | It stops after 2 empty rounds even while unresearched, decision-relevant cells remain | Q4r1 / Q4r2 static, and Q3r3 adaptive: units found in round 3 after the would-stop |
| R8 | Plan variance between repetitions | `evaluation.evaluate` calls `freeze_plan` once **per repetition** (`plan_rep{k}`) | A fresh LLM plan per repetition: different criteria and cell counts | Q4: 12, 15 and 16 cells. Criterion names differ between repetitions, so coverage isn't comparable across repetitions. |
| R9 | Weak tie-related flip counted | `policy.classify_change`: the listed-order leader is kept under a tie, so provisional → tie with a different listed leader counts as `leader_changed` | Pre-registered in V2 (test D01); kept for V2 | Q1r2 adaptive round 2. **V2's count stays 1**; V3 adds a stricter, separately reported metric. |
| R10 | Discovery retries | `coverage.choose_next_discovery`: same attempt logic as R1 | No failure memory | 4 of 18 discovery rounds repeated the previous target (all found something, since discovery counts any facet evidence) |

## What the V3 changes target, and what they deliberately do not

| Root cause | V3 change | Applies to |
|---|---|---|
| R1, R10 | Failure memory, a one-round cool-down after a failed target, at most one immediate retry (only for a uniquely decisive target), a penalty per failure, a ladder of query variants and near-duplicate detection | Adaptive policy only (static never retries) |
| R2 | Counterfactual analysis per cell over its possible rubric scores, plus a greedy **minimal group** analysis for joint changes. Effects recorded: leader change, tie-break, robustness, readiness and rule-out. | Adaptive policy only |
| R3 | Failure penalty and exploration balance across alternatives | Adaptive policy only |
| R4 | Disputed interval = [min, max] of verified scores, still `disputed` and **not** counted as supported. Disputed and unknown coverage reported separately. | Scoring for **both** arms |
| R5 | Readiness blockers become targets at any stability. Added blockers: the leader's own disputed or unsupported critical cell, and self-reported evaluative claims. | Readiness (both arms); targeting (adaptive) |
| R6, R7 | No-progress counting starts after round 0 and skips provider-failure rounds. No-progress does not fire while an unattempted, decision-relevant cell remains (bounded by the budget). | Common stop rule (**both** arms) |
| R8 | One fixed plan per question across all repetitions | Evaluation protocol |
| R9 | V2 definition preserved. A stricter "strong flip" (real leader → different real leader) is reported separately and was pre-registered before the V3 benchmark. | Reporting |

Not changed: the static baseline (fixed diagonal round-robin, the same query builder at attempt 0, no skipping of supported cells), the verifier, the extraction prompts, the planner prompt and the budgets.
