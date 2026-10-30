# Evaluation report V3: static vs adaptive vs v2_policy (live, paired, 1 repetition(s))

- Folder: `outputs/eval_v3_E_20261030T071515_43c018` (protocol v3, mode record, started 2026-10-30T07:15:15+00:00, finished 2026-10-30T07:35:01+00:00)
- Config fingerprint `9e1d809c0d`: llm_provider=experiential, llm_model=gpt-6-luna, llm_base_url=https://api.experientiallabs.ai/v1, llm_structured_mode=json_schema, llm_temperature=0.0, llm_max_retries=2, exa_max_retries=2, max_search_calls=6, max_content_pages=12, max_research_rounds=3, max_no_progress=2, max_evidence_per_round=12, max_initial_queries=2, results_per_search=5, pages_per_search=2, max_llm_calls=None, max_seconds=None, protocol=v3
- Questions Q1, Q4, Q5; repetitions completed: [1]; arms: static, adaptive, v2_policy; spend cap: 0.45 USD; guard stop: not triggered
- Fixed plans (one per question, reused by every repetition and arm): Q1 `86d77f5966b533d0` from evaluations\v3\plans\Q1.json; Q4 `39b9ce6129bb70c8` from evaluations\v3\plans\Q4.json; Q5 `d8f8ebab8c004659` from evaluations\v3\plans\Q5.json
- Views: **common_stop** = trajectory prefix up to where the common stopping rule fires (same rule for every arm); **full_budget** = the whole run. Arms compared *within a view* measure target selection; common_stop vs full_budget *within an arm* measures stopping.
- Descriptive only: 1 repetition(s) per arm, no significance claims.

## Replay check

Offline replay `outputs/eval_v3_E_20261030T073516_6e4e76`: **all 18 rows identical** (decisions and metrics; run id, timestamp and model label excluded). Replay is a reproducibility check, not an additional repetition.

## Results per question and repetition

