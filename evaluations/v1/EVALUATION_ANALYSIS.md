# Evaluation analysis: static vs adaptive (live, 2026-10-29)

- **Source data:** `outputs/eval_E_20261029T225137_030e78` (record) and `outputs/eval_E_20261029T230926_ade675` (replay). Copies are in this folder: `results.csv`, `actions.jsonl`, `spend.json`, `eval_config.json`.
- **Auto-generated tables:** `EVALUATION_REPORT.md`. **Review sheet:** `review/AI_PROVISIONAL_REVIEW.md`.
- **No human scores exist yet.** Everything below is measured from run files or labelled as AI-assistant analysis.

## 1. Setup and validity checks

| Check | Result |
|---|---|
| Configuration | `MAX_SEARCH_CALLS=6`, `MAX_CONTENT_PAGES=12`, `PAGES_PER_SEARCH=2`, `MAX_RESEARCH_ROUNDS=3`, `MAX_NO_PROGRESS=2`, `gpt-6-luna` / `json_schema` / temperature 0 (fingerprint `a37e41b4ef`) |
| Equal budgets | Both arms ran under identical caps (from the same `Settings`) |
| Identical plan and round 0 | The same `plan_hash` and `round0_hash` in both arms for all 6 questions; no mismatch flags |
| Separate state after divergence | Each arm has its own `RunContext`, trace and output folder |
| Old 8-page Q2 recording | Kept as `snapshots/_Q2_8page_20261029`; not reused (snapshots are keyed by config fingerprint) |
| Replay | 12/12 rows identical (decisions and metrics), offline |
| Pre-run tests | `ruff check .` clean, `pytest` passed (now 120 tests) |
| Fixed before this run | The static arm previously used different query wording, which confounded the comparison. It was found by an offline test; the aborted partial run was set aside. |

## 2. Question-by-question results (n = 1 per arm)

Coverage is supported requirement units / total: cells for comparisons, verified entities for discovery. Actions = searches + pages.

| Q | Mode | Static coverage | Adaptive coverage | Actions S → A | Searches / pages S → A | Yield S → A | Recommendation (S / A) | Flips | Status changes S / A | Stop S / A | Outcome |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | comparison | 9/9 | 9/9 | 15 → 6 | 5/10 → 2/4 | 0.60 → 1.50 | Qdrant robust / Qdrant robust | 0 | 1 / 1 | budget / **stable** | Same full coverage. Adaptive's whole saving is the stop rule (it stopped after round 0 and made no targeted actions). |
| Q2 | discovery | 0/5 | 1/5 | 15 → 15 | 5/10 → 5/10 | 0.47 → 0.73 | n/a | n/a | 0 / 0 | budget / budget | Adaptive +1 entity; both far from complete |
| Q3 | comparison | 3/8 | 3/8 | 15 → 12 | 5/10 → 4/8 | 0.20 → 0.25 | Single-agent provisional (both) | 0 | 1 / 1 | budget / no_progress | **No coverage benefit** |
| Q4 | comparison | 0/9 | 0/9 | 15 → 9 | 5/10 → 3/6 | 0 → 0 | none | 0 | 0 / 0 | insufficient / insufficient | **Failed in both arms** (see §3.1) |
| Q5 | comparison | 1/8 | 4/8 | 15 → 15 | 5/10 → 5/10 | 0.07 → 0.27 | none / Managed provisional | 0 | 0 / 1 | budget / budget | Adaptive +3 cells. The baseline order partly explains this (see §3.3). |
| Q8 | discovery | 1/5 | 1/5 | 15 → 12 | 5/10 → 4/8 | 0.53 → 0.58 | n/a | n/a | 0 / 0 | budget / no_progress | **No coverage benefit** |

**Research actions and reasons:** every selection, with its priority score, flip relevance, query and stop reason, is listed in `EVALUATION_REPORT.md` → "Research actions and selection reasons" and in `actions.jsonl`. Examples:
- **Q5:** `Managed vector databases:operations_effort` was chosen with priority 10 (weight 5, width 2, flip-relevant). It found nothing at first, succeeded on the open-query retry, and gave a status change via EV_2–EV_4.
- **Q4:** `Persistent customer-profile memory:privacy_risk` was chosen with priority 6 (flip-relevant). No evidence survived.

## 3. Overall comparison (sums over 6 questions; descriptive only)

| Metric | Static | Adaptive |
|---|---|---|
| Requirement units supported | 14 / 44 | 18 / 44 |
| Research actions (searches + pages) | 90 (30 + 60) | 69 (23 + 46) |
| Verified evidence / rejected candidates | 34 / 82 | 43 / 56 |
| LLM requests / tokens (attributed) | 50 / 276,021 | 37 / 212,848 |
| Exa cost, attributed (USD, provider-reported) | 0.270 | 0.207 |
| Tool / LLM attempt errors | 0 / 0 | 0 / 0 |
| Confirmed decision flips | 0 | 0 |

