# Evaluation report V3.1: static vs adaptive vs v2_policy (live, paired, 1 repetition(s))

- Folder: `outputs/eval_v3.1_E_20261030T080154_a99d87` (protocol v3.1, mode record, started 2026-10-30T08:01:54+00:00, finished 2026-10-30T08:21:19+00:00)
- Config fingerprint `8b745878d6`: llm_provider=experiential, llm_model=gpt-6-luna, llm_base_url=https://api.experientiallabs.ai/v1, llm_structured_mode=json_schema, llm_temperature=0.0, llm_max_retries=2, exa_max_retries=2, max_search_calls=6, max_content_pages=12, max_research_rounds=3, max_no_progress=2, max_evidence_per_round=12, max_initial_queries=2, results_per_search=5, pages_per_search=2, max_llm_calls=None, max_seconds=None, protocol=v3.1
- Questions Q1, Q4, Q5; repetitions completed: [1]; arms: static, adaptive, v2_policy; spend cap: 0.4 USD; guard stop: not triggered
- Fixed plans (one per question, reused by every repetition and arm): Q1 `86d77f5966b533d0` from evaluations\v3\plans\Q1.json; Q4 `39b9ce6129bb70c8` from evaluations\v3\plans\Q4.json; Q5 `d8f8ebab8c004659` from evaluations\v3\plans\Q5.json
- Views: **common_stop** = trajectory prefix up to where the common stopping rule fires (same rule for every arm); **full_budget** = the whole run. Arms compared *within a view* measure target selection; common_stop vs full_budget *within an arm* measures stopping.
- Descriptive only: 1 repetition(s) per arm, no significance claims.

## Replay check

Offline replay `outputs/eval_v3.1_E_20261030T082133_ff0182`: **all 18 rows identical** (decisions and metrics; run id, timestamp and model label excluded). Replay is a reproducibility check, not an additional repetition.

## Results per question and repetition

