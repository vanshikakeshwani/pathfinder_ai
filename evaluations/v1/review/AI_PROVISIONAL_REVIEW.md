# AI-provisional review materials

> **AI-PROVISIONAL, NOT HUMAN EVALUATION.** The checks below are computed mechanically from the run files, and the flags were raised by the AI assistant. All human score columns are blank and must be filled in by a human reviewer (`evaluations/rubric.md`). Do not treat any flag as a verdict.

## Q1 / static - `EVAL_Q1_static_r1_20261029T225145_e4baf8`

- Status `partial`, stop `budget_exhausted`, confidence `moderate` (factual `moderate`, stability `robust`)
- Mechanical: 9 cited evidence IDs, **0 invalid**; 13 accepted / 3 rejected candidates; 8 cited sources from 3 domains
- Unresolved units: none
- AI-provisional flags: score saturation: Qdrant scored 2 on every criterion; check the anchors; one source supports 3+ targets (SRC_2: 4; SRC_1: 3): check for over-reading of a single page

| Rubric dim (0/1/2) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Reviewer | Date |
|---|---|---|---|---|---|---|---|---|---|---|
| **Human score** | | | | | | | | | | |

Accepted evidence to verify (does the excerpt really support the claim and score?):

| EV | Target | Score | Claim | Excerpt | Human: supports? |
|---|---|---|---|---|---|
| EV_1 | Qdrant:deployment_fit | 2 | Qdrant offers a simple self-hosted deployment and a managed cloud option, including a free tier, which fits a small team's RAG deployment needs. | Clean API, simple single-binary self-host - Managed Qdrant Cloud with a free tier | |
| EV_2 | Qdrant:filtering_capability | 2 | Qdrant integrates metadata filtering into vector search and uses filterable HNSW to support retrieval with filters. | Qdrant filters during the search, so you do not have to choose. Its query planner either scores the matching points directly when few points match, or searches the HNSW graph while skipping points that fail the filter. T... | |
| EV_3 | Qdrant:operational_effort | 2 | Qdrant Cloud offers managed hosting with automatic scaling, backups, and zero-downtime upgrades, reducing ongoing administration. | Managed Cloud — Run Qdrant as a managed service on AWS, GCP, or Azure with automatic scaling, backups, and zero-downtime upgrades. | |
| EV_4 | Weaviate:deployment_fit | 2 | Weaviate offers both self-hosted and cloud deployment options, and its vectorizer integrations can reduce setup work for RAG. | #### Strengths - Best-in-class built-in hybrid search - Vectorizer modules reduce integration time - Native multi-tenancy - Self-host plus Weaviate Cloud options | |
| EV_5 | Weaviate:filtering_capability | 2 | Weaviate combines inverted-index pre-filtering with HNSW/ACORN search and a brute-force path for smaller searches. | Weaviate pre-filters through its inverted index into an allow-list, walks HNSW with ACORN (default `filterStrategy` since v1.34), and uses brute force below `flatSearchCutoff` (default 40,000). | |
| EV_6 | Weaviate:operational_effort | 1 | Weaviate can require more resources and learning than Qdrant, although its cloud option provides a managed path. | #### Weaknesses - BM25 index can be memory-hungry - Higher resource footprint than Qdrant - More concepts to learn up front | |
| EV_7 | Milvus:deployment_fit | 1 | Milvus has a local Lite option, but its Standalone deployment involves multiple services, making it a workable option with meaningful setup tradeoffs. | Milvus Lite inside `pymilvus`, FLAT index only, Ubuntu and macOS (Lite); Standalone runs `milvus-standalone`, `milvus-etcd` and `milvus-minio`, serving on 19530 with a WebUI on 9091 (Compose guide) | |
| EV_8 | Milvus:filtering_capability | 2 | Milvus supports filtering search to matching entities and provides iterative mode for complex filter expressions. | Milvus restricts the search scope to matching entities before search, with iterative mode for complex expressions. | |
| EV_9 | Milvus:operational_effort | 0 | Self-hosted Milvus adds Kubernetes complexity and has a steeper operational learning curve, which can be substantial overhead for a small team. | - Self-hosting adds Kubernetes complexity - Overkill below tens of millions of vectors - Steeper operational learning curve | |
| EV_10 | Qdrant:filtering_capability | 2 | Payload indexes integrate filtering into semantic search through a single-pass graph traversal rather than pre- or post-filtering. | A unique aspect of the payload index is that it extends the HNSW graph, allowing filtering criteria to be applied during the semantic search phase. That means it’s a single-pass graph traversal, rather than pre- or post-... | |
| EV_11 | Qdrant:operational_effort | 2 | Qdrant Cloud manages upgrades, scaling, backups, and monitoring, allowing a team to avoid operating clusters itself. | Use when: you want managed infrastructure with zero-downtime updates, automatic backups, and resharding without operating clusters yourself — including when data-residency or compliance rules mean the data can't sit on Q... | |
| EV_12 | Qdrant:filtering_capability | 2 | Qdrant supports combining metadata filter conditions with AND, OR, and NOT, including recursively nested boolean expressions. | Qdrant allows you to combine conditions in clauses. Clauses are different logical operations, such as `OR`, `AND`, and `NOT`. Clauses can be recursively nested into each other so that you can reproduce an arbitrary boole... | |
| EV_13 | Qdrant:operational_effort | 2 | Qdrant offers a SaaS managed-cloud option for database clusters, which can reduce a small team's operational burden. | Qdrant Managed Cloud is our SaaS solution, providing managed Qdrant database clusters on the cloud. | |