- **Actual spend for the whole evaluation**, each provider call counted once: 151 calls, **Exa $0.358**, **gateway-reported LLM cost $0.060**, 381,337 tokens. This comes from `spend.json`. Note that the gateway's `usage.cost` was 0.0 in an earlier run, so check it against the provider's billing page.
- **Elapsed time:** static 736 s and adaptive 259 s, but **these are not comparable**. Adaptive reused the cached round-0 responses, so they are excluded from this comparison.
- **Outcome tally:**

| Outcome | Questions |
|---|---|
| Adaptive better coverage | 2 (Q2, Q5) |
| Same full coverage, adaptive used fewer actions | 1 (Q1) |
| No coverage benefit | 3 (Q3, Q4, Q8) |
| Adaptive worse coverage | 0 |

**What can and cannot be said.** In this single sample, adaptive never lost coverage and used 23% fewer research actions in total. It gained coverage on 2 of 6 questions. That is a small, descriptive result: one run per arm, with high variance between runs (§4). It is **not** evidence that decision-flip targeting improves research. The main reasons:
- **No confirmed decision flip occurred** in any of the 12 runs.
- Most of the saved actions come from **stopping early** (Q1 stopped after round 0; Q3 and Q8 stopped at `no_progress` with the same incomplete coverage).
- The Q5 gain is partly explained by the baseline's order (§4.3).

## 4. Serious problems found (ranked)

### 4.1 The lexical entity check fails for approach-type alternatives (serious, systematic)

The deterministic check requires the alternative's name or an alias to appear in the excerpt's context. That works for products ("Qdrant") but not for planner-coined approach labels ("Session-only context memory", "Managed vector databases").

Lexical rejections per question (both arms):

| Q1 | Q2 | Q3 | Q4 | Q5 | Q8 |
|---|---|---|---|---|---|
| 0 | 7 | 10 | **34** | **41** | 12 |

Q4 verified **zero** evidence in either arm, even though the verifier had accepted many of these excerpts. As a result, **for Q3–Q5 the evaluation mostly measures this filter, not the policy.**

**Proposed fix (not applied; changing it would invalidate this recording):**
- Have the planner give approach-type alternatives a set of descriptive keyword aliases, *or*
- Apply the lexical check only to named entities (products and companies), and rely on the verifier's `mentions_alternative` for approaches.

Either way, the fix needs a regression test and a full re-recording.

### 4.2 Q1's "robust" recommendation is not factually reliable (serious, factual)

Each cell rests on a single excerpt, and the decisive operational-effort scores are asymmetric:

| Option | Score | Evidence used |
|---|---|---|
| Qdrant | 2 | Managed-cloud docs |
| Weaviate | 1 | A third-party weaknesses list |
| Milvus | 0 | A self-hosting complaint |

Both Weaviate (EV_4 in the same run) and Milvus (Zilliz Cloud) also offer managed options, which the rubric's "strong" anchor explicitly credits. So the tool reports "robust" for a conclusion that depends on which excerpt each cell happened to find. "Robust under the rubric" is correctly defined, but here it can look like a factual verdict.

**Mitigations to consider:**
- Require 2 or more verified items (or 2 or more domains) before a cell counts as `supported`.
- Require factual confidence of `high` before reporting `robust`.
- Have the verifier check score consistency across alternatives.

### 4.3 The static baseline's order disadvantages static on comparisons (methodological)

Static follows the plan order: every criterion of the first alternative, then the next alternative. Within 3 rounds it only ever researches the **first** alternative:
- In Q1, Q3, Q4 and Q5, all of static's targeted actions went to alternative 1.
- In Q5, static researched only "Managed …" cells; adaptive researched both options.

A round-robin or randomized static order would be a fairer baseline. Until then, the Q5 coverage gain cannot be credited to decision-flip targeting.

### 4.4 Discovery coverage is very strict and the static discovery queries are weak (methodological)

- An entity counts only when all 4 facets are verified. Q2 adaptive verified 20 evidence items but just 1 complete company.
- Static's discovery queries are raw facet descriptions with no question context (e.g. "Company is headquartered in India; include evidence…"). They are poor search queries, so the static discovery arm is a weak baseline.

### 4.5 Smaller issues

- **Single run per arm.** Earlier Q1 runs gave different criteria, evidence and stop reasons, so `--repeat 3` is needed for any stable comparison.
- **Over-reading single sources.** 7 of the 12 runs have one source supporting 3 or more targets (flagged in the review sheet).
- **Score saturation.** Qdrant scored 2 on every Q1 criterion in every Q1 run so far.
- **Elapsed time** is confounded by caching (above).
- **Gateway cost.** `usage.cost` may not reflect real billing. Exa costs are provider-reported.

## 5. Not done (needs a human)

- Human 0/1/2 scores (`review/AI_PROVISIONAL_REVIEW.md` has blank columns plus every accepted excerpt to check).
- Checking wrongly rejected evidence, especially Q4 and Q5.
- The demo video.
