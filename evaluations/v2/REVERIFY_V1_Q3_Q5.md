# Phase 1 check: frozen V1 Q3–Q5 candidates through the V2 acceptance layer

- **Input:** `evaluations/v1/frozen_candidates_Q3_Q5.jsonl`. It holds 88 unique candidates, dumped by replaying the unchanged V1 recordings with the unchanged V1 code; the replay reproduced V1 coverage exactly. The V1 recordings were not modified.
- **Method:** one live call per question annotated alternative kinds (all 7 alternatives in Q3–Q5 came back as `approach`). The V2 verifier then judged the identical excerpts and contexts. V1's extractor produced no rubric rationale, so every V1 candidate fails V2's new rationale rule by construction (88/88 rejected under the full V2 rule). To isolate what Phase 1 changed, acceptance is also reported with **only** that rule waived (the "identity/support layer").
- **Output:** `reverify_Q3_Q5.jsonl`, with V1 and V2 outcomes, the verifier's attribution and the identification quote per candidate.
- **Cost:** 13 gateway requests, 81,840 tokens; gateway-reported cost $0.021.

## Outcome of V1's lexical rejections (identity/support layer)

| | Q3 | Q4 | Q5 | Total |
|---|---|---|---|---|
| V1 rejected by the lexical check | 9 | 25 | 35 | 69 |
| → V2 accepts (V1 rejection **unjustified**) | 1 | 4 | 14 | **19** |
| → V2 rejects: verdict `partial` | 6 | 4 | 10 | 20 |
| → V2 rejects: score not justified by the excerpt | 2 | 7 | 2 | 11 |
| → V2 rejects: approach identity (another approach, several, or generic) | 0 | 6 | 5 | 11 |
| → V2 rejects: verdict `irrelevant` | 0 | 4 | 0 | 4 |

Most of the 69 lexical rejections (50, about 72%) were still justified on other grounds. 19 (about 28%) were valid conceptual evidence that V1 discarded only because the planner's label was absent.

## AI-assistant spot check (not human review)

- **Rescued items are mostly genuine.** Examples: "automatically purged when the session ends" (session-only memory, retention); "A managed service hands you an endpoint and credentials. The vendor provisions machines, applies upgrades…" (managed databases, operations effort); "Self-hosting requires DevOps or MLOps engineers…" (self-hosted databases, engineering effort).
- **The verifier still errs in both directions:**
  - "Forgets long-range context abruptly…" and a `clear_session()` code snippet describe *session-only* memory, but were attributed to persistent memory and therefore wrongly rejected.
  - "Fact content arrives masked by default" was accepted for persistent-profile memory, but its identification quote shows the topic rather than the approach.
- **Conclusion:** the identity fix removes a systematic false-rejection bug. Attribution of approach-type alternatives is still only as reliable as the verifier, and the identification-quote check proves grounding, not meaning.
- **Non-determinism:** an earlier run of this same check (discarded only because it lacked the waived-rule column) gave somewhat different per-bucket counts. Verifier outcomes vary between runs.
