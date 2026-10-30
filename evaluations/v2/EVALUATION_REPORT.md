# Evaluation report V2: static vs adaptive (live, paired, 3 repetitions)

- Folder: `outputs/eval_v2_E_20261030T045521_1e5cc3` (protocol v2, mode record, started 2026-10-30T04:55:21+00:00, finished 2026-10-30T06:10:04+00:00)
- Config fingerprint `b891d16fe6`: llm_provider=experiential, llm_model=gpt-6-luna, llm_base_url=https://api.experientiallabs.ai/v1, llm_structured_mode=json_schema, llm_temperature=0.0, llm_max_retries=2, exa_max_retries=2, max_search_calls=6, max_content_pages=12, max_research_rounds=3, max_no_progress=2, max_evidence_per_round=12, max_initial_queries=2, results_per_search=5, pages_per_search=2, max_llm_calls=None, max_seconds=None, protocol=v2
- Questions Q1, Q2, Q3, Q4, Q5, Q8; repetitions completed: [1, 2, 3]; spend cap: 1.6 USD; guard stop: not triggered
- Views: **common_stop** = trajectory prefix up to where the common stopping rule fires (same rule for both arms); **full_budget** = the whole run. Static vs adaptive *within a view* measures target selection; common_stop vs full_budget *within an arm* measures stopping.
- Descriptive only: 3 repetitions per arm, no significance claims.

## Replay check

Offline replay `outputs/eval_v2_E_20261030T061020_502e7e`: **all 72 rows identical** (decisions and metrics; run id, timestamp and model label excluded). Replay is a reproducibility check, not an additional repetition.

## Results per question and repetition

