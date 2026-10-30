# Evaluation report V3.2: static vs v2_policy vs adaptive (live, paired, 1 repetition(s))

- Folder: `outputs/eval_v3.2_E_20261030T091146_fd68af` (protocol v3.2, mode replay, started 2026-10-30T09:11:46+00:00, finished 2026-10-30T09:11:47+00:00)
- Config fingerprint `6d056f2ad1`: llm_provider=experiential, llm_model=gpt-6-luna, llm_base_url=https://api.experientiallabs.ai/v1, llm_structured_mode=json_schema, llm_temperature=0.0, llm_max_retries=2, exa_max_retries=2, max_search_calls=6, max_content_pages=12, max_research_rounds=3, max_no_progress=2, max_evidence_per_round=12, max_initial_queries=2, results_per_search=5, pages_per_search=2, max_llm_calls=None, max_seconds=None, protocol=v3.2
- Questions Q1, Q2, Q3, Q4, Q5, Q8; repetitions completed: [1]; arms: static, v2_policy, adaptive; spend cap: None USD; guard stop: not triggered
- Fixed plans (one per question, reused by every repetition and arm): Q1 `86d77f5966b533d0` from evaluations\v3\plans\Q1.json; Q2 `e2dd8eb08eef0c34` from evaluations\v3\plans\Q2.json; Q3 `4ec777dd03d648be` from evaluations\v3\plans\Q3.json; Q4 `39b9ce6129bb70c8` from evaluations\v3\plans\Q4.json; Q5 `d8f8ebab8c004659` from evaluations\v3\plans\Q5.json; Q8 `f93cfd54aac04968` from evaluations\v3\plans\Q8.json
- Views: **common_stop** = trajectory prefix up to where the common stopping rule fires (same rule for every arm); **full_budget** = the whole run. Arms compared *within a view* measure target selection; common_stop vs full_budget *within an arm* measures stopping.
- Descriptive only: 1 repetition(s) per arm, no significance claims.

## Replay check

Offline replay `outputs/eval_v3.2_E_20261030T084005_cb1e8e`: **all 36 rows identical** (decisions and metrics; run id, timestamp and model label excluded). Replay is a reproducibility check, not an additional repetition.

## Results per question and repetition