Rejected candidates (check for wrongly rejected evidence):

- CAND_10 `Qdrant:deployment_fit` (verification): verdict=partial: It identifies managed, hybrid, and self-managed options, but does not address how easy they are for a small team to get started with.
- CAND_14 `Qdrant:deployment_fit` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_15 `Qdrant:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q1 / adaptive - `EVAL_Q1_adaptive_r1_20261029T225344_b5051e`

- Status `complete`, stop `stable`, confidence `moderate` (factual `moderate`, stability `robust`)
- Mechanical: 9 cited evidence IDs, **0 invalid**; 9 accepted / 0 rejected candidates; 4 cited sources from 3 domains
- Unresolved units: none
- AI-provisional flags: score saturation: Qdrant scored 2 on every criterion; check the anchors; one source supports 3+ targets (SRC_2: 4; SRC_1: 3): check for over-reading of a single page

| Rubric dim (0/1/2) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Reviewer | Date |
|---|---|---|---|---|---|---|---|---|---|---|
| **Human score** | | | | | | | | | | |

Accepted evidence to verify (does the excerpt really support the claim and score?):

| EV | Target | Score | Claim | Excerpt | Human: supports? |
|---|---|---|---|---|---|
| EV_1 | Qdrant:deployment_fit | 2 | Qdrant offers a simple self-hosted deployment and a managed cloud option, including a free tier, which fits a small team's RAG deployment needs. | Clean API, simple single-binary self-host - Managed Qdrant Cloud with a free tier | |
| EV_2 | Qdrant:filtering_capability | 2 | Qdrant integrates metadata filtering into vector search and uses filterable HNSW to support retrieval with filters. | Qdrant filters during the search, so you do not have to choose. Its query planner either scores the matching points directly when few points match, or searches the HNSW graph while skipping points that fail the filter. T... | |
| EV_3 | Qdrant:operational_effort | 2 | Qdrant Cloud offers managed hosting with automatic scaling, backups, and zero-downtime upgrades, reducing ongoing administration. | Managed Cloud — Run Qdrant as a managed service on AWS, GCP, or Azure with automatic scaling, backups, and zero-downtime upgrades. | |
| EV_4 | Weaviate:deployment_fit | 2 | Weaviate offers both self-hosted and cloud deployment options, and its vectorizer integrations can reduce setup work for RAG. | #### Strengths - Best-in-class built-in hybrid search - Vectorizer modules reduce integration time - Native multi-tenancy - Self-host plus Weaviate Cloud options | |
| EV_5 | Weaviate:filtering_capability | 2 | Weaviate combines inverted-index pre-filtering with HNSW/ACORN search and a brute-force path for smaller searches. | Weaviate pre-filters through its inverted index into an allow-list, walks HNSW with ACORN (default `filterStrategy` since v1.34), and uses brute force below `flatSearchCutoff` (default 40,000). | |
| EV_6 | Weaviate:operational_effort | 1 | Weaviate can require more resources and learning than Qdrant, although its cloud option provides a managed path. | #### Weaknesses - BM25 index can be memory-hungry - Higher resource footprint than Qdrant - More concepts to learn up front | |
| EV_7 | Milvus:deployment_fit | 1 | Milvus has a local Lite option, but its Standalone deployment involves multiple services, making it a workable option with meaningful setup tradeoffs. | Milvus Lite inside `pymilvus`, FLAT index only, Ubuntu and macOS (Lite); Standalone runs `milvus-standalone`, `milvus-etcd` and `milvus-minio`, serving on 19530 with a WebUI on 9091 (Compose guide) | |
| EV_8 | Milvus:filtering_capability | 2 | Milvus supports filtering search to matching entities and provides iterative mode for complex filter expressions. | Milvus restricts the search scope to matching entities before search, with iterative mode for complex expressions. | |
| EV_9 | Milvus:operational_effort | 0 | Self-hosted Milvus adds Kubernetes complexity and has a steeper operational learning curve, which can be substantial overhead for a small team. | - Self-hosting adds Kubernetes complexity - Overkill below tens of millions of vectors - Steeper operational learning curve | |

Rejected candidates (check for wrongly rejected evidence):

- none

## Q2 / static - `EVAL_Q2_static_r1_20261029T225355_e0fe80`

- Status `partial`, stop `budget_exhausted`, confidence `low` (factual `high`, stability `None`)
- Mechanical: 7 cited evidence IDs, **0 invalid**; 8 accepted / 6 rejected candidates; 5 cited sources from 4 domains
- Unresolved units: india_based, b2b_saas, hr_technology, positioning_evidence
- AI-provisional flags: none

| Rubric dim (0/1/2) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Reviewer | Date |
|---|---|---|---|---|---|---|---|---|---|---|
| **Human score** | | | | | | | | | | |

Accepted evidence to verify (does the excerpt really support the claim and score?):

| EV | Target | Score | Claim | Excerpt | Human: supports? |
|---|---|---|---|---|---|
| EV_1 | positioning_evidence | - | PeopleStrong positions its platform as covering the employee lifecycle for large enterprises. | Our comprehensive HR Tech 4.0 platform encompasses employee lifecycle from hire to exit, including Human Capital Management, Payroll, Talent Acquisition & Management, and Collaboration. Simplifying work life for over 2 M... | |
| EV_2 | hr_technology | - | ZingHR describes an AI-powered platform for HR processes across the employee lifecycle. | ZingHR's AI-powered Hire-to-ReHire platform permanently removes HR transactional layers from organisation. | |
| EV_3 | positioning_evidence | - | ZingHR positions itself for enterprise customers, including Fortune 500 companies. | Loved by 1200+ enterprises across Fortune 500s | |
| EV_4 | hr_technology | - | greytHR offers an HRMS platform covering HR processes from hiring through retirement. | # HIRE-TO-RETIRE Full Suite HRMS That Lets People Lead, While AI Does the Work. Plan, Recruit, Onboard, Pay, Manage, Upskill, Appraise and Empower your people — all in one platform. | |
| EV_5 | positioning_evidence | - | greytHR positions its full-suite HR and payroll product for companies managing people operations. | 33,000+ companies run People Operations on greytHR. Here's why they stay. Full-suite HR and payroll, with an AI agent built in, at a price point that makes the decision easy. | |
| EV_6 | hr_technology | - | Timelabs offers HR management software covering core HR, payroll, recruitment, and workforce management. | Timelabs is an HRMS and HR operating system that brings core HR, attendance, payroll, recruitment, employee self service, analytics, and workforce management together on one connected platform. | |
| EV_7 | positioning_evidence | - | Timelabs positions its HR product for large enterprises and growing businesses in India. | From large enterprises to fast growing businesses, organisations across India rely on Timelabs to manage HR simply, efficiently, and without the chaos. | |
| EV_8 | hr_technology | - | ZingHR offers an HR platform covering the employee lifecycle and HR operations. | ZingHR's AI-powered Hire-to-ReHire platform permanently removes HR transactional layers from organisation. | |

Rejected candidates (check for wrongly rejected evidence):

- CAND_1 `india_based` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_2 `b2b_saas` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_3 `hr_technology` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_10 `b2b_saas` (verification): verdict=partial: It mentions enterprise-grade HR technology and cloud infrastructure, but does not establish a SaaS business model.
- CAND_13 `positioning_evidence` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_14 `b2b_saas` (verification): verdict=partial: A customer calls ZingHR’s payroll system cloud-based, but the excerpt does not establish a SaaS delivery or business model.

## Q2 / adaptive - `EVAL_Q2_adaptive_r1_20261029T225458_c735ac`

- Status `partial`, stop `budget_exhausted`, confidence `low` (factual `moderate`, stability `None`)
- Mechanical: 10 cited evidence IDs, **0 invalid**; 20 accepted / 5 rejected candidates; 10 cited sources from 5 domains
- Unresolved units: india_based, b2b_saas, hr_technology, positioning_evidence
- AI-provisional flags: one source supports 3+ targets (SRC_5: 3; SRC_8: 3; SRC_10: 3): check for over-reading of a single page

| Rubric dim (0/1/2) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Reviewer | Date |
|---|---|---|---|---|---|---|---|---|---|---|
| **Human score** | | | | | | | | | | |

Accepted evidence to verify (does the excerpt really support the claim and score?):

| EV | Target | Score | Claim | Excerpt | Human: supports? |
|---|---|---|---|---|---|
| EV_1 | positioning_evidence | - | PeopleStrong positions its platform as covering the employee lifecycle for large enterprises. | Our comprehensive HR Tech 4.0 platform encompasses employee lifecycle from hire to exit, including Human Capital Management, Payroll, Talent Acquisition & Management, and Collaboration. Simplifying work life for over 2 M... | |
| EV_2 | hr_technology | - | ZingHR describes an AI-powered platform for HR processes across the employee lifecycle. | ZingHR's AI-powered Hire-to-ReHire platform permanently removes HR transactional layers from organisation. | |
| EV_3 | positioning_evidence | - | ZingHR positions itself for enterprise customers, including Fortune 500 companies. | Loved by 1200+ enterprises across Fortune 500s | |
| EV_4 | hr_technology | - | greytHR offers an HRMS platform covering HR processes from hiring through retirement. | # HIRE-TO-RETIRE Full Suite HRMS That Lets People Lead, While AI Does the Work. Plan, Recruit, Onboard, Pay, Manage, Upskill, Appraise and Empower your people — all in one platform. | |
| EV_5 | positioning_evidence | - | greytHR positions its full-suite HR and payroll product for companies managing people operations. | 33,000+ companies run People Operations on greytHR. Here's why they stay. Full-suite HR and payroll, with an AI agent built in, at a price point that makes the decision easy. | |
| EV_6 | hr_technology | - | Timelabs offers HR management software covering core HR, payroll, recruitment, and workforce management. | Timelabs is an HRMS and HR operating system that brings core HR, attendance, payroll, recruitment, employee self service, analytics, and workforce management together on one connected platform. | |
| EV_7 | positioning_evidence | - | Timelabs positions its HR product for large enterprises and growing businesses in India. | From large enterprises to fast growing businesses, organisations across India rely on Timelabs to manage HR simply, efficiently, and without the chaos. | |
| EV_8 | b2b_saas | - | PeopleStrong offers an HCM SaaS platform and identifies enterprises as customers. | A comprehensive Human Capital Management (HCM) SaaS platform streamlines the entire employee lifecycle from hire to retire, including Payroll, Talent Acquisition, Talent Management, AI-Chatbot and Collaboration, designed... | |
| EV_9 | b2b_saas | - | PeopleStrong provides its software as web-based SaaS and a cloud solution. | The software is operated by PeopleStrong as web-based SaaS, respectively as a Cloud solution. This allows you to use the software stored and operating on PeopleStrong servers, respectively on servers of a third-party com... | |
| EV_10 | hr_technology | - | PeopleStrong offers HCM and HR technology solutions for businesses and enterprises. | PeopleStrong stands as the premier Human Capital Management (HCM) SaaS platform, renowned for its comprehensive suite of HR technology solutions. We prioritize unique employee experience, data-driven insights, and enhanc... | |
| EV_11 | positioning_evidence | - | PeopleStrong positions its platform as mobile-first, AI/ML-enabled, and comprehensive across the employee lifecycle. | Empowering more than 2 million employees, our platform is distinguished by its mobile-first approach and sophisticated use of AI and ML technologies, covering every aspect of the employee lifecycle from hire to retire, i... | |
| EV_12 | positioning_evidence | - | PeopleStrong targets enterprises in Asia Pacific and the Middle East. | Trusted by over 500 leading enterprises, our platform is tailored for the Asia Pacific and Middle East region, currently enhancing the work lives of more than 2 million employees. | |
| EV_13 | india_based | - | PeopleStrong is headquartered in Gurugram and has a significant role in India’s HR technology landscape. | Gurugram, April 15, 2025: Today, PeopleStrong, a leading human capital management (“HCM”) SaaS provider headquartered in Gurugram, announced that the Private Equity business within Goldman Sachs Alternatives has acquired... | |
| EV_14 | b2b_saas | - | PeopleStrong is an HCM SaaS provider. | Today, PeopleStrong, a leading human capital management (“HCM”) SaaS provider headquartered in Gurugram, announced that the Private Equity business within Goldman Sachs Alternatives has acquired a majority stake in the c... | |
| EV_15 | hr_technology | - | PeopleStrong provides HR technology across the employee lifecycle, including HCM, payroll, talent acquisition and management, and collaboration. | Our comprehensive HR Tech 4.0 platform encompasses employee lifecycle from hire to exit, including Human Capital Management, Payroll, Talent Acquisition & Management, and Collaboration. | |
| EV_16 | positioning_evidence | - | PeopleStrong positions its AI-powered HCM platform for leading organizations across multiple industries, with capabilities including ATS, payroll, emp | The company offers a comprehensive, AI-powered HCM platform with robust capabilities across applicant tracking systems (ATS), payroll, employee experience and talent management. It serves leading organizations across key... | |
| EV_17 | b2b_saas | - | Timelabs offers an HRMS with SaaS licensing, supporting its B2B SaaS model. | Affordable compliance-ready HRMS with flexible licensing (SaaS + Perpetual) | |
| EV_18 | b2b_saas | - | Timelabs targets business customers, including startups, SMEs, and enterprises. | Focussed on offering straight forward HR solutions to all businesses, start-up, SME or enterprise. | |
| EV_19 | hr_technology | - | Timelabs provides recruiting and employee onboarding software, an HR technology offering. | Timelabs recruitment management lets you manage your entire recruiting process along with employee onboarding. | |
| EV_20 | positioning_evidence | - | Timelabs positions its cloud-based HR system for businesses ranging from startups and SMEs to enterprises. | Cloud Based HR System Focussed on offering straight forward HR solutions to all businesses, start-up, SME or enterprise. | |

Rejected candidates (check for wrongly rejected evidence):

- CAND_1 `india_based` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_2 `b2b_saas` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_3 `hr_technology` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_10 `b2b_saas` (verification): verdict=partial: It mentions enterprise-grade HR technology and cloud infrastructure, but does not establish a SaaS business model.
- CAND_12 `india_based` (grounding): excerpt not found in source text

## Q3 / static - `EVAL_Q3_static_r1_20261029T225624_cbbd05`

- Status `partial`, stop `budget_exhausted`, confidence `moderate` (factual `moderate`, stability `provisional`)
- Mechanical: 3 cited evidence IDs, **0 invalid**; 3 accepted / 14 rejected candidates; 2 cited sources from 1 domains
- Unresolved units: Single-agent support automation:implementation_complexity, Single-agent support automation:reliability, Single-agent support automation:safeguards, Multi-agent support automation:cost, Multi-agent support automation:safeguards
- AI-provisional flags: none

| Rubric dim (0/1/2) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Reviewer | Date |
|---|---|---|---|---|---|---|---|---|---|---|
| **Human score** | | | | | | | | | | |

Accepted evidence to verify (does the excerpt really support the claim and score?):

| EV | Target | Score | Claim | Excerpt | Human: supports? |
|---|---|---|---|---|---|
| EV_1 | Single-agent support automation:cost | 1 | A single agent uses fewer tokens and API calls than adding orchestration, though the source recommends validating cost benefits through prototyping. | Single-agent designs reduce token usage and API calls by maintaining context within one entity. Validate cost benefits through prototyping before adding orchestration overhead. | |
| EV_2 | Multi-agent support automation:implementation_complexity | 0 | Multi-agent systems require additional coordination design, error handling, state synchronization, monitoring, and debugging effort. | Each agent interaction requires protocol design, error handling, and state synchronization. Every component needs separate prompt engineering, monitoring infrastructure, and debugging capabilities. | |
| EV_3 | Multi-agent support automation:reliability | 1 | Multi-agent systems can tolerate an individual agent failure, but coordination and context-sharing challenges remain. | - Fault tolerance Multi-agent systems can recover from the failure of individual agents without collapsing. There are challenges in multi-agent architectures, though. For example, it can be complex to share context betwe... | |

Rejected candidates (check for wrongly rejected evidence):

- CAND_1 `Single-agent support automation:implementation_complexity` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_3 `Single-agent support automation:reliability` (verification): verdict=partial: It supports easier debugging and fewer inter-agent failure points, but does not establish recovery or escalation.
- CAND_4 `Single-agent support automation:safeguards` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_6 `Multi-agent support automation:cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_8 `Multi-agent support automation:safeguards` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_9 `Single-agent support automation:implementation_complexity` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_10 `Single-agent support automation:reliability` (verification): verdict=partial: The runtime provides retries and observability, but the excerpt does not establish resolution consistency or monitoring and escalation needs, n
- CAND_11 `Single-agent support automation:safeguards` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_12 `Single-agent support automation:cost` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_13 `Single-agent support automation:implementation_complexity` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_14 `Single-agent support automation:reliability` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_15 `Single-agent support automation:safeguards` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_16 `Multi-agent support automation:implementation_complexity` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_17 `Multi-agent support automation:reliability` (acceptance): lexical check: entity name/alias not found in excerpt context