| Q | rep | arm | view | supported | searches | pages | accepted / rejected | domains | stability | interval leader | recommendation | flips (strong) / status chg | stop | tokens | Exa $ | LLM $ | errors t/l | disputed / unknown / insufficient | kinds |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | 1 | static | common_stop | 6/9 | 5 | 10 | 7 / 7 | 3 | robust | Qdrant | withheld | 0 (0) / 1 | no_progress | 45526 | 0.045 | 0.010515 | 0/0 | 0 / 1 / 2 | static_schedule=3 |
| Q1 | 1 | static | full_budget | 6/9 | 5 | 10 | 7 / 7 | 3 | robust | Qdrant | withheld | 0 (0) / 1 | budget_exhausted | 45526 | 0.045 | 0.010515 | 0/0 | 0 / 1 / 2 | static_schedule=3 |
| Q1 | 1 | adaptive | common_stop | 7/9 | 5 | 10 | 9 / 6 | 4 | provisional | Qdrant | withheld | 0 (0) / 1 | budget_exhausted | 44973 | 0.045 | 0.010668 | 0/0 | 1 / 0 / 1 | targeted=3 |
| Q1 | 1 | adaptive | full_budget | 7/9 | 5 | 10 | 9 / 6 | 4 | provisional | Qdrant | withheld | 0 (0) / 1 | budget_exhausted | 44973 | 0.045 | 0.010668 | 0/0 | 1 / 0 / 1 | targeted=3 |
| Q1 | 1 | v2_policy | common_stop | 6/9 | 5 | 10 | 12 / 8 | 4 | provisional | Weaviate | withheld | 1 (0) / 0 | budget_exhausted | 51001 | 0.045 | 0.011816 | 0/0 | 2 / 0 / 1 | bounded_retry=1 targeted=2 |
| Q1 | 1 | v2_policy | full_budget | 6/9 | 5 | 10 | 12 / 8 | 4 | provisional | Weaviate | withheld | 1 (0) / 0 | budget_exhausted | 51001 | 0.045 | 0.011816 | 0/0 | 2 / 0 / 1 | bounded_retry=1 targeted=2 |
| Q4 | 1 | static | common_stop | 9/12 | 5 | 10 | 14 / 4 | 5 | provisional | Session-only memory | withheld | 0 (0) / 1 | budget_exhausted | 62753 | 0.044 | 0.014157 | 0/0 | 1 / 1 / 1 | static_schedule=3 |
| Q4 | 1 | static | full_budget | 9/12 | 5 | 10 | 14 / 4 | 5 | provisional | Session-only memory | withheld | 0 (0) / 1 | budget_exhausted | 62753 | 0.044 | 0.014157 | 0/0 | 1 / 1 / 1 | static_schedule=3 |
| Q4 | 1 | adaptive | common_stop | 10/12 | 5 | 10 | 13 / 3 | 4 | provisional | Session-only memory | withheld | 0 (0) / 1 | budget_exhausted | 56700 | 0.044 | 0.011791 | 0/0 | 0 / 0 / 2 | conflict_resolution=1 targeted=2 |
| Q4 | 1 | adaptive | full_budget | 10/12 | 5 | 10 | 13 / 3 | 4 | provisional | Session-only memory | withheld | 0 (0) / 1 | budget_exhausted | 56700 | 0.044 | 0.011791 | 0/0 | 0 / 0 / 2 | conflict_resolution=1 targeted=2 |
| Q4 | 1 | v2_policy | common_stop | 9/12 | 5 | 10 | 11 / 3 | 3 | provisional | Session-only memory | withheld | 0 (0) / 1 | budget_exhausted | 54415 | 0.044 | 0.010972 | 0/0 | 1 / 0 / 2 | bounded_retry=1 targeted=2 |
| Q4 | 1 | v2_policy | full_budget | 9/12 | 5 | 10 | 11 / 3 | 3 | provisional | Session-only memory | withheld | 0 (0) / 1 | budget_exhausted | 54415 | 0.044 | 0.010972 | 0/0 | 1 / 0 / 2 | bounded_retry=1 targeted=2 |
| Q5 | 1 | static | common_stop | 3/6 | 5 | 10 | 20 / 3 | 5 | provisional | Managed vector database | withheld | 0 (0) / 2 | budget_exhausted | 63307 | 0.045 | 0.014729 | 0/0 | 2 / 0 / 0 | static_schedule=3 |
| Q5 | 1 | static | full_budget | 3/6 | 5 | 10 | 20 / 3 | 5 | provisional | Managed vector database | withheld | 0 (0) / 2 | budget_exhausted | 63307 | 0.045 | 0.014729 | 0/0 | 2 / 0 / 0 | static_schedule=3 |
| Q5 | 1 | adaptive | common_stop | 5/6 | 5 | 10 | 15 / 7 | 6 | robust | Managed vector database | withheld | 0 (0) / 1 | budget_exhausted | 58710 | 0.045 | 0.013102 | 0/0 | 1 / 0 / 0 | corroboration=3 |
| Q5 | 1 | adaptive | full_budget | 5/6 | 5 | 10 | 15 / 7 | 6 | robust | Managed vector database | withheld | 0 (0) / 1 | budget_exhausted | 58710 | 0.045 | 0.013102 | 0/0 | 1 / 0 / 0 | corroboration=3 |
| Q5 | 1 | v2_policy | common_stop | 6/6 | 5 | 10 | 15 / 10 | 5 | robust | Managed vector database | withheld | 0 (0) / 1 | budget_exhausted | 62261 | 0.045 | 0.014634 | 0/3 | 0 / 0 / 0 | bounded_retry=1 corroboration=2 |
| Q5 | 1 | v2_policy | full_budget | 6/6 | 5 | 10 | 15 / 10 | 5 | robust | Managed vector database | withheld | 0 (0) / 1 | budget_exhausted | 62261 | 0.045 | 0.014634 | 0/3 | 0 / 0 / 0 | bounded_retry=1 corroboration=2 |

