# Research report - EVAL_Q1_adaptive_r1_20261029T225344_b5051e

**Question:** Compare Qdrant, Weaviate, and Milvus for a small team building RAG; consider deployment, filtering and operational effort.

**Short answer:** Qdrant is interval-robust under the disclosed criteria and weights (score intervals: Qdrant [18,18], Weaviate [15,15], Milvus [9,9]). The main differentiators are setup and ongoing administration, alongside each system’s approach to filtered retrieval. The evidence does not quantify costs or test performance on a representative RAG workload.

| Mode | Status | Stop reason | Confidence | Factual confidence | Decision stability |
|---|---|---|---|---|---|
| comparison | complete | stable | moderate | moderate | robust |

_Confidence rule: confidence = min(decision stability, lowest factual confidence among the recommended option's supported/disputed cells); robust/high=high, provisional/moderate=moderate, otherwise low._

## Decision matrix

| Alternative | deployment_fit (w3, default) | filtering_capability (w3, default) | operational_effort (w3, default) | LB | UB |
|---|---|---|---|---|---|
| Qdrant | 2 (EV_1) | 2 (EV_2) | 2 (EV_3) | 18 | 18 |
| Weaviate | 2 (EV_4) | 2 (EV_5) | 1 (EV_6) | 15 | 15 |
| Milvus | 1 (EV_7) | 2 (EV_8) | 0 (EV_9) | 9 | 9 |

### Scoring rules

- **deployment_fit** (higher_is_better, weight 3 [default]): 0 = Deployment choices or setup are a poor fit for a small team and likely require substantial infrastructure work.; 1 = A workable deployment path exists, but entails meaningful setup or compromises for the team's likely needs.; 2 = A straightforward deployment path fits a small team's RAG use case, with suitable hosting options.
- **filtering_capability** (higher_is_better, weight 3 [default]): 0 = Filtering support is limited or awkward for common metadata-filtered RAG retrieval.; 1 = Common metadata filtering is supported, but important query patterns or usability may require workarounds.; 2 = Flexible, well-integrated metadata filtering supports common and more demanding RAG retrieval patterns.
- **operational_effort** (lower_is_better, weight 3 [default]): 0 = Likely requires substantial ongoing administration, infrastructure expertise, or operational overhead.; 1 = Manageable for a small team, though routine maintenance or scaling requires noticeable effort.; 2 = Can be operated with little ongoing effort through straightforward administration or managed-service options.

## Findings

- Qdrant offers a single-binary self-hosted option and managed cloud, with managed features such as backups and automatic scaling. Its filtering is integrated into vector search through filterable HNSW. [EV_1, EV_2, EV_3]
  - EV_1 (SRC_2, chars 6225-6306): "Clean API, simple single-binary self-host - Managed Qdrant Cloud with a free tier"
  - EV_2 (SRC_4, chars 2590-2966): "Qdrant filters during the search, so you do not have to choose. Its query planner either scores the matching points directly when few points match, or searches the HNSW graph while skipping points that fail the filter. To keep that graph walk from getting stuck, Qdrant builds a filterable HNSW index: extra edges between points that share a value of an indexed payload field."
  - EV_3 (SRC_3, chars 932-1062): "Managed Cloud — Run Qdrant as a managed service on AWS, GCP, or Azure with automatic scaling, backups, and zero-downtime upgrades."
- Weaviate supports self-hosting and cloud deployment, and vectorizer integrations may reduce RAG setup work. Its filtering combines inverted-index pre-filtering with HNSW/ACORN and a brute-force path; the evidence also notes a higher resource footprint and more concepts to learn. [EV_4, EV_5, EV_6]
  - EV_4 (SRC_2, chars 7162-7323): "#### Strengths - Best-in-class built-in hybrid search - Vectorizer modules reduce integration time - Native multi-tenancy - Self-host plus Weaviate Cloud options"
  - EV_5 (SRC_1, chars 9021-9214): "Weaviate pre-filters through its inverted index into an allow-list, walks HNSW with ACORN (default `filterStrategy` since v1.34), and uses brute force below `flatSearchCutoff` (default 40,000)."
  - EV_6 (SRC_2, chars 7324-7447): "#### Weaknesses - BM25 index can be memory-hungry - Higher resource footprint than Qdrant - More concepts to learn up front"
- Milvus Lite provides a local option, while Standalone uses multiple services. It supports filtered search, but the evidence flags Kubernetes complexity and a steeper operational learning curve for self-hosting. [EV_7, EV_8, EV_9]
  - EV_7 (SRC_1, chars 3523-3720): "Milvus Lite inside `pymilvus`, FLAT index only, Ubuntu and macOS (Lite); Standalone runs `milvus-standalone`, `milvus-etcd` and `milvus-minio`, serving on 19530 with a WebUI on 9091 (Compose guide)"
  - EV_8 (SRC_1, chars 9215-9329): "Milvus restricts the search scope to matching entities before search, with iterative mode for complex expressions."
  - EV_9 (SRC_2, chars 8389-8512): "- Self-hosting adds Kubernetes complexity - Overkill below tens of millions of vectors - Steeper operational learning curve"

## Decision changes (attributed to newly verified evidence)

- Round 0: became_robust None/undetermined -> Qdrant/robust via EV_1, EV_2, EV_3, EV_4, EV_5, EV_6, EV_7, EV_8, EV_9

Decision flips: 0; status changes: 1

## Sources

- SRC_1: [Qdrant vs Weaviate vs Milvus: Recall, RAM, and Scale](https://vectoropsreport.com/posts/qdrant-vs-weaviate-vs-milvus/) - retrieved 2026-10-29T22:53:44+00:00, published 2026-08-27T00:00:00.000Z
- SRC_2: [Vector Database Comparison for RAG: Qdrant vs Weaviate vs Milvus | Lushbinary](https://lushbinary.com/blog/vector-database-comparison-rag-qdrant-weaviate-milvus/) - retrieved 2026-10-29T22:53:44+00:00, published 2026-05-29T15:21:45.000Z
- SRC_3: [Deploy Qdrant](https://qdrant.tech/documentation/deploy-intro/index.md) - retrieved 2026-10-29T22:53:44+00:00
- SRC_4: [Filtering in Vector Search: When to Use What - Qdrant](https://qdrant.tech/documentation/search-patterns/vector-search-filtering/) - retrieved 2026-10-29T22:53:44+00:00

## Assumptions

- Assume the team has not specified cloud provider, deployment environment, scale, or budget, so compare broadly applicable deployment options rather than a particular architecture.
- Assume filtering means metadata-based filtering during vector retrieval for typical RAG use cases; no specific filter language or query complexity was specified.
- Treat operational effort as a qualitative small-team concern, without assuming the team has dedicated database or infrastructure staff.
- No stated priority for deployment_fit, filtering_capability, operational_effort: equal default weight 3.

## Limitations

- Fit scores (0/1/2) are model-assisted assessments under the disclosed rubric and weights, not measurements.
- Support verification uses the same model family as extraction; it is not ground truth and needs human audit.
- 'Robust' means interval dominance under the chosen criteria and weights, not that the option is factually best.

## Next steps

- Test filtered retrieval quality and latency using representative RAG queries, metadata, and expected collection sizes.
- Estimate total cost and resource needs for the intended deployment mode, including managed-service pricing and self-hosting administration.
- Verify current version-specific deployment and filtering requirements before selecting a production setup.

## Budget

Searches 2/6, content pages 4/12, LLM requests 3, elapsed 5.27 s. LLM: gpt-6-luna (record).