| Q | rep | arm | view | supported | searches | pages | accepted / rejected | domains | stability | interval leader | recommendation | flips (strong) / status chg | stop | tokens | Exa $ | LLM $ | errors t/l | strict / consensus | disputed / unknown / insufficient | kinds |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | 1 | static | common_stop | 5/9 | 5 | 10 | 6 / 8 | 3 | provisional | Weaviate | withheld | 2 (2) / 1 | budget_exhausted | 45736 | 0.045 | 0.01057 | 0/0 | 4 / 0 | 0 / 1 / 3 | static_schedule=3 |
| Q1 | 1 | static | full_budget | 5/9 | 5 | 10 | 6 / 8 | 3 | provisional | Weaviate | withheld | 2 (2) / 1 | budget_exhausted | 45736 | 0.045 | 0.01057 | 0/0 | 4 / 0 | 0 / 1 / 3 | static_schedule=3 |
| Q1 | 1 | v2_policy | common_stop | 3/9 | 5 | 10 | 5 / 13 | 2 | provisional | Milvus | withheld | 1 (1) / 1 | budget_exhausted | 50170 | 0.045 | 0.011717 | 0/0 | 2 / 0 | 0 / 2 / 4 | bounded_retry=1 targeted=2 |
| Q1 | 1 | v2_policy | full_budget | 3/9 | 5 | 10 | 5 / 13 | 2 | provisional | Milvus | withheld | 1 (1) / 1 | budget_exhausted | 50170 | 0.045 | 0.011717 | 0/0 | 2 / 0 | 0 / 2 / 4 | bounded_retry=1 targeted=2 |
| Q1 | 1 | adaptive | common_stop | 3/9 | 5 | 10 | 4 / 9 | 2 | provisional | Milvus | withheld | 1 (1) / 1 | budget_exhausted | 44840 | 0.045 | 0.010355 | 0/0 | 2 / 0 | 0 / 2 / 4 | targeted=3 |
| Q1 | 1 | adaptive | full_budget | 3/9 | 5 | 10 | 4 / 9 | 2 | provisional | Milvus | withheld | 1 (1) / 1 | budget_exhausted | 44840 | 0.045 | 0.010355 | 0/0 | 2 / 0 | 0 / 2 / 4 | targeted=3 |
| Q2 | 1 | static | common_stop | 3/5 | 5 | 10 | 28 / 8 | 9 | n/a | - | not_applicable | 0 (0) / 0 | budget_exhausted | 51028 | 0.045 | 0.011194 | 0/0 |  /  |  /  /  | static_schedule=3 |
| Q2 | 1 | static | full_budget | 3/5 | 5 | 10 | 28 / 8 | 9 | n/a | - | not_applicable | 0 (0) / 0 | budget_exhausted | 51028 | 0.045 | 0.011194 | 0/0 |  /  |  /  /  | static_schedule=3 |
| Q2 | 1 | v2_policy | common_stop | 3/5 | 5 | 10 | 18 / 4 | 5 | n/a | - | not_applicable | 0 (0) / 0 | budget_exhausted | 38070 | 0.045 | 0.007967 | 0/0 |  /  |  /  /  | targeted=3 |
| Q2 | 1 | v2_policy | full_budget | 3/5 | 5 | 10 | 18 / 4 | 5 | n/a | - | not_applicable | 0 (0) / 0 | budget_exhausted | 38070 | 0.045 | 0.007967 | 0/0 |  /  |  /  /  | targeted=3 |
| Q2 | 1 | adaptive | common_stop | 3/5 | 5 | 10 | 18 / 4 | 5 | n/a | - | not_applicable | 0 (0) / 0 | budget_exhausted | 38070 | 0.045 | 0.007967 | 0/0 |  /  |  /  /  | targeted=3 |
| Q2 | 1 | adaptive | full_budget | 3/5 | 5 | 10 | 18 / 4 | 5 | n/a | - | not_applicable | 0 (0) / 0 | budget_exhausted | 38070 | 0.045 | 0.007967 | 0/0 |  /  |  /  /  | targeted=3 |
| Q3 | 1 | static | common_stop | 4/8 | 5 | 10 | 4 / 14 | 1 | provisional | Single-agent support automation | withheld | 0 (0) / 1 | budget_exhausted | 57621 | 0.045 | 0.012271 | 0/0 | 4 / 0 | 0 / 0 / 4 | static_schedule=3 |
| Q3 | 1 | static | full_budget | 4/8 | 5 | 10 | 4 / 14 | 1 | provisional | Single-agent support automation | withheld | 0 (0) / 1 | budget_exhausted | 57621 | 0.045 | 0.012271 | 0/0 | 4 / 0 | 0 / 0 / 4 | static_schedule=3 |
| Q3 | 1 | v2_policy | common_stop | 5/8 | 5 | 10 | 9 / 16 | 3 | provisional | Single-agent support automation | withheld | 0 (0) / 1 | budget_exhausted | 66171 | 0.045 | 0.01526 | 0/0 | 5 / 0 | 0 / 0 / 3 | bounded_retry=1 targeted=2 |
| Q3 | 1 | v2_policy | full_budget | 5/8 | 5 | 10 | 9 / 16 | 3 | provisional | Single-agent support automation | withheld | 0 (0) / 1 | budget_exhausted | 66171 | 0.045 | 0.01526 | 0/0 | 5 / 0 | 0 / 0 / 3 | bounded_retry=1 targeted=2 |
| Q3 | 1 | adaptive | common_stop | 7/8 | 5 | 10 | 17 / 12 | 4 | provisional | Single-agent support automation | withheld | 0 (0) / 1 | budget_exhausted | 67041 | 0.045 | 0.015378 | 0/0 | 7 / 0 | 1 / 0 / 0 | corroboration=1 targeted=2 |
| Q3 | 1 | adaptive | full_budget | 7/8 | 5 | 10 | 17 / 12 | 4 | provisional | Single-agent support automation | withheld | 0 (0) / 1 | budget_exhausted | 67041 | 0.045 | 0.015378 | 0/0 | 7 / 0 | 1 / 0 / 0 | corroboration=1 targeted=2 |
| Q4 | 1 | static | common_stop | 8/12 | 5 | 10 | 14 / 6 | 5 | provisional | Hybrid layered memory | withheld | 0 (0) / 1 | budget_exhausted | 66096 | 0.045 | 0.014834 | 0/0 | 8 / 0 | 1 / 1 / 2 | static_schedule=3 |
| Q4 | 1 | static | full_budget | 8/12 | 5 | 10 | 14 / 6 | 5 | provisional | Hybrid layered memory | withheld | 0 (0) / 1 | budget_exhausted | 66096 | 0.045 | 0.014834 | 0/0 | 8 / 0 | 1 / 1 / 2 | static_schedule=3 |
| Q4 | 1 | v2_policy | common_stop | 10/12 | 5 | 10 | 10 / 4 | 4 | provisional | Hybrid layered memory | withheld | 0 (0) / 1 | budget_exhausted | 50379 | 0.045 | 0.01057 | 0/0 | 10 / 0 | 0 / 0 / 2 | bounded_retry=1 targeted=2 |
| Q4 | 1 | v2_policy | full_budget | 10/12 | 5 | 10 | 10 / 4 | 4 | provisional | Hybrid layered memory | withheld | 0 (0) / 1 | budget_exhausted | 50379 | 0.045 | 0.01057 | 0/0 | 10 / 0 | 0 / 0 / 2 | bounded_retry=1 targeted=2 |
| Q4 | 1 | adaptive | common_stop | 10/12 | 5 | 10 | 10 / 5 | 4 | provisional | Hybrid layered memory | withheld | 0 (0) / 1 | budget_exhausted | 53475 | 0.045 | 0.011197 | 0/0 | 10 / 0 | 0 / 0 / 2 | targeted=3 |
| Q4 | 1 | adaptive | full_budget | 10/12 | 5 | 10 | 10 / 5 | 4 | provisional | Hybrid layered memory | withheld | 0 (0) / 1 | budget_exhausted | 53475 | 0.045 | 0.011197 | 0/0 | 10 / 0 | 0 / 0 / 2 | targeted=3 |
| Q5 | 1 | static | common_stop | 5/6 | 5 | 10 | 15 / 7 | 6 | robust | Managed vector database | withheld | 0 (0) / 1 | budget_exhausted | 57697 | 0.045 | 0.01272 | 0/0 | 3 / 2 | 1 / 0 / 0 | static_schedule=3 |
| Q5 | 1 | static | full_budget | 5/6 | 5 | 10 | 15 / 7 | 6 | robust | Managed vector database | withheld | 0 (0) / 1 | budget_exhausted | 57697 | 0.045 | 0.01272 | 0/0 | 3 / 2 | 1 / 0 / 0 | static_schedule=3 |
| Q5 | 1 | v2_policy | common_stop | 4/6 | 5 | 10 | 9 / 6 | 4 | robust | Managed vector database | withheld | 0 (0) / 1 | no_progress | 48476 | 0.045 | 0.0096 | 0/0 | 4 / 0 | 1 / 0 / 1 | bounded_retry=1 corroboration=2 |
| Q5 | 1 | v2_policy | full_budget | 4/6 | 5 | 10 | 9 / 6 | 4 | robust | Managed vector database | withheld | 0 (0) / 1 | budget_exhausted | 48476 | 0.045 | 0.0096 | 0/0 | 4 / 0 | 1 / 0 / 1 | bounded_retry=1 corroboration=2 |
| Q5 | 1 | adaptive | common_stop | 4/6 | 5 | 10 | 9 / 6 | 4 | robust | Managed vector database | withheld | 0 (0) / 1 | no_progress | 48059 | 0.045 | 0.010169 | 0/0 | 4 / 0 | 1 / 0 / 1 | conflict_resolution=1 corroboration=2 |
| Q5 | 1 | adaptive | full_budget | 4/6 | 5 | 10 | 9 / 6 | 4 | robust | Managed vector database | withheld | 0 (0) / 1 | budget_exhausted | 48059 | 0.045 | 0.010169 | 0/0 | 4 / 0 | 1 / 0 / 1 | conflict_resolution=1 corroboration=2 |
| Q8 | 1 | static | common_stop | 3/5 | 5 | 9 | 16 / 5 | 3 | n/a | - | not_applicable | 0 (0) / 0 | budget_exhausted | 38271 | 0.043 | 0.007182 | 0/0 |  /  |  /  /  | static_schedule=3 |
| Q8 | 1 | static | full_budget | 3/5 | 5 | 9 | 16 / 5 | 3 | n/a | - | not_applicable | 0 (0) / 0 | budget_exhausted | 38271 | 0.043 | 0.007182 | 0/0 |  /  |  /  /  | static_schedule=3 |
| Q8 | 1 | v2_policy | common_stop | 3/5 | 5 | 10 | 12 / 5 | 4 | n/a | - | not_applicable | 0 (0) / 0 | budget_exhausted | 35689 | 0.044 | 0.006642 | 0/0 |  /  |  /  /  | targeted=3 |
| Q8 | 1 | v2_policy | full_budget | 3/5 | 5 | 10 | 12 / 5 | 4 | n/a | - | not_applicable | 0 (0) / 0 | budget_exhausted | 35689 | 0.044 | 0.006642 | 0/0 |  /  |  /  /  | targeted=3 |
| Q8 | 1 | adaptive | common_stop | 5/5 | 5 | 10 | 22 / 2 | 3 | n/a | - | not_applicable | 0 (0) / 0 | stable | 41716 | 0.044 | 0.007938 | 0/0 |  /  |  /  /  | targeted=3 |
| Q8 | 1 | adaptive | full_budget | 5/5 | 5 | 10 | 22 / 2 | 3 | n/a | - | not_applicable | 0 (0) / 0 | budget_exhausted | 41716 | 0.044 | 0.007938 | 0/0 |  /  |  /  /  | targeted=3 |