## Distribution across repetitions: median [min-max]

| Q | arm | view | coverage | units_supported | actions | accepted | rejected | relevant_retrieval_yield | distinct_domains | llm_tokens | exa_cost_usd | llm_cost_usd | units_disputed | units_unknown | units_insufficient | units_evidenced | high_confidence_cells | repeat_prev_target | failed_targeted_rounds |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | static | common_stop | 0.667 [0.667-0.667] | 6 [6-6] | 15 [15-15] | 7 [7-7] | 7 [7-7] | 0.4 [0.4-0.4] | 3 [3-3] | 45526 [45526-45526] | 0.045 [0.045-0.045] | 0.0105 [0.0105-0.0105] | 0 [0-0] | 1 [1-1] | 2 [2-2] | 6 [6-6] | 4 [4-4] | 0 [0-0] | 1 [1-1] |
| Q1 | static | full_budget | 0.667 [0.667-0.667] | 6 [6-6] | 15 [15-15] | 7 [7-7] | 7 [7-7] | 0.4 [0.4-0.4] | 3 [3-3] | 45526 [45526-45526] | 0.045 [0.045-0.045] | 0.0105 [0.0105-0.0105] | 0 [0-0] | 1 [1-1] | 2 [2-2] | 6 [6-6] | 4 [4-4] | 0 [0-0] | 1 [1-1] |
| Q1 | adaptive | common_stop | 0.778 [0.778-0.778] | 7 [7-7] | 15 [15-15] | 9 [9-9] | 6 [6-6] | 0.467 [0.467-0.467] | 4 [4-4] | 44973 [44973-44973] | 0.045 [0.045-0.045] | 0.0107 [0.0107-0.0107] | 1 [1-1] | 0 [0-0] | 1 [1-1] | 8 [8-8] | 5 [5-5] | 0 [0-0] | 1 [1-1] |
| Q1 | adaptive | full_budget | 0.778 [0.778-0.778] | 7 [7-7] | 15 [15-15] | 9 [9-9] | 6 [6-6] | 0.467 [0.467-0.467] | 4 [4-4] | 44973 [44973-44973] | 0.045 [0.045-0.045] | 0.0107 [0.0107-0.0107] | 1 [1-1] | 0 [0-0] | 1 [1-1] | 8 [8-8] | 5 [5-5] | 0 [0-0] | 1 [1-1] |
| Q1 | v2_policy | common_stop | 0.667 [0.667-0.667] | 6 [6-6] | 15 [15-15] | 12 [12-12] | 8 [8-8] | 0.4 [0.4-0.4] | 4 [4-4] | 51001 [51001-51001] | 0.045 [0.045-0.045] | 0.0118 [0.0118-0.0118] | 2 [2-2] | 0 [0-0] | 1 [1-1] | 8 [8-8] | 1 [1-1] | 1 [1-1] | 2 [2-2] |
| Q1 | v2_policy | full_budget | 0.667 [0.667-0.667] | 6 [6-6] | 15 [15-15] | 12 [12-12] | 8 [8-8] | 0.4 [0.4-0.4] | 4 [4-4] | 51001 [51001-51001] | 0.045 [0.045-0.045] | 0.0118 [0.0118-0.0118] | 2 [2-2] | 0 [0-0] | 1 [1-1] | 8 [8-8] | 1 [1-1] | 1 [1-1] | 2 [2-2] |
| Q4 | static | common_stop | 0.75 [0.75-0.75] | 9 [9-9] | 15 [15-15] | 14 [14-14] | 4 [4-4] | 0.6 [0.6-0.6] | 5 [5-5] | 62753 [62753-62753] | 0.044 [0.044-0.044] | 0.0142 [0.0142-0.0142] | 1 [1-1] | 1 [1-1] | 1 [1-1] | 10 [10-10] | 2 [2-2] | 0 [0-0] | 1 [1-1] |
| Q4 | static | full_budget | 0.75 [0.75-0.75] | 9 [9-9] | 15 [15-15] | 14 [14-14] | 4 [4-4] | 0.6 [0.6-0.6] | 5 [5-5] | 62753 [62753-62753] | 0.044 [0.044-0.044] | 0.0142 [0.0142-0.0142] | 1 [1-1] | 1 [1-1] | 1 [1-1] | 10 [10-10] | 2 [2-2] | 0 [0-0] | 1 [1-1] |
| Q4 | adaptive | common_stop | 0.833 [0.833-0.833] | 10 [10-10] | 15 [15-15] | 13 [13-13] | 3 [3-3] | 0.667 [0.667-0.667] | 4 [4-4] | 56700 [56700-56700] | 0.044 [0.044-0.044] | 0.0118 [0.0118-0.0118] | 0 [0-0] | 0 [0-0] | 2 [2-2] | 10 [10-10] | 1 [1-1] | 0 [0-0] | 2 [2-2] |
| Q4 | adaptive | full_budget | 0.833 [0.833-0.833] | 10 [10-10] | 15 [15-15] | 13 [13-13] | 3 [3-3] | 0.667 [0.667-0.667] | 4 [4-4] | 56700 [56700-56700] | 0.044 [0.044-0.044] | 0.0118 [0.0118-0.0118] | 0 [0-0] | 0 [0-0] | 2 [2-2] | 10 [10-10] | 1 [1-1] | 0 [0-0] | 2 [2-2] |
| Q4 | v2_policy | common_stop | 0.75 [0.75-0.75] | 9 [9-9] | 15 [15-15] | 11 [11-11] | 3 [3-3] | 0.6 [0.6-0.6] | 3 [3-3] | 54415 [54415-54415] | 0.044 [0.044-0.044] | 0.011 [0.011-0.011] | 1 [1-1] | 0 [0-0] | 2 [2-2] | 10 [10-10] | 0 [0-0] | 1 [1-1] | 3 [3-3] |
| Q4 | v2_policy | full_budget | 0.75 [0.75-0.75] | 9 [9-9] | 15 [15-15] | 11 [11-11] | 3 [3-3] | 0.6 [0.6-0.6] | 3 [3-3] | 54415 [54415-54415] | 0.044 [0.044-0.044] | 0.011 [0.011-0.011] | 1 [1-1] | 0 [0-0] | 2 [2-2] | 10 [10-10] | 0 [0-0] | 1 [1-1] | 3 [3-3] |
| Q5 | static | common_stop | 0.5 [0.5-0.5] | 3 [3-3] | 15 [15-15] | 20 [20-20] | 3 [3-3] | 0.2 [0.2-0.2] | 5 [5-5] | 63307 [63307-63307] | 0.045 [0.045-0.045] | 0.0147 [0.0147-0.0147] | 2 [2-2] | 0 [0-0] | 0 [0-0] | 6 [6-6] | 3 [3-3] | 0 [0-0] | 0 [0-0] |
| Q5 | static | full_budget | 0.5 [0.5-0.5] | 3 [3-3] | 15 [15-15] | 20 [20-20] | 3 [3-3] | 0.2 [0.2-0.2] | 5 [5-5] | 63307 [63307-63307] | 0.045 [0.045-0.045] | 0.0147 [0.0147-0.0147] | 2 [2-2] | 0 [0-0] | 0 [0-0] | 6 [6-6] | 3 [3-3] | 0 [0-0] | 0 [0-0] |
| Q5 | adaptive | common_stop | 0.833 [0.833-0.833] | 5 [5-5] | 15 [15-15] | 15 [15-15] | 7 [7-7] | 0.333 [0.333-0.333] | 6 [6-6] | 58710 [58710-58710] | 0.045 [0.045-0.045] | 0.0131 [0.0131-0.0131] | 1 [1-1] | 0 [0-0] | 0 [0-0] | 6 [6-6] | 3 [3-3] | 0 [0-0] | 1 [1-1] |
| Q5 | adaptive | full_budget | 0.833 [0.833-0.833] | 5 [5-5] | 15 [15-15] | 15 [15-15] | 7 [7-7] | 0.333 [0.333-0.333] | 6 [6-6] | 58710 [58710-58710] | 0.045 [0.045-0.045] | 0.0131 [0.0131-0.0131] | 1 [1-1] | 0 [0-0] | 0 [0-0] | 6 [6-6] | 3 [3-3] | 0 [0-0] | 1 [1-1] |
| Q5 | v2_policy | common_stop | 1 [1-1] | 6 [6-6] | 15 [15-15] | 15 [15-15] | 10 [10-10] | 0.4 [0.4-0.4] | 5 [5-5] | 62261 [62261-62261] | 0.045 [0.045-0.045] | 0.0146 [0.0146-0.0146] | 0 [0-0] | 0 [0-0] | 0 [0-0] | 6 [6-6] | 2 [2-2] | 1 [1-1] | 2 [2-2] |
| Q5 | v2_policy | full_budget | 1 [1-1] | 6 [6-6] | 15 [15-15] | 15 [15-15] | 10 [10-10] | 0.4 [0.4-0.4] | 5 [5-5] | 62261 [62261-62261] | 0.045 [0.045-0.045] | 0.0146 [0.0146-0.0146] | 0 [0-0] | 0 [0-0] | 0 [0-0] | 6 [6-6] | 2 [2-2] | 1 [1-1] | 2 [2-2] |