## Q3 / adaptive - `EVAL_Q3_adaptive_r1_20261029T225859_d662cd`

- Status `partial`, stop `no_progress`, confidence `moderate` (factual `moderate`, stability `provisional`)
- Mechanical: 3 cited evidence IDs, **0 invalid**; 3 accepted / 5 rejected candidates; 2 cited sources from 1 domains
- Unresolved units: Single-agent support automation:implementation_complexity, Single-agent support automation:reliability, Single-agent support automation:safeguards, Multi-agent support automation:cost, Multi-agent support automation:safeguards
- AI-provisional flags: none

| Rubric dim (0/1/2) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Reviewer | Date |
|---|---|---|---|---|---|---|---|---|---|---|
| **Human score** | | | | | | | | | | |

Accepted evidence to verify (does the excerpt really support the claim and score?):

| EV | Target | Score | Claim | Excerpt | Human: supports? |
|---|---|---|---|---|---|
| EV_1 | Single-agent support automation:cost | 1 | A single agent uses fewer tokens and API calls than adding orchestration, though the source recommends validating cost benefits through prototyping. | Single-agent designs reduce token usage and API calls by maintaining context within one entity. Validate cost benefits through prototyping before adding orchestration overhead. | |
| EV_2 | Multi-agent support automation:implementation_complexity | 0 | Multi-agent systems require additional coordination design, error handling, state synchronization, monitoring, and debugging effort. | Each agent interaction requires protocol design, error handling, and state synchronization. Every component needs separate prompt engineering, monitoring infrastructure, and debugging capabilities. | |
| EV_3 | Multi-agent support automation:reliability | 1 | Multi-agent systems can tolerate an individual agent failure, but coordination and context-sharing challenges remain. | - Fault tolerance Multi-agent systems can recover from the failure of individual agents without collapsing. There are challenges in multi-agent architectures, though. For example, it can be complex to share context betwe... | |

