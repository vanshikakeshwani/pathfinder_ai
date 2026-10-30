# V3.1 controlled live pilot: Q1, Q4, Q5 × 1 repetition × 3 arms

> **Run:**
> - record: `outputs/eval_v3.1_E_20261030T080154_a99d87`;
> - replay: `outputs/eval_v3.1_E_20261030T082133_ff0182`;
> - snapshots: `evaluations/snapshots_v31_pilot/`;
> - generated report: `EVALUATION_REPORT.md`; AI-provisional review sheet: `review/`.
>
> **Procedure:** exactly `PREREGISTRATION_V31.md`, protocol v3.1, frozen plans, cap $0.40.
> **Purpose:** a correctness and fairness pilot, with one repetition per question. Performance numbers are descriptive only.
> **Review status:** evidence judgements are **AI-provisional, not human review**, and a consensus is **not** independently verified truth.

## 1. Pre-registered pass criteria

| # | Criterion | Result |
|---|---|---|
| 1 | Replay identical; same plan and round-0 hashes; same budgets | **Pass.** 18/18 rows identical. Plan hashes Q1 `86d77f59…`, Q4 `39b9ce61…`, Q5 `d8f8ebab…` (equal to the frozen plans). Round-0 hash identical across the 3 arms per question. Every run used 5 searches and 10 pages. |
| 2 | 0 invalid citations; no future-data leakage | **Pass.** 0 invalid cited IDs. All 9 V3.1 decisions were rebuilt exactly (target, query) from earlier-round evidence only. |
| 3 | No duplicate family voting; dissent retained | **Pass.** `audit_cell` found 0 problems in 81 cells. |
| 4 | Same-document conflicts labelled `source_inconsistent` | **Pass.** v2_policy Q1 Milvus:deployment_fit is `source_inconsistent`; no other same-document conflict occurred. |
| 5 | Cost dimensions never pooled | **Pass, with one misclassification** (§4). Self-hosted startup cost was split by dimension in static and in V3.1. |
| 6 | Only reachable outcomes pinned; discount by k | **Pass, but barely exercised.** 0 counterfactual values outside `pin_values`. Every one of the 40 ranked candidates was `resolvable_by_one_source` (2 `not_applicable`), so the k-discount and the unreachable path never triggered live. |
| 7 | Conservative withholding | **Pass.** 0 ready recommendations, each with explicit reasons: self-reported advantage, the leader's own disputed cell, single-source differentiating cells, overlapping intervals. |
| 8 | Spend ≤ $0.40 | **Pass.** $0.321 provider-reported. Every call was priced, so the estimate is identical. |

There were no premature stops and no tool errors. Memory never fell below 0.60 GB free, and the pilot process peaked at 102 MB.

## 2. Results (full_budget; common_stop is identical except static Q1, which would stop for no progress after round 2, with no units lost)

Strict = cells in state `supported`. Total supported (v3.1) = strict + consensus + scope-dependent (dimension mismatches excluded). Evidenced = total + disputed.