## Targeting value: static vs adaptive (same stopping rule)

Matched-actions compares coverage when each arm has spent no more than the other arm's common-stop actions, so neither arm gets credit just for spending more.

| Q | rep | common_stop outcome | supported static → adaptive | actions static → adaptive | matched-actions supported static vs arm (at ≤ k actions) | full_budget outcome | full supported static → arm |
|---|---|---|---|---|---|---|---|
| Q1 | 1 | adaptive better coverage | 6 → 7 | 15 → 15 | 6 vs 7 (k=15; used 15/15) | adaptive better coverage | 6 → 7 |
| Q4 | 1 | adaptive better coverage | 9 → 10 | 15 → 15 | 9 vs 10 (k=15; used 15/15) | adaptive better coverage | 9 → 10 |
| Q5 | 1 | adaptive better coverage | 3 → 5 | 15 → 15 | 3 vs 5 (k=15; used 15/15) | adaptive better coverage | 3 → 5 |

**Paired differences (adaptive − static), units supported:**
- common_stop: median +1 [+1 to +2]; 3 better / 0 equal / 0 worse
- full_budget: median +1 [+1 to +2]; 3 better / 0 equal / 0 worse
- matched actions: median +1 [+1 to +2]; 3 better / 0 equal / 0 worse
- full_budget units with verified evidence (supported + disputed): median +0 [+0 to +2]; 1 better / 2 equal / 0 worse