Rejected candidates (check for wrongly rejected evidence):

- CAND_1 `Single-agent support automation:implementation_complexity` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_3 `Single-agent support automation:reliability` (verification): verdict=partial: It supports easier debugging and fewer inter-agent failure points, but does not establish recovery or escalation.
- CAND_4 `Single-agent support automation:safeguards` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_6 `Multi-agent support automation:cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_8 `Multi-agent support automation:safeguards` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q4 / static - `EVAL_Q4_static_r1_20261029T225928_c13388`

- Status `failed`, stop `insufficient_evidence`, confidence `low` (factual `n.a.`, stability `undetermined`)
- Mechanical: 0 cited evidence IDs, **0 invalid**; 0 accepted / 25 rejected candidates; 0 cited sources from 0 domains
- Unresolved units: Session-only context memory:retrieval_effectiveness, Session-only context memory:privacy_risk, Session-only context memory:retention_and_deletion_control, Retrieval-augmented memory:retrieval_effectiveness, Retrieval-augmented memory:privacy_risk, Retrieval-augmented memory:retention_and_deletion_control, Persistent customer-profile memory:retrieval_effectiveness, Persistent customer-profile memory:privacy_risk, Persistent customer-profile memory:retention_and_deletion_control
- AI-provisional flags: none

| Rubric dim (0/1/2) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Reviewer | Date |
|---|---|---|---|---|---|---|---|---|---|---|
| **Human score** | | | | | | | | | | |

Accepted evidence to verify (does the excerpt really support the claim and score?):

| EV | Target | Score | Claim | Excerpt | Human: supports? |
|---|---|---|---|---|---|

Rejected candidates (check for wrongly rejected evidence):

- CAND_1 `Session-only context memory:retrieval_effectiveness` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_2 `Session-only context memory:privacy_risk` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_3 `Session-only context memory:retention_and_deletion_control` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_4 `Retrieval-augmented memory:retrieval_effectiveness` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_5 `Retrieval-augmented memory:privacy_risk` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_6 `Retrieval-augmented memory:retention_and_deletion_control` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_7 `Persistent customer-profile memory:retrieval_effectiveness` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_8 `Persistent customer-profile memory:privacy_risk` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_9 `Persistent customer-profile memory:retention_and_deletion_control` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_10 `Session-only context memory:retrieval_effectiveness` (verification): verdict=partial: The excerpt supports multi-turn history and continuity but does not establish that memory is limited to the current session or justify a poor f
- CAND_11 `Session-only context memory:retrieval_effectiveness` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_12 `Session-only context memory:retention_and_deletion_control` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_13 `Retrieval-augmented memory:retrieval_effectiveness` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_14 `Retrieval-augmented memory:privacy_risk` (verification): verdict=partial: The excerpt supports excluding sensitive data from extraction, but does not establish persistent storage or justify a poor privacy score.
- CAND_15 `Retrieval-augmented memory:retention_and_deletion_control` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_16 `Persistent customer-profile memory:retrieval_effectiveness` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_17 `Persistent customer-profile memory:privacy_risk` (verification): verdict=partial: The excerpt supports sensitive-data exclusions but does not establish that the stored memories persist or justify a poor privacy score.
- CAND_18 `Persistent customer-profile memory:retention_and_deletion_control` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_19 `Session-only context memory:privacy_risk` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_20 `Session-only context memory:retention_and_deletion_control` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_21 `Retrieval-augmented memory:privacy_risk` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_22 `Retrieval-augmented memory:retention_and_deletion_control` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_23 `Persistent customer-profile memory:privacy_risk` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_24 `Persistent customer-profile memory:retention_and_deletion_control` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_25 `Session-only context memory:retention_and_deletion_control` (acceptance): lexical check: entity name/alias not found in excerpt context

## Q4 / adaptive - `EVAL_Q4_adaptive_r1_20261029T230209_0ad38a`

- Status `failed`, stop `insufficient_evidence`, confidence `low` (factual `n.a.`, stability `undetermined`)
- Mechanical: 0 cited evidence IDs, **0 invalid**; 0 accepted / 12 rejected candidates; 0 cited sources from 0 domains
- Unresolved units: Session-only context memory:retrieval_effectiveness, Session-only context memory:privacy_risk, Session-only context memory:retention_and_deletion_control, Retrieval-augmented memory:retrieval_effectiveness, Retrieval-augmented memory:privacy_risk, Retrieval-augmented memory:retention_and_deletion_control, Persistent customer-profile memory:retrieval_effectiveness, Persistent customer-profile memory:privacy_risk, Persistent customer-profile memory:retention_and_deletion_control
- AI-provisional flags: none

| Rubric dim (0/1/2) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Reviewer | Date |
|---|---|---|---|---|---|---|---|---|---|---|
| **Human score** | | | | | | | | | | |

Accepted evidence to verify (does the excerpt really support the claim and score?):

| EV | Target | Score | Claim | Excerpt | Human: supports? |
|---|---|---|---|---|---|

Rejected candidates (check for wrongly rejected evidence):

- CAND_1 `Session-only context memory:retrieval_effectiveness` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_2 `Session-only context memory:privacy_risk` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_3 `Session-only context memory:retention_and_deletion_control` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_4 `Retrieval-augmented memory:retrieval_effectiveness` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_5 `Retrieval-augmented memory:privacy_risk` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_6 `Retrieval-augmented memory:retention_and_deletion_control` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_7 `Persistent customer-profile memory:retrieval_effectiveness` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_8 `Persistent customer-profile memory:privacy_risk` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_9 `Persistent customer-profile memory:retention_and_deletion_control` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_10 `Session-only context memory:retrieval_effectiveness` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_11 `Persistent customer-profile memory:retrieval_effectiveness` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_12 `Persistent customer-profile memory:privacy_risk` (acceptance): lexical check: entity name/alias not found in excerpt context

## Q5 / static - `EVAL_Q5_static_r1_20261029T230259_914677`

- Status `partial`, stop `budget_exhausted`, confidence `low` (factual `moderate`, stability `undetermined`)
- Mechanical: 1 cited evidence IDs, **0 invalid**; 1 accepted / 26 rejected candidates; 1 cited sources from 1 domains
- Unresolved units: Managed vector databases:operations_effort, Managed vector databases:engineering_effort, Managed vector databases:operational_resilience, Self-hosted vector databases:operations_effort, Self-hosted vector databases:engineering_effort, Self-hosted vector databases:operational_resilience, Self-hosted vector databases:control_and_customization
- AI-provisional flags: none

| Rubric dim (0/1/2) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Reviewer | Date |
|---|---|---|---|---|---|---|---|---|---|---|
| **Human score** | | | | | | | | | | |

Accepted evidence to verify (does the excerpt really support the claim and score?):

| EV | Target | Score | Claim | Excerpt | Human: supports? |
|---|---|---|---|---|---|
| EV_1 | Managed vector databases:control_and_customization | 1 | Managed platforms provide configuration and security options, while retaining some provider dependency and constraints compared with self-hosting. | They usually offer: • Strong APIs • Security controls • Access management • Backup and recovery • Performance configuration • Usage monitoring • Enterprise-grade reliability | |

Rejected candidates (check for wrongly rejected evidence):

- CAND_1 `Managed vector databases:operations_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_2 `Managed vector databases:engineering_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_3 `Managed vector databases:operational_resilience` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_5 `Self-hosted vector databases:operations_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_6 `Self-hosted vector databases:engineering_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_7 `Self-hosted vector databases:operational_resilience` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_8 `Self-hosted vector databases:control_and_customization` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_9 `Managed vector databases:operations_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_10 `Self-hosted vector databases:operations_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_11 `Self-hosted vector databases:operational_resilience` (verification): verdict=partial: The listed operator responsibilities support substantial in-house operational work, but the excerpt does not directly establish effects on reli
- CAND_12 `Self-hosted vector databases:control_and_customization` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_18 `Self-hosted vector databases:control_and_customization` (grounding): excerpt not found in source text
- CAND_13 `Managed vector databases:operations_effort` (acceptance): verifier: excerpt is not about this entity
- CAND_14 `Managed vector databases:engineering_effort` (verification): verdict=partial: Pipeline abstraction suggests less setup, but the excerpt does not address backend engineering effort or integration maintenance specifically.
- CAND_15 `Self-hosted vector databases:engineering_effort` (verification): verdict=partial: The custom stack is said to require higher implementation effort, but the excerpt does not establish that the workload is substantial enough to
- CAND_16 `Self-hosted vector databases:operations_effort` (verification): verdict=partial: The excerpt names several production tasks, but does not establish that they amount to substantial ongoing operations work.
- CAND_17 `Self-hosted vector databases:operational_resilience` (verification): verdict=partial: It identifies configuration and backup work tied to production reliability, supporting deliberate operational effort, but does not explicitly a
- CAND_19 `Managed vector databases:operations_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_20 `Managed vector databases:engineering_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_21 `Managed vector databases:operational_resilience` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_22 `Managed vector databases:operational_resilience` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_23 `Managed vector databases:control_and_customization` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_24 `Self-hosted vector databases:operations_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_25 `Self-hosted vector databases:engineering_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_26 `Self-hosted vector databases:operational_resilience` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_27 `Self-hosted vector databases:control_and_customization` (acceptance): lexical check: entity name/alias not found in excerpt context

## Q5 / adaptive - `EVAL_Q5_adaptive_r1_20261029T230539_8ca8e4`

- Status `partial`, stop `budget_exhausted`, confidence `moderate` (factual `moderate`, stability `provisional`)
- Mechanical: 4 cited evidence IDs, **0 invalid**; 4 accepted / 25 rejected candidates; 2 cited sources from 2 domains
- Unresolved units: Managed vector databases:operations_effort, Managed vector databases:operational_resilience, Self-hosted vector databases:engineering_effort, Self-hosted vector databases:operational_resilience
- AI-provisional flags: one source supports 3+ targets (SRC_7: 3): check for over-reading of a single page

| Rubric dim (0/1/2) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Reviewer | Date |
|---|---|---|---|---|---|---|---|---|---|---|
| **Human score** | | | | | | | | | | |

Accepted evidence to verify (does the excerpt really support the claim and score?):

| EV | Target | Score | Claim | Excerpt | Human: supports? |
|---|---|---|---|---|---|
| EV_1 | Managed vector databases:control_and_customization | 1 | Managed platforms provide configuration and security options, while retaining some provider dependency and constraints compared with self-hosting. | They usually offer: • Strong APIs • Security controls • Access management • Backup and recovery • Performance configuration • Usage monitoring • Enterprise-grade reliability | |
| EV_2 | Managed vector databases:engineering_effort | 2 | Managed services simplify setup and let engineers focus on application and retrieval work, supporting modest backend engineering effort. | Instead of provisioning and maintaining every infrastructure component, teams can create an index or collection, load embeddings, configure metadata, and connect the database to the application. For many AI products, thi... | |
| EV_3 | Self-hosted vector databases:operations_effort | 0 | Self-hosting makes the team responsible for a broad set of ongoing operations tasks. | Self-hosted vector databases give teams the most control over infrastructure, data placement, configuration, and long-term cost, but they also make the team responsible for deployment, scaling, monitoring, backups, upgra... | |
| EV_4 | Self-hosted vector databases:control_and_customization | 2 | Self-hosting provides broad control over infrastructure, data placement, deployment, and configuration choices. | Self-hosting is attractive because it gives teams direct control over the database environment. They can choose instance types, storage classes, regions, network topology, backup tooling, deployment cadence, and resource... | |

Rejected candidates (check for wrongly rejected evidence):

- CAND_1 `Managed vector databases:operations_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_2 `Managed vector databases:engineering_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_3 `Managed vector databases:operational_resilience` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_5 `Self-hosted vector databases:operations_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_6 `Self-hosted vector databases:engineering_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_7 `Self-hosted vector databases:operational_resilience` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_8 `Self-hosted vector databases:control_and_customization` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_9 `Managed vector databases:operations_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_10 `Self-hosted vector databases:operations_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_11 `Self-hosted vector databases:operational_resilience` (verification): verdict=partial: The listed operator responsibilities support substantial in-house operational work, but the excerpt does not directly establish effects on reli
- CAND_12 `Self-hosted vector databases:control_and_customization` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_13 `Managed vector databases:operations_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_15 `Managed vector databases:operational_resilience` (verification): verdict=partial: It supports managed availability and scaling with less operational work, but does not address recovery enough to establish the strong anchor.
- CAND_16 `Managed vector databases:control_and_customization` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_18 `Self-hosted vector databases:engineering_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_19 `Self-hosted vector databases:operational_resilience` (verification): verdict=partial: It identifies traffic spikes, node failures, and index rebuilds as team-owned questions and warns that lack of ownership can slow the product.
- CAND_21 `Self-hosted vector databases:operational_resilience` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_22 `Managed vector databases:operations_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_23 `Managed vector databases:operational_resilience` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_24 `Self-hosted vector databases:engineering_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_25 `Self-hosted vector databases:operations_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_26 `Managed vector databases:engineering_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_27 `Managed vector databases:engineering_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_28 `Managed vector databases:control_and_customization` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_29 `Self-hosted vector databases:control_and_customization` (acceptance): lexical check: entity name/alias not found in excerpt context

