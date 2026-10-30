# Evaluation analysis V2 (2026-10-30)

> **Scope:**
> - questions: Q1–Q5 and Q8;
> - pairs: 3 independently recorded paired repetitions per question = 18 pairs and 36 arm runs;
> - views: each run reported as `common_stop` and `full_budget` (72 rows).
>
> **Source of every number:** `evaluations/EVALUATION_REPORT.md`, generated from `outputs/eval_v2_E_20261030T045521_1e5cc3`.
>
> **Status:** descriptive only, no significance claims. Quality judgements here are the AI assistant's. **No human review has been done.**
> The V1 evaluation is archived unchanged in `evaluations/v1/`. V2 numbers are not comparable to V1: a different protocol, fixed bugs and a different static baseline.

## 1. Setup

| Item | Value |
|---|---|
| Config fingerprint | `b891d16fe6` (protocol v2), with MAX_SEARCH_CALLS=6, MAX_CONTENT_PAGES=12, PAGES_PER_SEARCH=2, MAX_RESEARCH_ROUNDS=3, MAX_NO_PROGRESS=2 |
| Model / tools | `gpt-6-luna` via the Experiential Labs gateway (strict `json_schema`, temperature 0); Exa Search + Get Contents |
| Pairing | Per repetition: one frozen plan (`plan_rep{k}`) and one shared round 0 (`rep{k}` store); the arms are independent after round 0 |
| Static baseline | Fixed diagonal round-robin over alternatives × criteria (facets in plan order for discovery). Uses the **same query builder** (`queries.py`) as adaptive. |
| Stopping | One common rule for both arms. Each run goes to the full budget and logs where the rule *would* stop. |
| Reuse of earlier calls | The 4 calls recorded for Q1 rep 1 before the out-of-memory stop were reused. Reuse is by exact request hash under the same fingerprint and the code was unchanged. A copy is preserved in `evaluations/snapshots/_Q1_partial_v2_20261030/`. |
| Replay | Offline replays `outputs/eval_v2_E_20261030T061020_502e7e` and `outputs/eval_v2_E_20261030T061724_a5472e` (the latter on the final code, after the post-benchmark spend-accounting edit): **all 72 rows identical** in both |
| Guard | `--max-usd 1.60`, not triggered |

## 2. Headline results

**Targeting value:** adaptive did **not** beat the fair static baseline. Classification of the 18 pairs:

| View | Adaptive better coverage | Equal coverage (both incomplete) | Adaptive worse coverage |
|---|---|---|---|
| common_stop | 5 | 7 | 6 |
| full_budget | 4 | 7 | 7 (plus 1 equal with fewer adaptive actions) |

**Aggregate units supported** (out of 142):

| View | Static | Adaptive |
|---|---|---|
| common_stop | 70 | 69 |
| full_budget | 75 | 71 |

**Actions:** 254 static vs 245 adaptive (common_stop).

**Median coverage per question** (common_stop, median [range] over 3 repetitions):

| Q | Kind | Static | Adaptive |
|---|---|---|---|
| Q1 | comparison, named | 4/9 [0–6] | 4/9 [4–6] |
| Q2 | discovery | 2/5 [2–4] | 4/5 [1–4] |
| Q3 | comparison, approach | 5/8 [4–7] | 5/8 [2–7] |
| Q4 | comparison, approach | 4/12–16 [2–8] | 4/12–16 [0–9] |
| Q5 | comparison, approach | 3/6 [2–6] | 3/6 [3–5] |
| Q8 | discovery | 4/5 [2–5] | 3/5 [2–3] |

Repetition-to-repetition variance is larger than the static/adaptive difference on every question. Medians tie on four questions. Adaptive is ahead on Q2 and behind on Q8.

**Recommendations:** 1 "ready" recommendation in 36 runs (Q5 rep 1, adaptive). Every other comparison run either withheld a recommendation (provisional or not comparable) or had none (undetermined).

**Decision flips:** 1 counted (Q1 rep 2, adaptive; see §5). There were 11–13 status changes per arm.

## 3. Targeting vs stopping (separated)

- **Targeting** (static vs adaptive within one view, same stop rule): no consistent benefit (above).
  - Matched-actions coverage gives the same picture, so the result isn't caused by one arm spending more.
- **Stopping** (common_stop vs full_budget within one arm, same trajectory):
  - The common rule saved 15 actions in each arm.
  - It cost 5 coverage units for static (premature stops Q1r1, Q4r1, Q4r2) and 2 for adaptive (Q3r3, Q4r3).
  - 5 of 36 stops were premature, i.e. full-budget research later found more.
  - Q1r1/static is the worst case: the shared round 0 found nothing, so one more empty round triggered `no_progress`, at 0/9 coverage instead of 3/9.
- So V1's reported adaptive saving (69 vs 90 actions) was largely a stopping effect. With stopping held equal, it disappears.

## 4. Why adaptive did not help (from the traces)

1. **Retries consume the budget.**
   - Only 11 of 51 adaptive targeted rounds were flip-relevant, and 5 were corroboration rounds.
   - In 15 of 51 (29%), adaptive repeated the same target as the previous round ("retry with an open query"), usually after a miss. Static never repeats, so it spreads over more cells.
2. **Flip relevance is rare with 2–4 alternatives and wide intervals.**
   - Most open cells are "not flip-relevant x1". Adaptive then falls back to priority = weight × width, which carries no more information than round-robin.
3. **More evidence produces disputes, which lowers coverage.**
   - Any disagreement among verified rubric scores (for example 1 vs 2 from different sources) makes a cell `disputed` [0, 2], and a disputed cell does not count as supported.
   - Static accepted **266** evidence items vs adaptive's 213, but did not cover more cells.
   - Q5 rep 1 is the clearest case. Static gathered 21 accepted items and ended with 4 disputed cells and a provisional result. Adaptive stopped after one corroboration round, with 10 items, at "ready".
   - The coverage metric therefore rewards stopping before sources disagree. This is a **measurement weakness**, not evidence that adaptive found better facts.