**Tally, common_stop view:** adaptive better coverage: 3 (Q1r1, Q4r1, Q5r1)

**Tally, full_budget view:** adaptive better coverage: 3 (Q1r1, Q4r1, Q5r1)


## Targeting value: static vs v2_policy (same stopping rule)

Matched-actions compares coverage when each arm has spent no more than the other arm's common-stop actions, so neither arm gets credit just for spending more.

| Q | rep | common_stop outcome | supported static → v2_policy | actions static → v2_policy | matched-actions supported static vs arm (at ≤ k actions) | full_budget outcome | full supported static → arm |
|---|---|---|---|---|---|---|---|
| Q1 | 1 | NO coverage benefit (equal, incomplete) | 6 → 6 | 15 → 15 | 6 vs 6 (k=15; used 15/15) | NO coverage benefit (equal, incomplete) | 6 → 6 |
| Q4 | 1 | NO coverage benefit (equal, incomplete) | 9 → 9 | 15 → 15 | 9 vs 9 (k=15; used 15/15) | NO coverage benefit (equal, incomplete) | 9 → 9 |
| Q5 | 1 | adaptive better coverage | 3 → 6 | 15 → 15 | 3 vs 6 (k=15; used 15/15) | adaptive better coverage | 3 → 6 |

**Paired differences (v2_policy − static), units supported:**
- common_stop: median +0 [+0 to +3]; 1 better / 2 equal / 0 worse
- full_budget: median +0 [+0 to +3]; 1 better / 2 equal / 0 worse
- matched actions: median +0 [+0 to +3]; 1 better / 2 equal / 0 worse
- full_budget units with verified evidence (supported + disputed): median +0 [+0 to +2]; 1 better / 2 equal / 0 worse