## Distribution across repetitions: median [min-max]

| Q | arm | view | coverage | units_supported | actions | accepted | rejected | relevant_retrieval_yield | distinct_domains | llm_tokens | exa_cost_usd | llm_cost_usd | units_strict_supported | units_consensus | units_disputed | units_unknown | units_insufficient | units_evidenced | high_confidence_cells | repeat_prev_target | failed_targeted_rounds |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | static | common_stop | 0.556 [0.556-0.556] | 5 [5-5] | 15 [15-15] | 6 [6-6] | 8 [8-8] | 0.333 [0.333-0.333] | 3 [3-3] | 45736 [45736-45736] | 0.045 [0.045-0.045] | 0.0106 [0.0106-0.0106] | 4 [4-4] | 0 [0-0] | 0 [0-0] | 1 [1-1] | 3 [3-3] | 5 [5-5] | 5 [5-5] | 0 [0-0] | 1 [1-1] |
| Q1 | static | full_budget | 0.556 [0.556-0.556] | 5 [5-5] | 15 [15-15] | 6 [6-6] | 8 [8-8] | 0.333 [0.333-0.333] | 3 [3-3] | 45736 [45736-45736] | 0.045 [0.045-0.045] | 0.0106 [0.0106-0.0106] | 4 [4-4] | 0 [0-0] | 0 [0-0] | 1 [1-1] | 3 [3-3] | 5 [5-5] | 5 [5-5] | 0 [0-0] | 1 [1-1] |
| Q1 | v2_policy | common_stop | 0.333 [0.333-0.333] | 3 [3-3] | 15 [15-15] | 5 [5-5] | 13 [13-13] | 0.2 [0.2-0.2] | 2 [2-2] | 50170 [50170-50170] | 0.045 [0.045-0.045] | 0.0117 [0.0117-0.0117] | 2 [2-2] | 0 [0-0] | 0 [0-0] | 2 [2-2] | 4 [4-4] | 3 [3-3] | 3 [3-3] | 1 [1-1] | 2 [2-2] |
| Q1 | v2_policy | full_budget | 0.333 [0.333-0.333] | 3 [3-3] | 15 [15-15] | 5 [5-5] | 13 [13-13] | 0.2 [0.2-0.2] | 2 [2-2] | 50170 [50170-50170] | 0.045 [0.045-0.045] | 0.0117 [0.0117-0.0117] | 2 [2-2] | 0 [0-0] | 0 [0-0] | 2 [2-2] | 4 [4-4] | 3 [3-3] | 3 [3-3] | 1 [1-1] | 2 [2-2] |
| Q1 | adaptive | common_stop | 0.333 [0.333-0.333] | 3 [3-3] | 15 [15-15] | 4 [4-4] | 9 [9-9] | 0.2 [0.2-0.2] | 2 [2-2] | 44840 [44840-44840] | 0.045 [0.045-0.045] | 0.0104 [0.0104-0.0104] | 2 [2-2] | 0 [0-0] | 0 [0-0] | 2 [2-2] | 4 [4-4] | 3 [3-3] | 3 [3-3] | 0 [0-0] | 2 [2-2] |
| Q1 | adaptive | full_budget | 0.333 [0.333-0.333] | 3 [3-3] | 15 [15-15] | 4 [4-4] | 9 [9-9] | 0.2 [0.2-0.2] | 2 [2-2] | 44840 [44840-44840] | 0.045 [0.045-0.045] | 0.0104 [0.0104-0.0104] | 2 [2-2] | 0 [0-0] | 0 [0-0] | 2 [2-2] | 4 [4-4] | 3 [3-3] | 3 [3-3] | 0 [0-0] | 2 [2-2] |
| Q2 | static | common_stop | 0.6 [0.6-0.6] | 3 [3-3] | 15 [15-15] | 28 [28-28] | 8 [8-8] | 0.2 [0.2-0.2] | 9 [9-9] | 51028 [51028-51028] | 0.045 [0.045-0.045] | 0.0112 [0.0112-0.0112] | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0 [0-0] | 0 [0-0] |
| Q2 | static | full_budget | 0.6 [0.6-0.6] | 3 [3-3] | 15 [15-15] | 28 [28-28] | 8 [8-8] | 0.2 [0.2-0.2] | 9 [9-9] | 51028 [51028-51028] | 0.045 [0.045-0.045] | 0.0112 [0.0112-0.0112] | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0 [0-0] | 0 [0-0] |
| Q2 | v2_policy | common_stop | 0.6 [0.6-0.6] | 3 [3-3] | 15 [15-15] | 18 [18-18] | 4 [4-4] | 0.2 [0.2-0.2] | 5 [5-5] | 38070 [38070-38070] | 0.045 [0.045-0.045] | 0.00797 [0.00797-0.00797] | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0 [0-0] | 0 [0-0] |
| Q2 | v2_policy | full_budget | 0.6 [0.6-0.6] | 3 [3-3] | 15 [15-15] | 18 [18-18] | 4 [4-4] | 0.2 [0.2-0.2] | 5 [5-5] | 38070 [38070-38070] | 0.045 [0.045-0.045] | 0.00797 [0.00797-0.00797] | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0 [0-0] | 0 [0-0] |
| Q2 | adaptive | common_stop | 0.6 [0.6-0.6] | 3 [3-3] | 15 [15-15] | 18 [18-18] | 4 [4-4] | 0.2 [0.2-0.2] | 5 [5-5] | 38070 [38070-38070] | 0.045 [0.045-0.045] | 0.00797 [0.00797-0.00797] | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0 [0-0] | 0 [0-0] |
| Q2 | adaptive | full_budget | 0.6 [0.6-0.6] | 3 [3-3] | 15 [15-15] | 18 [18-18] | 4 [4-4] | 0.2 [0.2-0.2] | 5 [5-5] | 38070 [38070-38070] | 0.045 [0.045-0.045] | 0.00797 [0.00797-0.00797] | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0 [0-0] | 0 [0-0] |
| Q3 | static | common_stop | 0.5 [0.5-0.5] | 4 [4-4] | 15 [15-15] | 4 [4-4] | 14 [14-14] | 0.267 [0.267-0.267] | 1 [1-1] | 57621 [57621-57621] | 0.045 [0.045-0.045] | 0.0123 [0.0123-0.0123] | 4 [4-4] | 0 [0-0] | 0 [0-0] | 0 [0-0] | 4 [4-4] | 4 [4-4] | 0 [0-0] | 0 [0-0] | 3 [3-3] |
| Q3 | static | full_budget | 0.5 [0.5-0.5] | 4 [4-4] | 15 [15-15] | 4 [4-4] | 14 [14-14] | 0.267 [0.267-0.267] | 1 [1-1] | 57621 [57621-57621] | 0.045 [0.045-0.045] | 0.0123 [0.0123-0.0123] | 4 [4-4] | 0 [0-0] | 0 [0-0] | 0 [0-0] | 4 [4-4] | 4 [4-4] | 0 [0-0] | 0 [0-0] | 3 [3-3] |
| Q3 | v2_policy | common_stop | 0.625 [0.625-0.625] | 5 [5-5] | 15 [15-15] | 9 [9-9] | 16 [16-16] | 0.333 [0.333-0.333] | 3 [3-3] | 66171 [66171-66171] | 0.045 [0.045-0.045] | 0.0153 [0.0153-0.0153] | 5 [5-5] | 0 [0-0] | 0 [0-0] | 0 [0-0] | 3 [3-3] | 5 [5-5] | 1 [1-1] | 1 [1-1] | 3 [3-3] |
| Q3 | v2_policy | full_budget | 0.625 [0.625-0.625] | 5 [5-5] | 15 [15-15] | 9 [9-9] | 16 [16-16] | 0.333 [0.333-0.333] | 3 [3-3] | 66171 [66171-66171] | 0.045 [0.045-0.045] | 0.0153 [0.0153-0.0153] | 5 [5-5] | 0 [0-0] | 0 [0-0] | 0 [0-0] | 3 [3-3] | 5 [5-5] | 1 [1-1] | 1 [1-1] | 3 [3-3] |
| Q3 | adaptive | common_stop | 0.875 [0.875-0.875] | 7 [7-7] | 15 [15-15] | 17 [17-17] | 12 [12-12] | 0.467 [0.467-0.467] | 4 [4-4] | 67041 [67041-67041] | 0.045 [0.045-0.045] | 0.0154 [0.0154-0.0154] | 7 [7-7] | 0 [0-0] | 1 [1-1] | 0 [0-0] | 0 [0-0] | 8 [8-8] | 1 [1-1] | 0 [0-0] | 1 [1-1] |
| Q3 | adaptive | full_budget | 0.875 [0.875-0.875] | 7 [7-7] | 15 [15-15] | 17 [17-17] | 12 [12-12] | 0.467 [0.467-0.467] | 4 [4-4] | 67041 [67041-67041] | 0.045 [0.045-0.045] | 0.0154 [0.0154-0.0154] | 7 [7-7] | 0 [0-0] | 1 [1-1] | 0 [0-0] | 0 [0-0] | 8 [8-8] | 1 [1-1] | 0 [0-0] | 1 [1-1] |
| Q4 | static | common_stop | 0.667 [0.667-0.667] | 8 [8-8] | 15 [15-15] | 14 [14-14] | 6 [6-6] | 0.533 [0.533-0.533] | 5 [5-5] | 66096 [66096-66096] | 0.045 [0.045-0.045] | 0.0148 [0.0148-0.0148] | 8 [8-8] | 0 [0-0] | 1 [1-1] | 1 [1-1] | 2 [2-2] | 9 [9-9] | 3 [3-3] | 0 [0-0] | 1 [1-1] |
| Q4 | static | full_budget | 0.667 [0.667-0.667] | 8 [8-8] | 15 [15-15] | 14 [14-14] | 6 [6-6] | 0.533 [0.533-0.533] | 5 [5-5] | 66096 [66096-66096] | 0.045 [0.045-0.045] | 0.0148 [0.0148-0.0148] | 8 [8-8] | 0 [0-0] | 1 [1-1] | 1 [1-1] | 2 [2-2] | 9 [9-9] | 3 [3-3] | 0 [0-0] | 1 [1-1] |
| Q4 | v2_policy | common_stop | 0.833 [0.833-0.833] | 10 [10-10] | 15 [15-15] | 10 [10-10] | 4 [4-4] | 0.667 [0.667-0.667] | 4 [4-4] | 50379 [50379-50379] | 0.045 [0.045-0.045] | 0.0106 [0.0106-0.0106] | 10 [10-10] | 0 [0-0] | 0 [0-0] | 0 [0-0] | 2 [2-2] | 10 [10-10] | 0 [0-0] | 1 [1-1] | 2 [2-2] |
| Q4 | v2_policy | full_budget | 0.833 [0.833-0.833] | 10 [10-10] | 15 [15-15] | 10 [10-10] | 4 [4-4] | 0.667 [0.667-0.667] | 4 [4-4] | 50379 [50379-50379] | 0.045 [0.045-0.045] | 0.0106 [0.0106-0.0106] | 10 [10-10] | 0 [0-0] | 0 [0-0] | 0 [0-0] | 2 [2-2] | 10 [10-10] | 0 [0-0] | 1 [1-1] | 2 [2-2] |
| Q4 | adaptive | common_stop | 0.833 [0.833-0.833] | 10 [10-10] | 15 [15-15] | 10 [10-10] | 5 [5-5] | 0.667 [0.667-0.667] | 4 [4-4] | 53475 [53475-53475] | 0.045 [0.045-0.045] | 0.0112 [0.0112-0.0112] | 10 [10-10] | 0 [0-0] | 0 [0-0] | 0 [0-0] | 2 [2-2] | 10 [10-10] | 0 [0-0] | 0 [0-0] | 2 [2-2] |
| Q4 | adaptive | full_budget | 0.833 [0.833-0.833] | 10 [10-10] | 15 [15-15] | 10 [10-10] | 5 [5-5] | 0.667 [0.667-0.667] | 4 [4-4] | 53475 [53475-53475] | 0.045 [0.045-0.045] | 0.0112 [0.0112-0.0112] | 10 [10-10] | 0 [0-0] | 0 [0-0] | 0 [0-0] | 2 [2-2] | 10 [10-10] | 0 [0-0] | 0 [0-0] | 2 [2-2] |
| Q5 | static | common_stop | 0.833 [0.833-0.833] | 5 [5-5] | 15 [15-15] | 15 [15-15] | 7 [7-7] | 0.333 [0.333-0.333] | 6 [6-6] | 57697 [57697-57697] | 0.045 [0.045-0.045] | 0.0127 [0.0127-0.0127] | 3 [3-3] | 2 [2-2] | 1 [1-1] | 0 [0-0] | 0 [0-0] | 6 [6-6] | 2 [2-2] | 0 [0-0] | 1 [1-1] |
| Q5 | static | full_budget | 0.833 [0.833-0.833] | 5 [5-5] | 15 [15-15] | 15 [15-15] | 7 [7-7] | 0.333 [0.333-0.333] | 6 [6-6] | 57697 [57697-57697] | 0.045 [0.045-0.045] | 0.0127 [0.0127-0.0127] | 3 [3-3] | 2 [2-2] | 1 [1-1] | 0 [0-0] | 0 [0-0] | 6 [6-6] | 2 [2-2] | 0 [0-0] | 1 [1-1] |
| Q5 | v2_policy | common_stop | 0.667 [0.667-0.667] | 4 [4-4] | 15 [15-15] | 9 [9-9] | 6 [6-6] | 0.267 [0.267-0.267] | 4 [4-4] | 48476 [48476-48476] | 0.045 [0.045-0.045] | 0.0096 [0.0096-0.0096] | 4 [4-4] | 0 [0-0] | 1 [1-1] | 0 [0-0] | 1 [1-1] | 5 [5-5] | 1 [1-1] | 1 [1-1] | 2 [2-2] |
| Q5 | v2_policy | full_budget | 0.667 [0.667-0.667] | 4 [4-4] | 15 [15-15] | 9 [9-9] | 6 [6-6] | 0.267 [0.267-0.267] | 4 [4-4] | 48476 [48476-48476] | 0.045 [0.045-0.045] | 0.0096 [0.0096-0.0096] | 4 [4-4] | 0 [0-0] | 1 [1-1] | 0 [0-0] | 1 [1-1] | 5 [5-5] | 1 [1-1] | 1 [1-1] | 2 [2-2] |
| Q5 | adaptive | common_stop | 0.667 [0.667-0.667] | 4 [4-4] | 15 [15-15] | 9 [9-9] | 6 [6-6] | 0.267 [0.267-0.267] | 4 [4-4] | 48059 [48059-48059] | 0.045 [0.045-0.045] | 0.0102 [0.0102-0.0102] | 4 [4-4] | 0 [0-0] | 1 [1-1] | 0 [0-0] | 1 [1-1] | 5 [5-5] | 1 [1-1] | 0 [0-0] | 2 [2-2] |
| Q5 | adaptive | full_budget | 0.667 [0.667-0.667] | 4 [4-4] | 15 [15-15] | 9 [9-9] | 6 [6-6] | 0.267 [0.267-0.267] | 4 [4-4] | 48059 [48059-48059] | 0.045 [0.045-0.045] | 0.0102 [0.0102-0.0102] | 4 [4-4] | 0 [0-0] | 1 [1-1] | 0 [0-0] | 1 [1-1] | 5 [5-5] | 1 [1-1] | 0 [0-0] | 2 [2-2] |
| Q8 | static | common_stop | 0.6 [0.6-0.6] | 3 [3-3] | 14 [14-14] | 16 [16-16] | 5 [5-5] | 0.214 [0.214-0.214] | 3 [3-3] | 38271 [38271-38271] | 0.043 [0.043-0.043] | 0.00718 [0.00718-0.00718] | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0 [0-0] | 0 [0-0] |
| Q8 | static | full_budget | 0.6 [0.6-0.6] | 3 [3-3] | 14 [14-14] | 16 [16-16] | 5 [5-5] | 0.214 [0.214-0.214] | 3 [3-3] | 38271 [38271-38271] | 0.043 [0.043-0.043] | 0.00718 [0.00718-0.00718] | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0 [0-0] | 0 [0-0] |
| Q8 | v2_policy | common_stop | 0.6 [0.6-0.6] | 3 [3-3] | 15 [15-15] | 12 [12-12] | 5 [5-5] | 0.2 [0.2-0.2] | 4 [4-4] | 35689 [35689-35689] | 0.044 [0.044-0.044] | 0.00664 [0.00664-0.00664] | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0 [0-0] | 0 [0-0] |
| Q8 | v2_policy | full_budget | 0.6 [0.6-0.6] | 3 [3-3] | 15 [15-15] | 12 [12-12] | 5 [5-5] | 0.2 [0.2-0.2] | 4 [4-4] | 35689 [35689-35689] | 0.044 [0.044-0.044] | 0.00664 [0.00664-0.00664] | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0 [0-0] | 0 [0-0] |
| Q8 | adaptive | common_stop | 1 [1-1] | 5 [5-5] | 15 [15-15] | 22 [22-22] | 2 [2-2] | 0.333 [0.333-0.333] | 3 [3-3] | 41716 [41716-41716] | 0.044 [0.044-0.044] | 0.00794 [0.00794-0.00794] | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0 [0-0] | 0 [0-0] |
| Q8 | adaptive | full_budget | 1 [1-1] | 5 [5-5] | 15 [15-15] | 22 [22-22] | 2 [2-2] | 0.333 [0.333-0.333] | 3 [3-3] | 41716 [41716-41716] | 0.044 [0.044-0.044] | 0.00794 [0.00794-0.00794] | n/a | n/a | n/a | n/a | n/a | n/a | n/a | 0 [0-0] | 0 [0-0] |