| Q | rep | arm | view | coverage | searches | pages | accepted / rejected | domains | stability | interval leader | recommendation | flips / status chg | stop | tokens | Exa $ | LLM $ | errors t/l |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | 1 | static | common_stop | 0/9 | 3 | 6 | 0 / 13 | 0 | undetermined | - | none | 0 / 0 | insufficient_evidence | 28751 | 0.027 | 0.0 | 0/0 |
| Q1 | 1 | static | full_budget | 3/9 | 5 | 10 | 4 / 14 | 2 | undetermined | Weaviate | none | 0 / 2 | budget_exhausted | 47116 | 0.045 | 0.0 | 0/0 |
| Q1 | 1 | adaptive | common_stop | 4/9 | 5 | 10 | 4 / 15 | 3 | provisional | Milvus | withheld | 0 / 1 | budget_exhausted | 46736 | 0.045 | 0.0 | 0/0 |
| Q1 | 1 | adaptive | full_budget | 4/9 | 5 | 10 | 4 / 15 | 3 | provisional | Milvus | withheld | 0 / 1 | budget_exhausted | 46736 | 0.045 | 0.0 | 0/0 |
| Q1 | 2 | static | common_stop | 6/9 | 5 | 10 | 17 / 7 | 5 | provisional | Weaviate | withheld | 0 / 1 | budget_exhausted | 55346 | 0.045 | 0.00394 | 0/0 |
| Q1 | 2 | static | full_budget | 6/9 | 5 | 10 | 17 / 7 | 5 | provisional | Weaviate | withheld | 0 / 1 | budget_exhausted | 55346 | 0.045 | 0.00394 | 0/0 |
| Q1 | 2 | adaptive | common_stop | 6/9 | 5 | 10 | 19 / 14 | 6 | provisional | Qdrant | withheld | 1 / 2 | budget_exhausted | 67967 | 0.045 | 0.00394 | 0/0 |
| Q1 | 2 | adaptive | full_budget | 6/9 | 5 | 10 | 19 / 14 | 6 | provisional | Qdrant | withheld | 1 / 2 | budget_exhausted | 67967 | 0.045 | 0.00394 | 0/0 |
| Q1 | 3 | static | common_stop | 4/9 | 5 | 10 | 10 / 4 | 3 | provisional | Qdrant | withheld | 0 / 1 | budget_exhausted | 45704 | 0.045 | 0.008749 | 0/0 |
| Q1 | 3 | static | full_budget | 4/9 | 5 | 10 | 10 / 4 | 3 | provisional | Qdrant | withheld | 0 / 1 | budget_exhausted | 45704 | 0.045 | 0.008749 | 0/0 |
| Q1 | 3 | adaptive | common_stop | 4/9 | 5 | 10 | 5 / 6 | 3 | provisional | Qdrant | withheld | 0 / 1 | budget_exhausted | 32641 | 0.045 | 0.006659 | 0/0 |
| Q1 | 3 | adaptive | full_budget | 4/9 | 5 | 10 | 5 / 6 | 3 | provisional | Qdrant | withheld | 0 / 1 | budget_exhausted | 32641 | 0.045 | 0.006659 | 0/0 |
| Q2 | 1 | static | common_stop | 4/5 | 5 | 10 | 32 / 3 | 8 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 50393 | 0.045 | 0.0 | 0/0 |
| Q2 | 1 | static | full_budget | 4/5 | 5 | 10 | 32 / 3 | 8 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 50393 | 0.045 | 0.0 | 0/0 |
| Q2 | 1 | adaptive | common_stop | 4/5 | 5 | 10 | 26 / 9 | 6 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 53442 | 0.045 | 0.0 | 0/0 |
| Q2 | 1 | adaptive | full_budget | 4/5 | 5 | 10 | 26 / 9 | 6 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 53442 | 0.045 | 0.0 | 0/0 |
| Q2 | 2 | static | common_stop | 2/5 | 5 | 10 | 31 / 7 | 8 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 45953 | 0.045 | 0.0 | 0/0 |
| Q2 | 2 | static | full_budget | 2/5 | 5 | 10 | 31 / 7 | 8 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 45953 | 0.045 | 0.0 | 0/0 |
| Q2 | 2 | adaptive | common_stop | 4/5 | 5 | 10 | 25 / 5 | 4 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 38817 | 0.045 | 0.0 | 0/0 |
| Q2 | 2 | adaptive | full_budget | 4/5 | 5 | 10 | 25 / 5 | 4 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 38817 | 0.045 | 0.0 | 0/0 |
| Q2 | 3 | static | common_stop | 2/5 | 5 | 10 | 26 / 9 | 9 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 47528 | 0.045 | 0.010856 | 0/0 |
| Q2 | 3 | static | full_budget | 2/5 | 5 | 10 | 26 / 9 | 9 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 47528 | 0.045 | 0.010856 | 0/0 |
| Q2 | 3 | adaptive | common_stop | 1/5 | 5 | 9 | 20 / 8 | 6 | n/a | - | not_applicable | 0 / 0 | no_progress | 44655 | 0.044 | 0.010214 | 0/0 |
| Q2 | 3 | adaptive | full_budget | 1/5 | 5 | 9 | 20 / 8 | 6 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 44655 | 0.044 | 0.010214 | 0/0 |
| Q3 | 1 | static | common_stop | 7/8 | 4 | 8 | 7 / 7 | 2 | provisional | Single-agent support automation | withheld | 0 / 1 | no_progress | 43655 | 0.036 | 0.0 | 0/0 |
| Q3 | 1 | static | full_budget | 7/8 | 5 | 10 | 7 / 10 | 2 | provisional | Single-agent support automation | withheld | 0 / 1 | budget_exhausted | 58472 | 0.045 | 0.0 | 0/0 |
| Q3 | 1 | adaptive | common_stop | 7/8 | 4 | 8 | 12 / 10 | 3 | provisional | Single-agent support automation | withheld | 0 / 1 | no_progress | 51743 | 0.036 | 0.0 | 0/0 |
| Q3 | 1 | adaptive | full_budget | 7/8 | 4 | 8 | 12 / 10 | 3 | provisional | Single-agent support automation | withheld | 0 / 1 | no_progress | 51743 | 0.036 | 0.0 | 0/0 |
| Q3 | 2 | static | common_stop | 4/8 | 5 | 10 | 10 / 4 | 2 | provisional | Single-agent support automation | withheld | 0 / 1 | no_progress | 53845 | 0.045 | 0.0 | 0/0 |
| Q3 | 2 | static | full_budget | 4/8 | 5 | 10 | 10 / 4 | 2 | provisional | Single-agent support automation | withheld | 0 / 1 | budget_exhausted | 53845 | 0.045 | 0.0 | 0/0 |
| Q3 | 2 | adaptive | common_stop | 5/8 | 4 | 8 | 5 / 4 | 1 | provisional | Single-agent support automation | withheld | 0 / 1 | no_progress | 34305 | 0.036 | 0.001318 | 0/0 |
| Q3 | 2 | adaptive | full_budget | 5/8 | 5 | 10 | 5 / 4 | 1 | provisional | Single-agent support automation | withheld | 0 / 1 | budget_exhausted | 42816 | 0.045 | 0.002447 | 0/0 |
| Q3 | 3 | static | common_stop | 5/8 | 5 | 10 | 8 / 11 | 2 | provisional | Single-agent support automation | withheld | 0 / 1 | no_progress | 57760 | 0.045 | 0.011823 | 0/0 |
| Q3 | 3 | static | full_budget | 5/8 | 5 | 10 | 8 / 11 | 2 | provisional | Single-agent support automation | withheld | 0 / 1 | budget_exhausted | 57760 | 0.045 | 0.011823 | 0/0 |
| Q3 | 3 | adaptive | common_stop | 2/8 | 4 | 8 | 2 / 7 | 1 | provisional | Single-agent support automation | withheld | 0 / 1 | no_progress | 36224 | 0.036 | 0.006741 | 0/0 |
| Q3 | 3 | adaptive | full_budget | 3/8 | 5 | 10 | 3 / 7 | 2 | provisional | Single-agent support automation | withheld | 0 / 1 | budget_exhausted | 41476 | 0.045 | 0.007643 | 0/0 |
| Q4 | 1 | static | common_stop | 8/12 | 4 | 8 | 9 / 8 | 2 | provisional | Session-only memory | withheld | 0 / 1 | no_progress | 49416 | 0.036 | 0.0 | 0/0 |
| Q4 | 1 | static | full_budget | 9/12 | 5 | 10 | 11 / 8 | 3 | provisional | Session-only memory | withheld | 0 / 1 | budget_exhausted | 60345 | 0.045 | 0.0 | 0/0 |
| Q4 | 1 | adaptive | common_stop | 9/12 | 5 | 10 | 10 / 4 | 3 | provisional | Session-only memory | withheld | 0 / 1 | no_progress | 49312 | 0.045 | 0.0 | 0/0 |
| Q4 | 1 | adaptive | full_budget | 9/12 | 5 | 10 | 10 / 4 | 3 | provisional | Session-only memory | withheld | 0 / 1 | budget_exhausted | 49312 | 0.045 | 0.0 | 0/0 |
| Q4 | 2 | static | common_stop | 4/15 | 4 | 8 | 6 / 12 | 3 | undetermined | Retrieval-augmented episodic memory | none | 0 / 0 | no_progress | 52889 | 0.036 | 0.010976 | 0/0 |
| Q4 | 2 | static | full_budget | 5/15 | 5 | 10 | 7 / 12 | 4 | undetermined | Retrieval-augmented episodic memory | none | 0 / 0 | budget_exhausted | 64167 | 0.045 | 0.012822 | 0/0 |
| Q4 | 2 | adaptive | common_stop | 4/15 | 4 | 8 | 4 / 8 | 2 | undetermined | Retrieval-augmented episodic memory | none | 0 / 0 | no_progress | 48070 | 0.036 | 0.0098 | 0/0 |
| Q4 | 2 | adaptive | full_budget | 4/15 | 5 | 10 | 4 / 9 | 2 | undetermined | Retrieval-augmented episodic memory | none | 0 / 0 | budget_exhausted | 59737 | 0.045 | 0.011827 | 0/0 |
| Q4 | 3 | static | common_stop | 2/16 | 5 | 10 | 3 / 5 | 1 | undetermined | Retrieval-augmented episodic memory | none | 0 / 0 | no_progress | 41068 | 0.045 | 0.008433 | 0/3 |
| Q4 | 3 | static | full_budget | 2/16 | 5 | 10 | 3 / 5 | 1 | undetermined | Retrieval-augmented episodic memory | none | 0 / 0 | budget_exhausted | 41068 | 0.045 | 0.008433 | 0/3 |
| Q4 | 3 | adaptive | common_stop | 0/16 | 3 | 6 | 0 / 0 | 0 | undetermined | - | none | 0 / 0 | insufficient_evidence | 10805 | 0.027 | 0.001367 | 0/3 |
| Q4 | 3 | adaptive | full_budget | 1/16 | 5 | 10 | 1 / 0 | 1 | undetermined | Session-only context-window memory | none | 0 / 0 | budget_exhausted | 32432 | 0.045 | 0.004746 | 0/3 |
| Q5 | 1 | static | common_stop | 2/6 | 5 | 10 | 21 / 2 | 6 | provisional | Managed vector database | withheld | 0 / 2 | budget_exhausted | 59089 | 0.045 | 0.0 | 0/0 |
| Q5 | 1 | static | full_budget | 2/6 | 5 | 10 | 21 / 2 | 6 | provisional | Managed vector database | withheld | 0 / 2 | budget_exhausted | 59089 | 0.045 | 0.0 | 0/0 |
| Q5 | 1 | adaptive | common_stop | 5/6 | 3 | 6 | 10 / 2 | 3 | robust | Managed vector database | ready | 0 / 1 | stable | 29729 | 0.027 | 0.0 | 0/0 |
| Q5 | 1 | adaptive | full_budget | 5/6 | 3 | 6 | 10 / 2 | 3 | robust | Managed vector database | ready | 0 / 1 | stable | 29729 | 0.027 | 0.0 | 0/0 |
| Q5 | 2 | static | common_stop | 6/6 | 5 | 10 | 9 / 4 | 5 | robust | Managed vector database | withheld | 0 / 1 | budget_exhausted | 52633 | 0.045 | 0.011809 | 0/0 |
| Q5 | 2 | static | full_budget | 6/6 | 5 | 10 | 9 / 4 | 5 | robust | Managed vector database | withheld | 0 / 1 | budget_exhausted | 52633 | 0.045 | 0.011809 | 0/0 |
| Q5 | 2 | adaptive | common_stop | 3/6 | 5 | 10 | 8 / 10 | 4 | robust | Managed vector database | withheld | 0 / 1 | no_progress | 57269 | 0.045 | 0.013197 | 0/0 |
| Q5 | 2 | adaptive | full_budget | 3/6 | 5 | 10 | 8 / 10 | 4 | robust | Managed vector database | withheld | 0 / 1 | budget_exhausted | 57269 | 0.045 | 0.013197 | 0/0 |
| Q5 | 3 | static | common_stop | 3/6 | 5 | 10 | 16 / 5 | 5 | provisional | Managed vector database | withheld | 0 / 2 | budget_exhausted | 53345 | 0.045 | 0.013003 | 0/0 |
| Q5 | 3 | static | full_budget | 3/6 | 5 | 10 | 16 / 5 | 5 | provisional | Managed vector database | withheld | 0 / 2 | budget_exhausted | 53345 | 0.045 | 0.013003 | 0/0 |
| Q5 | 3 | adaptive | common_stop | 3/6 | 5 | 10 | 14 / 6 | 5 | provisional | Managed vector database | withheld | 0 / 2 | no_progress | 53576 | 0.045 | 0.011883 | 0/0 |
| Q5 | 3 | adaptive | full_budget | 3/6 | 5 | 10 | 14 / 6 | 5 | provisional | Managed vector database | withheld | 0 / 2 | budget_exhausted | 53576 | 0.045 | 0.011883 | 0/0 |
| Q8 | 1 | static | common_stop | 4/5 | 5 | 9 | 19 / 6 | 2 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 41141 | 0.044 | 0.0 | 0/0 |
| Q8 | 1 | static | full_budget | 4/5 | 5 | 9 | 19 / 6 | 2 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 41141 | 0.044 | 0.0 | 0/0 |
| Q8 | 1 | adaptive | common_stop | 3/5 | 5 | 10 | 15 / 2 | 2 | n/a | - | not_applicable | 0 / 0 | no_progress | 35337 | 0.045 | 0.001208 | 0/0 |
| Q8 | 1 | adaptive | full_budget | 3/5 | 5 | 10 | 15 / 2 | 2 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 35337 | 0.045 | 0.001208 | 0/0 |
| Q8 | 2 | static | common_stop | 5/5 | 5 | 10 | 21 / 4 | 2 | n/a | - | not_applicable | 0 / 0 | stable | 45580 | 0.045 | 0.008304 | 0/0 |
| Q8 | 2 | static | full_budget | 5/5 | 5 | 10 | 21 / 4 | 2 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 45580 | 0.045 | 0.008304 | 0/0 |
| Q8 | 2 | adaptive | common_stop | 3/5 | 5 | 10 | 16 / 5 | 2 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 44551 | 0.045 | 0.008063 | 0/0 |
| Q8 | 2 | adaptive | full_budget | 3/5 | 5 | 10 | 16 / 5 | 2 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 44551 | 0.045 | 0.008063 | 0/0 |
| Q8 | 3 | static | common_stop | 2/5 | 5 | 10 | 21 / 11 | 2 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 50805 | 0.045 | 0.010727 | 0/0 |
| Q8 | 3 | static | full_budget | 2/5 | 5 | 10 | 21 / 11 | 2 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 50805 | 0.045 | 0.010727 | 0/0 |
| Q8 | 3 | adaptive | common_stop | 2/5 | 5 | 10 | 18 / 6 | 2 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 43964 | 0.045 | 0.009139 | 0/0 |
| Q8 | 3 | adaptive | full_budget | 2/5 | 5 | 10 | 18 / 6 | 2 | n/a | - | not_applicable | 0 / 0 | budget_exhausted | 43964 | 0.045 | 0.009139 | 0/0 |