## Q8 / static - `EVAL_Q8_static_r1_20261029T230659_6d7fc8`

- Status `partial`, stop `budget_exhausted`, confidence `low` (factual `high`, stability `None`)
- Mechanical: 9 cited evidence IDs, **0 invalid**; 9 accepted / 8 rejected candidates; 5 cited sources from 4 domains
- Unresolved units: llm_eval_or_observability, open_source_license, self_hosting_support
- AI-provisional flags: one source supports 3+ targets (SRC_3: 3; SRC_4: 3): check for over-reading of a single page

| Rubric dim (0/1/2) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Reviewer | Date |
|---|---|---|---|---|---|---|---|---|---|---|
| **Human score** | | | | | | | | | | |

Accepted evidence to verify (does the excerpt really support the claim and score?):

| EV | Target | Score | Claim | Excerpt | Human: supports? |
|---|---|---|---|---|---|
| EV_1 | open_source_license | - | The repository lists the Apache License 2.0. | - License: Apache License 2.0 - | |
| EV_2 | open_source_license | - | OpenLIT is available under Apache 2.0. | Free to self-host under Apache 2.0. | |
| EV_3 | self_hosting_support | - | OpenLIT supports self-hosting with Docker Compose or Kubernetes Helm. | How do I deploy OpenLIT? Self-host with Docker Compose or Kubernetes Helm. | |
| EV_4 | llm_eval_or_observability | - | Langfuse supports monitoring and evaluation of AI applications. | Langfuse is an open source LLM engineering platform. It helps teams collaboratively develop, monitor, evaluate, and debug AI applications. | |
| EV_5 | open_source_license | - | The repository is MIT licensed, with an exception for the ee folders. | This repository is MIT licensed, except for the `ee` folders. | |
| EV_6 | self_hosting_support | - | Langfuse supports self-hosting. | Langfuse can be self-hosted in minutes and is battle-tested. | |
| EV_7 | llm_eval_or_observability | - | Comet Opik is described as a tracing and evaluation tool. | Comet Opik is another Apache-2.0 option focused on tracing and evals. | |
| EV_8 | llm_eval_or_observability | - | The tool is an observability and evaluation platform for agents and LLM applications. | W&B Weave is an observability and evaluation platform for building reliable agents and LLM applications. | |
| EV_9 | self_hosting_support | - | Langfuse supports self-hosting using Docker. | Langfuse is open source and can be self-hosted using Docker. | |