## Targeting value: static vs v2_policy (same stopping rule)

Matched-actions compares coverage when each arm has spent no more than the other arm's common-stop actions, so neither arm gets credit just for spending more.

| Q | rep | common_stop outcome | supported static → v2_policy | actions static → v2_policy | matched-actions supported static vs arm (at ≤ k actions) | full_budget outcome | full supported static → arm |
|---|---|---|---|---|---|---|---|
| Q1 | 1 | adaptive WORSE coverage | 5 → 3 | 15 → 15 | 5 vs 3 (k=15; used 15/15) | adaptive WORSE coverage | 5 → 3 |
| Q2 | 1 | NO coverage benefit (equal, incomplete) | 3 → 3 | 15 → 15 | 3 vs 3 (k=15; used 15/15) | NO coverage benefit (equal, incomplete) | 3 → 3 |
| Q3 | 1 | adaptive better coverage | 4 → 5 | 15 → 15 | 4 vs 5 (k=15; used 15/15) | adaptive better coverage | 4 → 5 |
| Q4 | 1 | adaptive better coverage | 8 → 10 | 15 → 15 | 8 vs 10 (k=15; used 15/15) | adaptive better coverage | 8 → 10 |
| Q5 | 1 | adaptive WORSE coverage | 5 → 4 | 15 → 15 | 5 vs 4 (k=15; used 15/15) | adaptive WORSE coverage | 5 → 4 |
| Q8 | 1 | NO coverage benefit (equal, incomplete); adaptive MORE actions | 3 → 3 | 14 → 15 | 3 vs 3 (k=14; used 14/12) | NO coverage benefit (equal, incomplete); adaptive MORE actions | 3 → 3 |