| Q | rep | arm | view | supported | searches | pages | accepted / rejected | domains | stability | interval leader | recommendation | flips (strong) / status chg | stop | tokens | Exa $ | LLM $ | errors t/l | disputed / unknown / insufficient | kinds |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | 1 | static | common_stop | 5/9 | 5 | 10 | 12 / 4 | 5 | provisional | Qdrant | withheld | 1 (1) / 1 | budget_exhausted | 46385 | 0.045 | 0.010121 | 0/0 | 2 / 1 / 1 | static_schedule=3 |
| Q1 | 1 | static | full_budget | 5/9 | 5 | 10 | 12 / 4 | 5 | provisional | Qdrant | withheld | 1 (1) / 1 | budget_exhausted | 46385 | 0.045 | 0.010121 | 0/0 | 2 / 1 / 1 | static_schedule=3 |
| Q1 | 1 | adaptive | common_stop | 5/9 | 5 | 10 | 11 / 5 | 5 | provisional | Qdrant | withheld | 1 (1) / 1 | budget_exhausted | 45806 | 0.045 | 0.010402 | 0/0 | 2 / 1 / 1 | targeted=3 |
| Q1 | 1 | adaptive | full_budget | 5/9 | 5 | 10 | 11 / 5 | 5 | provisional | Qdrant | withheld | 1 (1) / 1 | budget_exhausted | 45806 | 0.045 | 0.010402 | 0/0 | 2 / 1 / 1 | targeted=3 |
| Q1 | 1 | v2_policy | common_stop | 4/9 | 5 | 10 | 12 / 5 | 5 | provisional | Milvus | withheld | 1 (1) / 1 | budget_exhausted | 46468 | 0.045 | 0.010524 | 0/0 | 3 / 0 / 2 | targeted=3 |
| Q1 | 1 | v2_policy | full_budget | 4/9 | 5 | 10 | 12 / 5 | 5 | provisional | Milvus | withheld | 1 (1) / 1 | budget_exhausted | 46468 | 0.045 | 0.010524 | 0/0 | 3 / 0 / 2 | targeted=3 |
| Q4 | 1 | static | common_stop | 8/12 | 5 | 10 | 11 / 8 | 4 | provisional | Summarized customer-profile memory | withheld | 0 (0) / 1 | budget_exhausted | 62447 | 0.045 | 0.013601 | 0/0 | 1 / 1 / 2 | static_schedule=3 |
| Q4 | 1 | static | full_budget | 8/12 | 5 | 10 | 11 / 8 | 4 | provisional | Summarized customer-profile memory | withheld | 0 (0) / 1 | budget_exhausted | 62447 | 0.045 | 0.013601 | 0/0 | 1 / 1 / 2 | static_schedule=3 |
| Q4 | 1 | adaptive | common_stop | 11/12 | 5 | 10 | 13 / 4 | 5 | provisional | Hybrid layered memory | withheld | 1 (1) / 1 | budget_exhausted | 55276 | 0.045 | 0.011829 | 0/0 | 1 / 0 / 0 | corroboration=1 targeted=2 |
| Q4 | 1 | adaptive | full_budget | 11/12 | 5 | 10 | 13 / 4 | 5 | provisional | Hybrid layered memory | withheld | 1 (1) / 1 | budget_exhausted | 55276 | 0.045 | 0.011829 | 0/0 | 1 / 0 / 0 | corroboration=1 targeted=2 |
| Q4 | 1 | v2_policy | common_stop | 11/12 | 5 | 10 | 14 / 5 | 5 | provisional | Hybrid layered memory | withheld | 1 (1) / 1 | budget_exhausted | 61976 | 0.045 | 0.013565 | 0/0 | 1 / 0 / 0 | targeted=3 |
| Q4 | 1 | v2_policy | full_budget | 11/12 | 5 | 10 | 14 / 5 | 5 | provisional | Hybrid layered memory | withheld | 1 (1) / 1 | budget_exhausted | 61976 | 0.045 | 0.013565 | 0/0 | 1 / 0 / 0 | targeted=3 |
| Q5 | 1 | static | common_stop | 3/6 | 5 | 10 | 16 / 5 | 6 | undetermined | Managed vector database | none | 0 (0) / 3 | budget_exhausted | 59710 | 0.045 | 0.013797 | 0/0 | 3 / 0 / 0 | static_schedule=3 |
| Q5 | 1 | static | full_budget | 3/6 | 5 | 10 | 16 / 5 | 6 | undetermined | Managed vector database | none | 0 (0) / 3 | budget_exhausted | 59710 | 0.045 | 0.013797 | 0/0 | 3 / 0 / 0 | static_schedule=3 |
| Q5 | 1 | adaptive | common_stop | 1/6 | 5 | 10 | 16 / 8 | 5 | provisional | Managed vector database | withheld | 0 (0) / 2 | budget_exhausted | 65167 | 0.045 | 0.015712 | 0/0 | 5 / 0 / 0 | conflict_resolution=1 corroboration=1 targeted=1 |
| Q5 | 1 | adaptive | full_budget | 1/6 | 5 | 10 | 16 / 8 | 5 | provisional | Managed vector database | withheld | 0 (0) / 2 | budget_exhausted | 65167 | 0.045 | 0.015712 | 0/0 | 5 / 0 / 0 | conflict_resolution=1 corroboration=1 targeted=1 |
| Q5 | 1 | v2_policy | common_stop | 2/6 | 5 | 10 | 19 / 6 | 6 | provisional | Managed vector database | withheld | 0 (0) / 2 | budget_exhausted | 64040 | 0.045 | 0.015081 | 0/0 | 4 / 0 / 0 | corroboration=1 targeted=2 |
| Q5 | 1 | v2_policy | full_budget | 2/6 | 5 | 10 | 19 / 6 | 6 | provisional | Managed vector database | withheld | 0 (0) / 2 | budget_exhausted | 64040 | 0.045 | 0.015081 | 0/0 | 4 / 0 / 0 | corroboration=1 targeted=2 |

## Distribution across repetitions: median [min-max]

