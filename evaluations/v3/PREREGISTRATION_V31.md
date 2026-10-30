# V3.1 controlled pilot: pre-registration (proposal; NOT authorized, NOT run)

> Written 2026-10-30, after the offline v3.1 work and **before** any v3.1 paid call. The definitions below are fixed before results exist. The V3-pilot pre-registration (`PREREGISTRATION.md`) and its results stay unchanged.

## What changed since the V3 pilot

| Change | Scope |
|---|---|
| **Aggregation** (`V31_DISPUTE_AGGREGATION.md`): source families, internal inconsistency, cost-dimension and scope splitting, conservative qualified consensus (C1–C5), dispute kinds | all arms |
| **Readiness:** `weak_consensus` and `incomparable_dimensions` blockers; consensus cells count as differentiating | all arms |
| **Counterfactuals:** only reachable scores are pinned, factors are discounted by k, and unreachable disputes are valued 0.5 | adaptive arms (the `v3` policy); the stop rule's relevance test (all arms) |
| **Metrics:** v3.1 supported coverage excludes dimension-mismatch cells; consensus, dispute kinds, source-inconsistent cells and dimension mismatches are reported separately | reporting |
| **Protocol:** `v3.1`, with a new snapshot fingerprint; V3-pilot recordings are not reused | evaluation |

**Unchanged:**
- the frozen plans (`evaluations/v3/plans`, same hashes: no criterion was redefined; cost dimensions are split in aggregation, not by editing plans);
- the budgets (6 searches, 12 pages, 2 pages per search, 3 rounds);
- the static round-robin and its queries;
- the query builder, extraction and verification prompts;
- the shared round 0;
- the common stop rule (except the reachable-relevance test above).

## Proposed run (needs your authorization)

```
python -m pathfinder.cli evaluate --record --ids Q1,Q4,Q5 --repeat 1 --arms static,adaptive,v2_policy \
       --plans-dir evaluations/v3/plans --snapshots evaluations/snapshots_v31_pilot --max-usd 0.40
python -m pathfinder.cli evaluate --replay --ids Q1,Q4,Q5 --repeat 1 --arms static,adaptive,v2_policy \
       --plans-dir evaluations/v3/plans --snapshots evaluations/snapshots_v31_pilot
python -m pathfinder.eval_report <record_dir> --replay <replay_dir> --out evaluations/v3/pilot_v31/EVALUATION_REPORT.md \
       --review-dir evaluations/v3/pilot_v31/review
```

**Cost:**

| Run | Estimate | Proposed cap |
|---|---|---|
| Pilot | **$0.29** (the V3 pilot cost $0.287 with the same plans, arms and budgets; all calls priced) | **$0.40**, enforced on the estimated total |
| Benchmark (later, separately): 18 pairs × 3 arms | about $1.75 (pilot rate) to $2.07 (V2-based estimate, including unpriced calls) | $2.50 |

## Minimum success criteria for the pilot

The pilot checks **correctness and fairness**, not whether V3 wins. It passes only if all of these hold:
1. Recorded runs replay offline with all rows identical. Plan and round-0 hashes are identical across arms, and budgets are identical.
2. 0 invalid citation IDs; 0 future-data leakage (every V3 decision rebuilds from earlier-round evidence).
3. Every consensus or disputed cell carries a consensus record with its families. No family is counted twice (automated check `consensus.audit_cell` on every cell of every run: each excerpt in exactly one family, each document and publisher in exactly one family). Every dissent is retained in the record.
4. Same-document conflicts are labelled `source_inconsistent`, never `independent_disagreement`.
5. Cost evidence measuring different dimensions is never pooled. It shows `dimension_mismatch`, or separate dimension contexts.
6. Every adaptive conflict or corroboration action records `reach`. No action pins a score that `reachability` marks unreachable, and factors are discounted by k as specified.
7. No recommendation is `ready` while a weak consensus, unresolved leader dispute, incomparable dimension or comparability issue sits on a differentiating cell.
8. Spend ≤ $0.40.

If a criterion fails, the cause is fixed offline before any benchmark.

## Benchmark metrics (fixed now; the benchmark needs a separate authorization)

- **Primary:**
  - v3.1 supported coverage at matched actions (adaptive − static and adaptive − v2_policy; median, range and better/equal/worse over the pairs);
  - full-budget supported coverage;
  - evidenced coverage (supported + consensus + scope-dependent + disputed).
- **Guard against consensus inflation:** also report *strictly supported* coverage (state `supported` only) and consensus counts per arm. A V3 advantage that exists only through consensus cells is reported as such.
- **Secondary:**
  - disputes by kind;
  - disputes resolved by research (disputed → consensus or supported);
  - reachability classes of chosen targets;
  - readiness changes;
  - strong vs tie-related flips;
  - repeats and failed targets;
  - premature stops;
  - tokens; provider-reported and estimated cost;
  - errors.
- **Decision rule (unchanged from V3):** an improvement is claimed only if the paired median at matched actions is > 0, better outnumbers worse, and evidenced coverage does not point the other way. There are no significance claims.

## Remaining measurement weaknesses

- One repetition per question in the pilot.
- Large differences between repetitions (V2) mean the 3-repetition benchmark can only be descriptive.
- Family and cost-dimension detection are heuristic (domains and keywords).
- The consensus thresholds are uncalibrated policy constants.
- The verifier is the same model family; there is no human review yet.
- Elapsed time is not comparable between arms (cached round 0).
- Gateway `usage.cost` may again under-report.
