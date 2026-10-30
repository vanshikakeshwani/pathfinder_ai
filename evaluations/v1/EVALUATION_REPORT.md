# Evaluation report: static vs adaptive (live)

- Evaluation folder: `outputs/eval_E_20261029T225137_030e78` (mode: record, started 2026-10-29T22:51:37+00:00)
- Config fingerprint `a37e41b4ef`: llm_provider=experiential, llm_model=gpt-6-luna, llm_base_url=https://api.experientiallabs.ai/v1, llm_structured_mode=json_schema, llm_temperature=0.0, llm_max_retries=2, exa_max_retries=2, max_search_calls=6, max_content_pages=12, max_research_rounds=3, max_no_progress=2, max_evidence_per_round=12, max_initial_queries=2, results_per_search=5, pages_per_search=2, max_llm_calls=None, max_seconds=None
- Questions: Q1, Q2, Q3, Q4, Q5, Q8; repeats: 1 (n=1 per arm per question: descriptive only, no significance claims)

## Replay check

Replay folder `outputs/eval_E_20261029T230926_ade675`: **identical decisions and metrics** (excluding run id, timestamp, elapsed time and model label).

## Question-by-question results

| Q | Mode | Arm | Coverage (units) | Searches | Pages | Actions | Yield | Verified ev. | Rejected | Recommendation / stability | Flips / status chg | Stop | Tokens | Exa $ | Errors (tool/LLM) | Time s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | comparison | static | 1.0 (9/9) | 5 | 10 | 15 | 0.6 | 13 | 3 | Qdrant / robust | 0 / 1 | budget_exhausted | 48413 | 0.045 | 0/0 | 119.44 |
| Q1 | comparison | adaptive | 1.0 (9/9) | 2 | 4 | 6 | 1.5 | 9 | 0 | Qdrant / robust | 0 / 1 | stable | 22777 | 0.018 | 0/0 | 5.27 |
| Q2 | discovery | static | 0.0 (0/5) | 5 | 10 | 15 | 0.467 | 8 | 6 | n/a | 0 / 0 | budget_exhausted | 31408 | 0.045 | 0/0 | 62.84 |
| Q2 | discovery | adaptive | 0.2 (1/5) | 5 | 10 | 15 | 0.733 | 20 | 5 | n/a | 0 / 0 | budget_exhausted | 41374 | 0.045 | 0/0 | 78.34 |
| Q3 | comparison | static | 0.375 (3/8) | 5 | 10 | 15 | 0.2 | 3 | 14 | Single-agent support automation / provisional | 0 / 1 | budget_exhausted | 50950 | 0.045 | 0/0 | 154.91 |
| Q3 | comparison | adaptive | 0.375 (3/8) | 4 | 8 | 12 | 0.25 | 3 | 5 | Single-agent support automation / provisional | 0 / 1 | no_progress | 31877 | 0.036 | 0/0 | 15.28 |
| Q4 | comparison | static | 0.0 (0/9) | 5 | 10 | 15 | 0.0 | 0 | 25 | - / undetermined | 0 / 0 | insufficient_evidence | 52003 | 0.045 | 0/0 | 160.94 |
| Q4 | comparison | adaptive | 0.0 (0/9) | 3 | 6 | 9 | 0.0 | 0 | 12 | - / undetermined | 0 / 0 | insufficient_evidence | 29418 | 0.027 | 0/0 | 38.8 |
| Q5 | comparison | static | 0.125 (1/8) | 5 | 10 | 15 | 0.067 | 1 | 26 | - / undetermined | 0 / 0 | budget_exhausted | 53996 | 0.045 | 0/0 | 160.55 |
| Q5 | comparison | adaptive | 0.5 (4/8) | 5 | 10 | 15 | 0.267 | 4 | 25 | Managed vector databases / provisional | 0 / 1 | budget_exhausted | 56265 | 0.045 | 0/0 | 75.39 |
| Q8 | discovery | static | 0.2 (1/5) | 5 | 10 | 15 | 0.533 | 9 | 8 | n/a | 0 / 0 | budget_exhausted | 39251 | 0.045 | 0/0 | 77.69 |
| Q8 | discovery | adaptive | 0.2 (1/5) | 4 | 8 | 12 | 0.583 | 7 | 9 | n/a | 0 / 0 | no_progress | 31137 | 0.036 | 0/0 | 45.58 |