| Q | arm | view | coverage | units_supported | actions | accepted | rejected | relevant_retrieval_yield | distinct_domains | llm_tokens | exa_cost_usd | llm_cost_usd | units_disputed | units_unknown | units_insufficient | units_evidenced | high_confidence_cells | repeat_prev_target | failed_targeted_rounds |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | static | common_stop | 0.556 [0.556-0.556] | 5 [5-5] | 15 [15-15] | 12 [12-12] | 4 [4-4] | 0.333 [0.333-0.333] | 5 [5-5] | 46385 [46385-46385] | 0.045 [0.045-0.045] | 0.0101 [0.0101-0.0101] | 2 [2-2] | 1 [1-1] | 1 [1-1] | 7 [7-7] | 4 [4-4] | 0 [0-0] | 0 [0-0] |
| Q1 | static | full_budget | 0.556 [0.556-0.556] | 5 [5-5] | 15 [15-15] | 12 [12-12] | 4 [4-4] | 0.333 [0.333-0.333] | 5 [5-5] | 46385 [46385-46385] | 0.045 [0.045-0.045] | 0.0101 [0.0101-0.0101] | 2 [2-2] | 1 [1-1] | 1 [1-1] | 7 [7-7] | 4 [4-4] | 0 [0-0] | 0 [0-0] |
| Q1 | adaptive | common_stop | 0.556 [0.556-0.556] | 5 [5-5] | 15 [15-15] | 11 [11-11] | 5 [5-5] | 0.333 [0.333-0.333] | 5 [5-5] | 45806 [45806-45806] | 0.045 [0.045-0.045] | 0.0104 [0.0104-0.0104] | 2 [2-2] | 1 [1-1] | 1 [1-1] | 7 [7-7] | 3 [3-3] | 0 [0-0] | 1 [1-1] |
| Q1 | adaptive | full_budget | 0.556 [0.556-0.556] | 5 [5-5] | 15 [15-15] | 11 [11-11] | 5 [5-5] | 0.333 [0.333-0.333] | 5 [5-5] | 45806 [45806-45806] | 0.045 [0.045-0.045] | 0.0104 [0.0104-0.0104] | 2 [2-2] | 1 [1-1] | 1 [1-1] | 7 [7-7] | 3 [3-3] | 0 [0-0] | 1 [1-1] |
| Q1 | v2_policy | common_stop | 0.444 [0.444-0.444] | 4 [4-4] | 15 [15-15] | 12 [12-12] | 5 [5-5] | 0.267 [0.267-0.267] | 5 [5-5] | 46468 [46468-46468] | 0.045 [0.045-0.045] | 0.0105 [0.0105-0.0105] | 3 [3-3] | 0 [0-0] | 2 [2-2] | 7 [7-7] | 3 [3-3] | 0 [0-0] | 1 [1-1] |
| Q1 | v2_policy | full_budget | 0.444 [0.444-0.444] | 4 [4-4] | 15 [15-15] | 12 [12-12] | 5 [5-5] | 0.267 [0.267-0.267] | 5 [5-5] | 46468 [46468-46468] | 0.045 [0.045-0.045] | 0.0105 [0.0105-0.0105] | 3 [3-3] | 0 [0-0] | 2 [2-2] | 7 [7-7] | 3 [3-3] | 0 [0-0] | 1 [1-1] |
| Q4 | static | common_stop | 0.667 [0.667-0.667] | 8 [8-8] | 15 [15-15] | 11 [11-11] | 8 [8-8] | 0.533 [0.533-0.533] | 4 [4-4] | 62447 [62447-62447] | 0.045 [0.045-0.045] | 0.0136 [0.0136-0.0136] | 1 [1-1] | 1 [1-1] | 2 [2-2] | 9 [9-9] | 0 [0-0] | 0 [0-0] | 1 [1-1] |
| Q4 | static | full_budget | 0.667 [0.667-0.667] | 8 [8-8] | 15 [15-15] | 11 [11-11] | 8 [8-8] | 0.533 [0.533-0.533] | 4 [4-4] | 62447 [62447-62447] | 0.045 [0.045-0.045] | 0.0136 [0.0136-0.0136] | 1 [1-1] | 1 [1-1] | 2 [2-2] | 9 [9-9] | 0 [0-0] | 0 [0-0] | 1 [1-1] |
| Q4 | adaptive | common_stop | 0.917 [0.917-0.917] | 11 [11-11] | 15 [15-15] | 13 [13-13] | 4 [4-4] | 0.733 [0.733-0.733] | 5 [5-5] | 55276 [55276-55276] | 0.045 [0.045-0.045] | 0.0118 [0.0118-0.0118] | 1 [1-1] | 0 [0-0] | 0 [0-0] | 12 [12-12] | 0 [0-0] | 0 [0-0] | 1 [1-1] |
| Q4 | adaptive | full_budget | 0.917 [0.917-0.917] | 11 [11-11] | 15 [15-15] | 13 [13-13] | 4 [4-4] | 0.733 [0.733-0.733] | 5 [5-5] | 55276 [55276-55276] | 0.045 [0.045-0.045] | 0.0118 [0.0118-0.0118] | 1 [1-1] | 0 [0-0] | 0 [0-0] | 12 [12-12] | 0 [0-0] | 0 [0-0] | 1 [1-1] |
| Q4 | v2_policy | common_stop | 0.917 [0.917-0.917] | 11 [11-11] | 15 [15-15] | 14 [14-14] | 5 [5-5] | 0.733 [0.733-0.733] | 5 [5-5] | 61976 [61976-61976] | 0.045 [0.045-0.045] | 0.0136 [0.0136-0.0136] | 1 [1-1] | 0 [0-0] | 0 [0-0] | 12 [12-12] | 0 [0-0] | 0 [0-0] | 0 [0-0] |
| Q4 | v2_policy | full_budget | 0.917 [0.917-0.917] | 11 [11-11] | 15 [15-15] | 14 [14-14] | 5 [5-5] | 0.733 [0.733-0.733] | 5 [5-5] | 61976 [61976-61976] | 0.045 [0.045-0.045] | 0.0136 [0.0136-0.0136] | 1 [1-1] | 0 [0-0] | 0 [0-0] | 12 [12-12] | 0 [0-0] | 0 [0-0] | 0 [0-0] |
| Q5 | static | common_stop | 0.5 [0.5-0.5] | 3 [3-3] | 15 [15-15] | 16 [16-16] | 5 [5-5] | 0.2 [0.2-0.2] | 6 [6-6] | 59710 [59710-59710] | 0.045 [0.045-0.045] | 0.0138 [0.0138-0.0138] | 3 [3-3] | 0 [0-0] | 0 [0-0] | 6 [6-6] | 2 [2-2] | 0 [0-0] | 0 [0-0] |
| Q5 | static | full_budget | 0.5 [0.5-0.5] | 3 [3-3] | 15 [15-15] | 16 [16-16] | 5 [5-5] | 0.2 [0.2-0.2] | 6 [6-6] | 59710 [59710-59710] | 0.045 [0.045-0.045] | 0.0138 [0.0138-0.0138] | 3 [3-3] | 0 [0-0] | 0 [0-0] | 6 [6-6] | 2 [2-2] | 0 [0-0] | 0 [0-0] |
| Q5 | adaptive | common_stop | 0.167 [0.167-0.167] | 1 [1-1] | 15 [15-15] | 16 [16-16] | 8 [8-8] | 0.067 [0.067-0.067] | 5 [5-5] | 65167 [65167-65167] | 0.045 [0.045-0.045] | 0.0157 [0.0157-0.0157] | 5 [5-5] | 0 [0-0] | 0 [0-0] | 6 [6-6] | 0 [0-0] | 0 [0-0] | 0 [0-0] |
| Q5 | adaptive | full_budget | 0.167 [0.167-0.167] | 1 [1-1] | 15 [15-15] | 16 [16-16] | 8 [8-8] | 0.067 [0.067-0.067] | 5 [5-5] | 65167 [65167-65167] | 0.045 [0.045-0.045] | 0.0157 [0.0157-0.0157] | 5 [5-5] | 0 [0-0] | 0 [0-0] | 6 [6-6] | 0 [0-0] | 0 [0-0] | 0 [0-0] |
| Q5 | v2_policy | common_stop | 0.333 [0.333-0.333] | 2 [2-2] | 15 [15-15] | 19 [19-19] | 6 [6-6] | 0.133 [0.133-0.133] | 6 [6-6] | 64040 [64040-64040] | 0.045 [0.045-0.045] | 0.0151 [0.0151-0.0151] | 4 [4-4] | 0 [0-0] | 0 [0-0] | 6 [6-6] | 2 [2-2] | 0 [0-0] | 0 [0-0] |
| Q5 | v2_policy | full_budget | 0.333 [0.333-0.333] | 2 [2-2] | 15 [15-15] | 19 [19-19] | 6 [6-6] | 0.133 [0.133-0.133] | 6 [6-6] | 64040 [64040-64040] | 0.045 [0.045-0.045] | 0.0151 [0.0151-0.0151] | 4 [4-4] | 0 [0-0] | 0 [0-0] | 6 [6-6] | 2 [2-2] | 0 [0-0] | 0 [0-0] |

