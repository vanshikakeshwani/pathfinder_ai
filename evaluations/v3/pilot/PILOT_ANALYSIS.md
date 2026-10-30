# V3 live pilot analysis (Phase 10): Q1, Q4, Q5 × 1 repetition × 3 arms

> **Run:**
> - record: `outputs/eval_v3_E_20261030T071515_43c018`;
> - replay: `outputs/eval_v3_E_20261030T073516_6e4e76`;
> - snapshots: `evaluations/snapshots_v3_pilot/`;
> - generated report: `EVALUATION_REPORT.md`; AI-provisional review: `review/`.
>
> **Procedure:** exactly the pre-registered pilot, with frozen plans, arms `static`, `adaptive` (V3) and `v2_policy`, and a cap of $0.45. **One repetition per question:** these numbers detect defects and confounds; they are not performance evidence. Evidence judgements below are **AI-provisional, not human review**.

## 1. Results (common_stop = full_budget in every run: no early stop fired)

| Q | Arm | Supported | Evidenced (supported + disputed) | Disputed / unknown / insufficient | Targeted rounds that found target evidence | Interval leader (stability) | Recommendation | Counted flips (strong) | Accepted / rejected | Tokens | Exa $ | LLM $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | static | 5/9 | 7 | 2 / 1 / 1 | 3/3 | Qdrant (provisional) | withheld | 1 (1) | 12 / 4 | 46,385 | 0.045 | 0.0101 |
| Q1 | **V3** | 5/9 | 7 | 2 / 1 / 1 | 2/3 | Qdrant (provisional) | withheld | 1 (1) | 11 / 5 | 45,806 | 0.045 | 0.0104 |
| Q1 | v2_policy | 4/9 | 7 | 3 / 0 / 2 | 2/3 | Milvus (provisional) | withheld | 1 (1) | 12 / 5 | 46,468 | 0.045 | 0.0105 |
| Q4 | static | 8/12 | 9 | 1 / 1 / 2 | 2/3 | Summarized customer-profile (provisional) | withheld | 0 | 11 / 8 | 62,447 | 0.045 | 0.0136 |
| Q4 | **V3** | 11/12 | 12 | 1 / 0 / 0 | 2/3 | Hybrid layered (provisional) | withheld | 1 (1) | 13 / 4 | 55,276 | 0.045 | 0.0118 |
| Q4 | v2_policy | 11/12 | 12 | 1 / 0 / 0 | 3/3 | Hybrid layered (provisional) | withheld | 1 (1) | 14 / 5 | 61,976 | 0.045 | 0.0136 |
| Q5 | static | 3/6 | 6 | 3 / 0 / 0 | 3/3 | Managed (undetermined) | none | 0 | 16 / 5 | 59,710 | 0.045 | 0.0138 |
| Q5 | **V3** | 1/6 | 6 | 5 / 0 / 0 | 3/3 | Managed (provisional) | withheld | 0 | 16 / 8 | 65,167 | 0.045 | 0.0157 |
| Q5 | v2_policy | 2/6 | 6 | 4 / 0 / 0 | 3/3 | Managed (provisional) | withheld | 0 | 19 / 6 | 64,040 | 0.045 | 0.0151 |

**Common to every arm:**
- 5 searches and 10 pages (15 actions);
- 0 tool and 0 model errors;
- 0 immediate repeats;
- 0 premature stops;
- 0 provider-failure rounds;
- 0 invalid cited evidence IDs (cited per run: 10–14);
- matched-actions coverage equals the full-budget figures, because every arm spent exactly 15 actions.

**Totals (V3 / v2_policy / static):**

| Measure | V3 | v2_policy | static |
|---|---|---|---|
| Supported | 17 | 17 | 16 |
| Evidenced | 25 | 25 | 22 |
| High-confidence cells | 3 | 5 | 6 |

**Elapsed time per run** was 40–208 s. It is **not comparable between arms**: static runs first and records the shared round 0, and later arms reuse cached identical calls. The pilot process peaked at about 100 MB, and free system memory never fell below 0.54 GB.