## Static vs adaptive per question

| Q | Coverage static → adaptive | Actions static → adaptive | Yield static → adaptive | Outcome |
|---|---|---|---|---|
| Q1 | 1.0 → 1.0 | 15 → 6 | 0.6 → 1.5 | same full coverage, adaptive fewer actions |
| Q2 | 0.0 → 0.2 | 15 → 15 | 0.467 → 0.733 | adaptive better coverage |
| Q3 | 0.375 → 0.375 | 15 → 12 | 0.2 → 0.25 | NO coverage benefit (equal, incomplete); adaptive stopped earlier |
| Q4 | 0.0 → 0.0 | 15 → 9 | 0.0 → 0.0 | NO coverage benefit (equal, incomplete); adaptive stopped earlier |
| Q5 | 0.125 → 0.5 | 15 → 15 | 0.067 → 0.267 | adaptive better coverage |
| Q8 | 0.2 → 0.2 | 15 → 12 | 0.533 → 0.583 | NO coverage benefit (equal, incomplete); adaptive stopped earlier |

## Overall (sums over questions; descriptive)

| Metric | Static | Adaptive |
|---|---|---|
| requirement_units_supported | 14.0 | 18.0 |
| requirement_units_total | 44.0 | 44.0 |
| search_calls | 30.0 | 23.0 |
| content_pages | 60.0 | 46.0 |
| research_actions_spent | 90.0 | 69.0 |
| verified_evidence | 34.0 | 43.0 |
| rejected_candidates | 82.0 | 56.0 |
| llm_requests | 50.0 | 37.0 |
| llm_total_tokens | 276021.0 | 212848.0 |
| exa_cost_usd | 0.27 | 0.207 |
| tool_attempt_errors | 0.0 | 0.0 |
| llm_attempt_errors | 0.0 | 0.0 |
| elapsed_s | 736.37 | 258.66 |

Outcome tally: NO coverage benefit (equal, incomplete); adaptive stopped earlier: 3; adaptive better coverage: 2; same full coverage, adaptive fewer actions: 1

**Elapsed time is NOT comparable between arms:** static runs first, and adaptive reuses the cached round-0 responses, so its wall-clock time excludes most round-0 latency. Compare actions, tokens and provider cost instead.

### Cases where adaptive was worse or showed no benefit

- Q3: NO coverage benefit (equal, incomplete); adaptive stopped earlier
- Q4: NO coverage benefit (equal, incomplete); adaptive stopped earlier
- Q8: NO coverage benefit (equal, incomplete); adaptive stopped earlier

## Actual recorded spend (each provider call counted once)

- Recorded calls: 151
- Exa cost reported by provider: $0.358
- LLM cost reported by gateway (`usage.cost`): $0.060397
- LLM tokens: 381337
- Per-arm cost/tokens in the tables are *attributed*: the shared round 0 counts for both arms.

## Research actions and selection reasons

### Q1
**static**
- round 0 `initial` (score 0.0): Initial planned queries (round 0, shared by static and adaptive strategies). Queries: ['Qdrant Weaviate Milvus comparison deployment filtering operations small team RAG', 'Qdrant Weaviate Milvus official documentation metadata filtering deployment options']
- **decision change** became_robust: None/undetermined → Qdrant/robust via EV_1, EV_2, EV_3, EV_4, EV_5, EV_6, EV_7, EV_8, EV_9
- round 1 `Qdrant:deployment_fit` (score 0.0): Static baseline: next pre-planned query (no adaptation). Queries: ['Qdrant How well the available deployment models fit a small team building RAG, including ease of getting started and options to run self-managed or managed. documentation']
- round 2 `Qdrant:filtering_capability` (score 0.0): Static baseline: next pre-planned query (no adaptation). Queries: ['Qdrant Support for filtering vector search results using metadata and combining filters with retrieval in common RAG workflows. documentation']
- round 3 `Qdrant:operational_effort` (score 0.0): Static baseline: next pre-planned query (no adaptation). Queries: ['Qdrant Ongoing effort for a small team to deploy, monitor, maintain, and scale the database for a RAG application. documentation']
- stop: `budget_exhausted` (MAX_RESEARCH_ROUNDS=3 reached)