## Targeting value: static vs adaptive (same stopping rule)

Matched-actions compares coverage when each arm has spent no more than the other arm's common-stop actions, so neither arm gets credit just for spending more.

| Q | rep | common_stop outcome | supported static → adaptive | actions static → adaptive | matched-actions supported static vs arm (at ≤ k actions) | full_budget outcome | full supported static → arm |
|---|---|---|---|---|---|---|---|
| Q1 | 1 | NO coverage benefit (equal, incomplete) | 5 → 5 | 15 → 15 | 5 vs 5 (k=15; used 15/15) | NO coverage benefit (equal, incomplete) | 5 → 5 |
| Q4 | 1 | adaptive better coverage | 8 → 11 | 15 → 15 | 8 vs 11 (k=15; used 15/15) | adaptive better coverage | 8 → 11 |
| Q5 | 1 | adaptive WORSE coverage | 3 → 1 | 15 → 15 | 3 vs 1 (k=15; used 15/15) | adaptive WORSE coverage | 3 → 1 |

**Paired differences (adaptive − static), units supported:**
- common_stop: median +0 [-2 to +3]; 1 better / 1 equal / 1 worse
- full_budget: median +0 [-2 to +3]; 1 better / 1 equal / 1 worse
- matched actions: median +0 [-2 to +3]; 1 better / 1 equal / 1 worse
- full_budget units with verified evidence (supported + disputed): median +0 [+0 to +3]; 1 better / 2 equal / 0 worse