## 2. Static vs V2 vs V3, and best arm per question

| Q | Best on supported coverage | Best on evidenced coverage | Comment |
|---|---|---|---|
| Q1 | static = V3 (5) | all equal (7) | V2-policy found the same amount of evidence, but one more cell ended disputed |
| Q4 | V3 = v2_policy (11) | V3 = v2_policy (12) | Both adaptive arms chose the **same first two targets**, so the gain over static (+3) is not V3-specific |
| Q5 | static (3) | all equal (6) | V3 found as much evidence, but more of its cells ended disputed (see §5) |

Paired differences on supported coverage (1 repetition, descriptive only):

| Comparison | Q1 | Q4 | Q5 | Better / equal / worse |
|---|---|---|---|---|
| V3 − static | 0 | +3 | −2 | 1 / 1 / 1 |
| V3 − v2_policy | +1 | 0 | −1 | 1 / 1 / 1 |
| v2_policy − static | −1 | +3 | −1 | 1 / 0 / 2 |

On evidenced coverage, V3 is never below static: +0, +3, +0.

## 3. Did V3 avoid wasteful retries?

**Yes.** V3 never repeated a target; failure memory was used correctly (Q1, round 2 failed on Weaviate:operational_effort, so round 3 moved to Milvus:operational_effort). There was no bounded retry and no fallback. Action labels were correct (targeted 6, corroboration 2, conflict resolution 1).

The `v2_policy` arm also made no repeats in this pilot, because its targets happened to succeed. So the pilot cannot show a *difference* in retry waste.

## 4. Did V3's targets yield useful evidence?

V3 targeted rounds: 7 of 9 found new verified evidence for their target (static 8/9, v2_policy 8/9).

| V3 target type | Rounds | Found target evidence | What it did to the decision |
|---|---|---|---|
| Decisive single cell (factor 2) | 4 | 4 | Q1 r1 caused the leader change (Weaviate → Qdrant). Q4 r2 supported another cell. Q5 r2 found the first self-hosted startup-cost evidence (supported 3 → 4). Q5 r3, the conflict-resolution search, added sources whose scores disagreed with existing ones: supported fell 4 → 1 and disputed rose 2 → 5 |
| Multi-cell group member (factor 1.5) | 3 | 2 | Q4 r1 caused the leader change (supported 8 → 10, 4 cells changed). Q1 r3 supported Milvus ops. Q1 r2 found nothing |
| Readiness corroboration | 2 | 1 | Q5 r1's independent source **disagreed** (4 sources say 2, 1 says 1), so Managed ops became disputed and robustness was lost (the same happened in static and v2_policy on that cell). Q4 r3 found nothing |

**Multi-cell analysis:** in this pilot it produced real search decisions, not just longer explanations. Q4 r1, its clearest case, changed the leader. But V2's policy reached the same target by a different route, so its *added* value is not demonstrated.

**Decisive targets in Q5:** they did reach the decisive cells, but the evidence there kept generating adjacent-score disagreements (§5). Under the current scoring, that lowers supported coverage.

## 5. Defect found: dispute aggregation (scoring, shared by every arm)

There are 22 disputed cells across the 9 runs:

| Pattern | Cells |
|---|---|
| Adjacent scores (1 point apart): rubric-judgement differences rather than factual contradictions | 19 |
| Disputed by a clear majority (3–4 independent domains vs 1), e.g. Managed:operational_effort with 4 domains at 2 and 1 at 1 | 4 |
| Disputed by two excerpts of the **same page** (weaviate.io, scored 1 and 2) | 3 |
| Resolved by later research, in any arm | **0** |

Consequences:
1. **Disputes cannot be resolved.** Adding a source can only add a score to a disputed cell, never remove one. `conflict_resolution` targeting (V3) and corroboration therefore cannot resolve anything under this rule, yet the counterfactual analysis values disputed cells as if they could be pinned to one score (factor 2). This is a real mismatch between the V3 policy and the scoring rule. The offline tests did not catch it, because they checked the counterfactual arithmetic, not whether evidence can reach those values.
2. **More sources lower supported coverage.** The arm that gathers more sources on a cell is penalised (Q5: V3 1/6 supported vs static 3/6, with equal evidenced coverage). The pre-registered *evidenced* metric exposes this, but the supported metric is distorted for every arm.
3. **One page can dispute itself.** A cell is "disputed" by a single source family judging two excerpts differently: rubric inconsistency, not independent conflict.