**adaptive**
- round 0 `initial` (score 0.0): Initial planned queries (round 0, shared by static and adaptive strategies). Queries: ['Qdrant Weaviate Milvus comparison deployment filtering operations small team RAG', 'Qdrant Weaviate Milvus official documentation metadata filtering deployment options']
- **decision change** became_robust: None/undetermined → Qdrant/robust via EV_1, EV_2, EV_3, EV_4, EV_5, EV_6, EV_7, EV_8, EV_9
- stop: `stable` (interval-robust winner under the disclosed rubric)

### Q2
**static**
- round 0 `initial` (score 0.0): Initial planned queries (round 0, shared by static and adaptive strategies). Queries: ['India headquartered HR technology B2B SaaS companies official company about headquarters product positioning', 'India HR SaaS companies headquarters B2B HRMS recruiting payroll official websites']
- round 1 `india_based` (score 0.0): Static baseline: next pre-planned query (no adaptation). Queries: ['Company is headquartered in India; include evidence supporting its headquarters location.']
- round 2 `b2b_saas` (score 0.0): Static baseline: next pre-planned query (no adaptation). Queries: ['Company offers software as a service to business customers, supported by evidence of its B2B SaaS model.']
- round 3 `hr_technology` (score 0.0): Static baseline: next pre-planned query (no adaptation). Queries: ["Company's product or service is in HR technology, such as HR management, recruiting, payroll, employee engagement, or workforce management."]
- stop: `budget_exhausted` (MAX_RESEARCH_ROUNDS=3 reached)

**adaptive**
- round 0 `initial` (score 0.0): Initial planned queries (round 0, shared by static and adaptive strategies). Queries: ['India headquartered HR technology B2B SaaS companies official company about headquarters product positioning', 'India HR SaaS companies headquarters B2B HRMS recruiting payroll official websites']
- round 1 `PeopleStrong|b2b_saas` (score 2.5): PeopleStrong is missing verified evidence for 'Company offers software as a service to business customers, supported by evidence of its B2B SaaS model.' (importance 5). Queries: ['PeopleStrong Company offers software as a service to business customers, supported by evidence of its B2B SaaS model.']
- round 2 `PeopleStrong|india_based` (score 2.5): PeopleStrong is missing verified evidence for 'Company is headquartered in India; include evidence supporting its headquarters location.' (importance 5). Queries: ['PeopleStrong Company is headquartered in India; include evidence supporting its headquarters location.']
- round 3 `Timelabs|b2b_saas` (score 2.5): Timelabs is missing verified evidence for 'Company offers software as a service to business customers, supported by evidence of its B2B SaaS model.' (importance 5). Queries: ['Timelabs Company offers software as a service to business customers, supported by evidence of its B2B SaaS model.']
- stop: `budget_exhausted` (MAX_RESEARCH_ROUNDS=3 reached)

### Q3
**static**
- round 0 `initial` (score 0.0): Initial planned queries (round 0, shared by static and adaptive strategies). Queries: ['single-agent vs multi-agent support automation complexity cost reliability safeguards SaaS', 'single-agent support automation architecture reliability safeguards cost']
- **decision change** stability_changed: None/undetermined → Single-agent support automation/provisional via EV_1, EV_2, EV_3
- round 1 `Single-agent support automation:implementation_complexity` (score 0.0): Static baseline: next pre-planned query (no adaptation). Queries: ['Single-agent support automation Assess the raw implementation and ongoing orchestration complexity for a 20-person SaaS company, including setup, maintenance, and debugging effort. documentation']
- round 2 `Single-agent support automation:cost` (score 0.0): Static baseline: next pre-planned query (no adaptation). Queries: ['Single-agent support automation Assess total cost to operate the support automation, including applicable software, model usage, and maintenance costs at a scale appropriate to a 20-person SaaS company. official pricing plans']
- round 3 `Single-agent support automation:reliability` (score 0.0): Static baseline: next pre-planned query (no adaptation). Queries: ['Single-agent support automation Assess how consistently the approach can resolve or route support requests correctly, and how well it handles failures, edge cases, and handoffs. documentation']
- stop: `budget_exhausted` (MAX_RESEARCH_ROUNDS=3 reached)