## Distribution across repetitions: median [min-max]

| Q | arm | view | coverage | units_supported | actions | accepted | rejected | relevant_retrieval_yield | distinct_domains | llm_tokens | exa_cost_usd | llm_cost_usd |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | static | common_stop | 0.444 [0-0.667] | 4 [0-6] | 15 [9-15] | 10 [0-17] | 7 [4-13] | 0.267 [0-0.4] | 3 [0-5] | 45704 [28751-55346] | 0.045 [0.027-0.045] | 0.00394 [0-0.00875] |
| Q1 | static | full_budget | 0.444 [0.333-0.667] | 4 [3-6] | 15 [15-15] | 10 [4-17] | 7 [4-14] | 0.267 [0.2-0.4] | 3 [2-5] | 47116 [45704-55346] | 0.045 [0.045-0.045] | 0.00394 [0-0.00875] |
| Q1 | adaptive | common_stop | 0.444 [0.444-0.667] | 4 [4-6] | 15 [15-15] | 5 [4-19] | 14 [6-15] | 0.267 [0.267-0.4] | 3 [3-6] | 46736 [32641-67967] | 0.045 [0.045-0.045] | 0.00394 [0-0.00666] |
| Q1 | adaptive | full_budget | 0.444 [0.444-0.667] | 4 [4-6] | 15 [15-15] | 5 [4-19] | 14 [6-15] | 0.267 [0.267-0.4] | 3 [3-6] | 46736 [32641-67967] | 0.045 [0.045-0.045] | 0.00394 [0-0.00666] |
| Q2 | static | common_stop | 0.4 [0.4-0.8] | 2 [2-4] | 15 [15-15] | 31 [26-32] | 7 [3-9] | 0.133 [0.133-0.267] | 8 [8-9] | 47528 [45953-50393] | 0.045 [0.045-0.045] | 0 [0-0.0109] |
| Q2 | static | full_budget | 0.4 [0.4-0.8] | 2 [2-4] | 15 [15-15] | 31 [26-32] | 7 [3-9] | 0.133 [0.133-0.267] | 8 [8-9] | 47528 [45953-50393] | 0.045 [0.045-0.045] | 0 [0-0.0109] |
| Q2 | adaptive | common_stop | 0.8 [0.2-0.8] | 4 [1-4] | 15 [14-15] | 25 [20-26] | 8 [5-9] | 0.267 [0.071-0.267] | 6 [4-6] | 44655 [38817-53442] | 0.045 [0.044-0.045] | 0 [0-0.0102] |
| Q2 | adaptive | full_budget | 0.8 [0.2-0.8] | 4 [1-4] | 15 [14-15] | 25 [20-26] | 8 [5-9] | 0.267 [0.071-0.267] | 6 [4-6] | 44655 [38817-53442] | 0.045 [0.044-0.045] | 0 [0-0.0102] |
| Q3 | static | common_stop | 0.625 [0.5-0.875] | 5 [4-7] | 15 [12-15] | 8 [7-10] | 7 [4-11] | 0.333 [0.267-0.583] | 2 [2-2] | 53845 [43655-57760] | 0.045 [0.036-0.045] | 0 [0-0.0118] |
| Q3 | static | full_budget | 0.625 [0.5-0.875] | 5 [4-7] | 15 [15-15] | 8 [7-10] | 10 [4-11] | 0.333 [0.267-0.467] | 2 [2-2] | 57760 [53845-58472] | 0.045 [0.045-0.045] | 0 [0-0.0118] |
| Q3 | adaptive | common_stop | 0.625 [0.25-0.875] | 5 [2-7] | 12 [12-12] | 5 [2-12] | 7 [4-10] | 0.417 [0.167-0.583] | 1 [1-3] | 36224 [34305-51743] | 0.036 [0.036-0.036] | 0.00132 [0-0.00674] |
| Q3 | adaptive | full_budget | 0.625 [0.375-0.875] | 5 [3-7] | 15 [12-15] | 5 [3-12] | 7 [4-10] | 0.333 [0.2-0.583] | 2 [1-3] | 42816 [41476-51743] | 0.045 [0.036-0.045] | 0.00245 [0-0.00764] |
| Q4 | static | common_stop | 0.267 [0.125-0.667] | 4 [2-8] | 12 [12-15] | 6 [3-9] | 8 [5-12] | 0.333 [0.133-0.667] | 2 [1-3] | 49416 [41068-52889] | 0.036 [0.036-0.045] | 0.00843 [0-0.011] |
| Q4 | static | full_budget | 0.333 [0.125-0.75] | 5 [2-9] | 15 [15-15] | 7 [3-11] | 8 [5-12] | 0.333 [0.133-0.6] | 3 [1-4] | 60345 [41068-64167] | 0.045 [0.045-0.045] | 0.00843 [0-0.0128] |
| Q4 | adaptive | common_stop | 0.267 [0-0.75] | 4 [0-9] | 12 [9-15] | 4 [0-10] | 4 [0-8] | 0.333 [0-0.6] | 2 [0-3] | 48070 [10805-49312] | 0.036 [0.027-0.045] | 0.00137 [0-0.0098] |
| Q4 | adaptive | full_budget | 0.267 [0.062-0.75] | 4 [1-9] | 15 [15-15] | 4 [1-10] | 4 [0-9] | 0.267 [0.067-0.6] | 2 [1-3] | 49312 [32432-59737] | 0.045 [0.045-0.045] | 0.00475 [0-0.0118] |
| Q5 | static | common_stop | 0.5 [0.333-1] | 3 [2-6] | 15 [15-15] | 16 [9-21] | 4 [2-5] | 0.2 [0.133-0.4] | 5 [5-6] | 53345 [52633-59089] | 0.045 [0.045-0.045] | 0.0118 [0-0.013] |
| Q5 | static | full_budget | 0.5 [0.333-1] | 3 [2-6] | 15 [15-15] | 16 [9-21] | 4 [2-5] | 0.2 [0.133-0.4] | 5 [5-6] | 53345 [52633-59089] | 0.045 [0.045-0.045] | 0.0118 [0-0.013] |
| Q5 | adaptive | common_stop | 0.5 [0.5-0.833] | 3 [3-5] | 15 [9-15] | 10 [8-14] | 6 [2-10] | 0.2 [0.2-0.556] | 4 [3-5] | 53576 [29729-57269] | 0.045 [0.027-0.045] | 0.0119 [0-0.0132] |
| Q5 | adaptive | full_budget | 0.5 [0.5-0.833] | 3 [3-5] | 15 [9-15] | 10 [8-14] | 6 [2-10] | 0.2 [0.2-0.556] | 4 [3-5] | 53576 [29729-57269] | 0.045 [0.027-0.045] | 0.0119 [0-0.0132] |
| Q8 | static | common_stop | 0.8 [0.4-1] | 4 [2-5] | 15 [14-15] | 21 [19-21] | 6 [4-11] | 0.286 [0.133-0.333] | 2 [2-2] | 45580 [41141-50805] | 0.045 [0.044-0.045] | 0.0083 [0-0.0107] |
| Q8 | static | full_budget | 0.8 [0.4-1] | 4 [2-5] | 15 [14-15] | 21 [19-21] | 6 [4-11] | 0.286 [0.133-0.333] | 2 [2-2] | 45580 [41141-50805] | 0.045 [0.044-0.045] | 0.0083 [0-0.0107] |
| Q8 | adaptive | common_stop | 0.6 [0.4-0.6] | 3 [2-3] | 15 [15-15] | 16 [15-18] | 5 [2-6] | 0.2 [0.133-0.2] | 2 [2-2] | 43964 [35337-44551] | 0.045 [0.045-0.045] | 0.00806 [0.00121-0.00914] |
| Q8 | adaptive | full_budget | 0.6 [0.4-0.6] | 3 [2-3] | 15 [15-15] | 16 [15-18] | 5 [2-6] | 0.2 [0.133-0.2] | 2 [2-2] | 43964 [35337-44551] | 0.045 [0.045-0.045] | 0.00806 [0.00121-0.00914] |

