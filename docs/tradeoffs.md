# Tradeoffs and deliberate deviations

## Deviations from the blueprint (02_Pathfinder_AI_2.0_Implementation_Blueprint.md)

| Blueprint | Implemented | Why |
|---|---|---|
| OpenAI API, `OPENAI_API_KEY` | Experiential Labs gateway (`gpt-6-luna`, `EXPLABS_API_KEY`) through the OpenAI SDK with `base_url` | Project decision. `smoke-gateway` confirms strict `json_schema`. On 2026-10-29 the `json_object` fallback failed once (the model echoed the schema), so that fallback is not reliable. |
| `MAX_LLM_CALLS=7`, `MAX_SECONDS=90` defaults | Both optional (empty = off) | Rounds and retries are capped, which bounds the run: at most 30 LLM requests with the defaults |
| 5–7 graph nodes | 8 nodes + a `decide` router | A dedicated `verify` node separates grounding from support |
| Stop reasons without `cancelled` | `cancelled` added | Ctrl+C or cancel token produce a deterministic partial report |
| Flip relevance approximated from bounds | Exact single-cell test: pin the cell to 0 and to 2 and compare the outcome leader | Same cost, clearer to explain |
| `ResearchAction.query` | `queries: list[str]` | Round 0 issues several planned queries as one action |
| Static baseline: "generic query per (alternative × criterion)" in plan order | **V2:** a fixed diagonal round-robin over alternatives and criteria, with queries from the **same builder** as adaptive (`queries.py`) | V1 found two confounds. (1) Different query wording: the old static arm lost coverage purely because of phrasing. (2) Alternative-major order: static spent every targeted round on alternative 1. |
| `MAX_NO_PROGRESS=1` | Default 2 | The blueprint allows adjusting this "if justified". In live Q1 (`RUN_20261029T223304_235ce8`), one failed target ended the run with 7/9 cells unknown. |
| Single stopping behaviour | **V2:** one common stop rule for both arms; evaluation runs to the full budget and reports `common_stop` and `full_budget` views | V1 credited early-stopping savings to adaptive targeting. |
| "Robust" = recommendation | **V2:** interval stability and recommendation readiness are separate | V1 Q1 declared Qdrant robust from incomparable evidence (managed-cloud docs vs self-hosting complaints). |
| Disputed cell = [0, 2] | **V3:** [min, max] of the verified scores, still `disputed` and never supported | V2: 18 of 19 disputes were adjacent scores, and [0, 2] erased information, so more sources lowered coverage (`evaluations/v3/DIAGNOSIS_V2.md` R4). |
| Single-cell flip test drives priority | **V3:** graded counterfactual decision factor, plus exact minimal-group analysis (2–4 cells) | V2's binary test found nothing flip-relevant at 22 of 33 adaptive decision points (R2). |
| Retry a failed target until 2 attempts | **V3:** failure memory, one-round cool-down, at most one bounded immediate retry for a uniquely decisive target, query ladder, near-duplicate skip | V2 repeated a failed target 10 times; 3 succeeded (R1). |

## Choices worth defending

- **Disputed cells** were [0, 2] in V2, even when the conflict was only between 1 and 2, so a conflict could never raise a lower bound. V3 keeps [min, max] of the verified scores: the lower bound is the *lowest* verified score, so no credible source is overruled. The cell stays `disputed` and is never counted as supported.
- **Context differences are not disputes (V2).** Evidence for different scopes (managed 2, self-hosted 0) makes a cell `scope_dependent` with interval [min, max]. Such a cell is never targeted, because more research cannot choose the user's context. A `preferred_scope` (when the user's constraints select one) scores only that context.
- **Readiness instead of "two sources for everything" (V2).** Single-source support is disclosed for every cell but blocks a recommendation only when the cell *differentiates* the leader from a competitor. Repeated excerpts on several domains count as one source.
- **Approach identity uses a grounded quote, not the label (V2).** This removes the V1 false-rejection bug, but the quote proves grounding, not meaning. A frozen re-check of V1 candidates found both wrong acceptances and wrong rejections by the verifier (`evaluations/v2/REVERIFY_V1_Q3_Q5.md`).
- **Every model-proposed score needs a rubric rationale (V2)** that the verifier judges against the anchor. Scores derived from thresholds on a verified number need none.
- **Undetermined leader.** With equal midpoints the listed-order leader is kept internally (test D01), never reported as a recommendation. Leader moves while undetermined are not decision changes. Moving from a real leader into a tie with a different listed-order leader *does* count as a flip, under the same rule as D01. The single V2 live flip (Q1 r2) is of this weak kind. The rule was kept, because changing it after seeing results would be post-hoc.
- **Verification is batched**: one call per round. One malformed reply rejects the whole round's candidates (fail closed).
- **Domain diversity is a proxy for independence.** It is cheap and explainable, but it can over-trust syndicated content that is re-worded.
- **No DNS resolution in URL checks.** Exa fetches pages, not this program.

## V3 trade-offs (offline evidence only; live evaluation pending)

- **Stopping vs saving:** V3's stop rule removed all 5 premature stops on the V2 trajectories, but saves 3 actions instead of 30.
- **Cool-down can skip a valuable target:** a readiness target that just failed is skipped for one round when it is not uniquely decisive. V3 then explores a lower-value cell (Q5 r2, round 3, offline).
- **Exploration factors are heuristics:** the ×1.2 bonus and 1/(1 + 0.5n) concentration penalty are uncalibrated and can delay the highest-value target by a round.
- **Group analysis is bounded:** exact minimal groups are searched only up to 4 cells.
- **Stricter readiness:** it would have withheld V2's only "ready" recommendation, because the leader's own control score was disputed.

## V3.1 trade-offs (offline only)

- **Families are publishers:** registrable domain plus copy detection. Reworded syndication is missed, and multi-tenant hosts are marked uncertain rather than guessed.
- **Consensus thresholds are conservative constants:** 2:1 with 2 certain families; strong at 3 families and 3:1. A dissent at the opposite rubric end, or from a first-party source against its own product, or a measured or version-specific dissent, is never outvoted.
- **Cost dimensions are inferred by keywords:** incompatible dimensions are kept apart rather than converted into one score.
- **Weak consensus never makes a recommendation ready.**

## Known limitations from the live diagnostic (`evaluations/v3/diagnostics/RUN_20261030T092400_DIAGNOSTIC.md`)

- **Verifier strictness:** the verifier sometimes rejects on-anchor documentation excerpts as "score not justified" and judges similar excerpts inconsistently across rounds. Rejections now record its note for audit.
- **Literal-name identity:** for named products, the name or an alias must appear near the excerpt. Official pages that don't repeat the name are rejected. An official-domain exemption was tested and rejected because it would accept a competitor quoted on a vendor's own page.
- **First-attempt queries use criterion identifiers:** this can retrieve off-topic official pages (e.g. legal documents for "maintenance responsibilities"). The fix would change the shared, frozen static-baseline queries.

## Production improvements (not done)

- Joint (multi-cell) flip analysis and calibrated priorities from logged outcomes.
- A verifier from a different model family, or an NLI model, plus a human-labelled support and attribution set (especially for approach-type alternatives).
- Persisting the cost per run once the gateway's `usage.cost` is confirmed against billing, and alerting on rejection-rate drift.
- A semantic (not exact-string) query dedup to cut repeated searches.