**adaptive**
- round 0 `initial` (score 0.0): Initial planned queries (round 0, shared by static and adaptive strategies). Queries: ['single-agent vs multi-agent support automation complexity cost reliability safeguards SaaS', 'single-agent support automation architecture reliability safeguards cost']
- **decision change** stability_changed: None/undetermined → Single-agent support automation/provisional via EV_1, EV_2, EV_3
- round 1 `Multi-agent support automation:cost` (score 3.0): Multi-agent support automation:cost is unknown (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Multi-agent support automation: implementation_complexity, reliability. Queries: ['Multi-agent support automation Assess total cost to operate the support automation, including applicable software, model usage, and maintenance costs at a scale appropriate to a 20-person SaaS company. official pricing plans']
- round 2 `Multi-agent support automation:cost` (score 3.0): Multi-agent support automation:cost is unknown (width 2, weight 3, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Multi-agent support automation: implementation_complexity, reliability. Retry with an open query. Queries: ['Multi-agent support automation Assess total cost to operate the support automation, including applicable software, model usage, and maintenance costs at a scale appropriate to a 20-person SaaS company. review comparison']
- stop: `no_progress` (2 consecutive round(s) without newly verified evidence)

### Q4
**static**
- round 0 `initial` (score 0.0): Initial planned queries (round 0, shared by static and adaptive strategies). Queries: ['customer support AI session-only context memory vs retrieval augmented memory vs persistent customer profile memory', 'AI customer service agents conversation memory retrieval privacy data retention deletion controls']
- round 1 `Session-only context memory:retrieval_effectiveness` (score 0.0): Static baseline: next pre-planned query (no adaptation). Queries: ['Session-only context memory How reliably the approach makes relevant information available to the agent, including useful short-term conversation context and, where applicable, relevant information from prior interactions. documentation']
- round 2 `Session-only context memory:privacy_risk` (score 0.0): Static baseline: next pre-planned query (no adaptation). Queries: ['Session-only context memory The raw privacy risk created by storing, processing, and retrieving customer conversation or profile data, including exposure through access, misuse, or unnecessary collection. documentation']
- round 3 `Session-only context memory:retention_and_deletion_control` (score 0.0): Static baseline: next pre-planned query (no adaptation). Queries: ['Session-only context memory How well the approach supports explicit retention periods, deletion of data, and control over whether information persists between support interactions. documentation']
- stop: `insufficient_evidence` (MAX_RESEARCH_ROUNDS=3 reached; no verified evidence was found)

**adaptive**
- round 0 `initial` (score 0.0): Initial planned queries (round 0, shared by static and adaptive strategies). Queries: ['customer support AI session-only context memory vs retrieval augmented memory vs persistent customer profile memory', 'AI customer service agents conversation memory retrieval privacy data retention deletion controls']
- round 1 `Persistent customer-profile memory:privacy_risk` (score 6.0): Persistent customer-profile memory:privacy_risk is unknown (width 2, weight 3, flip-relevant x2); resolving it could change the leader. Queries: ['Persistent customer-profile memory The raw privacy risk created by storing, processing, and retrieving customer conversation or profile data, including exposure through access, misuse, or unnecessary collection. documentation']
- stop: `insufficient_evidence` (2 consecutive round(s) without newly verified evidence; no verified evidence was found)

### Q5
**static**
- round 0 `initial` (score 0.0): Initial planned queries (round 0, shared by static and adaptive strategies). Queries: ['managed versus self-hosted vector databases startup operations effort comparison', 'managed vector database vs self-hosted vector database engineering maintenance reliability']
- round 1 `Managed vector databases:operations_effort` (score 0.0): Static baseline: next pre-planned query (no adaptation). Queries: ['Managed vector databases Ongoing engineering and operations effort for deployment, upgrades, monitoring, backups, scaling, and incident response. documentation']
- round 2 `Managed vector databases:engineering_effort` (score 0.0): Static baseline: next pre-planned query (no adaptation). Queries: ['Managed vector databases Backend engineering effort needed to get a production-ready system running and maintain its integrations. documentation']
- round 3 `Managed vector databases:operational_resilience` (score 0.0): Static baseline: next pre-planned query (no adaptation). Queries: ['Managed vector databases How readily the approach supports reliable availability, recovery, and scaling without depending on extensive in-house operations capacity. documentation']
- stop: `budget_exhausted` (MAX_RESEARCH_ROUNDS=3 reached)

**adaptive**
- round 0 `initial` (score 0.0): Initial planned queries (round 0, shared by static and adaptive strategies). Queries: ['managed versus self-hosted vector databases startup operations effort comparison', 'managed vector database vs self-hosted vector database engineering maintenance reliability']
- round 1 `Managed vector databases:operations_effort` (score 10.0): Managed vector databases:operations_effort is unknown (width 2, weight 5, flip-relevant x2); resolving it could change the leader. Already supported for Managed vector databases: control_and_customization. Queries: ['Managed vector databases Ongoing engineering and operations effort for deployment, upgrades, monitoring, backups, scaling, and incident response. documentation']
- round 2 `Managed vector databases:operations_effort` (score 10.0): Managed vector databases:operations_effort is unknown (width 2, weight 5, flip-relevant x2); resolving it could change the leader. Already supported for Managed vector databases: control_and_customization. Retry with an open query. Queries: ['Managed vector databases Ongoing engineering and operations effort for deployment, upgrades, monitoring, backups, scaling, and incident response. review comparison']
- **decision change** stability_changed: Managed vector databases/undetermined → Managed vector databases/provisional via EV_2, EV_3, EV_4
- round 3 `Self-hosted vector databases:engineering_effort` (score 4.0): Self-hosted vector databases:engineering_effort is unknown (width 2, weight 4, not flip-relevant x1); resolving it cannot alone change the leader. Already supported for Self-hosted vector databases: operations_effort, control_and_customization. Queries: ['Self-hosted vector databases Backend engineering effort needed to get a production-ready system running and maintain its integrations. documentation']
- stop: `budget_exhausted` (MAX_RESEARCH_ROUNDS=3 reached)

### Q8
**static**
- round 0 `initial` (score 0.0): Initial planned queries (round 0, shared by static and adaptive strategies). Queries: ['open source LLM evaluation tools official license self hosted', 'open source LLM observability tools self hosted license official']
- round 1 `llm_eval_or_observability` (score 0.0): Static baseline: next pre-planned query (no adaptation). Queries: ['Tool is specifically for evaluating or observing LLM applications or models.']
- round 2 `open_source_license` (score 0.0): Static baseline: next pre-planned query (no adaptation). Queries: ['Tool has a verifiable open-source license, with evidence from an official repository or project source.']
- round 3 `self_hosting_support` (score 0.0): Static baseline: next pre-planned query (no adaptation). Queries: ['Tool supports self-hosting or on-premises deployment, with evidence from an official project source.']
- stop: `budget_exhausted` (MAX_RESEARCH_ROUNDS=3 reached)

**adaptive**
- round 0 `initial` (score 0.0): Initial planned queries (round 0, shared by static and adaptive strategies). Queries: ['open source LLM evaluation tools official license self hosted', 'open source LLM observability tools self hosted license official']
- round 1 `Comet Opik|open_source_license` (score 2.5): Comet Opik is missing verified evidence for 'Tool has a verifiable open-source license, with evidence from an official repository or project source.' (importance 5). Queries: ['Comet Opik Tool has a verifiable open-source license, with evidence from an official repository or project source.']
- round 2 `Comet Opik|open_source_license` (score 2.5): Comet Opik is missing verified evidence for 'Tool has a verifiable open-source license, with evidence from an official repository or project source.' (importance 5). Retry with a broadened query. Queries: ['Comet Opik Tool has a verifiable open-source license, with evidence from an official repository or project source. list overview']
- stop: `no_progress` (2 consecutive round(s) without newly verified evidence)