**Tally, common_stop view:** NO coverage benefit (equal, incomplete): 2 (Q1r1, Q4r1); adaptive better coverage: 1 (Q5r1)

**Tally, full_budget view:** NO coverage benefit (equal, incomplete): 2 (Q1r1, Q4r1); adaptive better coverage: 1 (Q5r1)

## Stopping value (common_stop vs full_budget, same trajectory)

| Q | rep | arm | stop rule fired | round | actions saved | coverage lost | premature? |
|---|---|---|---|---|---|---|---|
| Q1 | 1 | static | no_progress | 3 | 0 | 0 | no |
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
| units_supported | 18.0 | 22.0 | 21.0 | 18.0 | 22.0 | 21.0 |
| units_consensus | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| units_evidenced | 22.0 | 24.0 | 24.0 | 22.0 | 24.0 | 24.0 |
| units_disputed | 3.0 | 2.0 | 3.0 | 3.0 | 2.0 | 3.0 |
| units_unknown | 2.0 | 0.0 | 0.0 | 2.0 | 0.0 | 0.0 |
| units_insufficient | 3.0 | 3.0 | 3.0 | 3.0 | 3.0 | 3.0 |
| units_dimension_mismatch | 1.0 | 1.0 | 0.0 | 1.0 | 1.0 | 0.0 |
| source_inconsistent_cells | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 1.0 |
| units_total | 27.0 | 27.0 | 27.0 | 27.0 | 27.0 | 27.0 |
| high_confidence_cells | 9.0 | 9.0 | 3.0 | 9.0 | 9.0 | 3.0 |
| actions | 45.0 | 45.0 | 45.0 | 45.0 | 45.0 | 45.0 |
| accepted | 41.0 | 37.0 | 38.0 | 41.0 | 37.0 | 38.0 |
| rejected | 14.0 | 16.0 | 21.0 | 14.0 | 16.0 | 21.0 |
| distinct_domains | 13.0 | 14.0 | 12.0 | 13.0 | 14.0 | 12.0 |
| repeat_prev_target | 0.0 | 0.0 | 3.0 | 0.0 | 0.0 | 3.0 |
| failed_targeted_rounds | 2.0 | 4.0 | 7.0 | 2.0 | 4.0 | 7.0 |
| disputes_seen | 3.0 | 3.0 | 3.0 | 3.0 | 3.0 | 3.0 |
| disputes_resolved | 0.0 | 1.0 | 0.0 | 0.0 | 1.0 | 0.0 |
| consequential_disputes | 3.0 | 1.0 | 3.0 | 3.0 | 1.0 | 3.0 |
| consequential_disputes_resolved | 0.0 | 1.0 | 0.0 | 0.0 | 1.0 | 0.0 |
| readiness_changes | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| became_ready | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| flips | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 1.0 |
| strong_flips | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| tie_flips | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 1.0 |
| status_changes | 4.0 | 3.0 | 2.0 | 4.0 | 3.0 | 2.0 |
| provider_failure_rounds | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 1.0 |
| llm_tokens | 171586.0 | 160383.0 | 167677.0 | 171586.0 | 160383.0 | 167677.0 |
| exa_cost_usd | 0.134 | 0.134 | 0.134 | 0.134 | 0.134 | 0.134 |
| llm_cost_usd | 0.0394 | 0.0356 | 0.0374 | 0.0394 | 0.0356 | 0.0374 |
| tool_errors | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| llm_errors | 0.0 | 0.0 | 3.0 | 0.0 | 0.0 | 3.0 |