**Tally, common_stop view:** NO coverage benefit (equal, incomplete): 1 (Q1r1); adaptive WORSE coverage: 1 (Q5r1); adaptive better coverage: 1 (Q4r1)

**Tally, full_budget view:** NO coverage benefit (equal, incomplete): 1 (Q1r1); adaptive WORSE coverage: 1 (Q5r1); adaptive better coverage: 1 (Q4r1)


## Targeting value: static vs v2_policy (same stopping rule)

Matched-actions compares coverage when each arm has spent no more than the other arm's common-stop actions, so neither arm gets credit just for spending more.

| Q | rep | common_stop outcome | supported static → v2_policy | actions static → v2_policy | matched-actions supported static vs arm (at ≤ k actions) | full_budget outcome | full supported static → arm |
|---|---|---|---|---|---|---|---|
| Q1 | 1 | adaptive WORSE coverage | 5 → 4 | 15 → 15 | 5 vs 4 (k=15; used 15/15) | adaptive WORSE coverage | 5 → 4 |
| Q4 | 1 | adaptive better coverage | 8 → 11 | 15 → 15 | 8 vs 11 (k=15; used 15/15) | adaptive better coverage | 8 → 11 |
| Q5 | 1 | adaptive WORSE coverage | 3 → 2 | 15 → 15 | 3 vs 2 (k=15; used 15/15) | adaptive WORSE coverage | 3 → 2 |

**Paired differences (v2_policy − static), units supported:**
- common_stop: median -1 [-1 to +3]; 1 better / 0 equal / 2 worse
- full_budget: median -1 [-1 to +3]; 1 better / 0 equal / 2 worse
- matched actions: median -1 [-1 to +3]; 1 better / 0 equal / 2 worse
- full_budget units with verified evidence (supported + disputed): median +0 [+0 to +3]; 1 better / 2 equal / 0 worse

**Tally, common_stop view:** adaptive WORSE coverage: 2 (Q1r1, Q5r1); adaptive better coverage: 1 (Q4r1)

**Tally, full_budget view:** adaptive WORSE coverage: 2 (Q1r1, Q5r1); adaptive better coverage: 1 (Q4r1)

