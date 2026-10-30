# Research report - EVAL_Q5_adaptive_r1_20261029T230539_8ca8e4

**Question:** Choose between managed and self-hosted vector databases for a startup with one backend engineer and limited operations time.

**Short answer:** Managed vector databases leads provisionally, but score intervals overlap (Managed vector databases [11,27], Self-hosted vector databases [6,20]); current evidence does not force a unique recommendation. Limited operations capacity favors managed services because they reduce infrastructure work and allow the engineer to focus on application and retrieval tasks. The main gap is whether managed-service cost, constraints, and required control fit the startup’s specific workload and requirements.

| Mode | Status | Stop reason | Confidence | Factual confidence | Decision stability |
|---|---|---|---|---|---|
| comparison | partial | budget_exhausted | moderate | moderate | provisional |

_Confidence rule: confidence = min(decision stability, lowest factual confidence among the recommended option's supported/disputed cells); robust/high=high, provisional/moderate=moderate, otherwise low._

## Decision matrix

| Alternative | operations_effort (w5, inferred) | engineering_effort (w4, inferred) | operational_resilience (w3, default) | control_and_customization (w3, default) | LB | UB |
|---|---|---|---|---|---|---|
| Managed vector databases | unknown [0,2] | 2 (EV_2) | unknown [0,2] | 1 (EV_1) | 11 | 27 |
| Self-hosted vector databases | 0 (EV_3) | unknown [0,2] | unknown [0,2] | 2 (EV_4) | 6 | 20 |

### Scoring rules

- **operations_effort** (lower_is_better, weight 5 [inferred]): 0 = Requires substantial ongoing operations work that is a poor fit for a startup with limited operations time.; 1 = Some operational work is needed, but it may be manageable with careful scoping and automation.; 2 = Provider handles most routine operations, keeping ongoing work low for a small team.
- **engineering_effort** (lower_is_better, weight 4 [inferred]): 0 = Typically requires substantial infrastructure and maintenance work that could strain a one-engineer backend team.; 1 = Can be implemented by one backend engineer, but requires meaningful setup or continuing engineering attention.; 2 = Can typically be adopted and maintained with modest backend engineering effort.
- **operational_resilience** (higher_is_better, weight 3 [default]): 0 = Achieving reliable service and recovery would place substantial responsibility on the startup's small team.; 1 = Reliability and recovery are achievable, but require deliberate configuration or operational work.; 2 = Reliability, recovery, and scaling are well supported with little specialized in-house operations work.
- **control_and_customization** (higher_is_better, weight 3 [default]): 0 = The approach imposes significant constraints on deployment or infrastructure choices.; 1 = Provides useful configuration options, with some constraints or provider dependencies.; 2 = Provides broad control over deployment, configuration, and infrastructure.

## Findings

- Managed services simplify setup and reduce infrastructure maintenance, which aligns with a startup that has only one backend engineer and limited operations time. [EV_2]
  - EV_2 (SRC_7, chars 6174-6535): "Instead of provisioning and maintaining every infrastructure component, teams can create an index or collection, load embeddings, configure metadata, and connect the database to the application. For many AI products, this is the fastest path from prototype to production because it lets engineers focus on retrieval quality, data pipelines, and user experience."
- Self-hosting offers greater control over infrastructure and configuration, but shifts deployment, scaling, monitoring, backups, upgrades, security, and incident response to the team. [EV_3, EV_4]
  - EV_3 (SRC_7, chars 156-413): "Self-hosted vector databases give teams the most control over infrastructure, data placement, configuration, and long-term cost, but they also make the team responsible for deployment, scaling, monitoring, backups, upgrades, security, and incident response."
  - EV_4 (SRC_7, chars 3244-3472): "Self-hosting is attractive because it gives teams direct control over the database environment. They can choose instance types, storage classes, regions, network topology, backup tooling, deployment cadence, and resource limits."
- Managed platforms provide configuration and security options, though they retain provider dependency and constraints compared with self-hosting. [EV_1]
  - EV_1 (SRC_2, chars 5841-6014): "They usually offer: • Strong APIs • Security controls • Access management • Backup and recovery • Performance configuration • Usage monitoring • Enterprise-grade reliability"

## Decision changes (attributed to newly verified evidence)

- Round 2: stability_changed Managed vector databases/undetermined -> Managed vector databases/provisional via EV_2, EV_3, EV_4

Decision flips: 0; status changes: 1

## Sources

- SRC_2: [Vector Database for SaaS: Self-Hosted vs. Managed for Founders](https://agintex.com/blog/vector-database-for-saas-self-hosted-vs.-managed-for-founders) - retrieved 2026-10-29T23:05:39+00:00
- SRC_7: [Self-Hosted vs Managed Vector Databases — The AI Database Blog](https://theaidatabaseblog.com/learn/self-hosted-vs-managed-vector-databases/) - retrieved 2026-10-29T23:05:42+00:00, published 2026-06-04T17:46:32.000Z

## Assumptions

- The startup is choosing an operating model rather than selecting a particular vector database product.
- Limited operations time is the primary stated constraint; no workload size, availability target, data residency requirement, or budget was specified.
- The comparison should consider general tradeoffs and avoid assuming a particular cloud provider, deployment environment, or technology stack.
- No stated priority for operational_resilience, control_and_customization: equal default weight 3.

## Limitations

- Fit scores (0/1/2) are model-assisted assessments under the disclosed rubric and weights, not measurements.
- Support verification uses the same model family as extraction; it is not ground truth and needs human audit.
- 'Robust' means interval dominance under the chosen criteria and weights, not that the option is factually best.
- Unknown (no verified evidence, interval [0,2]): Managed vector databases:operations_effort, Managed vector databases:operational_resilience, Self-hosted vector databases:engineering_effort, Self-hosted vector databases:operational_resilience.
- 25 extracted candidate(s) were rejected by grounding/verification (see verification_log.jsonl).
- Stopped: budget_exhausted (MAX_RESEARCH_ROUNDS=3 reached).

## Next steps

- Estimate total cost for the expected workload under managed and self-hosted options, including growth and support needs.
- Identify any non-negotiable requirements for data placement, security, configuration, or portability, then validate them with candidate providers and deployment options.
- Run a representative workload test to compare retrieval performance, operational effort, and scaling behavior.

## Budget

Searches 5/6, content pages 10/12, LLM requests 9, elapsed 75.38 s. LLM: gpt-6-luna (record).