Ready recommendations (full_budget): static 0, adaptive 0, v2_policy 0.

Counted leader changes, preserved V2 definition (full_budget): Q1r1/v2_policy (tie-related). A *strong* flip replaces a real leader with a different real leader; tie-related changes move into or out of a tie.

## Recorded spend (each provider call counted once)

- Recorded calls: 113; Exa (provider-reported): $0.239; gateway `usage.cost`: $0.081668; total reported: $0.320668; tokens: 370894
- provider-reported values (Exa cost_dollars, gateway usage.cost); not an invoice. Each recorded call counted once.
- Per-arm figures above are attributed (the shared round 0 counts for every arm).

## Research actions and selection reasons

**Q1 r1 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Qdrant:deployment_fit` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Weaviate:filtering_capability` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Milvus:operational_effort` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- decision change round 1: became_robust Qdrant/undetermined → Qdrant/robust

**Q1 r1 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Qdrant:operational_effort` [targeted] score 10.0 flip-relevant: Researching Qdrant:operational_effort (weight 5) because it is unknown: could break the tie. Priority 5 x 2 x 2.00 (decision) x 1.00 (exploration) x 1.00 (retry) / 2 = 10.00.
- round 2 `Weaviate:operational_effort` [targeted] score 12.0 flip-relevant: Researching Weaviate:operational_effort (weight 5) because it is unknown: could change the leader. Priority 5 x 2 x 2.00 (decision) x 1.20 (exploration) x 1.00 (retry) / 2 = 12.00.
- round 3 `Milvus:operational_effort` [targeted] score 12.0 flip-relevant: Researching Milvus:operational_effort (weight 5) because it is unknown: could change the leader. Priority 5 x 2 x 2.00 (decision) x 1.20 (exploration) x 1.00 (retry) / 2 = 12.00.
- decision change round 1: stability_changed Qdrant/undetermined → Qdrant/provisional

**Q1 r1 v2_policy** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Milvus:operational_effort` [targeted] score 10.0 flip-relevant: Milvus:operational_effort is unknown (width 2, weight 5, flip-relevant x2); resolving it could change the leader. Already supported for Milvus: filtering_capability.
- round 2 `Milvus:operational_effort` [bounded_retry] score 10.0 flip-relevant: Milvus:operational_effort is insufficient (width 2, weight 5, flip-relevant x2); resolving it could change the leader. Already supported for Milvus: deployment_fit, filtering_capability. Retry with an open query.
- round 3 `Weaviate:operational_effort` [targeted] score 10.0 flip-relevant: Weaviate:operational_effort is unknown (width 2, weight 5, flip-relevant x2); resolving it could change the leader. Already supported for Weaviate: deployment_fit, filtering_capability.
- decision change round 2: leader_changed Qdrant/undetermined → Weaviate/provisional

**Q4 r1 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Session-only memory:retrieval_effectiveness` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Persistent conversation-log retrieval:privacy_protection` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Summarized customer-profile memory:retention_and_deletion_control` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- decision change round 0: stability_changed None/undetermined → Session-only memory/provisional

