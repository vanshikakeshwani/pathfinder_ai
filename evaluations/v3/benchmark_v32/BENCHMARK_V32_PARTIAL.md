# V3.2 three-arm benchmark: PARTIAL results (stopped early for the submission deadline)

> **What happened:**
> - The pre-registered benchmark (`../PREREGISTRATION_V32_BENCHMARK.md`: 6 questions × 3 repetitions × 3 arms, cap $2.50) started at 14:10 IST on 2026-10-30.
> - It was **stopped deliberately at 14:41 IST**, as instructed, to prioritise the submission.
> - The stop came right after **repetition 1 completed for all six questions** (18 runs). Repetitions 2 and 3 were not run.
> - A few calls from the interrupted start of Q1 repetition 2 were recorded and are included in the spend. No result from them is reported.
>
> **Status:** with one repetition per question, these results are **descriptive only**. The pre-registered decision rule was written for 18 pairs; applied to these 6 pairs, it gives **"mixed / not supported"** (below).
>
> **Files:**
> - record: `outputs/eval_v3.2_E_20261030T084005_cb1e8e`;
> - offline replay: `outputs/eval_v3.2_E_20261030T091146_fd68af` (**all 36 rows identical**);
> - generated report: `EVALUATION_REPORT.md`; review sheets: `review/` (AI-provisional, plus a blank human worksheet).

## Results (full budget; protocol v3.2; frozen plans; identical round 0 and budgets per question)

| Q | Arm | Strict supported | Consensus | Total supported | Evidenced | Disputed | Targeted rounds that found target evidence | Immediate repeats | Stability | Recommendation | Flips (strong) | Tokens |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | static | 4 | 0 | **5/9** | 5 | 0 | 2/3 | 0 | provisional | withheld | 2 (2) | 45,736 |
| Q1 | v2_policy | 2 | 0 | 3/9 | 3 | 0 | 1/3 | 1 | provisional | withheld | 1 (1) | 50,170 |
| Q1 | V3.2 | 2 | 0 | 3/9 | 3 | 0 | 1/3 | 0 | provisional | withheld | 1 (1) | 44,840 |
| Q2 (discovery) | static | – | – | 3/5 | – | – | 3/3 | 0 | – | – | 0 | 51,028 |
| Q2 | v2_policy | – | – | 3/5 | – | – | 3/3 | 0 | – | – | 0 | 38,070 |
| Q2 | V3.2 | – | – | 3/5 | – | – | 3/3 | 0 | – | – | 0 | 38,070 |
| Q3 | static | 4 | 0 | 4/8 | 4 | 0 | 0/3 | 0 | provisional | withheld | 0 | 57,621 |
| Q3 | v2_policy | 5 | 0 | 5/8 | 5 | 0 | 0/3 | 1 | provisional | withheld | 0 | 66,171 |
| Q3 | V3.2 | 7 | 0 | **7/8** | 8 | 1 | 2/3 | 0 | provisional | withheld | 0 | 67,041 |
| Q4 | static | 8 | 0 | 8/12 | 9 | 1 | 2/3 | 0 | provisional | withheld | 0 | 66,096 |
| Q4 | v2_policy | 10 | 0 | **10/12** | 10 | 0 | 1/3 | 1 | provisional | withheld | 0 | 50,379 |
| Q4 | V3.2 | 10 | 0 | **10/12** | 10 | 0 | 1/3 | 0 | provisional | withheld | 0 | 53,475 |
| Q5 | static | 3 | 2 | **5/6** | 6 | 1 | 2/3 | 0 | robust | withheld | 0 | 57,697 |
| Q5 | v2_policy | 4 | 0 | 4/6 | 5 | 1 | 1/3 | 1 | robust | withheld | 0 | 48,476 |
| Q5 | V3.2 | 4 | 0 | 4/6 | 5 | 1 | 1/3 | 0 | robust | withheld | 0 | 48,059 |
| Q8 (discovery) | static | – | – | 3/5 | – | – | 3/3 | 0 | – | – | 0 | 38,271 |
| Q8 | v2_policy | – | – | 3/5 | – | – | 3/3 | 0 | – | – | 0 | 35,689 |
| Q8 | V3.2 | – | – | **5/5** | – | – | 3/3 | 0 | – | – | 0 | 41,716 |

Discovery questions have no cell-level metrics. Totals:

| Measure | Static | v2_policy | V3.2 |
|---|---|---|---|
| Total supported (of 45) | 28 | 28 | 32 |
| Strictly supported, comparison questions (of 35) | 19 | 21 | 23 |
| Consensus cells | 2 | 0 | 0 |
| Immediate repeats of a failed target | 0 | 4 | 0 |
| Ready recommendations | 0 | 0 | 0 |
| Premature stops | 0 | 0 | 0 |
| Tool and model errors | 0 | 0 | 0 |

**Paired differences** (from `EVALUATION_REPORT.md`; 6 pairs, or 4 comparison pairs for strict):

| Comparison | Total, full budget | Total, matched actions | Strict, full budget |
|---|---|---|---|
| V3.2 − static | median +1 (3 better / 1 equal / 2 worse) | **median 0 (2 / 2 / 2)** | median +1.5 (3 / 0 / 1) |
| v2_policy − static | median 0 (2 / 2 / 2) | median 0 (2 / 2 / 2) | median +1 (3 / 0 / 1) |

**Pre-registered decision rule:** an improvement is claimed only if, at matched actions, *both* strict and total supported coverage have a positive paired median, better outnumbers worse, and evidenced coverage agrees. The matched-actions median for total coverage is 0, so this is **mixed / not supported**.
- **Where V3.2 helped:** Q3 (+3 over static) and Q8 (+2, the only arm that covered every facet). It also never repeated a failed target.
- **Where it didn't:** static was better on Q1 (+2) and Q5 (+1).
- **Q4:** V3.2 tied with the unchanged V2 policy.

## Integrity

- **Replay:** 36/36 rows identical offline.
- **Shared conditions:** plan hashes equal the frozen plans; round 0 shared across arms per question; budgets identical (≤ 6 searches, ≤ 12 pages).
- **Errors and stops:** 0 tool errors, 0 model errors, 0 premature stops.

## Spend

**$0.610 provider-reported** for everything recorded (217 calls; Exa $0.471, gateway $0.139; 644,068 tokens). Every gateway call reported a price, so the estimate is identical. That is well under the $2.50 cap. It includes the few calls from the interrupted start of repetition 2.

## Limitations

- One repetition per question; differences between repetitions were large in V2.
- No human review.
- The scoring heuristics (source families, cost dimensions, product names) and the same-model verifier still apply.
- Repetitions 2 and 3 can be completed later with the same command and the same snapshot folder. Recorded calls would be reused, and a resumed run would add only the remaining spend (about $1.2).