Rejected candidates (check for wrongly rejected evidence):

- CAND_1 `llm_eval_or_observability` (grounding): excerpt not found in source text
- CAND_5 `llm_eval_or_observability` (grounding): excerpt not found in source text
- CAND_3 `llm_eval_or_observability` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_4 `open_source_license` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_13 `llm_eval_or_observability` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_14 `open_source_license` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_15 `self_hosting_support` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_16 `llm_eval_or_observability` (verification): verdict=partial: It says tracing and evaluation events are handled, but does not explicitly connect them to observing or evaluating LLM applications or models.

## Q8 / adaptive - `EVAL_Q8_adaptive_r1_20261029T230817_0c5218`

- Status `partial`, stop `no_progress`, confidence `low` (factual `high`, stability `None`)
- Mechanical: 7 cited evidence IDs, **0 invalid**; 7 accepted / 9 rejected candidates; 3 cited sources from 2 domains
- Unresolved units: llm_eval_or_observability, open_source_license, self_hosting_support
- AI-provisional flags: one source supports 3+ targets (SRC_3: 3; SRC_4: 3): check for over-reading of a single page

| Rubric dim (0/1/2) | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Reviewer | Date |
|---|---|---|---|---|---|---|---|---|---|---|
| **Human score** | | | | | | | | | | |

