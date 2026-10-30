# V3 live evaluation: pre-registration and cost estimate

> Written **before** any V3 paid call (2026-10-30).
> **Authorization:** paid phases (pilot and benchmark) need explicit owner approval of the arms and the spending cap. None has been given yet; nothing below has been run.
> **Locking:** the definitions here are fixed before results exist. Any later change is reported as a deviation, never applied retroactively. V1 and V2 results are never rewritten.

## Fixed conditions (all arms)

| Item | Value |
|---|---|
| Questions | Pilot: Q1, Q4, Q5. Benchmark: Q1–Q5 and Q8 |
| Plans | One frozen plan per question: `evaluations/v3/plans/<Q>.json` (V2 repetition-1 plans regenerated offline; hashes in `PLANS.md`), reused by every repetition and arm |
| Budgets | MAX_SEARCH_CALLS=6, MAX_CONTENT_PAGES=12, PAGES_PER_SEARCH=2, MAX_RESEARCH_ROUNDS=3, MAX_NO_PROGRESS=2 (unchanged from V2) |
| Model / tools | `gpt-6-luna` (strict json_schema, temperature 0); Exa Search plus Get Contents |
| Pairing | Per repetition: same plan and same round 0 (hash-checked) for every arm; independent retrieval across repetitions (store `rep{k}`); separate state after round 0 |
| Shared by all arms | Query builder, verifier, scoring (V3 dispute rule), readiness rules, common stop rule, evaluation to full budget with `common_stop` and `full_budget` views |
| Only intended difference | Which target is researched next |
| Static baseline | Fixed diagonal round-robin with attempt-0 queries, exactly as in V2 |
| Snapshots | Protocol `v3` fingerprint; V2 recordings are not reused. Mixing old V2 recordings with new V3 retrieval is **not** a controlled comparison and will not be presented as one. |

## Arms

- `static`: the fair baseline.
- `adaptive`: the full V3 policy.
- `v2_policy`: the unchanged V2 targeting policy under the same V3 scoring and stopping. This is the **controlled** V2→V3 policy comparison.
- Optional ablations, one V3 component off each: `no_retry`, `no_decision`, `no_readiness`, `no_conflict`, `no_exploration`.

## Pilot (Phase 10): Q1, Q4, Q5 × 1 repetition

```
python -m pathfinder.cli evaluate --record --ids Q1,Q4,Q5 --repeat 1 --arms static,adaptive,v2_policy \
       --plans-dir evaluations/v3/plans --snapshots evaluations/snapshots_v3_pilot --max-usd 0.45
python -m pathfinder.cli evaluate --replay --ids Q1,Q4,Q5 --repeat 1 --arms static,adaptive,v2_policy \
       --plans-dir evaluations/v3/plans --snapshots evaluations/snapshots_v3_pilot
python -m pathfinder.eval_report <record_dir> --replay <replay_dir> --out evaluations/v3/pilot/EVALUATION_REPORT.md \
       --review-dir evaluations/v3/pilot/review
```

The pilot is for **bugs and confounds**, not for performance claims. It passes only if all of these hold:
- identical `round0_hash` and `plan_hash` across arms;
- replay reproduces every row;
- no crash or `error` stop;
- every action carries an `action_kind`, and no unlabelled repeats;
- 0 invalid cited evidence IDs;
- AI-provisional review of every accepted and rejected candidate finds no new systematic verification error.

Any fix after the pilot is documented and re-tested offline, and the pilot is labelled pre-fix.

## Benchmark (Phase 11): Q1–Q5 and Q8 × 3 repetitions = 18 paired repetitions

**Primary measures**, per question (median and range) and as paired differences across the 18 pairs (median, range, better/equal/worse):

1. **Supported coverage at matched actions**: adaptive − static, and adaptive − v2_policy. This is the primary efficiency and quality measure, because neither arm gets credit for spending more.
2. Supported coverage in the `full_budget` and `common_stop` views.
3. **Evidenced coverage** (supported + disputed) in `full_budget`. This guards against a policy "winning" by finding fewer contradicting sources.

**Secondary measures:**
- disputed, unknown and insufficient units;
- relevant evidence yield;
- distinct source domains;
- high-confidence cells;
- consequential disputes and how many were resolved;
- readiness changes and `became_ready`;
- counted flips (preserved V2 definition), with **strong flips** and tie-related changes reported separately;
- immediate repeats and failed targeted rounds;
- premature stops;
- tokens; Exa and gateway usage; provider-reported and estimated cost;
- errors.

**Decision rule, fixed now:**
- **Supported:** the claim "V3 targeting improved on static (or on V2)" is described as *supported by this benchmark* only if, at matched actions, the paired median difference in supported coverage is > 0 **and** better-pairs outnumber worse-pairs, **and** evidenced coverage does not point the other way.
- **Mixed:** otherwise the result is reported as "not supported" or "mixed".
- **No significance claims:** 18 pairs and 3 repetitions per question do not support significance testing.
- **Unfavourable results** are reported in full.

**Human review:** a representative subset will be marked for human review. The worksheet is generated blank, and no human scores are fabricated.

## Cost estimate (from the V2 recordings; provider-reported values plus an estimate for the gateway calls that reported $0)

| Component | Estimate |
|---|---|
| Exa search | $0.007 per call (133 V2 calls) |
| Exa contents | $0.001 per page |
| Gateway | about $0.21 per million tokens (rate of the priced calls) |
| One V2 two-arm pair (measured) | $0.084 (range across questions $0.079–$0.089) |
| Shared round 0 per pair | about $0.022 |
| Each extra arm | about $0.031 (upper bound about $0.035: 3 searches, 6 pages and about 7 LLM calls at most) |
| Planning | $0 (plans already frozen offline) |

| Run | Arms | Estimate | Suggested cap (`--max-usd`, guard uses the estimated total) |
|---|---|---|---|
| Pilot (3 pairs) | static, adaptive | $0.25 | $0.35 |
| Pilot (3 pairs) | + v2_policy | **$0.35** | **$0.45** |
| Benchmark (18 pairs) | static, adaptive | $1.51 | $1.85 |
| Benchmark (18 pairs) | + v2_policy (**recommended**) | **$2.07** | **$2.50** |
| Benchmark (18 pairs) | + v2_policy, no_retry, no_decision | $3.19 | $3.80 |
| Benchmark (18 pairs) | all 8 arms | $4.86 | $5.60 |

Further notes:
- **Stopping safely:** the spend guard stops before a pair whenever estimated spend plus the largest pair cost seen so far would exceed the cap. Results are saved after every pair.
- **Not an invoice:** provider-reported `usage.cost` is not an invoice. In V2, 130 of 276 gateway calls reported $0 despite using tokens, so the estimate includes them at the average priced rate.