| Q | Arm | Strict | Consensus | Total | Evidenced | Disputed | Unknown / insufficient | Dim. mismatch | Targeted rounds that found target evidence | Immediate repeats | Leader (stability) | Ready | Tokens | Exa $ | LLM $ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | static | 6 | 0 | 6/9 | 6 | 0 | 1 / 2 | 0 | 2/3 | 0 | Qdrant (robust) | no | 45,526 | 0.045 | 0.0105 |
| Q1 | **V3.1** | 7 | 0 | **7/9** | 8 | 1 | 0 / 1 | 0 | 2/3 | 0 | Qdrant (provisional) | no | 44,973 | 0.045 | 0.0107 |
| Q1 | v2_policy | 6 | 0 | 6/9 | 8 | 2 | 0 / 1 | 0 | 1/3 | 1 | Weaviate (provisional) | no | 51,001 | 0.045 | 0.0118 |
| Q4 | static | 9 | 0 | 9/12 | 10 | 1 | 1 / 1 | 0 | 2/3 | 0 | Session-only (provisional) | no | 62,753 | 0.044 | 0.0142 |
| Q4 | **V3.1** | 9 | 1 | **10/12** | 10 | 0 | 0 / 2 | 0 | 1/3 | 0 | Session-only (provisional) | no | 56,700 | 0.044 | 0.0118 |
| Q4 | v2_policy | 9 | 0 | 9/12 | 10 | 1 | 0 / 2 | 0 | 0/3 | 1 | Session-only (provisional) | no | 54,415 | 0.044 | 0.0110 |
| Q5 | static | 2 | 1 | 3/6 | 6 | 2 | 0 / 0 | 1 | 3/3 | 0 | Managed (provisional) | no | 63,307 | 0.045 | 0.0147 |
| Q5 | **V3.1** | 5 | 0 | 5/6 | 6 | 1 | 0 / 0 | 1* | 2/3 | 0 | Managed (robust) | no | 58,710 | 0.045 | 0.0131 |
| Q5 | v2_policy | 5 | 1 | **6/6** | 6 | 0 | 0 / 0 | 0 | 1/3 | 1 | Managed (robust) | no | 62,261 | 0.045 | 0.0146 |

\* In Q5 V3.1, Self-hosted:startup_cost is disputed **inside** one cost dimension (it is split by dimension and one dimension is disputed). It is counted as disputed, not supported.

**Totals:**

| Measure | Static | V3.1 | v2_policy |
|---|---|---|---|
| Strict supported | 17 | **21** | 20 |
| Qualified consensus | 1 | 1 | 1 |
| Total supported | 18 | **22** | 21 |
| Evidenced | 22 | 24 | 24 |
| Source families (certain independence) | 40 (36) | 37 (33) | 36 (31) |
| Targeted rounds that found target evidence | 7/9 | 5/9 | 2/9 |
| Immediate repeats | 0 | 0 | 3 (1 succeeded) |
| Disputes genuinely resolved by research | 0 | 1 | 0 |
| Counted flips | 0 | 0 | 1 (tie-related) |
| Strong flips | 0 | 0 | 0 |
| Model errors | 0 | 0 | 3 (one verifier timeout in Q5; fail-closed; logged as a provider-failure round, not "no progress") |

Paired differences in total supported coverage (descriptive, n = 3):

| Comparison | Q1 | Q4 | Q5 | Better / equal / worse |
|---|---|---|---|---|
| V3.1 − static | +1 | +1 | +2 | 3 / 0 / 0 |
| V3.1 − v2_policy | +1 | +1 | −1 | 2 / 0 / 1 |

On strict coverage only, V3.1 − static is +1, 0, +3. Coverage at matched actions equals the full-budget figures, because every arm spent exactly 15 actions.

## 3. Does V3.1 make useful target-selection decisions?

**Partly.**
- **Retries:** V3.1 avoided wasteful retries. The cool-down skipped a just-failed target 3 times, while the V2 policy repeated a failed target 3 times (1 success).
- **Resolved dispute:** its single conflict-resolution search (Q4, round 3) found an independent arXiv source agreeing with an existing score of 1, turning a 1-vs-1 dispute into a weak consensus. That is the only dispute any arm resolved.
- **Target success:** V3.1 found evidence for its target in 5 of 9 rounds, below static's 7/9. Its higher coverage came partly from evidence found for other cells on the same pages.
- **Q5 corroboration:** all three V3.1 actions were readiness corroboration. They made the leader robust, but readiness stayed blocked by a single-source differentiating cell.

## 4. Manual inspection (AI-provisional)