## Stopping value (common_stop vs full_budget, same trajectory)

| Q | rep | arm | stop rule fired | round | actions saved | coverage lost | premature? |
|---|---|---|---|---|---|---|---|
| Q1 | 1 | static | budget_exhausted | 3 | 0 | 0 | no |
| Q1 | 1 | adaptive | budget_exhausted | 3 | 0 | 0 | no |
| Q1 | 1 | v2_policy | budget_exhausted | 3 | 0 | 0 | no |
| Q4 | 1 | static | budget_exhausted | 3 | 0 | 0 | no |
| Q4 | 1 | adaptive | budget_exhausted | 3 | 0 | 0 | no |
| Q4 | 1 | v2_policy | budget_exhausted | 3 | 0 | 0 | no |
| Q5 | 1 | static | budget_exhausted | 3 | 0 | 0 | no |
| Q5 | 1 | adaptive | budget_exhausted | 3 | 0 | 0 | no |
| Q5 | 1 | v2_policy | budget_exhausted | 3 | 0 | 0 | no |

Premature stops (the common rule stopped before units that the full budget later found): none

## Aggregate (sums over all questions and repetitions; descriptive)

| metric | static common | adaptive common | v2_policy common | static full | adaptive full | v2_policy full |
|---|---|---|---|---|---|---|
| units_supported | 16.0 | 17.0 | 17.0 | 16.0 | 17.0 | 17.0 |
| units_evidenced | 22.0 | 25.0 | 25.0 | 22.0 | 25.0 | 25.0 |
| units_disputed | 6.0 | 8.0 | 8.0 | 6.0 | 8.0 | 8.0 |
| units_unknown | 2.0 | 1.0 | 0.0 | 2.0 | 1.0 | 0.0 |
| units_insufficient | 3.0 | 1.0 | 2.0 | 3.0 | 1.0 | 2.0 |
| units_total | 27.0 | 27.0 | 27.0 | 27.0 | 27.0 | 27.0 |
| high_confidence_cells | 6.0 | 3.0 | 5.0 | 6.0 | 3.0 | 5.0 |
| actions | 45.0 | 45.0 | 45.0 | 45.0 | 45.0 | 45.0 |
| accepted | 39.0 | 40.0 | 45.0 | 39.0 | 40.0 | 45.0 |
| rejected | 17.0 | 17.0 | 16.0 | 17.0 | 17.0 | 16.0 |
| distinct_domains | 15.0 | 15.0 | 16.0 | 15.0 | 15.0 | 16.0 |
| repeat_prev_target | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| failed_targeted_rounds | 1.0 | 2.0 | 1.0 | 1.0 | 2.0 | 1.0 |
| disputes_seen | 6.0 | 8.0 | 8.0 | 6.0 | 8.0 | 8.0 |
| disputes_resolved | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| consequential_disputes | 6.0 | 8.0 | 7.0 | 6.0 | 8.0 | 7.0 |
| consequential_disputes_resolved | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| readiness_changes | 1.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 |
| became_ready | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| flips | 1.0 | 2.0 | 2.0 | 1.0 | 2.0 | 2.0 |
| strong_flips | 1.0 | 2.0 | 2.0 | 1.0 | 2.0 | 2.0 |
| tie_flips | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| status_changes | 5.0 | 4.0 | 4.0 | 5.0 | 4.0 | 4.0 |
| provider_failure_rounds | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| llm_tokens | 168542.0 | 166249.0 | 172484.0 | 168542.0 | 166249.0 | 172484.0 |
| exa_cost_usd | 0.135 | 0.135 | 0.135 | 0.135 | 0.135 | 0.135 |
| llm_cost_usd | 0.0375 | 0.0379 | 0.0392 | 0.0375 | 0.0379 | 0.0392 |
| tool_errors | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| llm_errors | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

Ready recommendations (full_budget): static 0, adaptive 0, v2_policy 0.

Counted leader changes, preserved V2 definition (full_budget): Q1r1/static (strong), Q1r1/adaptive (strong), Q1r1/v2_policy (strong), Q4r1/adaptive (strong), Q4r1/v2_policy (strong). A *strong* flip replaces a real leader with a different real leader; tie-related changes move into or out of a tie.

