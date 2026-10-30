# OFFLINE POLICY COMPARISON: V2 vs V3 decisions on identical frozen inputs

> **This is not a measurement of live research performance.**
> - **What it compares:** which target each policy *chooses*, given exactly the state V2 was in at each recorded decision point.
> - **What it cannot tell:** what V3's different choices would have found, because those searches were never made. No coverage, accuracy or efficiency claim for V3 follows from this file. That needs the controlled live pilot and benchmark (`PREREGISTRATION.md`).
> - **Source:** `evaluations/v3/offline_policy_comparison.py` on `outputs/eval_v2_E_20261030T045521_1e5cc3`; full output in `offline_policy_comparison.json`. No API calls.

## Method and safeguards

- **Rebuilt state:** the state before the action of round r is rebuilt from evidence verified in rounds < r only (`trace_replay.evidence_before`), plus that run's own earlier attempts, failures and queries (`trace_replay.history_before`).
- **No look-ahead:**
  - offline, on a synthetic V3 run, rebuilding from earlier rounds reproduces every live V3 decision: target, query and action kind (`tests/test_trace_replay.py`);
  - on the V2 benchmark, re-running the **V2** policy on the rebuilt state reproduces the action V2 actually took in **33 of 33** adaptive decision points.
- **Conditioning:** later V3 choices are conditioned on V2's path (V2's evidence and attempts), not on what V3 would have found.

## Results (24 comparison runs; 33 adaptive decision points)

| Measure | V2 (recorded) | V3 (offline choice) |
|---|---|---|
| Same target as V2 | — | 7 / 33 |
| Repeat of a target that failed in the previous round | **10** | **0** at those same 10 points |
| Choice is a decision-relevant open cell (alone or in a minimal group) | 26 | 25 |
| Corroboration (readiness blocker) | 5 | 7 |
| Conflict resolution (disputed cell) | 0 | 1 |
| Labelled fallback (coverage only) | — | 1 |

V3's decision factors at its 33 choices:

| Decision factor | Choices |
|---|---|
| 2.0 (decisive alone, or the sole readiness blocker) | 13 |
| 1.5 | 11 |
| 1.33 | 6 |
| 1.25 (could rule out an alternative) | 2 |
| 1.0 | 1 |

V2's binary single-cell test labelled 22 of these 33 points "nothing flip-relevant". V3 finds group-level or readiness value at most of them.

## Examples

| Point | V2 chose | V3 chooses | Why (V3 trace) |
|---|---|---|---|
| Q1 r2, round 2 | Qdrant:operational_effort again, after it failed in round 1 | Weaviate:operational_effort | "could change the leader" (decisive; the failed target is in cool-down) |
| Q1 r3, round 1 | Milvus:deployment_fit | Qdrant:filtering_capability | "jointly matters: Weaviate overtakes Qdrant needs a group of 3 cells" |
| Q4 r1, round 1 | Hybrid layered memory:retention_and_deletion_control | Summarized customer-profile memory:retrieval_effectiveness | "jointly matters: … overtakes Session-only memory needs a group of 2 cells" |
| Q3 r1, round 2 | Single-agent:implementation_complexity again, after it failed | Multi-agent:total_cost#corroborate | readiness blocker: a single-source differentiating cell |
| Q5 r2, round 3 | Self-hosted:operational_effort#corroborate again, after it failed | Managed:total_cost (fallback, factor 1.0) | The failed readiness target is in cool-down and no other valuable target remains, so V3 explores a coverage-only cell. **This is a possible weakness:** one more attempt at the blocker might have been worth more. |

## Common stopping rule on the same V2 trajectories (decisions unchanged)

| | V2 rule (recorded) | V3 rule (offline) |
|---|---|---|
| Premature stops (stopped before units the full budget later found) | 5 / 36 | **0 / 36** |
| Units lost to early stopping | 7 | 0 |
| Actions saved by early stopping | 30 | **3** |
| Runs where V3 stops later / earlier than V2 | — | 7 later / 0 earlier |

V3 removes every premature stop, at the price of almost all of the stopping savings. On this budget (3 targeted rounds) the stop rule has little room to save actions once empty and failed rounds are discounted.

## Re-scoring the final V2 evidence with the V3 rules (both arms)

| | V2 dispute interval [0, 2] | V3 dispute interval [min, max] |
|---|---|---|
| Supported cells | 110 | 110 (unchanged: disputes never count) |
| Disputed cells | 19 | 19, of which 18 are narrowed to a width-1 range |
| Insufficient cells (new state) | — | 43 |
| Interval stability robust / provisional / undetermined | 3 / 16 / 5 | 5 / 13 / 6 |
| Interval leader changed by the rule | — | 1 run |

Both columns use the V3 readiness rules. The single V2 "ready" recommendation (Q5 r1 adaptive) is **withheld under V3**: "Managed vector database's own score on control_and_customization is disputed (verified scores [0, 1])". The stricter readiness is deliberate; it is not an error in V2's arithmetic.

## What this does and does not support

- **Supported:** V3 no longer wastes rounds on immediate repeats of failed targets. It replaces V2's binary flip test with graded, recorded counterfactuals that identify jointly relevant cells. Its stopping rule would not have stopped prematurely on the V2 trajectories.
- **Not supported:** that V3 finds more or better evidence than static or V2. V3 chose a different target at 26 of 33 points, and whether those searches would succeed is unknown. V2's own data shows that hard cells often fail: adaptive's target success was 33% vs static's 64%. Only the live, paired benchmark can answer this.
