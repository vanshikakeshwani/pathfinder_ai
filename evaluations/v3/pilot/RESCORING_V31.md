# Retrospective offline re-scoring of V3 pilot evidence (v3.1 aggregation)

> **NOT a new controlled live benchmark.** Each pilot run's saved, verified evidence is re-aggregated with the v3.1 rules; no API call is made and no original artifact is modified (`HISTORICAL_ARTIFACTS_SHA256.txt` verifies this). The research trajectories were chosen under the pilot rules, so live v3.1 runs could follow different paths. Nothing here shows that V3 performs better.

Supported = cells with a single comparable score or a scope-dependent split (v3.1 excludes cells whose cost evidence measures incompatible dimensions). Old figures are the pilot's own (`rescoring_baseline_pilot_rules.json`).

## Per run

| Q | arm | supported old → new | consensus (new) | disputed old → new | leader old → new | stability old → new | recommendation old → new |
|---|---|---|---|---|---|---|---|
| Q1 | static | 5 → 5 | 0 | 2 → 2 | Qdrant → Qdrant | provisional → provisional | withheld → withheld |
| Q1 | v2_policy | 4 → 4 | 0 | 3 → 3 | Milvus → Milvus | provisional → provisional | withheld → withheld |
| Q1 | adaptive | 5 → 5 | 0 | 2 → 2 | Qdrant → Qdrant | provisional → provisional | withheld → withheld |
| Q4 | static | 8 → 8 | 0 | 1 → 1 | Summarized customer-profile memory → Summarized customer-profile memory | provisional → provisional | withheld → withheld |
| Q4 | v2_policy | 11 → 11 | 0 | 1 → 1 | Hybrid layered memory → Hybrid layered memory | provisional → provisional | withheld → withheld |
| Q4 | adaptive | 11 → 11 | 0 | 1 → 1 | Hybrid layered memory → Hybrid layered memory | provisional → provisional | withheld → withheld |
| Q5 | static | 3 → 4 | 1 | 3 → 2 | Managed vector database → Managed vector database | undetermined → provisional | none → withheld |
| Q5 | v2_policy | 2 → 5 | 3 | 4 → 1 | Managed vector database → Managed vector database | provisional → robust | withheld → withheld |
| Q5 | adaptive | 1 → 3 | 2 | 5 → 2 | Managed vector database → Managed vector database | provisional → robust | withheld → withheld |

Totals, supported cells (old → new): static 16 → 17; v2_policy 17 → 20; adaptive 17 → 19

## Changed cells

- **Q1 static:**
  - `Weaviate:deployment_fit`: disputed [1, 2] [1,2] → **disputed** (source_inconsistent) [1,2]; families 1 (1 certain). not resolved: the only assessment(s) are internally inconsistent source families
- **Q1 v2_policy:**
  - `Weaviate:deployment_fit`: disputed [1, 2] [1,2] → **disputed** (source_inconsistent) [1,2]; families 1 (1 certain). not resolved: the only assessment(s) are internally inconsistent source families
- **Q1 adaptive:**
  - `Weaviate:deployment_fit`: disputed [1, 2] [1,2] → **disputed** (source_inconsistent) [1,2]; families 1 (1 certain). not resolved: the only assessment(s) are internally inconsistent source families
- **Q4 static:** no cell changed state or interval.
- **Q4 v2_policy:** no cell changed state or interval.
- **Q4 adaptive:** no cell changed state or interval.
- **Q5 static:**
  - `Self-hosted vector database:operational_effort`: disputed [0, 1] [0,1] → **consensus** (strong) [0,0]; families 4 (4 certain). qualified consensus: 3 supporting vs 1 dissenting families (3 with certain independence); dissent retained
  - utility intervals: {'Managed vector database': [10, 19], 'Self-hosted vector database': [12, 17]} → {'Managed vector database': [10, 19], 'Self-hosted vector database': [12, 12]}