## Recorded spend (each provider call counted once)

- Recorded calls: 103; Exa (provider-reported): $0.209; gateway `usage.cost`: $0.078281; total reported: $0.287281; tokens: 349989
- provider-reported values (Exa cost_dollars, gateway usage.cost); not an invoice. Each recorded call counted once.
- Per-arm figures above are attributed (the shared round 0 counts for every arm).

## Research actions and selection reasons

**Q1 r1 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Qdrant:deployment_fit` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Weaviate:filtering_capability` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Milvus:operational_effort` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- decision change round 0: stability_changed None/undetermined → Weaviate/provisional
- decision change round 1: leader_changed Weaviate/provisional → Qdrant/provisional

**Q1 r1 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Qdrant:operational_effort` [targeted] score 10.0 flip-relevant: Researching Qdrant:operational_effort (weight 5) because it is unknown: could change the leader. Priority 5 x 2 x 2.00 (decision) x 1.00 (exploration) x 1.00 (retry) / 2 = 10.00.
- round 2 `Weaviate:operational_effort` [targeted] score 9.0: Researching Weaviate:operational_effort (weight 5) because it is unknown: jointly matters: Weaviate overtakes Qdrant needs a group of 2 cells. Priority 5 x 2 x 1.50 (decision) x 1.20 (exploration) x 1.00 (retry) / 2 = 9.00.
- round 3 `Milvus:operational_effort` [targeted] score 9.0: Researching Milvus:operational_effort (weight 5) because it is insufficient: jointly matters: Milvus overtakes Qdrant needs a group of 2 cells. Priority 5 x 2 x 1.50 (decision) x 1.20 (exploration) x 1.00 (retry) / 2 = 9.00.
- decision change round 0: stability_changed None/undetermined → Weaviate/provisional
- decision change round 1: leader_changed Weaviate/provisional → Qdrant/provisional

**Q1 r1 v2_policy** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Milvus:operational_effort` [targeted] score 10.0 flip-relevant: Milvus:operational_effort is insufficient (width 2, weight 5, flip-relevant x2); resolving it could change the leader. Already supported for Milvus: deployment_fit.
- round 2 `Qdrant:operational_effort` [targeted] score 10.0 flip-relevant: Qdrant:operational_effort is unknown (width 2, weight 5, flip-relevant x2); resolving it could change the leader. Already supported for Qdrant: deployment_fit, filtering_capability.
- round 3 `Weaviate:operational_effort` [targeted] score 10.0 flip-relevant: Weaviate:operational_effort is unknown (width 2, weight 5, flip-relevant x2); resolving it could change the leader. Already supported for Weaviate: filtering_capability.
- decision change round 0: stability_changed None/undetermined → Weaviate/provisional
- decision change round 1: leader_changed Weaviate/provisional → Milvus/provisional

**Q4 r1 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Session-only memory:retrieval_effectiveness` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Persistent conversation-log retrieval:privacy_protection` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Summarized customer-profile memory:retention_and_deletion_control` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- decision change round 0: stability_changed None/undetermined → Summarized customer-profile memory/provisional

**Q4 r1 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Persistent conversation-log retrieval:retrieval_effectiveness` [targeted] score 4.5: Researching Persistent conversation-log retrieval:retrieval_effectiveness (weight 3) because it is insufficient: jointly matters: Persistent conversation-log retrieval overtakes Summarized customer-profile memory needs a group of 2 cells. Priority 3 x 2 x 1.50 (decision) x 1.00 (exploration) x 1.00 (retry) / 2 = 4.50.
- round 2 `Summarized customer-profile memory:retention_and_deletion_control` [targeted] score 7.2 flip-relevant: Researching Summarized customer-profile memory:retention_and_deletion_control (weight 3) because it is unknown: could change the leader; could make the leader interval-robust. Priority 3 x 2 x 2.00 (decision) x 1.20 (exploration) x 1.00 (retry) / 2 = 7.20.
- round 3 `Session-only memory:retrieval_effectiveness#corroborate` [corroboration] score 2.25: Researching Session-only memory:retrieval_effectiveness (weight 3) because it is supported but blocks readiness: readiness blocker: Session-only memory:retrieval_effectiveness has one source family or no official source. Priority 3 x 1 x 1.25 (decision) x 1.20 (exploration) x 1.00 (retry) / 2 = 2.25.
- decision change round 0: stability_changed None/undetermined → Summarized customer-profile memory/provisional
- decision change round 1: leader_changed Summarized customer-profile memory/provisional → Hybrid layered memory/provisional

