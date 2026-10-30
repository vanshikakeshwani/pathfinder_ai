# Research report - EVAL_Q5_r1_adaptive_20261030T051350_6f5523

**Question:** Choose between managed and self-hosted vector databases for a startup with one backend engineer and limited operations time.

**Short answer:** Recommendation: Managed vector database. It is interval-robust under the disclosed criteria and weights (score intervals: Managed vector database [13,19], Self-hosted vector database [9,9]), and the evidence on the differentiating criteria is comparable and well supported. For a one-engineer startup with limited operations time, the practical tradeoff is less infrastructure work versus greater control and potentially lower direct hosting costs. The main remaining uncertainty is how the options compare for the startup’s actual workload and requirements.

| Mode | Status | Stop reason | Confidence | Factual confidence | Decision stability |
|---|---|---|---|---|---|
| comparison | complete | stable | low | low | robust |

_Confidence rule: confidence = min(interval stability, lowest factual confidence among the leader's supported/disputed cells); robust/high=high, provisional/moderate=moderate, otherwise low. A withheld recommendation caps confidence at moderate, and at low when the withholding is due to non-comparable evidence._

**Requirement coverage:** 5/6 units with verified support.

## Recommendation readiness

- Interval leader: Managed vector database (robust)
- Recommendation: **ready** (Managed vector database)

## Decision matrix

_Cell = score (evidence; independent sources; scope)._

| Alternative | operational_effort (w5, inferred) | startup_cost (w3, default) | control_and_customization (w3, default) | LB | UB |
|---|---|---|---|---|---|
| Managed vector database (approach) | 2 (EV_1, EV_6; 2 src) | 1 (EV_2, EV_7; 2 src) | disputed [0,2] (EV_3, EV_8; 2 src) | 13 | 19 |
| Self-hosted vector database (approach) | 0 (EV_4, EV_9; 2 src) | 1 (EV_10; 1 src) | 2 (EV_5; 1 src) | 9 | 9 |

### Scoring rules

- **operational_effort** (lower_is_better, weight 5 [inferred]): 0 = Requires substantial ongoing infrastructure work or frequent hands-on intervention that is difficult for one backend engineer to sustain.; 1 = Can be operated with some recurring engineering attention, but leaves manageable time for other startup work.; 2 = Requires little ongoing operational attention and is practical for a startup with one backend engineer and limited operations time.
- **startup_cost** (lower_is_better, weight 3 [default]): 0 = Likely to impose high or unpredictable costs relative to an early-stage startup's needs.; 1 = Cost appears manageable at modest usage, though meaningful charges or overhead may arise as usage grows.; 2 = Offers a clear, affordable path for modest early-stage usage with costs that appear reasonably predictable.
- **control_and_customization** (higher_is_better, weight 3 [default]): 0 = Provides limited control over deployment or important configuration and data-handling choices.; 1 = Provides adequate control for common startup needs, with some provider or platform constraints.; 2 = Provides extensive control over deployment, configuration, and data-handling choices.

## Findings

- Managed services handle much of the infrastructure and maintenance, while self-hosting leaves the team responsible for deployment, scaling, monitoring, backups, upgrades, security, and incident response—an especially relevant burden for a small team. [EV_1, EV_4]
  - EV_1 (SRC_2, chars 6536-6747, score 2 via verified_proposal): "The biggest advantage is operational simplicity. Managed services usually handle infrastructure provisioning, routine maintenance, patching, availability architecture, scaling workflows, and parts of monitoring."
    - rubric rationale: Strong anchor: the excerpt describes the provider taking on routine operations and scaling work, which supports little ongoing operational attention for a startup with limited operations time.
  - EV_4 (SRC_2, chars 156-413, score 0 via verified_proposal): "Self-hosted vector databases give teams the most control over infrastructure, data placement, configuration, and long-term cost, but they also make the team responsible for deployment, scaling, monitoring, backups, upgrades, security, and incident response."
    - rubric rationale: Poor anchor: the excerpt lists substantial ongoing infrastructure responsibilities that would be difficult to sustain with one backend engineer and limited operations time.
- Self-hosting offers more control over deployment and configuration, while managed services can limit some infrastructure and data-handling choices. The cited cost examples are about $280/month for one managed workload and $120/month for one self-hosted cluster, so they should not be treated as a general cost comparison. [EV_3, EV_5, EV_7, EV_8, EV_10]
  - EV_3 (SRC_2, chars 8027-8307, score 1 via verified_proposal): "The tradeoff is that managed services can limit certain choices. A team may have fewer options for low-level index tuning, infrastructure placement, deployment topology, private networking patterns, or maintenance timing. Some of these limits are acceptable for most applications."
    - rubric rationale: Plausible anchor: the excerpt supports adequate control for many common applications, while identifying provider-imposed limits on important configuration and deployment choices.
  - EV_5 (SRC_2, chars 3244-3472, score 2 via verified_proposal): "Self-hosting is attractive because it gives teams direct control over the database environment. They can choose instance types, storage classes, regions, network topology, backup tooling, deployment cadence, and resource limits."
    - rubric rationale: Strong anchor: the excerpt explicitly describes direct control across a wide range of deployment and configuration choices.
  - EV_7 (SRC_5, chars 1267-1427, score 1 via verified_proposal): "The s1.x1 pod sufficient for our index ran ~$70/mo per pod, and we needed 2 for redundancy. Add metadata filtering and we ended up at ~$280/mo just for vectors."
    - rubric rationale: Plausible anchor: the excerpt gives a concrete monthly charge and notes additional redundancy and filtering costs, indicating meaningful charges, without establishing that costs are unaffordable for modest usage.
  - EV_8 (SRC_6, chars 2733-2801, score 0 via verified_proposal): "Data sovereignty | Data leaves your VPC (unless BYOC) | Full control"
    - rubric rationale: Poor anchor: the excerpt identifies a significant data-handling constraint for managed deployment, supporting limited control over an important choice.
  - EV_10 (SRC_5, chars 4287-4371, score 1 via verified_proposal): "Cost was middle-of-the-road: ~$120/mo for a 2-node cluster with reasonable headroom."
    - rubric rationale: Plausible anchor: the excerpt gives a concrete infrastructure charge that may be manageable at modest scale, but does not establish a broadly affordable or predictable path for an early-stage startup.

## Decision changes (attributed to newly verified evidence)

- Round 0: became_robust None/undetermined -> Managed vector database/robust via EV_1, EV_2, EV_3, EV_4, EV_5

Decision flips: 0; status changes: 1

## Sources

- SRC_2: [Self-Hosted vs Managed Vector Databases — The AI Database Blog](https://theaidatabaseblog.com/learn/self-hosted-vs-managed-vector-databases/) - retrieved 2026-10-30T05:13:50+00:00, published 2026-06-04T17:46:32.000Z
- SRC_5: [Vector Database Selection: Pinecone, pgvector, Qdrant After](https://www.devopsness.com/blog/vector-database-selection-pinecone-pgvector-qdrant-after-6-months-in-production-2026-04-14) - retrieved 2026-10-30T05:13:52+00:00, published 2026-04-14T12:00:00.000Z
- SRC_6: [Vector Database Comparison - Awesome RAG Production](https://yigtwxx.github.io/awesome-rag-production/vector-database-comparison/) - retrieved 2026-10-30T05:13:52+00:00

## Assumptions

- The startup expects to use a vector database in a production application, not only for a short-lived experiment.
- No specific workload size, latency target, compliance requirement, cloud provider, or budget was provided.
- The comparison should consider general managed and self-hosted approaches rather than specific database products.
- No stated priority for startup_cost, control_and_customization: equal default weight 3.

## Limitations

- Fit scores (0/1/2) are model-assisted assessments under the disclosed rubric and weights, not measurements.
- Support verification uses the same model family as extraction; it is not ground truth and needs human audit.
- 'Robust' means interval dominance under the chosen criteria and weights, not that the option is factually best.
- Single-source support (one independent source): Self-hosted vector database:startup_cost, Self-hosted vector database:control_and_customization.
- Disputed (conflicting verified evidence, interval [0,2]): Managed vector database:control_and_customization.
- Pricing/plan terms change often; values reflect the retrieval date of each source.
- 2 extracted candidate(s) were rejected by grounding/verification (see verification_log.jsonl).

## Next steps

- Estimate total monthly cost for both options using the startup’s expected data volume, query load, redundancy, and growth.
- Confirm whether managed-service data placement and configuration limits meet the startup’s security and product requirements.
- Validate self-hosting effort with a small deployment, including sizing, backups, upgrades, and incident-response coverage.

## Budget

Searches 3/6, content pages 6/12, LLM requests 5, elapsed 56.22 s. LLM: gpt-6-luna (record).