4. **Plan variance.** Each repetition re-plans the question, so criterion sets differ: Q4 had 12, 15 and 16 cells in the three repetitions, with different criterion names. Coverage is not comparable across repetitions, only within a pair.

## 5. Decision flips and status changes

- **Q1 r2 adaptive, round 2:** Weaviate/provisional → Qdrant/**undetermined**. It is counterfactually attributed to EV_9–EV_16, and Qdrant became provisional in round 3.
  - It counts under the pre-registered rule (`policy.classify_change`; a listed-order leader is kept under a tie, test D01).
  - **It is a weak flip:** the round ended in a tie, not with a new real leader.
  - I considered tightening the rule after seeing this result and decided against it. Changing a pre-registered definition after the results are known would be post-hoc.
- No static flips. No flips were forced or simulated in live runs. The synthetic flip remains fixture-only (`demo-fixture`).
- **Interval-leader disagreement between the arms of a pair:** Q1 r1 (Weaviate vs Milvus, both weak), Q1 r2 (Weaviate vs Qdrant) and Q4 r3 (both undetermined). In all other pairs the leaders matched.

## 6. Did the V2 fixes work?

| Fix | Evidence in this run | Verdict |
|---|---|---|
| Approach-identity verification (Q3–Q5) | V1 had 0 supported Q4 cells. V2 Q4 reached 8–9/12 in rep 1, and approach cells are supported across Q3–Q5. 0 lexical-check rejections of approach alternatives. | Works. The verifier still makes attribution errors in both directions (`evaluations/v2/REVERIFY_V1_Q3_Q5.md`). |
| Context-aware scoring (Q1) | Qdrant ops shown as `scope-dependent` (managed 2, self-hosted 1) rather than disputed. No Q1 run reports a recommendation from non-comparable evidence. | Works for the V1 failure. Context labels come from the extractor. |
| Readiness safeguard | 1 ready in 36 runs; withheld reasons printed in each report | Works, though conservative. Most withholding is due to overlapping intervals or single-source cells. |
| Fair static baseline | Static covers different cells each round with identical query wording | Works. It removed V1's apparent adaptive advantage. |
| Common stop rule | Stopping and targeting reported separately | Works. It exposed the premature stops listed in §3. |

## 7. Failure cases and regressions

- **Q4 r3:** a gateway timeout during round-0 extraction ("Request timed out", 3 attempts) left the shared round 0 empty for both arms.
  - Adaptive then found 0 units in the common view (`insufficient_evidence`) and 1 at full budget; static found 2/16.
  - Recorded as a failure, not excluded.
- **Q1 r1:** the shared round 0 verified nothing (13 rejections: mostly "attributes the excerpt to multiple" and "no derivable fit score"). This led to the premature static stop.
- **Rejection reasons, Q3–Q5 (all runs):**

  | Reason | Count |
  |---|---|
  | No derivable fit score (verifier did not accept the proposed rubric score) | 55 |
  | Excerpt not found verbatim (grounding) | 25 |
  | Approach identity: "describes several alternatives" | 7 |
  | Approach identity: identification quote not found | 6 |
  | Lexical-check rejections | **0** (V1: 69) |

  Q1 (named products) had 6 lexical rejections and 9 "attributes to multiple". These are comparison articles that discuss all three products in one paragraph.
- **Regression vs V1:** none in safety or citation validity. 0 invalid cited IDs and 0 tool errors in all 36 runs. 3 LLM errors, all from the Q4 r3 timeout, which is counted in both arms because round 0 is shared.

## 8. Cost and tokens (provider-reported, not an invoice)

| Item | Value |
|---|---|
| Recorded calls | 526 (each counted once; the shared round 0 is counted once) |
| Exa `cost_dollars` | $1.197 |
| Gateway `usage.cost` | $0.169 |
| **Total provider-reported** | **$1.366** |
| LLM tokens | 1,539,539 |
| Under-reporting | 130 gateway calls (726,540 tokens) reported `usage.cost = 0`. At the average rate of the priced calls (about $0.21 per million tokens) they would cost about $0.151, giving an **estimated total of $1.52**. The spend guard now uses this estimate. |

Earlier V2-phase spend, provider-reported:

| Item | Reported | Estimated |
|---|---|---|
| Pilot 1 | $0.168 | $0.168 |
| Pilot 2 | $0.156 | $0.183 (21 unpriced calls) |
| V1 re-check | $0.040 | |
| Smoke tests | $0.007 | |

**V2 phase total:** about $1.74 reported, about $1.92 estimated, against the ~$2 target.

## 9. What can be claimed

- **Can be claimed:**
  - The V2 pipeline produces cited, verifiable, replayable reports.
  - It withholds recommendations when evidence is weak or not comparable.
  - It verifies conceptual alternatives that V1 could not.
- **Cannot be claimed:** that adaptive flip-targeting improves coverage, accuracy or efficiency over a fair round-robin baseline at this budget. In this benchmark it did not.
- **Not measured:** factual accuracy (no human labels), and elapsed time (the second arm reuses cached round-0 calls).

## 10. Suggested next steps (not implemented: new features were out of scope)

1. Treat close disagreements (1 vs 2) as a narrower interval [1, 2] instead of [0, 2], or report "disputed" separately from "unknown" in coverage.
2. Skip a failed target for one round instead of retrying it immediately, or cap retries at one.
3. Freeze one plan per question across repetitions, so that repetition variance reflects retrieval rather than planning.
4. Human review of the AI-provisional materials (`evaluations/review/`).