| Cell | What happened | Judgement |
|---|---|---|
| Q4 V3.1 Summarized:retrieval_effectiveness (disputed → weak consensus at 1) | communicate.so (1) and arxiv.org (1, found by the conflict search) vs twilio.com (2), whose excerpt describes Twilio's own product behaviour | Plausible. The dissent is a vendor describing its product (not detected as first-party, because this is an approach alternative with no official domains). It remains a rubric-level weak consensus, not verified truth. |
| Q5 static Managed:startup_cost (weak consensus at 1) | zilliz.com (1, "cheaper for low volume"), adaptiverecall.com (1, Qdrant Cloud $25–65/mo) vs dev.to (2, Weaviate Flex, about $45 minimum) | **Numerical threshold rather than real agreement.** The three families price *different* managed products under one approach-level alternative. The rules work as specified, but pooling different products is a limitation of approach-type plans. |
| Q5 v2_policy Self-hosted:operational_effort (weak consensus at 0) | theaidatabaseblog.com, devopsness.com (0) vs dev.to (1, "0.15 FTE") | Rubric interpretation; adjacent scores. Reasonable as a weak, disclosed consensus. |
| Q5 static Self-hosted:startup_cost (dimension mismatch) | $20–50/month VPS (recurring infrastructure, 1) vs $7–16k initial engineering build (labour, 0) | **Correct:** split, not pooled, not called a contradiction. |
| Q5 V3.1 Self-hosted:startup_cost (disputed within "recurring infrastructure") | c17.io "$9.99/month" (1) vs vecstore.app "infrastructure $530/month; **real cost** $3,530/month" (0, scored on total cost) | **Defect.** The keyword dimension detector labelled the vecstore excerpt as recurring infrastructure because "/month" matched, missing that the score reflects total cost of ownership ("real cost" is not in its TCO list). This created a false dispute. It errs conservatively (a dispute, not a false consensus), but it is a misclassification. |

On Q5 specifically, did research genuinely resolve disagreement, or just satisfy the threshold?
- **No resolution through research in Q5:** in this pilot no Q5 dispute was resolved by targeted research.
- **Where Q5 consensus came from:** both Q5 consensus cells (static, v2_policy) came from evidence gathered for other purposes. One of them, Managed:startup_cost, satisfies the 2:1 threshold across different products rather than reflecting agreement about one fact.
- **The one genuine resolution** was in Q4.

## 5. Defects and limitations found

1. **Cost-dimension heuristic gap (moderate, conservative direction).** Wording such as "real cost", "true cost" or "including engineering" is not recognised as total cost of ownership. Proposed fix (offline, before any benchmark): extend the TCO keyword list, add a regression test from this excerpt, and re-score this pilot offline to confirm only that cell changes.
2. **Approach-level alternatives pool different products** (limitation, not a code bug). A consensus over "managed vector databases" can mix prices of different services. It should be stated in reports; a plan change would need a new, versioned plan.
3. **Reachability discounting is untested live.** No candidate needed more than one source. The offline tests cover it; the benchmark may or may not exercise it.
4. **First-party detection misses vendors for approach alternatives.** For example, Twilio describing its own product counted as an ordinary independent family.

No semantic-verification defect was found. Rejection patterns are similar across arms, there were 0 invalid citations, and the verifier timeout was handled fail-closed.

## 6. Recommendation

**Technically justified, after one small offline fix.** All 8 pre-registered correctness criteria passed. The scoring fix behaves as specified live:
- no double counting;
- same-page conflicts labelled correctly;
- dimensions split;
- only reachable pins;
- conservative withholding.

Descriptively, V3.1 had the highest supported coverage (3/0/0 vs static, 2/0/1 vs the V2 policy). But n = 3, and target success was lower than static's, so this is not evidence of superiority.

Before the 18-pair benchmark (estimate $1.75–2.07, cap $2.50, separate authorization):
1. Fix the TCO keyword gap with a regression test and an offline re-score of this pilot. No spend; the benchmark then runs on the fixed code, and this pilot stays labelled pre-fix.
2. Add a report note that approach-level consensus may pool different products.
3. Keep "strict supported" as a co-primary reporting line, so consensus cannot inflate a result unnoticed.
