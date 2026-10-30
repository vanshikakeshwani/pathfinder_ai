# Post-fix (v3.2) retrospective re-scoring of the V3.1 pilot evidence

> **NOT a new controlled live benchmark.** The 9 V3.1 pilot runs' saved, verified evidence is re-aggregated with the v3.2 rules (cost-dimension classification of the scored quantity, word-bounded patterns, product-heterogeneity flags) and compared with the v3.1 result of the same evidence. No API call; the pilot's own artifacts are unchanged (`V31_PILOT_ARTIFACTS_SHA256.txt`). Trajectories were chosen under v3.1.

## Per run

| Q | arm | strict old → new | consensus old → new | total supported old → new | leader old → new | stability old → new | recommendation old → new |
|---|---|---|---|---|---|---|---|
| Q1 | static | 6 → 6 | 0 → 0 | 6 → 6 | Qdrant → Qdrant | robust → robust | withheld → withheld |
| Q1 | v2_policy | 6 → 6 | 0 → 0 | 6 → 6 | Weaviate → Weaviate | provisional → provisional | withheld → withheld |
| Q1 | adaptive | 7 → 7 | 0 → 0 | 7 → 7 | Qdrant → Qdrant | provisional → provisional | withheld → withheld |
| Q4 | static | 9 → 9 | 0 → 0 | 9 → 9 | Session-only memory → Session-only memory | provisional → provisional | withheld → withheld |
| Q4 | v2_policy | 9 → 9 | 0 → 0 | 9 → 9 | Session-only memory → Session-only memory | provisional → provisional | withheld → withheld |
| Q4 | adaptive | 9 → 9 | 1 → 1 | 10 → 10 | Session-only memory → Session-only memory | provisional → provisional | withheld → withheld |
| Q5 | static | 2 → 2 | 1 → 1 | 3 → 3 | Managed vector database → Managed vector database | provisional → provisional | withheld → withheld |
| Q5 | v2_policy | 5 → 5 | 1 → 1 | 6 → 6 | Managed vector database → Managed vector database | robust → robust | withheld → withheld |
| Q5 | adaptive | 5 → 5 | 0 → 0 | 5 → 5 | Managed vector database → Managed vector database | robust → robust | withheld → withheld |

## Cost-dimension changes (evidence level)

- Q5_r1_adaptive `EV_4` Self-hosted vector database:startup_cost (score 0): engineering_labour → **total_cost_of_ownership** — "However, self-hosting does not mean the database is free. It shifts costs from the vendor bill to infrastructure spend a"
- Q5_r1_adaptive `EV_8` Managed vector database:startup_cost (score 1): engineering_labour → **total_cost_of_ownership** — "If you have no dedicated infra/SRE capacity, a managed service is almost always cheaper once engineering time is priced "
- Q5_r1_adaptive `EV_9` Managed vector database:startup_cost (score 1): engineering_labour → **recurring_infrastructure** — "Cost. The s1.x1 pod sufficient for our index ran ~$70/mo per pod, and we needed 2 for redundancy. Add metadata filtering"
- Q5_r1_adaptive `EV_14` Self-hosted vector database:startup_cost (score 0): recurring_infrastructure → **total_cost_of_ownership** — "The infrastructure is $530/month. The real cost is $3,530/month. That's what the pricing comparisons miss."
- Q5_r1_static `EV_4` Self-hosted vector database:startup_cost (score 0): engineering_labour → **total_cost_of_ownership** — "However, self-hosting does not mean the database is free. It shifts costs from the vendor bill to infrastructure spend a"
- Q5_r1_v2_policy `EV_4` Self-hosted vector database:startup_cost (score 0): engineering_labour → **total_cost_of_ownership** — "However, self-hosting does not mean the database is free. It shifts costs from the vendor bill to infrastructure spend a"
- Q5_r1_v2_policy `EV_8` Managed vector database:startup_cost (score 1): engineering_labour → **total_cost_of_ownership** — "If you have no dedicated infra/SRE capacity, a managed service is almost always cheaper once engineering time is priced "
- Q5_r1_v2_policy `EV_9` Managed vector database:startup_cost (score 1): engineering_labour → **recurring_infrastructure** — "Cost. The s1.x1 pod sufficient for our index ran ~$70/mo per pod, and we needed 2 for redundancy. Add metadata filtering"

## Changed or flagged cells