## Targeting value (static vs adaptive, same stopping rule)

Matched-actions compares coverage when each arm has spent no more than the other arm's common-stop actions, so neither arm gets credit just for spending more.

| Q | rep | common_stop outcome | coverage S → A | actions S → A | matched-actions coverage S vs A (at ≤ k actions) | full_budget outcome | full coverage S → A |
|---|---|---|---|---|---|---|---|
| Q1 | 1 | adaptive better coverage | 0 → 4 | 9 → 15 | 0 vs 1 (k=9; used 9/9) | adaptive better coverage | 3 → 4 |
| Q1 | 2 | NO coverage benefit (equal, incomplete) | 6 → 6 | 15 → 15 | 6 vs 6 (k=15; used 15/15) | NO coverage benefit (equal, incomplete) | 6 → 6 |
| Q1 | 3 | NO coverage benefit (equal, incomplete) | 4 → 4 | 15 → 15 | 4 vs 4 (k=15; used 15/15) | NO coverage benefit (equal, incomplete) | 4 → 4 |
| Q2 | 1 | NO coverage benefit (equal, incomplete) | 4 → 4 | 15 → 15 | 4 vs 4 (k=15; used 15/15) | NO coverage benefit (equal, incomplete) | 4 → 4 |
| Q2 | 2 | adaptive better coverage | 2 → 4 | 15 → 15 | 2 vs 4 (k=15; used 15/15) | adaptive better coverage | 2 → 4 |
| Q2 | 3 | adaptive WORSE coverage | 2 → 1 | 15 → 14 | 2 vs 1 (k=14; used 12/14) | adaptive WORSE coverage | 2 → 1 |
| Q3 | 1 | NO coverage benefit (equal, incomplete) | 7 → 7 | 12 → 12 | 7 vs 7 (k=12; used 12/12) | NO coverage benefit (equal, incomplete); adaptive fewer actions | 7 → 7 |
| Q3 | 2 | adaptive better coverage | 4 → 5 | 15 → 12 | 4 vs 5 (k=12; used 12/12) | adaptive better coverage | 4 → 5 |
| Q3 | 3 | adaptive WORSE coverage | 5 → 2 | 15 → 12 | 5 vs 2 (k=12; used 12/12) | adaptive WORSE coverage | 5 → 3 |
| Q4 | 1 | adaptive better coverage | 8 → 9 | 12 → 15 | 8 vs 9 (k=12; used 12/12) | NO coverage benefit (equal, incomplete) | 9 → 9 |
| Q4 | 2 | NO coverage benefit (equal, incomplete) | 4 → 4 | 12 → 12 | 4 vs 4 (k=12; used 12/12) | adaptive WORSE coverage | 5 → 4 |
| Q4 | 3 | adaptive WORSE coverage | 2 → 0 | 15 → 9 | 2 vs 0 (k=9; used 9/9) | adaptive WORSE coverage | 2 → 1 |
| Q5 | 1 | adaptive better coverage | 2 → 5 | 15 → 9 | 3 vs 5 (k=9; used 9/9) | adaptive better coverage | 2 → 5 |
| Q5 | 2 | adaptive WORSE coverage | 6 → 3 | 15 → 15 | 6 vs 3 (k=15; used 15/15) | adaptive WORSE coverage | 6 → 3 |
| Q5 | 3 | NO coverage benefit (equal, incomplete) | 3 → 3 | 15 → 15 | 3 vs 3 (k=15; used 15/15) | NO coverage benefit (equal, incomplete) | 3 → 3 |
| Q8 | 1 | adaptive WORSE coverage | 4 → 3 | 14 → 15 | 4 vs 3 (k=14; used 14/12) | adaptive WORSE coverage | 4 → 3 |
| Q8 | 2 | adaptive WORSE coverage | 5 → 3 | 15 → 15 | 5 vs 3 (k=15; used 15/15) | adaptive WORSE coverage | 5 → 3 |
| Q8 | 3 | NO coverage benefit (equal, incomplete) | 2 → 2 | 15 → 15 | 2 vs 2 (k=15; used 15/15) | NO coverage benefit (equal, incomplete) | 2 → 2 |

