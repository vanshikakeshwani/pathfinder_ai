# Research report - EVAL_Q1_r2_adaptive_20261030T052052_62dd99

**Question:** Compare Qdrant, Weaviate, and Milvus for a small team building RAG; consider deployment, filtering and operational effort.

**Short answer:** Qdrant leads provisionally, but score intervals overlap (Qdrant [9,18], Weaviate [9,15], Milvus [3,9]); current evidence does not force a unique recommendation. The comparison turns mainly on how much infrastructure a small team wants to operate and how selective its metadata filters are. Evidence is strongest for deployment and operational trade-offs; it does not establish a like-for-like performance or cost comparison across all three.

| Mode | Status | Stop reason | Confidence | Factual confidence | Decision stability |
|---|---|---|---|---|---|
| comparison | partial | budget_exhausted | low | low | provisional |

_Confidence rule: confidence = min(interval stability, lowest factual confidence among the leader's supported/disputed cells); robust/high=high, provisional/moderate=moderate, otherwise low. A withheld recommendation caps confidence at moderate, and at low when the withholding is due to non-comparable evidence._

**Requirement coverage:** 6/9 units with verified support.

## Recommendation readiness

- Interval leader: Qdrant (provisional)
- Recommendation: **withheld**
  - withheld because: score intervals overlap (provisional leader only)
  - withheld because: differentiating cells lack strong support (single source or non-official): Qdrant:filtering_capability, Milvus:filtering_capability

## Decision matrix

_Cell = score (evidence; independent sources; scope)._

| Alternative | deployment_fit (w3, default) | filtering_capability (w3, default) | operational_effort (w3, default) | LB | UB |
|---|---|---|---|---|---|
| Qdrant (named) | disputed [0,2] (EV_1, EV_2, EV_9, EV_17; 3 src; managed/self_hosted) | 2 (EV_3; 1 src) | scope-dependent [1,2] (managed=2, self_hosted=1) (EV_10, EV_11, EV_18, EV_19; 2 src; managed/self_hosted) | 9 | 18 |
| Weaviate (named) | 2 (EV_4, EV_5; 1 src; managed/self_hosted) | disputed [0,2] (EV_6, EV_12; 2 src) | 1 (EV_13, EV_14; 2 src; self_hosted) | 9 | 15 |
| Milvus (named) | disputed [0,2] (EV_8, EV_15; 2 src; self_hosted) | 1 (EV_7; 1 src) | 0 (EV_16; 1 src; self_hosted) | 3 | 9 |

### Scoring rules

- **deployment_fit** (higher_is_better, weight 3 [default]): 0 = Deployment options or setup are a poor fit for a small RAG team and require substantial commitment or adaptation.; 1 = Offers a workable deployment path, though setup or hosting choices may involve notable trade-offs for a small team.; 2 = Provides a clear, practical deployment path for a small RAG team with suitable hosting choices and manageable setup.; scopes ['managed', 'self_hosted']
- **filtering_capability** (higher_is_better, weight 3 [default]): 0 = Filtering is limited or awkward for common RAG metadata and query-time filtering needs.; 1 = Supports common filtering needs, with some meaningful limitations or added complexity.; 2 = Provides flexible, well-supported filtering that readily accommodates common RAG retrieval patterns.
- **operational_effort** (lower_is_better, weight 3 [default]): 0 = Requires substantial ongoing specialist effort or operational work that is difficult for a small team to sustain.; 1 = Operational effort is manageable for a small team but involves notable ongoing maintenance or expertise.; 2 = Keeps routine operational work low and is practical for a small team to maintain.; scopes ['managed', 'self_hosted']

## Findings

- Qdrant offers a simple persistent Docker quickstart and a small managed free tier, though the free tier has resource limits and can be suspended after inactivity. Its filtering approach integrates metadata constraints into HNSW traversal, including for highly selective filters. [EV_1, EV_2, EV_3]
  - EV_1 (SRC_3, chars 5923-6002, score 2 via verified_proposal, scope self_hosted): "Qdrant’s quickstart is one `docker run` with a mounted `qdrant_storage` volume."
    - rubric rationale: The one-command quickstart with a mounted volume is a clear, practical self-hosted setup path, matching the strong anchor.
  - EV_2 (SRC_3, chars 5037-5208, score 1 via verified_proposal, scope managed): "Managed free tier | Qdrant Cloud: 1 node, 0.5 vCPU, 1 GB RAM, 4 GB disk, about 1M 768-dimension vectors, no card; suspended after 1 week idle, deleted after 4 (Cloud docs)"
    - rubric rationale: The free managed tier provides a workable hosting choice, but its small resource limits and idle suspension are notable trade-offs for a team evaluating a production path.
  - EV_3 (SRC_2, chars 2934-3204, score 2 via verified_proposal): "Qdrant's ACORN approach folds metadata filtering directly into the HNSW graph traversal instead of filtering after the search. That keeps queries fast even when a filter eliminates 99% of candidates, which is the exact scenario that makes naive vector search fall apart."
    - rubric rationale: The excerpt describes filter-aware traversal and strong performance under highly selective filtering, directly supporting flexible filtering for common RAG retrieval patterns.
- Self-hosting Qdrant leaves backups, monitoring, scaling, and failure recovery to the team; the supplied estimate is 10–20 engineering hours per month. Managed Cloud is presented as removing infrastructure management, so deployment choice substantially changes the operational burden. [EV_9, EV_10, EV_11, EV_18, EV_19]
  - EV_9 (SRC_6, chars 4343-4496, score 1 via verified_proposal, scope self_hosted): "Docker deployment is straightforward, Kubernetes helm charts work, but you're responsible for backups, monitoring, scaling, and recovering from failures."
    - rubric rationale: Plausible: Docker and Kubernetes Helm provide workable deployment paths, but the team must handle backups, monitoring, scaling, and failure recovery.
  - EV_10 (SRC_6, chars 4300-4588, score 1 via verified_proposal, scope self_hosted): "The trade-off: you're running it yourself. Docker deployment is straightforward, Kubernetes helm charts work, but you're responsible for backups, monitoring, scaling, and recovering from failures. The distributed mode works but isn't as battle-tested as Pinecone's managed infrastructure."
    - rubric rationale: Plausible: the excerpt identifies notable ongoing maintenance responsibilities and a less battle-tested distributed mode, but does not establish that the work is unsustainable for a small team.
  - EV_11 (SRC_6, chars 9238-9385, score 1 via verified_proposal, scope self_hosted): "Note: self-hosted costs include compute only. Add 10-20 hours/month of engineering time for maintenance, monitoring, and the occasional 2 AM alert."
    - rubric rationale: Plausible: the excerpt quantifies notable ongoing maintenance and monitoring effort, without saying it is impossible for a small team to sustain.
  - EV_18 (SRC_9, chars 4511-4630, score 2 via verified_proposal, scope managed): "No Infrastructure Management | Qdrant fully manages your infrastructure, so you can focus on building your application."
    - rubric rationale: Strong anchor: the excerpt explicitly says Qdrant fully manages the infrastructure, reducing routine operational work for a small team.
  - EV_19 (SRC_9, chars 9369-9482, score 1 via verified_proposal, scope self_hosted): "In self-hosted deployments, you must manually create or drop replicas and move shards between nodes as you scale."
    - rubric rationale: Plausible anchor: the excerpt identifies ongoing manual scaling tasks, indicating notable maintenance, but does not show that the work is unsustainable for a small team.
- Weaviate offers managed Cloud and a documented path from Docker experimentation to Kubernetes. Its filtering combines inverted-index pre-filtering, ACORN traversal, and a brute-force cutoff. The evidence also flags resource and latency variability concerns, including one report of memory pressure and debugging at 8 million vectors; these are not a controlled comparison. [EV_4, EV_5, EV_6, EV_12, EV_13]
  - EV_4 (SRC_1, chars 1171-1366, score 2 via verified_proposal, scope managed): "Weaviate Cloud - From evaluation (free tier) to production - Shared Cloud (infrastructure managed by Weaviate) - (Optional) Data replication (high-availability) - (Optional) Zero-downtime updates"
    - rubric rationale: The managed cloud option spans evaluation through production and identifies provider-managed infrastructure, giving a small team a clear hosting path.
  - EV_5 (SRC_1, chars 3165-3350, score 2 via verified_proposal, scope self_hosted): "If you are self-hosting, consider experimenting on a small scale with Docker and then transferring your configuration to Kubernetes Helm charts when you are more familiar with Weaviate."
    - rubric rationale: The excerpt gives a concrete path to begin at small scale and move to Kubernetes as needs or familiarity grow, matching a practical deployment path.
  - EV_6 (SRC_3, chars 9021-9214, score 2 via verified_proposal): "Weaviate pre-filters through its inverted index into an allow-list, walks HNSW with ACORN (default `filterStrategy` since v1.34), and uses brute force below `flatSearchCutoff` (default 40,000)."
    - rubric rationale: The excerpt describes several integrated mechanisms for filtered retrieval, including a defined strategy for smaller result sets, supporting flexible and well-supported filtering.
  - EV_12 (SRC_6, chars 6378-6584, score 1 via verified_proposal): "The trade-off: it's hungry for resources and the performance isn't quite in Qdrant's league. That 6.8 GB/million vectors adds up fast, and the query latency with filtering shows more variance than I'd like."
    - rubric rationale: Plausible: the excerpt indicates filtered queries work but reports a meaningful performance concern; it does not characterize the flexibility or usability of the filtering features.
  - EV_13 (SRC_6, chars 2478-2843, score 1 via verified_proposal, scope self_hosted): "That Weaviate memory number — 6.8 GB per million vectors — is what almost killed us. We had 8 million vectors and Weaviate was eating 54 GB of RAM. Our Kubernetes pods kept getting OOM-killed. We ended up enabling PQ (product quantization) compression which brought it down to manageable levels, but it took a weekend of debugging to figure out why pods were dying."
    - rubric rationale: Plausible: the excerpt documents significant troubleshooting in a self-hosted Kubernetes deployment, but also says the issue was brought to manageable levels.
- Milvus supports pre-search filtering and iterative processing for complex expressions, but the cited self-hosted setup has substantial hardware requirements and involves multiple services and supporting stores to operate. The evidence does not establish its managed-deployment options or effort for a small team. [EV_7, EV_8, EV_15, EV_16]
  - EV_7 (SRC_3, chars 9215-9329, score 1 via verified_proposal): "Milvus restricts the search scope to matching entities before search, with iterative mode for complex expressions."
    - rubric rationale: The excerpt shows support for common filtering and complex expressions, but gives limited detail about flexibility or usability compared with the strong anchor.
  - EV_8 (SRC_3, chars 5710-5922, score 1 via verified_proposal, scope self_hosted): "Milvus Standalone’s Docker requirements ask for at least 4 cores and 8 GB of RAM (16 GB recommended), a CPU with SSE4.2, AVX, AVX2 or AVX-512, and etcd on a disk with more than 500 IOPS and p99 fsync under 10 ms."
    - rubric rationale: The requirements show a workable self-hosted option, but its hardware, CPU-feature, and etcd storage prerequisites are notable trade-offs for a small team.
  - EV_15 (SRC_7, chars 5251-5486, score 0 via verified_proposal, scope self_hosted): "The minimum production deployment has, depending on how you count, six or seven separate services plus etcd plus MinIO or S3. For 40M vectors, this is overkill in the worst way: you pay the operational cost without getting the benefit."
    - rubric rationale: Poor: the excerpt describes a substantial multi-service production deployment and explicitly calls it overkill at the stated scale, a difficult fit for a small RAG team.
  - EV_16 (SRC_7, chars 4927-5250, score 0 via verified_proposal, scope self_hosted): "Milvus is the option for billion-vector workloads. The architecture is impressive — separate components for query nodes, data nodes, index nodes, root coordinator, an external object store for cold data, an external metadata store. It scales to scales I do not have. It also requires you to operate all of those components."
    - rubric rationale: Poor: the excerpt describes multiple components that must all be operated, a substantial operational burden for a small team.

## Decision changes (attributed to newly verified evidence)

- Round 0: stability_changed None/undetermined -> Weaviate/provisional via EV_1, EV_2, EV_3, EV_4, EV_5, EV_6, EV_7, EV_8
- Round 2: leader_changed Weaviate/provisional -> Qdrant/undetermined via EV_9, EV_10, EV_11, EV_12, EV_13, EV_14, EV_15, EV_16
- Round 3: stability_changed Qdrant/undetermined -> Qdrant/provisional via EV_17, EV_18, EV_19

Decision flips: 1; status changes: 2

## Sources

- SRC_1: [Deploying Weaviate | Weaviate Documentation](https://docs.weaviate.io/deploy) - retrieved 2026-10-30T05:20:52+00:00
- SRC_2: [Qdrant vs Weaviate vs Milvus: Which Vector Database for Your RAG Pipeline?](https://blog.elest.io/qdrant-vs-weaviate-vs-milvus-which-vector-database-for-your-rag-pipeline/) - retrieved 2026-10-30T05:20:52+00:00, published 2026-03-11T08:00:14.000Z
- SRC_3: [Qdrant vs Weaviate vs Milvus: Recall, RAM, and Scale](https://vectoropsreport.com/posts/qdrant-vs-weaviate-vs-milvus/) - retrieved 2026-10-30T05:20:52+00:00, published 2026-08-27T00:00:00.000Z
- SRC_6: [I've Used Pinecone, Weaviate, and Qdrant in Production. Here's What I'd Pick.](https://augustyniak.ai/blog/vector-databases-comparison-guide) - retrieved 2026-10-30T05:21:33+00:00, published 2024-12-25T22:02:46.000Z
- SRC_7: [Why I Run Qdrant in Production: A 3-Node Cluster vs the Alternatives — Makmel](https://makmel.info/blog/2026-04-25-qdrant-vector-db-production) - retrieved 2026-10-30T05:21:33+00:00, published 2026-03-20T22:10:39.000Z
- SRC_8: [Deploy Qdrant](https://qdrant.tech/documentation/deploy-intro/) - retrieved 2026-10-30T05:22:52+00:00
- SRC_9: [Overview - Qdrant](https://qdrant.tech/documentation/overview/) - retrieved 2026-10-30T05:22:52+00:00

## Assumptions

- The team has limited operational capacity, but no specific team size or infrastructure expertise was given.
- The intended workload is a typical RAG application using vector search with metadata filters; scale, latency, and availability requirements were not specified.
- Both managed and self-hosted deployments should be considered because the user did not state a hosting preference.
- No stated priority for deployment_fit, filtering_capability, operational_effort: equal default weight 3.

## Limitations

- Fit scores (0/1/2) are model-assisted assessments under the disclosed rubric and weights, not measurements.
- Support verification uses the same model family as extraction; it is not ground truth and needs human audit.
- 'Robust' means interval dominance under the chosen criteria and weights, not that the option is factually best.
- Single-source support (one independent source): Qdrant:filtering_capability, Weaviate:deployment_fit, Milvus:filtering_capability, Milvus:operational_effort.
- Disputed (conflicting verified evidence, interval [0,2]): Qdrant:deployment_fit, Weaviate:filtering_capability, Milvus:deployment_fit.
- 14 extracted candidate(s) were rejected by grounding/verification (see verification_log.jsonl).
- Stopped: budget_exhausted (MAX_RESEARCH_ROUNDS=3 reached).

## Next steps

- Compare current managed-service pricing, quotas, and production limits for all three using the team's expected vector count and query volume.
- Benchmark representative RAG queries with the team's metadata filters, measuring latency, recall, and resource use on comparable configurations.
- Validate production deployment and backup/recovery procedures for the shortlisted options, including what the team must operate versus what the provider manages.

## Budget

Searches 5/6, content pages 10/12, LLM requests 9, elapsed 168.92 s. LLM: gpt-6-luna (record).