- **Q5_r1_adaptive `Managed vector database:startup_cost`**: supported (None) [1, 1] conf moderate dims ['engineering_labour'] → **supported (None) [1, 1]** conf moderate dims ['recurring_infrastructure', 'total_cost_of_ownership']. all families agree
- **Q5_r1_adaptive `Self-hosted vector database:startup_cost`**: disputed (independent_disagreement) [0, 1] conf low dims ['engineering_labour', 'recurring_infrastructure'] → **scope_dependent (dimension_mismatch) [0, 1]** conf high dims ['recurring_infrastructure', 'total_cost_of_ownership']. cost evidence measures different dimensions: recurring_infrastructure=1, total_cost_of_ownership=0; not pooled into one score
- **Q5_r1_static `Managed vector database:startup_cost`**: consensus (weak) [1, 1] conf moderate dims ['recurring_infrastructure'] → **consensus (heterogeneous) [1, 1]** conf moderate dims ['recurring_infrastructure']; heterogeneous products {'adaptiverecall.com': ['Pinecone', 'Qdrant'], 'zilliz.com': ['Zilliz'], 'dev.to': ['Weaviate']}; ambiguous dimension. qualified consensus: 2 supporting vs 1 dissenting families (2 with certain independence); dissent retained
- **Q5_r1_static `Self-hosted vector database:startup_cost`**: scope_dependent (dimension_mismatch) [0, 1] conf high dims ['engineering_labour', 'recurring_infrastructure'] → **scope_dependent (dimension_mismatch) [0, 1]** conf high dims ['engineering_labour', 'recurring_infrastructure', 'total_cost_of_ownership']. cost evidence measures different dimensions: engineering_labour=0, recurring_infrastructure=1, total_cost_of_ownership=0; not pooled into one score
- **Q5_r1_v2_policy `Managed vector database:startup_cost`**: supported (None) [1, 1] conf moderate dims ['engineering_labour', 'recurring_infrastructure'] → **supported (None) [1, 1]** conf moderate dims ['recurring_infrastructure', 'total_cost_of_ownership']. all families agree
- **Q5_r1_v2_policy `Self-hosted vector database:startup_cost`**: supported (None) [0, 0] conf moderate dims ['engineering_labour'] → **supported (None) [0, 0]** conf moderate dims ['total_cost_of_ownership']. all families agree

## Readiness reasons after the fix

- Q1 static: withheld — differentiating cells lack strong support (single source or non-official): Qdrant:filtering_capability, Milvus:filtering_capability; Qdrant's advantage on deployment_fit rests only on Qdrant's own (self-reported) claims
- Q1 v2_policy: withheld — score intervals overlap (provisional leader only); differentiating cells lack strong support (single source or non-official): Weaviate:filtering_capability, Milvus:filtering_capability; critical criterion operational_effort (weight 5) has no supported score for Weaviate
- Q1 adaptive: withheld — score intervals overlap (provisional leader only); Qdrant's advantage on deployment_fit rests only on Qdrant's own (self-reported) claims; Qdrant's own score on filtering_capability is disputed (verified scores [1, 2])
- Q4 static: withheld — score intervals overlap (provisional leader only); differentiating cells lack strong support (single source or non-official): Session-only memory:retrieval_effectiveness, Persistent conversation-log retrieval:retrieval_effectiveness, Hybrid layered memory:retrieval_effectiveness, Session-only memory:privacy_protection
- Q4 v2_policy: withheld — score intervals overlap (provisional leader only); differentiating cells lack strong support (single source or non-official): Session-only memory:retrieval_effectiveness, Persistent conversation-log retrieval:retrieval_effectiveness, Hybrid layered memory:retrieval_effectiveness, Session-only memory:privacy_protection, Persistent conversation-log retrieval:privacy_protection
- Q4 adaptive: withheld — score intervals overlap (provisional leader only); differentiating cells lack strong support (single source or non-official): Session-only memory:retrieval_effectiveness, Persistent conversation-log retrieval:retrieval_effectiveness, Session-only memory:privacy_protection, Persistent conversation-log retrieval:privacy_protection; Summarized customer-profile memory:retrieval_effectiveness rests on a weak qualified consensus (dissent disclosed; needs more independent agreement)
- Q5 static: withheld — score intervals overlap (provisional leader only); Managed vector database's own score on control_and_customization is disputed (verified scores [0, 1]); Managed vector database:startup_cost rests on prices of different named products/plans; they are examples, not one comparable category-level cost; Managed vector database:startup_cost includes cost evidence whose dimension (infrastructure, labour, total, ...) cannot be determined
- Q5 v2_policy: withheld — differentiating cells lack strong support (single source or non-official): Managed vector database:startup_cost, Self-hosted vector database:startup_cost, Self-hosted vector database:control_and_customization; Self-hosted vector database:operational_effort rests on a weak qualified consensus (dissent disclosed; needs more independent agreement)
- Q5 adaptive: withheld — differentiating cells lack strong support (single source or non-official): Self-hosted vector database:control_and_customization