**Q4 r1 v2_policy** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Persistent conversation-log retrieval:retrieval_effectiveness` [targeted] score 6.0 flip-relevant: Persistent conversation-log retrieval:retrieval_effectiveness is insufficient (width 2, weight 3, flip-relevant x2); resolving it could change the leader. Already supported for Persistent conversation-log retrieval: privacy_protection, retention_and_deletion_control.
- round 2 `Summarized customer-profile memory:retention_and_deletion_control` [targeted] score 6.0 flip-relevant: Summarized customer-profile memory:retention_and_deletion_control is unknown (width 2, weight 3, flip-relevant x2); resolving it could change the leader. Already supported for Summarized customer-profile memory: privacy_protection.
- round 3 `Summarized customer-profile memory:retrieval_effectiveness` [targeted] score 3.0 flip-relevant: Summarized customer-profile memory:retrieval_effectiveness is disputed (width 1, weight 3, flip-relevant x2); resolving it could change the leader. Already supported for Summarized customer-profile memory: privacy_protection, retention_and_deletion_control.
- decision change round 0: stability_changed None/undetermined → Summarized customer-profile memory/provisional
- decision change round 1: leader_changed Summarized customer-profile memory/provisional → Hybrid layered memory/provisional

**Q5 r1 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Managed vector database:operational_effort` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Self-hosted vector database:startup_cost` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Managed vector database:startup_cost` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- decision change round 0: became_robust None/undetermined → Managed vector database/robust
- decision change round 1: lost_robustness Managed vector database/robust → Managed vector database/provisional
- decision change round 3: stability_changed Managed vector database/provisional → Managed vector database/undetermined

**Q5 r1 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Managed vector database:operational_effort#corroborate` [corroboration] score 3.125: Researching Managed vector database:operational_effort (weight 5) because it is supported but blocks readiness: readiness blocker: Managed vector database:operational_effort has one source family or no official source. Priority 5 x 1 x 1.25 (decision) x 1.00 (exploration) x 1.00 (retry) / 2 = 3.12.
- round 2 `Self-hosted vector database:startup_cost` [targeted] score 7.2 flip-relevant: Researching Self-hosted vector database:startup_cost (weight 3) because it is insufficient: could make the leader interval-robust. Priority 3 x 2 x 2.00 (decision) x 1.20 (exploration) x 1.00 (retry) / 2 = 7.20.
- round 3 `Self-hosted vector database:operational_effort#conflict` [conflict_resolution] score 3.3333 flip-relevant: Researching Self-hosted vector database:operational_effort (weight 5) because it is disputed (interval width 1): could make the leader interval-robust. Priority 5 x 1 x 2.00 (decision) x 0.67 (exploration) x 1.00 (retry) / 2 = 3.33.
- decision change round 0: became_robust None/undetermined → Managed vector database/robust
- decision change round 1: lost_robustness Managed vector database/robust → Managed vector database/provisional

**Q5 r1 v2_policy** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Managed vector database:operational_effort#corroborate` [corroboration] score 2.5: Interval winner is robust but the recommendation is withheld (single-source/weak support): corroborate Managed vector database:operational_effort (weight 5).
- round 2 `Managed vector database:startup_cost` [targeted] score 3.0: Managed vector database:startup_cost is insufficient (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Managed vector database: operational_effort.
- round 3 `Self-hosted vector database:operational_effort` [targeted] score 5.0 flip-relevant: Self-hosted vector database:operational_effort is disputed (width 1, weight 5, flip-relevant x2); resolving it could change the leader. Already supported for Self-hosted vector database: startup_cost.
- decision change round 0: became_robust None/undetermined → Managed vector database/robust
- decision change round 1: lost_robustness Managed vector database/robust → Managed vector database/provisional

