# Live verification log

These are factual records of live checks run on 2026-10-29 (UTC) with the Experiential Labs gateway (`gpt-6-luna`) and Exa (`exa-py 2.26.0`). Run folders are under `outputs/`, which is gitignored and stays local. **These runs are integration checks, not evaluation results.**

## 1. Gateway smoke test (`smoke-gateway`)

Every check passed: basic completion with usage reported, strict `json_schema`, `json_object`, `temperature=0` and `seed`. An invalid model name returns HTTP 403, which is classified as `auth` and stops the run without retrying. **`LLM_STRUCTURED_MODE=json_schema` was kept.** Details are in `docs/gateway-compat.md`.

## 2. Exa integration

- `search(query, contents=False, include_domains=["qdrant.tech"])` returned 3 qdrant.tech documentation URLs.
- `get_contents([url], text={"max_characters": …})` returned 20,000 characters of page text, as a separate call.
- An invalid key returns a 401, classified as `auth` and not retried.

## 3. First real research runs (Q1)

| Run | Outcome | What inspection showed |
|---|---|---|
| `RUN_20261029T223012_46d466` | partial, `budget_exhausted` | **Bug:** the 2-query cap dropped the planner's only Milvus query, so round 0 covered just 2 of 3 alternatives. The report prose also repeated the decision statement. I checked the suspicious EV_6 (Milvus ops effort = 2); it is justified by the rubric's "deployment option suited to its capacity" anchor, so not a bug. |
| `RUN_20261029T223304_235ce8` | partial, `no_progress` | Round-0 queries now name all three options. **Issue:** two milvus.io pages came back from Exa as `302 Found nginx` stubs (status `success`). Also, `MAX_NO_PROGRESS=1` ended the run after one failed target with 7/9 cells unknown and 50% of the searches unused. |
| `RUN_20261029T223528_7a3691` | partial, `budget_exhausted`, 3 targeted rounds | Stubs are rejected as `unusable`. **Bug:** the same stub URL was fetched twice, because unusable URLs were not remembered by dedup. |

## 4. Evaluation harness (Q2, discovery)

- First record (`eval_E_20261029T223726_5bbcfe`): **invalid**. The fairness guard flagged `round0 mismatch`, because record mode re-called the non-deterministic LLM for the second arm. The snapshot was kept as `evaluations/snapshots/_invalid_Q2_round0_mismatch_20261029`.
- After the fix: record (`eval_E_20261029T224038_fb5a9e`) and replay (`eval_E_20261029T224224_21dd33`) gave identical rows, and both arms had round-0 hash `95fd3834911f745b`. *This is one sample of one question and supports no conclusion about static vs adaptive.*

## Fixes made from these runs (each with an offline regression test)

| Fix | Test |
|---|---|
| Initial-query cap now maximises how many alternatives are covered, and the planner is told to name every alternative | `test_initial_query_cap_keeps_alternative_coverage`, `test_uncovered_alternative_is_noted` |
| Report prose must not restate the decision statement | prompt change, checked in the live run |
| Pages that are near-empty, HTTP-error/redirect stubs or bot walls are marked `unusable` and never sent to extraction | `test_X03_redirect_and_error_stubs_are_unusable` |
| Unusable/empty URLs are remembered, so they are never fetched again | same test, `known_url` assertions |
| `MAX_NO_PROGRESS` default changed from 1 to 2 | the existing stop-policy tests still pass |
| Record mode reuses stored responses for identical calls, so both arms share round 0 | `test_E02_record_mode_gives_identical_round0_with_nondeterministic_llm` |

## Observations, not changed (decide before the full evaluation)

- **Budget shape:** with `PAGES_PER_SEARCH=2`, `MAX_CONTENT_PAGES=8` is always reached before `MAX_SEARCH_CALLS=6`. In every live run, 4 of the 6 searches were usable. Options: keep it, set `MAX_CONTENT_PAGES=12`, or set `PAGES_PER_SEARCH=1`. Whatever is chosen must be the same for both arms and recorded with the results.
- **Score saturation:** Qdrant reached 2/2/2 (= the 18 ceiling) in two of the three Q1 runs. When a leader is at the ceiling, no single cell is flip-relevant (a known single-cell limitation), so targets fall back to weight × width with a name tie-break.
- **Run-to-run variance:** the three Q1 runs produced different criteria ids, evidence and stop reasons. For the evaluation, use `--repeat` where budget allows, and compare arms only within the same recording.
- `relevant_retrieval_yield` can exceed 1, because one page can verify several units.