Accepted evidence to verify (does the excerpt really support the claim and score?):

| EV | Target | Score | Claim | Excerpt | Human: supports? |
|---|---|---|---|---|---|
| EV_1 | open_source_license | - | The repository lists the Apache License 2.0. | - License: Apache License 2.0 - | |
| EV_2 | open_source_license | - | OpenLIT is available under Apache 2.0. | Free to self-host under Apache 2.0. | |
| EV_3 | self_hosting_support | - | OpenLIT supports self-hosting with Docker Compose or Kubernetes Helm. | How do I deploy OpenLIT? Self-host with Docker Compose or Kubernetes Helm. | |
| EV_4 | llm_eval_or_observability | - | Langfuse supports monitoring and evaluation of AI applications. | Langfuse is an open source LLM engineering platform. It helps teams collaboratively develop, monitor, evaluate, and debug AI applications. | |
| EV_5 | open_source_license | - | The repository is MIT licensed, with an exception for the ee folders. | This repository is MIT licensed, except for the `ee` folders. | |
| EV_6 | self_hosting_support | - | Langfuse supports self-hosting. | Langfuse can be self-hosted in minutes and is battle-tested. | |
| EV_7 | llm_eval_or_observability | - | Comet Opik is described as a tracing and evaluation tool. | Comet Opik is another Apache-2.0 option focused on tracing and evals. | |

Rejected candidates (check for wrongly rejected evidence):

- CAND_1 `llm_eval_or_observability` (grounding): excerpt not found in source text
- CAND_5 `llm_eval_or_observability` (grounding): excerpt not found in source text
- CAND_3 `llm_eval_or_observability` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_4 `open_source_license` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_12 `llm_eval_or_observability` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_13 `open_source_license` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_14 `self_hosting_support` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_15 `llm_eval_or_observability` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_16 `self_hosting_support` (acceptance): lexical check: entity name/alias not found in excerpt context

