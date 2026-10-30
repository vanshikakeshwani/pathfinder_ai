# Live sample outputs

These are three **real** runs from the recorded evaluation `eval_E_20261029T225137_030e78` (2026-10-29, gateway `gpt-6-luna`, Exa, config `a37e41b4ef`). Each folder holds the complete outputs of one adaptive run:
- `report.md` / `report.json`
- `decision_trace.jsonl`
- `matrix.json` or `coverage.json`
- `tool_usage.json`
- `verification_log.jsonl`

The files are unedited.

| Folder | Question | What it shows | Caveats a reader must know |
|---|---|---|---|
| `EVAL_Q1_adaptive_r1_…b5051e` | Q1 Qdrant / Weaviate / Milvus | All 9 cells supported after round 0, so the run stops as `stable` with "Qdrant robust" and no targeted rounds are needed | **The recommendation is not factually reliable.** Qdrant wins only on operational effort (2 vs Weaviate 1 vs Milvus 0). Qdrant's 2 comes from its managed-cloud docs; Weaviate's 1 and Milvus's 0 come from a third-party weaknesses list, even though both also have managed offerings. One excerpt per cell is decisive. See `evaluations/EVALUATION_ANALYSIS.md` §3. |
| `EVAL_Q5_adaptive_r1_…8ca8e4` | Q5 managed vs self-hosted | Flip-relevant targeting (`operations_effort`, priority 10), an open-query retry, then a status change (undetermined → provisional) attributed to EV_2–EV_4 | Only 4 of 8 cells are supported, all from 2 domains, and 25 candidates were rejected (22 by the lexical check). The result is provisional, not a recommendation. |
| `EVAL_Q2_adaptive_r1_…c735ac` | Q2 India HR-tech companies | Discovery mode: entity-targeted follow-ups, and an honest **partial** result (1 of 5 companies verified on all 4 facets) | ZingHR, greytHR and Timelabs lack verified India-HQ evidence in this run (they may well be India-based, but it was not verified). The coverage rule requires every facet. |

Synthetic fixture runs never go in this folder.