**Q4 r1 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Hybrid layered memory:privacy_protection` [targeted] score 4.5: Researching Hybrid layered memory:privacy_protection (weight 3) because it is insufficient: jointly matters: Hybrid layered memory overtakes Session-only memory needs a group of 2 cells. Priority 3 x 2 x 1.50 (decision) x 1.00 (exploration) x 1.00 (retry) / 2 = 4.50.
- round 2 `Hybrid layered memory:retention_and_deletion_control` [targeted] score 3.0: Researching Hybrid layered memory:retention_and_deletion_control (weight 3) because it is unknown: jointly matters: Hybrid layered memory overtakes Session-only memory needs a group of 2 cells. Priority 3 x 2 x 1.50 (decision) x 0.67 (exploration) x 1.00 (retry) / 2 = 3.00.
- round 3 `Summarized customer-profile memory:retrieval_effectiveness#conflict` [conflict_resolution] score 2.7: Researching Summarized customer-profile memory:retrieval_effectiveness (weight 3) because it is disputed (interval width 1): jointly matters: Session-only memory becomes interval-robust needs a group of 2 cells. Priority 3 x 1 x 1.50 (decision) x 1.20 (exploration) x 1.00 (retry) / 2 = 2.70.
- decision change round 0: stability_changed None/undetermined → Session-only memory/provisional

**Q4 r1 v2_policy** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Hybrid layered memory:privacy_protection` [targeted] score 3.0: Hybrid layered memory:privacy_protection is insufficient (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Hybrid layered memory: retrieval_effectiveness.
- round 2 `Hybrid layered memory:privacy_protection` [bounded_retry] score 3.0: Hybrid layered memory:privacy_protection is insufficient (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Hybrid layered memory: retrieval_effectiveness. Retry with an open query.
- round 3 `Hybrid layered memory:retention_and_deletion_control` [targeted] score 3.0: Hybrid layered memory:retention_and_deletion_control is unknown (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Hybrid layered memory: retrieval_effectiveness.
- decision change round 0: stability_changed None/undetermined → Session-only memory/provisional

**Q5 r1 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Managed vector database:operational_effort` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Self-hosted vector database:startup_cost` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Managed vector database:startup_cost` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- decision change round 0: became_robust None/undetermined → Managed vector database/robust
- decision change round 3: lost_robustness Managed vector database/robust → Managed vector database/provisional

**Q5 r1 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Managed vector database:operational_effort#corroborate` [corroboration] score 3.125: Researching Managed vector database:operational_effort (weight 5) because it is supported but blocks readiness: readiness blocker: Managed vector database:operational_effort has one source family or no official source. Priority 5 x 1 x 1.25 (decision) x 1.00 (exploration) x 1.00 (retry) / 2 = 3.12.
- round 2 `Self-hosted vector database:startup_cost#corroborate` [corroboration] score 2.3999: Researching Self-hosted vector database:startup_cost (weight 3) because it is supported but blocks readiness: readiness blocker: Self-hosted vector database:startup_cost has one source family or no official source. Priority 3 x 1 x 1.33 (decision) x 1.20 (exploration) x 1.00 (retry) / 2 = 2.40.
- round 3 `Self-hosted vector database:control_and_customization#corroborate` [corroboration] score 3.0: Researching Self-hosted vector database:control_and_customization (weight 3) because it is supported but blocks readiness: readiness blocker: Self-hosted vector database:control_and_customization has one source family or no official source. Priority 3 x 1 x 2.00 (decision) x 1.00 (exploration) x 1.00 (retry) / 2 = 3.00.
- decision change round 0: became_robust None/undetermined → Managed vector database/robust

**Q5 r1 v2_policy** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Managed vector database:operational_effort#corroborate` [corroboration] score 2.5: Interval winner is robust but the recommendation is withheld (single-source/weak support): corroborate Managed vector database:operational_effort (weight 5).
- round 2 `Managed vector database:startup_cost#corroborate` [corroboration] score 1.5: Interval winner is robust but the recommendation is withheld (single-source/weak support): corroborate Managed vector database:startup_cost (weight 3).
- round 3 `Managed vector database:startup_cost#corroborate` [bounded_retry] score 1.5: Interval winner is robust but the recommendation is withheld (single-source/weak support): corroborate Managed vector database:startup_cost (weight 3).
- decision change round 0: became_robust None/undetermined → Managed vector database/robust