**Tally, common_stop view:** NO coverage benefit (equal, incomplete): 7 (Q1r2, Q1r3, Q2r1, Q3r1, Q4r2, Q5r3, Q8r3); adaptive WORSE coverage: 6 (Q2r3, Q3r3, Q4r3, Q5r2, Q8r1, Q8r2); adaptive better coverage: 5 (Q1r1, Q2r2, Q3r2, Q4r1, Q5r1)

**Tally, full_budget view:** NO coverage benefit (equal, incomplete): 6 (Q1r2, Q1r3, Q2r1, Q4r1, Q5r3, Q8r3); NO coverage benefit (equal, incomplete); adaptive fewer actions: 1 (Q3r1); adaptive WORSE coverage: 7 (Q2r3, Q3r3, Q4r2, Q4r3, Q5r2, Q8r1, Q8r2); adaptive better coverage: 4 (Q1r1, Q2r2, Q3r2, Q5r1)

## Stopping value (common_stop vs full_budget, same trajectory)

| Q | rep | arm | stop rule fired | round | actions saved | coverage lost | premature? |
|---|---|---|---|---|---|---|---|
| Q1 | 1 | static | insufficient_evidence | 1 | 6 | 3 | YES |
| Q1 | 1 | adaptive | budget_exhausted | 3 | 0 | 0 | no |
| Q1 | 2 | static | budget_exhausted | 3 | 0 | 0 | no |
| Q1 | 2 | adaptive | budget_exhausted | 3 | 0 | 0 | no |
| Q1 | 3 | static | budget_exhausted | 3 | 0 | 0 | no |
| Q1 | 3 | adaptive | budget_exhausted | 3 | 0 | 0 | no |
| Q2 | 1 | static | budget_exhausted | 3 | 0 | 0 | no |
| Q2 | 1 | adaptive | budget_exhausted | 3 | 0 | 0 | no |
| Q2 | 2 | static | budget_exhausted | 3 | 0 | 0 | no |
| Q2 | 2 | adaptive | budget_exhausted | 3 | 0 | 0 | no |
| Q2 | 3 | static | budget_exhausted | 3 | 0 | 0 | no |
| Q2 | 3 | adaptive | no_progress | 3 | 0 | 0 | no |
| Q3 | 1 | static | no_progress | 2 | 3 | 0 | no |
| Q3 | 1 | adaptive | no_progress | 2 | 0 | 0 | no |
| Q3 | 2 | static | no_progress | 3 | 0 | 0 | no |
| Q3 | 2 | adaptive | no_progress | 2 | 3 | 0 | no |
| Q3 | 3 | static | no_progress | 3 | 0 | 0 | no |
| Q3 | 3 | adaptive | no_progress | 2 | 3 | 1 | YES |
| Q4 | 1 | static | no_progress | 2 | 3 | 1 | YES |
| Q4 | 1 | adaptive | no_progress | 3 | 0 | 0 | no |
| Q4 | 2 | static | no_progress | 2 | 3 | 1 | YES |
| Q4 | 2 | adaptive | no_progress | 2 | 3 | 0 | no |
| Q4 | 3 | static | no_progress | 3 | 0 | 0 | no |
| Q4 | 3 | adaptive | insufficient_evidence | 1 | 6 | 1 | YES |
| Q5 | 1 | static | budget_exhausted | 3 | 0 | 0 | no |
| Q5 | 1 | adaptive | stable | 1 | 0 | 0 | no |
| Q5 | 2 | static | budget_exhausted | 3 | 0 | 0 | no |
| Q5 | 2 | adaptive | no_progress | 3 | 0 | 0 | no |
| Q5 | 3 | static | budget_exhausted | 3 | 0 | 0 | no |
| Q5 | 3 | adaptive | no_progress | 3 | 0 | 0 | no |
| Q8 | 1 | static | budget_exhausted | 3 | 0 | 0 | no |
| Q8 | 1 | adaptive | no_progress | 3 | 0 | 0 | no |
| Q8 | 2 | static | stable | 3 | 0 | 0 | no |
| Q8 | 2 | adaptive | budget_exhausted | 3 | 0 | 0 | no |
| Q8 | 3 | static | budget_exhausted | 3 | 0 | 0 | no |
| Q8 | 3 | adaptive | budget_exhausted | 3 | 0 | 0 | no |