**Paired differences (v2_policy − static), units supported:**
- common_stop: median +0 [-2 to +2]; 2 better / 2 equal / 2 worse
- full_budget: median +0 [-2 to +2]; 2 better / 2 equal / 2 worse
- matched actions: median +0 [-2 to +2]; 2 better / 2 equal / 2 worse
- full_budget units with verified evidence (supported + disputed): median +0 [-2 to +1]; 2 better / 0 equal / 2 worse
- full_budget STRICTLY supported units (no consensus, no scope split): median +1 [-2 to +2]; 3 better / 0 equal / 1 worse

**Tally, common_stop view:** NO coverage benefit (equal, incomplete): 1 (Q2r1); NO coverage benefit (equal, incomplete); adaptive MORE actions: 1 (Q8r1); adaptive WORSE coverage: 2 (Q1r1, Q5r1); adaptive better coverage: 2 (Q3r1, Q4r1)

**Tally, full_budget view:** NO coverage benefit (equal, incomplete): 1 (Q2r1); NO coverage benefit (equal, incomplete); adaptive MORE actions: 1 (Q8r1); adaptive WORSE coverage: 2 (Q1r1, Q5r1); adaptive better coverage: 2 (Q3r1, Q4r1)


## Targeting value: static vs adaptive (same stopping rule)

