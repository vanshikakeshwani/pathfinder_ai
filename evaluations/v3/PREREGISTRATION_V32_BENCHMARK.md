# V3.2 three-arm benchmark: pre-registration (frozen 2026-10-30; NOT authorized, NOT run)

> Written before any v3.2 paid call. It supersedes nothing: the V3 and V3.1 pre-registrations and their pilot results stay as recorded. Any later change is reported as a deviation.

## Frozen protocol

| Item | Value |
|---|---|
| Protocol / fingerprint | `v3.2` (new snapshot folder; no earlier recording reused) |
| Questions | Q1, Q2, Q3, Q4, Q5, Q8 (`evaluations/queries.json`, required set) |
| Repetitions | 3 independent paired repetitions per question = 18 pairs |
| Arms | `static` (fixed diagonal round-robin, attempt-0 queries); `v2_policy` (unchanged V2 targeting, including V2 discovery behaviour); `adaptive` (V3.2) |
| Plans | `evaluations/v3/plans/<Q>.json`: one frozen plan per question, reused by every repetition and arm (hashes in `plans/PLANS.md`) |
| Shared by all arms | round 0 (hash-checked), budgets (6 searches, 12 pages, 2 pages per search, 3 rounds), query builder, extraction and verification prompts, v3.2 aggregation and readiness, common stop rule, evaluation to full budget with `common_stop` and `full_budget` views |
| Only intended difference | which target is researched next |

```
python -m pathfinder.cli evaluate --record --repeat 3 --arms static,v2_policy,adaptive \
       --plans-dir evaluations/v3/plans --snapshots evaluations/snapshots_v32_benchmark --max-usd 2.50
python -m pathfinder.cli evaluate --replay --repeat 3 --arms static,v2_policy,adaptive \
       --plans-dir evaluations/v3/plans --snapshots evaluations/snapshots_v32_benchmark
python -m pathfinder.eval_report <record_dir> --replay <replay_dir> --out evaluations/v3/benchmark_v32/EVALUATION_REPORT.md \
       --review-dir evaluations/v3/benchmark_v32/review
```

## Metrics (fixed now)

**Co-primary**, each reported per question (median and range) and as paired differences (adaptive − static, adaptive − v2_policy, v2_policy − static; median, range and better/equal/worse):
1. **Strictly supported coverage**: cells in state `supported` only.
2. **Total supported coverage**: supported + qualified consensus + scope-dependent, excluding dimension mismatches. Consensus counts are shown separately and are never described as verified truth.
3. Both at **matched actions** and at full budget, plus **evidenced coverage** (total + disputed).

**Secondary:**
- disputes by kind, and disputes resolved by research;
- heterogeneous and ambiguous-dimension cells;
- reachability classes of chosen targets;
- target success;
- immediate repeats;
- readiness changes, with ready recommendations and their reasons;
- strong vs tie-related flips;
- premature stops;
- source families;
- tokens; provider-reported and estimated cost;
- tool, model and provider-failure rounds.

**Decision rule:** "V3.2 targeting improved on X" is claimed only if, at matched actions, the paired median of **both** strictly supported and total supported coverage is > 0, better outnumbers worse for both, and evidenced coverage does not point the other way. Otherwise the result is "not supported" or "mixed". There are no significance claims (18 pairs).

**Integrity checks** (must pass, or the result is flagged):
- replay is identical;
- plan and round-0 hashes are identical across arms;
- 0 invalid citations;
- `audit_cell` is clean;
- no future-data leakage (V3 decisions rebuild from earlier rounds);
- no pin outside reachable values;
- spend ≤ cap.

## Cost (from the live pilots with these exact plans, budgets and arms)

| Source | Cost | Per question-repetition (3 arms) |
|---|---|---|
| V3 pilot (3 question-repetitions) | $0.287 | $0.096 |
| V3.1 pilot (3 question-repetitions) | $0.321 | $0.107 |

- **Benchmark:** 18 question-repetitions × $0.096–0.107 = **$1.72–1.93 provider-reported**. Discovery questions cost about the same per pair in V2 ($0.084 vs $0.083 per two-arm pair).
- **Margin:** the gateway reported $0 for 47% of calls in V2 (0% in both pilots). The spend guard counts such calls at the average priced rate.
- **Proposed cap: `--max-usd 2.50`** (estimated total). The guard stops before a pair if spent + the largest pair so far would exceed it, and results are saved after each pair.

## Known measurement weaknesses

- Large differences between repetitions (V2) mean 3 repetitions are descriptive only.
- Source families and cost dimensions use heuristics (domains, word patterns); product names use a capitalised-word heuristic, which is recorded for audit.
- The consensus thresholds are uncalibrated constants.
- The verifier is the same model family; there is no human review yet.
- Elapsed time is not comparable between arms.
- The approach-type plans (Q3–Q5) pool products under categories; heterogeneity is flagged, not resolved.