Premature stops (the common rule stopped before units that the full budget later found): Q1r1/static (lost 3 unit(s)); Q3r3/adaptive (lost 1 unit(s)); Q4r1/static (lost 1 unit(s)); Q4r2/static (lost 1 unit(s)); Q4r3/adaptive (lost 1 unit(s))

## Aggregate (sums over all questions and repetitions; descriptive)

| metric | static common | adaptive common | static full | adaptive full |
|---|---|---|---|---|
| units_supported | 70.0 | 69.0 | 75.0 | 71.0 |
| units_total | 142.0 | 142.0 | 142.0 | 142.0 |
| actions | 254.0 | 245.0 | 269.0 | 260.0 |
| accepted | 266.0 | 213.0 | 273.0 | 215.0 |
| rejected | 122.0 | 121.0 | 126.0 | 122.0 |
| flips | 0.0 | 1.0 | 0.0 | 1.0 |
| status_changes | 11.0 | 12.0 | 13.0 | 12.0 |
| llm_tokens | 874901.0 | 779143.0 | 930290.0 | 826200.0 |
| exa_cost_usd | 0.764 | 0.737 | 0.809 | 0.782 |
| llm_cost_usd | 0.0986 | 0.0835 | 0.1005 | 0.091 |
| tool_errors | 0.0 | 0.0 | 0.0 | 0.0 |
| llm_errors | 3.0 | 3.0 | 3.0 | 3.0 |

Confirmed evidence-caused leader flips (full_budget): Q1r2/adaptive.

## Recorded spend (each provider call counted once)

- Recorded calls: 526; Exa (provider-reported): $1.197; gateway `usage.cost`: $0.169118; total reported: $1.366118; tokens: 1539539
- provider-reported values (Exa cost_dollars, gateway usage.cost); not an invoice. Each recorded call counted once. usage.cost 0 on a token-consuming call is counted as unpriced, not free.
- **Under-reported LLM cost:** 130 gateway calls (726540 tokens) reported `usage.cost` 0. At the average rate of the priced calls they would cost about $0.151133, giving an estimated total of $1.517251 (an estimate, not provider-reported).
- Per-arm figures above are attributed (the shared round 0 counts for both arms).

## Research actions and selection reasons