Matched-actions compares coverage when each arm has spent no more than the other arm's common-stop actions, so neither arm gets credit just for spending more.

| Q | rep | common_stop outcome | supported static → adaptive | actions static → adaptive | matched-actions supported static vs arm (at ≤ k actions) | full_budget outcome | full supported static → arm |
|---|---|---|---|---|---|---|---|
| Q1 | 1 | adaptive WORSE coverage | 5 → 3 | 15 → 15 | 5 vs 3 (k=15; used 15/15) | adaptive WORSE coverage | 5 → 3 |
| Q2 | 1 | NO coverage benefit (equal, incomplete) | 3 → 3 | 15 → 15 | 3 vs 3 (k=15; used 15/15) | NO coverage benefit (equal, incomplete) | 3 → 3 |
| Q3 | 1 | adaptive better coverage | 4 → 7 | 15 → 15 | 4 vs 7 (k=15; used 15/15) | adaptive better coverage | 4 → 7 |
| Q4 | 1 | adaptive better coverage | 8 → 10 | 15 → 15 | 8 vs 10 (k=15; used 15/15) | adaptive better coverage | 8 → 10 |
| Q5 | 1 | adaptive WORSE coverage | 5 → 4 | 15 → 15 | 5 vs 4 (k=15; used 15/15) | adaptive WORSE coverage | 5 → 4 |
| Q8 | 1 | adaptive better coverage | 3 → 5 | 14 → 15 | 3 vs 3 (k=14; used 14/12) | adaptive better coverage | 3 → 5 |

**Paired differences (adaptive − static), units supported:**
- common_stop: median +1 [-2 to +3]; 3 better / 1 equal / 2 worse
- full_budget: median +1 [-2 to +3]; 3 better / 1 equal / 2 worse
- matched actions: median +0 [-2 to +3]; 2 better / 2 equal / 2 worse
- full_budget units with verified evidence (supported + disputed): median +0 [-2 to +4]; 2 better / 0 equal / 2 worse
- full_budget STRICTLY supported units (no consensus, no scope split): median +1.5 [-2 to +3]; 3 better / 0 equal / 1 worse

**Tally, common_stop view:** NO coverage benefit (equal, incomplete): 1 (Q2r1); adaptive WORSE coverage: 2 (Q1r1, Q5r1); adaptive better coverage: 3 (Q3r1, Q4r1, Q8r1)

**Tally, full_budget view:** NO coverage benefit (equal, incomplete): 1 (Q2r1); adaptive WORSE coverage: 2 (Q1r1, Q5r1); adaptive better coverage: 3 (Q3r1, Q4r1, Q8r1)

## Stopping value (common_stop vs full_budget, same trajectory)

| Q | rep | arm | stop rule fired | round | actions saved | coverage lost | premature? |
|---|---|---|---|---|---|---|---|
| Q1 | 1 | static | budget_exhausted | 3 | 0 | 0 | no |
| Q1 | 1 | v2_policy | budget_exhausted | 3 | 0 | 0 | no |
| Q1 | 1 | adaptive | budget_exhausted | 3 | 0 | 0 | no |
| Q2 | 1 | static | budget_exhausted | 3 | 0 | 0 | no |
| Q2 | 1 | v2_policy | budget_exhausted | 3 | 0 | 0 | no |
| Q2 | 1 | adaptive | budget_exhausted | 3 | 0 | 0 | no |
| Q3 | 1 | static | budget_exhausted | 3 | 0 | 0 | no |
| Q3 | 1 | v2_policy | budget_exhausted | 3 | 0 | 0 | no |
| Q3 | 1 | adaptive | budget_exhausted | 3 | 0 | 0 | no |
| Q4 | 1 | static | budget_exhausted | 3 | 0 | 0 | no |
| Q4 | 1 | v2_policy | budget_exhausted | 3 | 0 | 0 | no |
| Q4 | 1 | adaptive | budget_exhausted | 3 | 0 | 0 | no |
| Q5 | 1 | static | budget_exhausted | 3 | 0 | 0 | no |
| Q5 | 1 | v2_policy | no_progress | 3 | 0 | 0 | no |
| Q5 | 1 | adaptive | no_progress | 3 | 0 | 0 | no |
| Q8 | 1 | static | budget_exhausted | 3 | 0 | 0 | no |
| Q8 | 1 | v2_policy | budget_exhausted | 3 | 0 | 0 | no |
| Q8 | 1 | adaptive | stable | 3 | 0 | 0 | no |

Premature stops (the common rule stopped before units that the full budget later found): none

## Aggregate (sums over all questions and repetitions; descriptive)

| metric | static common | v2_policy common | adaptive common | static full | v2_policy full | adaptive full |
|---|---|---|---|---|---|---|
| units_strict_supported | 19.0 | 21.0 | 23.0 | 19.0 | 21.0 | 23.0 |
| units_consensus | 2.0 | 0.0 | 0.0 | 2.0 | 0.0 | 0.0 |
| units_supported | 28.0 | 28.0 | 32.0 | 28.0 | 28.0 | 32.0 |
| units_evidenced | 24.0 | 23.0 | 26.0 | 24.0 | 23.0 | 26.0 |
| units_disputed | 2.0 | 1.0 | 2.0 | 2.0 | 1.0 | 2.0 |
| units_unknown | 2.0 | 2.0 | 2.0 | 2.0 | 2.0 | 2.0 |
| units_insufficient | 9.0 | 10.0 | 7.0 | 9.0 | 10.0 | 7.0 |
| units_dimension_mismatch | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| source_inconsistent_cells | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| units_heterogeneous | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| units_ambiguous_dimension | 2.0 | 2.0 | 2.0 | 2.0 | 2.0 | 2.0 |
| units_total | 45.0 | 45.0 | 45.0 | 45.0 | 45.0 | 45.0 |
| high_confidence_cells | 10.0 | 5.0 | 5.0 | 10.0 | 5.0 | 5.0 |
| actions | 89.0 | 90.0 | 90.0 | 89.0 | 90.0 | 90.0 |
| accepted | 83.0 | 63.0 | 80.0 | 83.0 | 63.0 | 80.0 |
| rejected | 48.0 | 48.0 | 38.0 | 48.0 | 48.0 | 38.0 |
| distinct_domains | 27.0 | 22.0 | 22.0 | 27.0 | 22.0 | 22.0 |
| repeat_prev_target | 0.0 | 4.0 | 0.0 | 0.0 | 4.0 | 0.0 |
| failed_targeted_rounds | 6.0 | 9.0 | 7.0 | 6.0 | 9.0 | 7.0 |
| disputes_seen | 2.0 | 1.0 | 2.0 | 2.0 | 1.0 | 2.0 |
| disputes_resolved | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| consequential_disputes | 1.0 | 0.0 | 1.0 | 1.0 | 0.0 | 1.0 |
| consequential_disputes_resolved | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| readiness_changes | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| became_ready | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| flips | 2.0 | 1.0 | 1.0 | 2.0 | 1.0 | 1.0 |
| strong_flips | 2.0 | 1.0 | 1.0 | 2.0 | 1.0 | 1.0 |
| tie_flips | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| status_changes | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 | 4.0 |
| provider_failure_rounds | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| llm_tokens | 316449.0 | 288955.0 | 293201.0 | 316449.0 | 288955.0 | 293201.0 |
| exa_cost_usd | 0.268 | 0.269 | 0.269 | 0.268 | 0.269 | 0.269 |
| llm_cost_usd | 0.0688 | 0.0618 | 0.063 | 0.0688 | 0.0618 | 0.063 |
| tool_errors | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| llm_errors | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

