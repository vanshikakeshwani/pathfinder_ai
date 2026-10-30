# Live sample outputs (V2)

These are three **real** adaptive runs from the recorded V2 benchmark `eval_v2_E_20261030T045521_1e5cc3`:
- date: 2026-10-30;
- model: `gpt-6-luna` via the Experiential Labs gateway, with Exa for search and contents;
- config fingerprint: `b891d16fe6`, protocol v2.

Each folder holds the complete, unedited outputs of one run:
- `report.md` / `report.json`;
- `decision_trace.jsonl`;
- `matrix.json`;
- `tool_usage.json`;
- `verification_log.jsonl`.

The paired static run of each pair is in the same `outputs/` folder. The offline replay of every run is byte-for-byte identical in decisions and metrics.

The samples were picked to show three different outcomes, not the best ones. Across the benchmark, adaptive did **not** outperform static (see `evaluations/EVALUATION_ANALYSIS.md`).

| Folder | Question | What it shows | Caveats a reader must know |
|---|---|---|---|
| `EVAL_Q5_r1_adaptive_…6f5523` | Q5 managed vs self-hosted (approach alternatives) | Interval-robust after round 0, but recommendation **withheld** because a differentiating cell had one source. Adaptive then ran one `#corroborate` search ("independent review comparison"), got a second independent source, and the recommendation became **ready**. The run stopped as `stable` after 9 of 15 actions. | It is the only "ready" recommendation in 36 runs. Overall confidence is still **low**, and one cell is disputed. The paired static run researched the same cell with different wording, collected 21 accepted excerpts, and ended with four disputed cells and a provisional result. More sources made it *less* settled, so this outcome depends on which sources came back. Cost figures are single anecdotes ($280/mo managed vs $120/mo self-hosted), not a cost comparison. |
| `EVAL_Q1_r2_adaptive_…62dd99` | Q1 Qdrant / Weaviate / Milvus (named products) | Context-aware cells: Qdrant operational effort is `scope-dependent` (managed 2, self-hosted 1) rather than "disputed". Recommendation withheld (overlapping intervals; single-source differentiating cells). It also holds the benchmark's single counted **decision flip**. | The flip (round 2: Weaviate/provisional → Qdrant/**undetermined**) moved into a tie. It counts under the pre-registered rule (a listed-order leader is kept under a tie, test D01), but it is a weak flip: Qdrant only became the provisional leader in round 3. |
| `EVAL_Q4_r1_adaptive_…398ba3` | Q4 conversation-memory designs (approach alternatives) | V2 approach-identity verification: 9 of 12 cells are supported by conceptual evidence, which the V1 lexical check rejected (V1 had 0 cells). | Every supported cell has **one source**. The interval leader (Session-only memory) is provisional and the recommendation is withheld. Adaptive spent all three rounds on Hybrid layered memory cells that were not flip-relevant. |

The V1 samples (protocol v1, config `a37e41b4ef`) are kept unchanged in `v1/`. Synthetic fixture runs never go in this folder.