**Q1 r1 static** (common stop after round 1; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Qdrant:deployment_fit` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Weaviate:filtering_capability` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Milvus:operational_effort` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- decision change round 2: stability_changed None/undetermined → Weaviate/provisional
- decision change round 3: stability_changed Weaviate/provisional → Weaviate/undetermined

**Q1 r1 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Milvus:operational_effort` score 10.0 flip-relevant: Milvus:operational_effort is unknown (width 2, weight 5, flip-relevant x2); resolving it could change the leader.
- round 2 `Milvus:operational_effort` score 10.0 flip-relevant: Milvus:operational_effort is unknown (width 2, weight 5, flip-relevant x2); resolving it could change the leader. Already supported for Milvus: deployment_fit. Retry with an open query.
- round 3 `Qdrant:operational_effort` score 5.0: Qdrant:operational_effort is unknown (width 2, weight 5, not flip-relevant x1); resolving it cannot alone change the leader.
- decision change round 1: stability_changed None/undetermined → Milvus/provisional

**Q1 r2 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Qdrant:deployment_fit` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Weaviate:filtering_capability` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Milvus:operational_effort` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- decision change round 0: stability_changed None/undetermined → Weaviate/provisional

**Q1 r2 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Qdrant:operational_effort` score 6.0 flip-relevant: Qdrant:operational_effort is unknown (width 2, weight 3, flip-relevant x2); resolving it could change the leader. Already supported for Qdrant: deployment_fit, filtering_capability.
- round 2 `Qdrant:operational_effort` score 6.0 flip-relevant: Qdrant:operational_effort is unknown (width 2, weight 3, flip-relevant x2); resolving it could change the leader. Already supported for Qdrant: deployment_fit, filtering_capability. Retry with an open query.
- round 3 `Qdrant:deployment_fit` score 6.0 flip-relevant: Qdrant:deployment_fit is disputed (width 2, weight 3, flip-relevant x2); resolving it could change the leader. Already supported for Qdrant: filtering_capability, operational_effort.
- decision change round 0: stability_changed None/undetermined → Weaviate/provisional
- decision change round 2: leader_changed Weaviate/provisional → Qdrant/undetermined
- decision change round 3: stability_changed Qdrant/undetermined → Qdrant/provisional

**Q1 r3 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Qdrant:deployment_fit` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Weaviate:filtering_capability` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Milvus:operational_effort` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- decision change round 0: stability_changed None/undetermined → Qdrant/provisional

**Q1 r3 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Milvus:deployment_fit` score 3.0: Milvus:deployment_fit is unknown (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader.
- round 2 `Milvus:deployment_fit` score 3.0: Milvus:deployment_fit is unknown (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Retry with an open query.
- round 3 `Milvus:filtering_capability` score 3.0: Milvus:filtering_capability is unknown (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Milvus: operational_effort.
- decision change round 0: stability_changed None/undetermined → Qdrant/provisional

**Q2 r1 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `india_headquarters` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `b2b_saas` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `hr_technology` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).

**Q2 r1 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `new_entities` score 2.25: Only 3 candidate entities known; 5 required.
- round 2 `new_entities` score 2.25: Only 4 candidate entities known; 5 required. Retry with a broadened query.
- round 3 `Cutshort|b2b_saas` score 2.5: Cutshort is missing verified evidence for 'Company offers software as a service to business customers, supported by evidence of its product and business-customer market.' (importance 5).

**Q2 r2 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `india_based` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `b2b_saas` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `hr_technology` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).

**Q2 r2 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `FabHR|b2b_saas` score 2.5: FabHR is missing verified evidence for 'Company offers software as a service to business customers, rather than operating only as a staffing agency, consultancy, or consumer service.' (importance 5).
- round 2 `HRORA|b2b_saas` score 2.5: HRORA is missing verified evidence for 'Company offers software as a service to business customers, rather than operating only as a staffing agency, consultancy, or consumer service.' (importance 5).
- round 3 `new_entities` score 2.25: Only 2 candidate entities known; 5 required.

**Q2 r3 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `india_headquarters` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `b2b_saas` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `hr_technology` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).

**Q2 r3 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `greytHR|b2b_saas` score 2.5: greytHR is missing verified evidence for 'Company provides software as a service to business customers, supported by company or credible third-party evidence.' (importance 5).
- round 2 `greytHR|india_headquarters` score 2.5: greytHR is missing verified evidence for 'Company is headquartered in India; support the claim with a reliable source.' (importance 5).
- round 3 `greytHR|india_headquarters` score 2.5: greytHR is missing verified evidence for 'Company is headquartered in India; support the claim with a reliable source.' (importance 5). Retry with a broadened query.

**Q3 r1 static** (common stop after round 2; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Single-agent support automation:implementation_complexity` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Multi-agent support automation:total_cost` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Single-agent support automation:total_cost` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- decision change round 0: stability_changed None/undetermined → Single-agent support automation/provisional

**Q3 r1 adaptive** (common stop after round 2; final no_progress)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Single-agent support automation:implementation_complexity` score 3.0: Single-agent support automation:implementation_complexity is unknown (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Single-agent support automation: total_cost, reliability, safeguards.
- round 2 `Single-agent support automation:implementation_complexity` score 3.0: Single-agent support automation:implementation_complexity is unknown (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Single-agent support automation: total_cost, reliability, safeguards. Retry with an open query.
- decision change round 0: stability_changed None/undetermined → Single-agent support automation/provisional

**Q3 r2 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Single-agent support automation:implementation_and_operational_complexit` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Multi-agent support automation:total_cost` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Single-agent support automation:total_cost` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- decision change round 0: stability_changed None/undetermined → Single-agent support automation/provisional

**Q3 r2 adaptive** (common stop after round 2; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Multi-agent support automation:safeguards` score 3.0: Multi-agent support automation:safeguards is unknown (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Multi-agent support automation: implementation_and_operational_complexit, reliability.
- round 2 `Multi-agent support automation:safeguards` score 3.0: Multi-agent support automation:safeguards is unknown (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Multi-agent support automation: implementation_and_operational_complexit, reliability. Retry with an open query.
- round 3 `Multi-agent support automation:total_cost` score 3.0: Multi-agent support automation:total_cost is unknown (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Multi-agent support automation: implementation_and_operational_complexit, reliability.
- decision change round 0: stability_changed None/undetermined → Single-agent support automation/provisional

**Q3 r3 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Single-agent support automation:implementation_complexity` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Multi-agent support automation:total_cost` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Single-agent support automation:total_cost` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- decision change round 0: stability_changed None/undetermined → Single-agent support automation/provisional

**Q3 r3 adaptive** (common stop after round 2; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Multi-agent support automation:reliability` score 3.0: Multi-agent support automation:reliability is unknown (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Multi-agent support automation: implementation_complexity.
- round 2 `Multi-agent support automation:reliability` score 3.0: Multi-agent support automation:reliability is unknown (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Multi-agent support automation: implementation_complexity. Retry with an open query.
- round 3 `Multi-agent support automation:safeguards` score 3.0: Multi-agent support automation:safeguards is unknown (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Multi-agent support automation: implementation_complexity.
- decision change round 0: stability_changed None/undetermined → Single-agent support automation/provisional

**Q4 r1 static** (common stop after round 2; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Session-only memory:retrieval_effectiveness` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Persistent conversation-log retrieval:privacy_protection` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Summarized customer-profile memory:retention_and_deletion_control` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- decision change round 0: stability_changed None/undetermined → Session-only memory/provisional

**Q4 r1 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Hybrid layered memory:retention_and_deletion_control` score 3.0: Hybrid layered memory:retention_and_deletion_control is unknown (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Hybrid layered memory: privacy_protection.
- round 2 `Hybrid layered memory:retrieval_effectiveness` score 3.0: Hybrid layered memory:retrieval_effectiveness is unknown (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Hybrid layered memory: privacy_protection, retention_and_deletion_control.
- round 3 `Hybrid layered memory:retrieval_effectiveness` score 3.0: Hybrid layered memory:retrieval_effectiveness is unknown (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Hybrid layered memory: privacy_protection, retention_and_deletion_control. Retry with an open query.
- decision change round 0: stability_changed None/undetermined → Session-only memory/provisional

**Q4 r2 static** (common stop after round 2; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Session-only context:retrieval_quality` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Retrieval-augmented episodic memory:short_term_continuity` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Structured persistent customer profile:long_term_continuity` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).

**Q4 r2 adaptive** (common stop after round 2; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Retrieval-augmented episodic memory:long_term_continuity` score 6.0 flip-relevant: Retrieval-augmented episodic memory:long_term_continuity is unknown (width 2, weight 3, flip-relevant x2); resolving it could change the leader.
- round 2 `Retrieval-augmented episodic memory:long_term_continuity` score 6.0 flip-relevant: Retrieval-augmented episodic memory:long_term_continuity is unknown (width 2, weight 3, flip-relevant x2); resolving it could change the leader. Retry with an open query.
- round 3 `Retrieval-augmented episodic memory:privacy_controls` score 6.0 flip-relevant: Retrieval-augmented episodic memory:privacy_controls is unknown (width 2, weight 3, flip-relevant x2); resolving it could change the leader.

**Q4 r3 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Session-only context-window memory:retrieval_usefulness` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Retrieval-augmented episodic memory:privacy_controls` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Structured customer-profile memory:retention_and_deletion` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).

**Q4 r3 adaptive** (common stop after round 1; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Hybrid tiered memory:operational_effort` score 6.0 flip-relevant: Hybrid tiered memory:operational_effort is unknown (width 2, weight 3, flip-relevant x2); resolving it could change the leader.
- round 2 `Hybrid tiered memory:operational_effort` score 6.0 flip-relevant: Hybrid tiered memory:operational_effort is unknown (width 2, weight 3, flip-relevant x2); resolving it could change the leader. Retry with an open query.
- round 3 `Hybrid tiered memory:privacy_controls` score 6.0 flip-relevant: Hybrid tiered memory:privacy_controls is unknown (width 2, weight 3, flip-relevant x2); resolving it could change the leader.

**Q5 r1 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Managed vector database:operational_effort` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Self-hosted vector database:startup_cost` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Managed vector database:startup_cost` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- decision change round 0: became_robust None/undetermined → Managed vector database/robust
- decision change round 1: lost_robustness Managed vector database/robust → Managed vector database/provisional

**Q5 r1 adaptive** (common stop after round 1; final stable)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Managed vector database:operational_effort#corroborate` score 2.5: Interval winner is robust but the recommendation is withheld (single-source/weak support): corroborate Managed vector database:operational_effort (weight 5).
- decision change round 0: became_robust None/undetermined → Managed vector database/robust

**Q5 r2 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Managed vector database:operational_effort` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Self-hosted vector database:total_cost` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Managed vector database:total_cost` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- decision change round 0: became_robust None/undetermined → Managed vector database/robust

**Q5 r2 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Managed vector database:operational_effort#corroborate` score 2.5: Interval winner is robust but the recommendation is withheld (single-source/weak support): corroborate Managed vector database:operational_effort (weight 5).
- round 2 `Self-hosted vector database:operational_effort#corroborate` score 2.5: Interval winner is robust but the recommendation is withheld (single-source/weak support): corroborate Self-hosted vector database:operational_effort (weight 5).
- round 3 `Self-hosted vector database:operational_effort#corroborate` score 2.5: Interval winner is robust but the recommendation is withheld (single-source/weak support): corroborate Self-hosted vector database:operational_effort (weight 5).
- decision change round 0: became_robust None/undetermined → Managed vector database/robust

**Q5 r3 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Managed vector database:operational_effort` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `Self-hosted vector database:time_to_production` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `Managed vector database:time_to_production` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- decision change round 0: became_robust None/undetermined → Managed vector database/robust
- decision change round 2: lost_robustness Managed vector database/robust → Managed vector database/provisional

**Q5 r3 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Managed vector database:operational_effort#corroborate` score 2.5: Interval winner is robust but the recommendation is withheld (single-source/weak support): corroborate Managed vector database:operational_effort (weight 5).
- round 2 `Self-hosted vector database:operational_effort` score 5.0: Self-hosted vector database:operational_effort is disputed (width 2, weight 5, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Self-hosted vector database: time_to_production.
- round 3 `Self-hosted vector database:operational_effort` score 5.0: Self-hosted vector database:operational_effort is disputed (width 2, weight 5, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Self-hosted vector database: time_to_production. Retry with an open query.
- decision change round 0: became_robust None/undetermined → Managed vector database/robust
- decision change round 1: lost_robustness Managed vector database/robust → Managed vector database/provisional

**Q8 r1 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `llm_evaluation_or_observability` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `open_source_license` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `self_hosting_support` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).

**Q8 r1 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `DeepEval|llm_evaluation_or_observability` score 2.5: DeepEval is missing verified evidence for 'The entity is a tool for evaluating LLMs or observing LLM application behavior.' (importance 5).
- round 2 `OpenLLMetry|self_hosting_support` score 2.5: OpenLLMetry is missing verified evidence for 'The entity provides evidence that users can self-host or deploy it on their own infrastructure.' (importance 5).
- round 3 `OpenLLMetry|self_hosting_support` score 2.5: OpenLLMetry is missing verified evidence for 'The entity provides evidence that users can self-host or deploy it on their own infrastructure.' (importance 5). Retry with a broadened query.

**Q8 r2 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `llm_evaluation_or_observability` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `open_source_license` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `self_hosting_support` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).

**Q8 r2 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `new_entities` score 2.25: Only 1 candidate entities known; 5 required.
- round 2 `OpenLIT|llm_evaluation_or_observability` score 2.5: OpenLIT is missing verified evidence for 'The tool is specifically used to evaluate or observe LLM applications, models, or workflows.' (importance 5).
- round 3 `new_entities` score 2.25: Only 3 candidate entities known; 5 required. Retry with a broadened query.

**Q8 r3 static** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `llm_eval_or_observability` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 2 `open_source_license` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).
- round 3 `self_hosting_support` score 0.0: Static baseline: next target in the fixed round-robin schedule (computed from the plan before retrieval; no adaptation).

**Q8 r3 adaptive** (common stop after round 3; final budget_exhausted)
- round 0 `initial` score 0.0: Initial planned queries (round 0, shared by static and adaptive strategies).
- round 1 `Langfuse|license_and_deployment_evidence` score 2.5: Langfuse is missing verified evidence for 'For each tool, provide evidence from project documentation or its source repository supporting both the stated license and self-hosting support.' (importance 5).
- round 2 `Langfuse|license_and_deployment_evidence` score 2.5: Langfuse is missing verified evidence for 'For each tool, provide evidence from project documentation or its source repository supporting both the stated license and self-hosting support.' (importance 5). Retry with a broadened query.
- round 3 `Langfuse|open_source_license` score 2.5: Langfuse is missing verified evidence for 'Each tool has publicly available source code under a stated open-source license; record the exact license and verify it from a primary source.' (importance 5).