No new **verification** defect was found:
- rejection patterns are similar across arms (mostly "no derivable fit score", plus a few approach-identity, lexical and partial verdicts);
- spot-checked accepted excerpts are attributed to the right alternative and column.

One context issue remains: Self-hosted:startup_cost compares a $20/month VPS (infrastructure cost, scored 2) with $9–18k of engineering time (cost of ownership, scored 0). These are different cost notions, and the plan's criterion does not separate them.

## 6. Readiness and decision quality

- **Readiness:** no arm reached a ready recommendation. V3 and v2_policy ended *provisional* (withheld) on all three questions. Static ended undetermined, with no recommendation, on Q5.
- **Flips:** all counted flips are leader changes between **provisional** leaders (strong under the V3 definition). No robust winner was ever reversed, and there were no tie-related flips.
- **Q1:** every arm flipped Weaviate → a new leader in round 1, but not to the same one (static and V3 → Qdrant, v2_policy → Milvus). Leaders are sensitive to which cell is researched first.
- **Q5:** robustness was lost in round 1 in all arms, because a disagreeing source was found (honest handling of corroboration that fails).
- **Verdict:** the pilot shows no improvement in readiness or decision quality for V3.

## 7. Reproducibility, fairness and leakage

| Check | Result |
|---|---|
| Offline replay | **all 18 rows identical** |
| `plan_hash` | identical across arms per question, and equal to the frozen plans: Q1 `86d77f59…`, Q4 `39b9ce61…`, Q5 `d8f8ebab…` |
| `round0_hash` | identical across the three arms per question |
| Budgets | identical (5 searches, 10 pages) |
| Future-data leakage | none. All 9 V3 decisions were rebuilt exactly (target, query, action kind) from evidence verified in *earlier* rounds only |

## 8. Spend

**$0.287** provider-reported (Exa $0.209, gateway $0.078), 103 recorded calls, 349,989 tokens. Every gateway call reported a price this time, so the estimate is identical. The pre-pilot estimate was $0.35; the cap was $0.45. The spend guard did not trigger.

## 9. Acceptance criteria

| Criterion | Result |
|---|---|
| Valid recorded and replayable executions | met |
| No invalid citation IDs | met |
| No unintended differences in budgets or initial conditions | met |
| Correct action classification and failure memory | met |
| No future-data leakage | met |
| No new systematic semantic-verification defect | met for verification. **Not met for scoring**: the dispute-aggregation defect in §5 is systematic and interacts with V3's conflict and corroboration targeting |
| Spend within the cap | met ($0.287 ≤ $0.45) |

## 10. Is the full V3 benchmark justified now?

**Not yet.** Under the pre-registration, a defect found in the pilot must be fixed and re-tested offline first. As it stands:
- V3's conflict-resolution and corroboration targets cannot achieve what their counterfactual value assumes;
- supported coverage penalises arms that find more sources.

A benchmark now would mostly measure the scoring artefact.

The fix changes scoring for every arm, so it needs your decision on the rule. Options:
- **(a) Same-source rule:** excerpts from one domain count as one source family. If that family scores the cell two ways, record it as inconsistent and keep the range, but do not call it a dispute between sources.
- **(b) Majority resolution:** the cell is supported at score s when at least 2 independent source families agree on s and outnumber dissenting families at least 2 to 1. The dissent stays disclosed and lowers factual confidence. Otherwise the cell stays disputed.
- **(c) Reachable counterfactuals:** value a disputed cell only by outcomes that more evidence can actually reach under the chosen rule.

After the fix: offline tests, then replay of these pilot recordings under the new scoring (scoring changes need no new calls; only the arms' later choices would differ). Then either a small re-pilot (about $0.29) or the benchmark (estimate $2.07 with v2_policy).