Ready recommendations (full_budget): static 0, v2_policy 0, adaptive 0.

Counted leader changes, preserved V2 definition (full_budget): Q1r1/static (strong), Q1r1/v2_policy (strong), Q1r1/adaptive (strong). A *strong* flip replaces a real leader with a different real leader; tie-related changes move into or out of a tie.

## Recorded spend (each provider call counted once)

- Recorded calls: 216; Exa (provider-reported): $0.464; gateway `usage.cost`: $0.139008; total reported: $0.603008; tokens: 644068
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
- decision change round 2: leader_changed Qdrant/provisional → Weaviate/provisional

**Q1 r1 v2_policy** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Milvus:operational_effort` [targeted] score 10.0 flip-relevant: Milvus:operational_effort is unknown (width 2, weight 5, flip-relevant x2); resolving it could change the leader.
- round 2 `Weaviate:operational_effort` [targeted] score 10.0 flip-relevant: Weaviate:operational_effort is unknown (width 2, weight 5, flip-relevant x2); resolving it could change the leader. Already supported for Weaviate: deployment_fit.
- round 3 `Weaviate:operational_effort` [bounded_retry] score 10.0 flip-relevant: Weaviate:operational_effort is insufficient (width 2, weight 5, flip-relevant x2); resolving it could change the leader. Already supported for Weaviate: deployment_fit. Retry with an open query.
- decision change round 0: stability_changed None/undetermined → Weaviate/provisional
- decision change round 1: leader_changed Weaviate/provisional → Milvus/provisional

**Q1 r1 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Qdrant:operational_effort` [targeted] score 10.0 flip-relevant: Researching Qdrant:operational_effort (weight 5) because it is unknown: could change the leader. Priority 5 x 2 x 2.00 (decision) x 1.00 (exploration) x 1.00 (retry) / 2 = 10.00.
- round 2 `Milvus:operational_effort` [targeted] score 12.0 flip-relevant: Researching Milvus:operational_effort (weight 5) because it is unknown: could change the leader. Priority 5 x 2 x 2.00 (decision) x 1.20 (exploration) x 1.00 (retry) / 2 = 12.00.
- round 3 `Weaviate:operational_effort` [targeted] score 12.0 flip-relevant: Researching Weaviate:operational_effort (weight 5) because it is unknown: could change the leader. Priority 5 x 2 x 2.00 (decision) x 1.20 (exploration) x 1.00 (retry) / 2 = 12.00.
- decision change round 0: stability_changed None/undetermined → Weaviate/provisional
- decision change round 2: leader_changed Weaviate/provisional → Milvus/provisional

**Q2 r1 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `india_headquarters` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `b2b_saas` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `hr_technology` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).

**Q2 r1 v2_policy** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `ZingHR|b2b_saas` [targeted] score 2.5: ZingHR is missing verified evidence for 'Company offers software as a service to business customers, supported by evidence of its product and business-customer market.' (importance 5).
- round 2 `ZingHR|hr_technology` [targeted] score 2.5: ZingHR is missing verified evidence for 'Company’s product or service falls within HR technology, such as HR management, recruiting, payroll, or workforce management.' (importance 5).
- round 3 `greytHR|b2b_saas` [targeted] score 2.5: greytHR is missing verified evidence for 'Company offers software as a service to business customers, supported by evidence of its product and business-customer market.' (importance 5).

**Q2 r1 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `ZingHR|b2b_saas` [targeted] score 2.5: ZingHR is missing verified evidence for 'Company offers software as a service to business customers, supported by evidence of its product and business-customer market.' (importance 5).
- round 2 `ZingHR|hr_technology` [targeted] score 2.5: ZingHR is missing verified evidence for 'Company’s product or service falls within HR technology, such as HR management, recruiting, payroll, or workforce management.' (importance 5).
- round 3 `greytHR|b2b_saas` [targeted] score 2.5: greytHR is missing verified evidence for 'Company offers software as a service to business customers, supported by evidence of its product and business-customer market.' (importance 5).