- **Q5 v2_policy:**
  - `Managed vector database:control_and_customization`: disputed [0, 1] [0,1] → **consensus** (weak) [1,1]; families 3 (2 certain). qualified consensus: 2 supporting vs 1 dissenting families (2 with certain independence); dissent retained
  - `Self-hosted vector database:operational_effort`: disputed [0, 1] [0,1] → **consensus** (weak) [0,0]; families 4 (3 certain). qualified consensus: 3 supporting vs 1 dissenting families (2 with certain independence); dissent retained
  - `Self-hosted vector database:control_and_customization`: disputed [1, 2] [1,2] → **consensus** (weak) [1,1]; families 3 (3 certain). qualified consensus: 2 supporting vs 1 dissenting families (2 with certain independence); dissent retained
  - utility intervals: {'Managed vector database': [10, 19], 'Self-hosted vector database': [6, 14]} → {'Managed vector database': [13, 19], 'Self-hosted vector database': [6, 6]}
- **Q5 adaptive:**
  - `Managed vector database:operational_effort`: disputed [1, 2] [1,2] → **consensus** (strong) [2,2]; families 5 (4 certain). qualified consensus: 4 supporting vs 1 dissenting families (3 with certain independence); dissent retained
  - `Self-hosted vector database:operational_effort`: disputed [0, 1] [0,1] → **consensus** (weak) [0,0]; families 4 (3 certain). qualified consensus: 3 supporting vs 1 dissenting families (2 with certain independence); dissent retained
  - `Self-hosted vector database:startup_cost`: disputed [0, 2] [0,2] → **scope_dependent** (dimension_mismatch) [0,2]; families 2 (2 certain). cost evidence measures different dimensions: engineering_labour=0, recurring_infrastructure=2; not pooled into one score
  - utility intervals: {'Managed vector database': [11, 19], 'Self-hosted vector database': [3, 17]} → {'Managed vector database': [16, 19], 'Self-hosted vector database': [3, 12]}

## Readiness after re-scoring

- Q1 static: withheld — score intervals overlap (provisional leader only); Qdrant's own score on deployment_fit is disputed (verified scores [1, 2])
- Q1 v2_policy: withheld — score intervals overlap (provisional leader only); Milvus's advantage on operational_effort rests only on Milvus's own (self-reported) claims
- Q1 adaptive: withheld — score intervals overlap (provisional leader only); Qdrant's own score on deployment_fit is disputed (verified scores [1, 2])
- Q4 static: withheld — score intervals overlap (provisional leader only); differentiating cells lack strong support (single source or non-official): Summarized customer-profile memory:retrieval_effectiveness, Session-only memory:retrieval_effectiveness
- Q4 v2_policy: withheld — score intervals overlap (provisional leader only); differentiating cells lack strong support (single source or non-official): Hybrid layered memory:retrieval_effectiveness, Session-only memory:retrieval_effectiveness, Persistent conversation-log retrieval:retrieval_effectiveness
- Q4 adaptive: withheld — score intervals overlap (provisional leader only); differentiating cells lack strong support (single source or non-official): Hybrid layered memory:retrieval_effectiveness, Session-only memory:retrieval_effectiveness, Persistent conversation-log retrieval:retrieval_effectiveness
- Q5 static: withheld — score intervals overlap (provisional leader only); Managed vector database's own score on startup_cost is disputed (verified scores [0, 2]); Managed vector database's own score on control_and_customization is disputed (verified scores [0, 1])
- Q5 v2_policy: withheld — Self-hosted vector database:operational_effort rests on a weak qualified consensus (dissent disclosed; needs more independent agreement); Managed vector database's own score on startup_cost is disputed (verified scores [0, 1, 2])
- Q5 adaptive: withheld — Self-hosted vector database:operational_effort rests on a weak qualified consensus (dissent disclosed; needs more independent agreement); Managed vector database's own score on control_and_customization is disputed (verified scores [0, 1])