**Q3 r1 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Single-agent support automation:implementation_complexity` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Multi-agent support automation:total_cost` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Single-agent support automation:total_cost` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- decision change round 0: stability_changed None/undetermined → Single-agent support automation/provisional

**Q3 r1 v2_policy** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Multi-agent support automation:implementation_complexity` [targeted] score 3.0: Multi-agent support automation:implementation_complexity is insufficient (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Multi-agent support automation: safeguards.
- round 2 `Multi-agent support automation:implementation_complexity` [bounded_retry] score 3.0: Multi-agent support automation:implementation_complexity is insufficient (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Multi-agent support automation: total_cost, safeguards. Retry with an open query.
- round 3 `Multi-agent support automation:reliability` [targeted] score 3.0: Multi-agent support automation:reliability is insufficient (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Multi-agent support automation: total_cost, safeguards.
- decision change round 0: stability_changed None/undetermined → Single-agent support automation/provisional

**Q3 r1 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Single-agent support automation:reliability` [targeted] score 4.5: Researching Single-agent support automation:reliability (weight 3) because it is insufficient: jointly matters: Multi-agent support automation overtakes Single-agent support automation needs a group of 2 cells. Priority 3 x 2 x 1.50 (decision) x 1.00 (exploration) x 1.00 (retry) / 2 = 4.50.
- round 2 `Multi-agent support automation:implementation_complexity` [targeted] score 5.4: Researching Multi-agent support automation:implementation_complexity (weight 3) because it is insufficient: jointly matters: Multi-agent support automation overtakes Single-agent support automation needs a group of 2 cells. Priority 3 x 2 x 1.50 (decision) x 1.20 (exploration) x 1.00 (retry) / 2 = 5.40.
- round 3 `Single-agent support automation:implementation_complexity#corroborate` [corroboration] score 1.25: Researching Single-agent support automation:implementation_complexity (weight 3) because it is supported but blocks readiness: readiness blocker: Single-agent support automation:implementation_complexity has one source family or no official source. Priority 3 x 1 x 1.25 (decision) x 0.67 (exploration) x 1.00 (retry) / 2 = 1.25.
- decision change round 0: stability_changed None/undetermined → Single-agent support automation/provisional

**Q4 r1 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Session-only memory:retrieval_effectiveness` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Persistent conversation-log retrieval:privacy_protection` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Summarized customer-profile memory:retention_and_deletion_control` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- decision change round 0: stability_changed None/undetermined → Hybrid layered memory/provisional

**Q4 r1 v2_policy** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Hybrid layered memory:retrieval_effectiveness` [targeted] score 6.0 flip-relevant: Hybrid layered memory:retrieval_effectiveness is insufficient (width 2, weight 3, flip-relevant x2); resolving it could change the leader. Already supported for Hybrid layered memory: privacy_protection, retention_and_deletion_control.
- round 2 `Hybrid layered memory:retrieval_effectiveness` [bounded_retry] score 6.0 flip-relevant: Hybrid layered memory:retrieval_effectiveness is insufficient (width 2, weight 3, flip-relevant x2); resolving it could change the leader. Already supported for Hybrid layered memory: privacy_protection, retention_and_deletion_control. Retry with an open query.
- round 3 `Persistent conversation-log retrieval:privacy_protection` [targeted] score 6.0 flip-relevant: Persistent conversation-log retrieval:privacy_protection is unknown (width 2, weight 3, flip-relevant x2); resolving it could change the leader. Already supported for Persistent conversation-log retrieval: retrieval_effectiveness, retention_and_deletion_control.
- decision change round 0: stability_changed None/undetermined → Hybrid layered memory/provisional

**Q4 r1 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Hybrid layered memory:retrieval_effectiveness` [targeted] score 6.0 flip-relevant: Researching Hybrid layered memory:retrieval_effectiveness (weight 3) because it is insufficient: could make the leader interval-robust. Priority 3 x 2 x 2.00 (decision) x 1.00 (exploration) x 1.00 (retry) / 2 = 6.00.
- round 2 `Session-only memory:retention_and_deletion_control` [targeted] score 5.4: Researching Session-only memory:retention_and_deletion_control (weight 3) because it is insufficient: jointly matters: Session-only memory overtakes Hybrid layered memory needs a group of 2 cells. Priority 3 x 2 x 1.50 (decision) x 1.20 (exploration) x 1.00 (retry) / 2 = 5.40.
- round 3 `Persistent conversation-log retrieval:privacy_protection` [targeted] score 5.4: Researching Persistent conversation-log retrieval:privacy_protection (weight 3) because it is unknown: jointly matters: Persistent conversation-log retrieval overtakes Hybrid layered memory needs a group of 2 cells. Priority 3 x 2 x 1.50 (decision) x 1.20 (exploration) x 1.00 (retry) / 2 = 5.40.
- decision change round 0: stability_changed None/undetermined → Hybrid layered memory/provisional

**Q5 r1 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Managed vector database:operational_effort` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Self-hosted vector database:startup_cost` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Managed vector database:startup_cost` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- decision change round 0: became_robust None/undetermined → Managed vector database/robust

**Q5 r1 v2_policy** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Managed vector database:operational_effort#corroborate` [corroboration] score 2.5: Interval winner is robust but the recommendation is withheld (single-source/weak support): corroborate Managed vector database:operational_effort (weight 5).
- round 2 `Managed vector database:operational_effort#corroborate` [bounded_retry] score 2.5: Interval winner is robust but the recommendation is withheld (single-source/weak support): corroborate Managed vector database:operational_effort (weight 5).
- round 3 `Self-hosted vector database:operational_effort#corroborate` [corroboration] score 2.5: Interval winner is robust but the recommendation is withheld (single-source/weak support): corroborate Self-hosted vector database:operational_effort (weight 5).
- decision change round 0: became_robust None/undetermined → Managed vector database/robust

**Q5 r1 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Managed vector database:operational_effort#corroborate` [corroboration] score 3.125: Researching Managed vector database:operational_effort (weight 5) because it is supported but blocks readiness: readiness blocker: Managed vector database:operational_effort has one source family or no official source. Priority 5 x 1 x 1.25 (decision) x 1.00 (exploration) x 1.00 (retry) / 2 = 3.12.
- round 2 `Self-hosted vector database:operational_effort#corroborate` [corroboration] score 3.9999: Researching Self-hosted vector database:operational_effort (weight 5) because it is supported but blocks readiness: readiness blocker: Self-hosted vector database:operational_effort has one source family or no official source. Priority 5 x 1 x 1.33 (decision) x 1.20 (exploration) x 1.00 (retry) / 2 = 4.00.
- round 3 `Managed vector database:control_and_customization#conflict` [conflict_resolution] score 2.25: Researching Managed vector database:control_and_customization (weight 3) because it is disputed (interval width 1): readiness blocker: Managed vector database's own score on control_and_customization is disputed (verified scores [0, 1]). Priority 3 x 1 x 1.50 (decision) x 1.00 (exploration) x 1.00 (retry) / 2 = 2.25.
- decision change round 0: became_robust None/undetermined → Managed vector database/robust

**Q8 r1 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `llm_evaluation_or_observability` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `open_source_license` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `self_hosting_support` [static_schedule] score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).

**Q8 r1 v2_policy** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `DeepEval|llm_evaluation_or_observability` [targeted] score 2.5: DeepEval is missing verified evidence for 'The entity is a tool for evaluating LLMs or observing LLM application behavior.' (importance 5).
- round 2 `Langfuse|open_source_license` [targeted] score 2.5: Langfuse is missing verified evidence for 'The entity has a clearly identified open-source license, supported by a source or official project evidence.' (importance 5).
- round 3 `new_entities` [targeted] score 2.25: Only 3 candidate entities known; 5 required.

**Q8 r1 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` [first_exploration] score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `DeepEval|llm_evaluation_or_observability` [targeted] score 2.5: DeepEval is missing verified evidence for 'The entity is a tool for evaluating LLMs or observing LLM application behavior.' (importance 5).
- round 2 `Langfuse|open_source_license` [targeted] score 2.5: Langfuse is missing verified evidence for 'The entity has a clearly identified open-source license, supported by a source or official project evidence.' (importance 5).
- round 3 `new_entities` [targeted] score 2.25: Only 3 candidate entities known; 5 required.

