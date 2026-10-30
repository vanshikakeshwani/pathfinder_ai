# AI-provisional review materials (V2)

> **AI-PROVISIONAL, NOT HUMAN EVALUATION.** These are mechanical checks computed from the run files, plus flags raised by the AI assistant. No score here is a human judgement. Human scores go in `HUMAN_REVIEW_WORKSHEET.csv`.

## Q1 r1 static - `EVAL_Q1_r1_static_20261030T045521_06512e`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (undetermined), recommendation `none`
- Mechanical: 4 cited evidence IDs, **0 invalid**; 4 accepted / 14 rejected (lexical 1, approach-identity 0); single-source cells: Weaviate:filtering_capability, Milvus:deployment_fit, Milvus:operational_effort
- AI-provisional flags: none

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Weaviate:filtering_capability | 2 | general | Weaviate provides powerful filtered vector search capabiliti... | Strong: the excerpt explicitly describes applying structured filters alongside vector search to find the closest matchin... | Weaviate provides powerful filtered vector search capabilities, allowing you to combine vector searches with structured, scalar filters. This enables you to find the closest vectors to a query vector ... |
| EV_2 | Milvus:deployment_fit | 2 | general | Milvus Lite | Strong: the excerpt gives a direct pip-install/local-file path and describes the single-machine deployment as convenient... | To integrate Milvus Lite into your applications, run`pip install pymilvus` to install it and use the`MilvusClient("./demo.db")` statement to instantiate a vector database with a local file that persis... |
| EV_3 | Milvus:operational_effort | 1 | self_hosted | Milvus Standalone | Plausible: the excerpt says Standalone requires much less DevOps than maintaining Kubernetes, but does not establish tha... | For early-stage production, when the project is still seeking product-market fit and agility is more important than scalability, Milvus Standalone is the best choice. It can still scale up to 100M vec... |
| EV_4 | Milvus:operational_effort | 1 | self_hosted | operate the K8s cluster that runs Milvus Distributed | Plausible: the excerpt explicitly identifies Kubernetes cluster operation as work for the Distributed deployment, but do... | You can keep using Milvus Standalone for dev or staging environment for its convenience, and operate the K8s cluster that runs Milvus Distributed. |

Rejected candidates:

- CAND_1 `Qdrant:deployment_fit` (acceptance): verifier attributes the excerpt to 'multiple', not Qdrant
- CAND_2 `Qdrant:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_3 `Milvus:operational_effort` (verification): verdict=partial: The context associates the extra operational moving parts with Milvus, but does not explicitly compare its operational burden with alternatives or establ
- CAND_4 `Weaviate:deployment_fit` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_5 `Weaviate:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_6 `Milvus:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_7 `Milvus:deployment_fit` (acceptance): verifier attributes the excerpt to 'multiple', not Milvus
- CAND_8 `Weaviate:deployment_fit` (acceptance): verifier attributes the excerpt to 'multiple', not Weaviate
- CAND_9 `Weaviate:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_12 `Qdrant:operational_effort` (grounding): excerpt not found in source text
- CAND_10 `Qdrant:deployment_fit` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_11 `Qdrant:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_13 `Qdrant:operational_effort` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_16 `Milvus:filtering_capability` (acceptance): lexical check: entity name/alias not found in excerpt context

## Q1 r1 adaptive - `EVAL_Q1_r1_adaptive_20261030T045738_a79d3f`

- Status `partial`, stop `budget_exhausted`, interval leader `Milvus` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only)
- Mechanical: 4 cited evidence IDs, **0 invalid**; 4 accepted / 15 rejected (lexical 1, approach-identity 0); single-source cells: Qdrant:deployment_fit, Milvus:deployment_fit, Milvus:filtering_capability, Milvus:operational_effort
- AI-provisional flags: none

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Milvus:deployment_fit | 2 | general | Milvus Standalone is a single-machine server deployment. | Strong anchor: the excerpt describes a readily selectable, convenient deployment path and explicitly identifies when it ... | Milvus Standalone is a single-machine server deployment. All components of Milvus Standalone are packed into a single Docker image, making deployment convenient. If you have a production workload but ... |
| EV_2 | Milvus:filtering_capability | 1 | general | client.search( collection_name="papers" | Plausible anchor: the example demonstrates a common metadata-filtered vector retrieval query, but it shows only a basic ... | hits = client.search( collection_name="papers", data=[query_vector], limit=5, filter="year >= 2023", output_fields=["title", "year"], ) |
| EV_3 | Milvus:operational_effort | 2 | managed | Zilliz Cloud sells the same engine with those decisions take... | Strong anchor: for the managed scope, the excerpt says decisions around failover, replica placement, compaction, and ind... | Self-hosting Milvus means owning coordinator failover, replica placement, compaction behaviour and index-build capacity. Zilliz Cloud sells the same engine with those decisions taken off the table, an... |
| EV_4 | Qdrant:deployment_fit | 2 | general | Create a free Qdrant Cloud cluster on AWS, GCP, or Azure and... | Strong: the excerpt describes a free deployment path on major cloud providers that can be queried in minutes, making it ... | Cloud Quickstart — Create a free Qdrant Cloud cluster on AWS, GCP, or Azure and query it in minutes. |

Rejected candidates:

- CAND_1 `Qdrant:deployment_fit` (acceptance): verifier attributes the excerpt to 'multiple', not Qdrant
- CAND_2 `Qdrant:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_3 `Milvus:operational_effort` (verification): verdict=partial: The context associates the extra operational moving parts with Milvus, but does not explicitly compare its operational burden with alternatives or establ
- CAND_4 `Weaviate:deployment_fit` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_5 `Weaviate:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_6 `Milvus:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_7 `Milvus:deployment_fit` (acceptance): verifier attributes the excerpt to 'multiple', not Milvus
- CAND_8 `Weaviate:deployment_fit` (acceptance): verifier attributes the excerpt to 'multiple', not Weaviate
- CAND_9 `Weaviate:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_11 `Milvus:filtering_capability` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_12 `Milvus:operational_effort` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_13 `Milvus:deployment_fit` (grounding): excerpt not found in source text
- CAND_15 `Milvus:operational_effort` (grounding): excerpt not found in source text
- CAND_18 `Qdrant:filtering_capability` (verification): verdict=partial: It confirms filtering in Qdrant search but does not establish metadata filtering alongside vector search or its flexibility.
- CAND_19 `Qdrant:operational_effort` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q2 r1 static - `EVAL_Q2_r1_static_20261030T045908_293c54`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (None), recommendation `not_applicable`
- Mechanical: 20 cited evidence IDs, **0 invalid**; 32 accepted / 3 rejected (lexical 3, approach-identity 0); single-source cells: none
- AI-provisional flags: one source supports 3+ targets: SRC_1 (4); SRC_4 (3); SRC_6 (4); SRC_7 (3); SRC_8 (3); SRC_9 (3); SRC_10 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | india_headquarters | - | general | Peoplestrong / Exact match / Gurgaon, India✓ HQ recorded |  | / 3 / Peoplestrong / Exact match / Gurgaon, India✓ HQ recorded Sep 29, 2026 |
| EV_2 | b2b_saas | - | general | PeopleStrong is Asia’s leading, and the most comprehensive H... |  | PeopleStrong is Asia’s leading, and the most comprehensive Human Capital Management SaaS platform. |
| EV_3 | hr_technology | - | general | one of Asia’s most widely adopted HRTech platforms, trusted ... |  | PeopleStrong PeopleStrong is one of Asia’s most widely adopted HRTech platforms, trusted by 500+ major enterprises and 2 million+ users across India and Asia‐Pacific. |
| EV_4 | market_positioning | - | general | best suited for large organisations with distributed workfor... |  | Its HR Tech 4.0 suite unifies recruitment, onboarding, payroll, performance, learning and talent management in one system rather than separate point tools — reducing manual effort and increasing HR in... |
| EV_5 | india_headquarters | - | general | Greythr / Exact match / Bangalore, India✓ HQ recorded |  | / 5 / Greythr / Exact match / Bangalore, India✓ HQ recorded Sep 29, 2026 |
| EV_6 | b2b_saas | - | general | HRMS solutions with strong adoption among SMEs and mid‐sized... |  | greytHR is one of India’s oldest and most trusted HRMS solutions with strong adoption among SMEs and mid‐sized businesses. |
| EV_7 | hr_technology | - | general | comprehensive payroll automation |  | It’s widely recognised for comprehensive payroll automation, statutory compliance support (PF, ESI, TDS) and core HR tasks such as attendance, leave and document management. |
| EV_8 | market_positioning | - | general | an excellent fit for small to medium businesses prioritising... |  | Its platform handles key day‐to‐day workforce operations with minimal complexity, freeing HR teams from manual spreadsheets and supporting compliance across India’s regulatory environment, making it a... |
| EV_9 | india_headquarters | - | general | Betterplace / Exact match / Bangalore, India✓ HQ recorded |  | / 7 / Betterplace / Exact match / Bangalore, India✓ HQ recorded Sep 29, 2026 |
| EV_10 | b2b_saas | - | general | human capital SaaS solution that enables enterprises |  | BetterPlace is Asia’s largest human capital SaaS solution that enables enterprises to manage the entire lifecycle of their frontline workers. |
| EV_11 | hr_technology | - | general | manage the entire lifecycle of their frontline workers |  | BetterPlace is Asia’s largest human capital SaaS solution that enables enterprises to manage the entire lifecycle of their frontline workers. |
| EV_12 | market_positioning | - | general | enables enterprises to manage the entire lifecycle of their ... |  | BetterPlace is Asia’s largest human capital SaaS solution that enables enterprises to manage the entire lifecycle of their frontline workers. |
| EV_13 | hr_technology | - | general | Human Capital Management, Payroll, Talent Acquisition & Mana... |  | Our comprehensive HR Tech 4.0 platform encompasses employee lifecycle from hire to exit, including Human Capital Management, Payroll, Talent Acquisition & Management, and Collaboration. |
| EV_14 | market_positioning | - | general | We power the experience of your talent workforce |  | We power the experience of your talent workforce, help you take data-driven decisions that impact your people, and bring agility to your business operations |
| EV_15 | india_headquarters | - | general | CoreHRx is a product of THINKNEXT INNOVATIONS PRIVATE LIMITE... |  | CoreHRx is a product of THINKNEXT INNOVATIONS PRIVATE LIMITED, headquartered in Sector 63, Noida, Uttar Pradesh. |
| EV_16 | b2b_saas | - | general | India's fastest-growing HR SaaS product. We serve 1,000+ org... |  | Incubated at IIM Lucknow's EIC and recognised as India's fastest-growing HR SaaS product. We serve 1,000+ organisations across India and 10+ countries — helping HR teams, business owners, and employee... |
| EV_17 | hr_technology | - | general | We're building the future of workforce management |  | We're building the future of workforce management CoreHRx was born from a simple frustration — why is HR so complicated for small Indian businesses? We're here to fix that. |
| EV_18 | market_positioning | - | general | why is HR so complicated for small Indian businesses? We're ... |  | CoreHRx was born from a simple frustration — why is HR so complicated for small Indian businesses? We're here to fix that. |
| EV_19 | b2b_saas | - | general | Indian businesses paying for 247HRM |  | 1,500+ Active customers Indian businesses paying for 247HRM in May 2026 |
| EV_20 | hr_technology | - | general | 247HRM runs HR and payroll for 1500+ companies |  | 247HRM runs HR and payroll for 1500+ companies across 30+ industries. |
| EV_21 | market_positioning | - | general | From single-location startups to 5,000-employee multi-site g... |  | From single-location startups to 5,000-employee multi-site groups across 28 states. If it pays a salary in India, we've probably done it. |
| EV_22 | b2b_saas | - | general | 33,000+ Companies |  | ### 30+ Countries ### 33,000+ Companies ### 3.5 million+ Employees |
| EV_23 | hr_technology | - | general | Plan, Recruit, Onboard, Pay, Manage, Upskill, Appraise and E... |  | Plan, Recruit, Onboard, Pay, Manage, Upskill, Appraise and Empower your people — all in one platform. |
| EV_24 | market_positioning | - | general | Whether you're replacing spreadsheets or outgrowing your cur... |  | Whether you're replacing spreadsheets or outgrowing your current HRMS, here's what changes on day one. |
| EV_25 | b2b_saas | - | general | Launched India's 1st cloud-based HR & Payroll software |  | 2007 Launched India's 1st cloud-based HR & Payroll software across the country. |
| EV_26 | b2b_saas | - | general | at least 1 million businesses around the world having minimu... |  | Similarly, we have created HRMantra as a beautiful piece of art & a work of love after investing tens of thousands of person years since 1999 to make it desirable for at least 1 million businesses aro... |
| EV_27 | hr_technology | - | general | HRMantra Human Capital Management software |  | The following are the major features of the HRMantra Human Capital Management software. |
| EV_28 | market_positioning | - | general | Any & all hire-to-retire HCM policies |  | Any & all hire-to-retire HCM policies, however complex, in any country, industry, or company of any size, will be readily personalized right down to the staff level, WITHOUT ANY EXTRA CODING |
| EV_29 | b2b_saas | - | general | brings core HR, attendance, payroll, recruitment |  | Timelabs is an HRMS and HR operating system that brings core HR, attendance, payroll, recruitment, employee self service, analytics, and workforce management together on one connected platform. |
| EV_30 | b2b_saas | - | general | 1000+ businesses choose Timelabs |  | See why 1000+ businesses choose Timelabs to simplify HR, connect everything, and get more done. |
| EV_31 | hr_technology | - | general | HRMS and HR operating system |  | Timelabs is an HRMS and HR operating system that brings core HR, attendance, payroll, recruitment, employee self service, analytics, and workforce management together on one connected platform. |
| EV_32 | market_positioning | - | general | centralized HR operations across employees, locations, teams... |  | Timelabs is a scalable HR software in India designed for organizations that need centralized HR operations across employees, locations, teams, and business units. |

Rejected candidates:

- CAND_13 `india_headquarters` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_14 `b2b_saas` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_32 `b2b_saas` (acceptance): lexical check: entity name/alias not found in excerpt context

## Q2 r1 adaptive - `EVAL_Q2_r1_adaptive_20261030T050127_d120ce`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (None), recommendation `not_applicable`
- Mechanical: 17 cited evidence IDs, **0 invalid**; 26 accepted / 9 rejected (lexical 3, approach-identity 0); single-source cells: none
- AI-provisional flags: one source supports 3+ targets: SRC_1 (4); SRC_4 (3); SRC_6 (4); SRC_7 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | india_headquarters | - | general | Peoplestrong / Exact match / Gurgaon, India✓ HQ recorded |  | / 3 / Peoplestrong / Exact match / Gurgaon, India✓ HQ recorded Sep 29, 2026 |
| EV_2 | b2b_saas | - | general | PeopleStrong is Asia’s leading, and the most comprehensive H... |  | PeopleStrong is Asia’s leading, and the most comprehensive Human Capital Management SaaS platform. |
| EV_3 | hr_technology | - | general | one of Asia’s most widely adopted HRTech platforms, trusted ... |  | PeopleStrong PeopleStrong is one of Asia’s most widely adopted HRTech platforms, trusted by 500+ major enterprises and 2 million+ users across India and Asia‐Pacific. |
| EV_4 | market_positioning | - | general | best suited for large organisations with distributed workfor... |  | Its HR Tech 4.0 suite unifies recruitment, onboarding, payroll, performance, learning and talent management in one system rather than separate point tools — reducing manual effort and increasing HR in... |
| EV_5 | india_headquarters | - | general | Greythr / Exact match / Bangalore, India✓ HQ recorded |  | / 5 / Greythr / Exact match / Bangalore, India✓ HQ recorded Sep 29, 2026 |
| EV_6 | b2b_saas | - | general | HRMS solutions with strong adoption among SMEs and mid‐sized... |  | greytHR is one of India’s oldest and most trusted HRMS solutions with strong adoption among SMEs and mid‐sized businesses. |
| EV_7 | hr_technology | - | general | comprehensive payroll automation |  | It’s widely recognised for comprehensive payroll automation, statutory compliance support (PF, ESI, TDS) and core HR tasks such as attendance, leave and document management. |
| EV_8 | market_positioning | - | general | an excellent fit for small to medium businesses prioritising... |  | Its platform handles key day‐to‐day workforce operations with minimal complexity, freeing HR teams from manual spreadsheets and supporting compliance across India’s regulatory environment, making it a... |
| EV_9 | india_headquarters | - | general | Betterplace / Exact match / Bangalore, India✓ HQ recorded |  | / 7 / Betterplace / Exact match / Bangalore, India✓ HQ recorded Sep 29, 2026 |
| EV_10 | b2b_saas | - | general | human capital SaaS solution that enables enterprises |  | BetterPlace is Asia’s largest human capital SaaS solution that enables enterprises to manage the entire lifecycle of their frontline workers. |
| EV_11 | hr_technology | - | general | manage the entire lifecycle of their frontline workers |  | BetterPlace is Asia’s largest human capital SaaS solution that enables enterprises to manage the entire lifecycle of their frontline workers. |
| EV_12 | market_positioning | - | general | enables enterprises to manage the entire lifecycle of their ... |  | BetterPlace is Asia’s largest human capital SaaS solution that enables enterprises to manage the entire lifecycle of their frontline workers. |
| EV_13 | hr_technology | - | general | Our comprehensive HR Tech 4.0 platform |  | Our comprehensive HR Tech 4.0 platform encompasses employee lifecycle from hire to exit, including Human Capital Management, Payroll, Talent Acquisition & Management, and Collaboration. |
| EV_14 | market_positioning | - | general | We power the experience of your talent workforce |  | We power the experience of your talent workforce, help you take data-driven decisions that impact your people, and bring agility to your business operations We are the momentum that powers your growth... |
| EV_15 | india_headquarters | - | general | CoreHRx is a product of THINKNEXT INNOVATIONS PRIVATE LIMITE... |  | CoreHRx is a product of THINKNEXT INNOVATIONS PRIVATE LIMITED, headquartered in Sector 63, Noida, Uttar Pradesh. |
| EV_16 | b2b_saas | - | general | recognised as India's fastest-growing HR SaaS product |  | Incubated at IIM Lucknow's EIC and recognised as India's fastest-growing HR SaaS product. We serve 1,000+ organisations across India and 10+ countries — helping HR teams, business owners, and employee... |
| EV_17 | hr_technology | - | general | Automated processes linked directly to payroll |  | Accurate & Transparent Attendance and payroll should be dispute-free. Automated processes linked directly to payroll — no guesswork. |
| EV_18 | market_positioning | - | general | why is HR so complicated for small Indian businesses? |  | CoreHRx was born from a simple frustration — why is HR so complicated for small Indian businesses? We're here to fix that. |
| EV_19 | india_headquarters | - | general | the Bengaluru-headquartered HR tech startup |  | In 2023, the Bengaluru-headquartered HR tech startup expanded into the UAE and Southeast Asia, acquired HR tech firms Troopers and MyRobin, and partnered with Microsoft to enhance its tech capabilitie... |
| EV_20 | hr_technology | - | general | Betterplace streamlines HR functions via a unified, data-dri... |  | Founded in 2015 by Pravin Agarwala, Uday Singh, and Saurabh Tandon, Betterplace streamlines HR functions via a unified, data-driven platform. From talent acquisition and onboarding to background verif... |
| EV_21 | market_positioning | - | general | consolidates key HR tasks into a single interface |  | Founded in 2015 by Pravin Agarwala, Uday Singh, and Saurabh Tandon, Betterplace streamlines HR functions via a unified, data-driven platform. From talent acquisition and onboarding to background verif... |
| EV_22 | hr_technology | - | general | Cutshort is a Pune-based HRTech platform that simplifies tec... |  | Founded in 2015 by Nikunj Verma and Anubhav Gupta, Cutshort is a Pune-based HRTech platform that simplifies tech hiring for companies and job seekers alike. With a focus on fast and reliable talent ma... |
| EV_23 | market_positioning | - | general | Using algorithmic matching and AI-based recommendations |  | The platform includes a trust score feature to verify candidate reliability and integrates with partner networks to expand the talent pool. Using algorithmic matching and AI-based recommendations, Cut... |
| EV_24 | hr_technology | - | general | solutions for recruitment, onboarding, payroll, travel, and ... |  | Darwinbox is a Hyderabad-based cloud HR technology platform that provides comprehensive solutions for recruitment, onboarding, payroll, travel, and people analytics. Incorporated in 2015 by Chaitanya ... |
| EV_25 | b2b_saas | - | general | they switched to Cutshort |  | The recruitment team of Antares Tech was looking for a self-service platform which would help capture the essence of their hiring philosophy. After trying agencies and quite a few traditional sources,... |
| EV_26 | hr_technology | - | general | they turned to Cutshort |  | When US headquartered gift card technology leader Blackhawk Network started their engineering centre in India, they turned to Cutshort to remove their operational bottlenecks and make their recruitmen... |

Rejected candidates:

- CAND_13 `india_headquarters` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_14 `b2b_saas` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_23 `b2b_saas` (verification): verdict=partial: It establishes business customers and HRMS/workforce solutions but does not explicitly establish a SaaS offering.
- CAND_25 `india_headquarters` (verification): verdict=partial: Pune-based identifies an Indian base, but does not expressly establish a headquarters or principal office.
- CAND_27 `b2b_saas` (verification): verdict=partial: It describes an employer-facing hiring platform, but does not explicitly establish SaaS delivery.
- CAND_29 `india_headquarters` (verification): verdict=partial: Hyderabad-based indicates an Indian base, but does not expressly establish a headquarters or principal office.
- CAND_30 `b2b_saas` (verification): verdict=partial: It identifies a cloud HR platform and its functions, but does not explicitly establish business customers or SaaS service to them.
- CAND_32 `market_positioning` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_35 `market_positioning` (verification): verdict=partial: The excerpt supports talent discovery and faster turnaround but does not directly establish Cutshort’s own market positioning as a hiring platform.

## Q3 r1 static - `EVAL_Q3_r1_static_20261030T050321_d86f10`

- Status `partial`, stop `budget_exhausted`, interval leader `Single-agent support automation` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only); differentiating cells lack strong support (single source or non-official): Single-agent support automation:total_cost, Multi-agent support automation:total_cost
- Mechanical: 7 cited evidence IDs, **0 invalid**; 7 accepted / 10 rejected (lexical 0, approach-identity 2); single-source cells: Single-agent support automation:total_cost, Single-agent support automation:reliability, Single-agent support automation:safeguards, Multi-agent support automation:implementation_complexity, Multi-agent support automation:total_cost, Multi-agent support automation:reliability, Multi-agent support automation:safeguards
- AI-provisional flags: one source supports 3+ targets: SRC_1 (6)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Single-agent support automation:total_cost | 1 | general | Single-agent designs reduce token usage and API calls | Plausible anchor: this supports lower usage costs, but does not give an absolute cost estimate or show that total implem... | Low-cost a priority. Single-agent designs reduce token usage and API calls by maintaining context within one entity. |
| EV_2 | Single-agent support automation:reliability | 1 | general | Single agents eliminate inter-agent communication protocols | Plausible anchor: fewer coordination failure points and straightforward debugging support consistency, but the excerpt d... | Single agents eliminate inter-agent communication protocols that introduce latency and failure points. Debugging becomes straightforward when all logic resides in one place. |
| EV_3 | Single-agent support automation:safeguards | 1 | general | around single agents | Plausible anchor: practical controls and auditability are available, but the excerpt describes them as workflow capabili... | Governance and compliance. Implement logging, approval gates, and audit trails through workflow capabilities. These controls satisfy regulatory requirements and provide operational visibility into age... |
| EV_4 | Multi-agent support automation:implementation_complexity | 1 | general | Each agent interaction requires protocol design | Plausible anchor: the excerpt shows meaningful orchestration and operational work, but does not establish that this effo... | Each agent interaction requires protocol design, error handling, and state synchronization. Every component needs separate prompt engineering, monitoring infrastructure, and debugging capabilities. |
| EV_5 | Multi-agent support automation:total_cost | 0 | general | multi-agent implementations typically use 3-10x more tokens | Poor anchor: the excerpt reports materially higher token usage for equivalent tasks, a cost risk for a small company; it... | In our testing, multi-agent implementations typically use 3-10x more tokens than single-agent approaches for equivalent tasks. This overhead stems from duplicating context across agents, coordination ... |
| EV_6 | Multi-agent support automation:reliability | 1 | general | Manual chaining of agents creates brittle connections | Plausible anchor: workflows can improve coordination reliability, while the excerpt also identifies unpredictable failur... | Manual chaining of agents creates brittle connections that fail unpredictably. Workflows provide structured coordination that ensures reliable agent interaction. |
| EV_7 | Multi-agent support automation:safeguards | 1 | general | limits the blast radius of security incidents | Plausible anchor: the excerpt supports data isolation and least-privilege boundaries, but does not establish approval ga... | Build multiple agents when regulations or policies mandate strict data isolation. Different security classifications need independent processing environments that single agents can't provide. This lea... |

Rejected candidates:

- CAND_1 `Single-agent support automation:implementation_complexity` (grounding): excerpt not found in source text
- CAND_9 `Single-agent support automation:implementation_complexity` (acceptance): approach identity: excerpt describes several alternatives without isolating this one
- CAND_10 `Single-agent support automation:reliability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_11 `Single-agent support automation:safeguards` (verification): verdict=partial: It recommends prompt-level behavioral guardrails for an agent generally, but does not attribute them specifically to single-agent support automation or e
- CAND_12 `Multi-agent support automation:implementation_complexity` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_13 `Multi-agent support automation:reliability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_14 `Multi-agent support automation:safeguards` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_15 `Single-agent support automation:implementation_complexity` (acceptance): approach identity: identification quote missing or not found verbatim in the source
- CAND_16 `Single-agent support automation:reliability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_17 `Single-agent support automation:safeguards` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q3 r1 adaptive - `EVAL_Q3_r1_adaptive_20261030T050553_bf37a7`

- Status `partial`, stop `no_progress`, interval leader `Single-agent support automation` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only); differentiating cells lack strong support (single source or non-official): Multi-agent support automation:total_cost
- Mechanical: 11 cited evidence IDs, **0 invalid**; 12 accepted / 10 rejected (lexical 0, approach-identity 1); single-source cells: Multi-agent support automation:implementation_complexity, Multi-agent support automation:total_cost
- AI-provisional flags: one source supports 3+ targets: SRC_1 (6); SRC_7 (5)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Single-agent support automation:total_cost | 1 | general | Single-agent designs reduce token usage and API calls | Plausible anchor: this supports lower usage costs, but does not give an absolute cost estimate or show that total implem... | Low-cost a priority. Single-agent designs reduce token usage and API calls by maintaining context within one entity. |
| EV_2 | Single-agent support automation:reliability | 1 | general | Single agents eliminate inter-agent communication protocols | Plausible anchor: fewer coordination failure points and straightforward debugging support consistency, but the excerpt d... | Single agents eliminate inter-agent communication protocols that introduce latency and failure points. Debugging becomes straightforward when all logic resides in one place. |
| EV_3 | Single-agent support automation:safeguards | 1 | general | around single agents | Plausible anchor: practical controls and auditability are available, but the excerpt describes them as workflow capabili... | Governance and compliance. Implement logging, approval gates, and audit trails through workflow capabilities. These controls satisfy regulatory requirements and provide operational visibility into age... |
| EV_4 | Multi-agent support automation:implementation_complexity | 1 | general | Each agent interaction requires protocol design | Plausible anchor: the excerpt shows meaningful orchestration and operational work, but does not establish that this effo... | Each agent interaction requires protocol design, error handling, and state synchronization. Every component needs separate prompt engineering, monitoring infrastructure, and debugging capabilities. |
| EV_5 | Multi-agent support automation:total_cost | 0 | general | multi-agent implementations typically use 3-10x more tokens | Poor anchor: the excerpt reports materially higher token usage for equivalent tasks, a cost risk for a small company; it... | In our testing, multi-agent implementations typically use 3-10x more tokens than single-agent approaches for equivalent tasks. This overhead stems from duplicating context across agents, coordination ... |
| EV_6 | Multi-agent support automation:reliability | 1 | general | Manual chaining of agents creates brittle connections | Plausible anchor: workflows can improve coordination reliability, while the excerpt also identifies unpredictable failur... | Manual chaining of agents creates brittle connections that fail unpredictably. Workflows provide structured coordination that ensures reliable agent interaction. |
| EV_7 | Multi-agent support automation:safeguards | 1 | general | limits the blast radius of security incidents | Plausible anchor: the excerpt supports data isolation and least-privilege boundaries, but does not establish approval ga... | Build multiple agents when regulations or policies mandate strict data isolation. Different security classifications need independent processing environments that single agents can't provide. This lea... |
| EV_8 | Single-agent support automation:total_cost | 1 | general | Usually simpler to predict and operate | This supports the plausible anchor because costs are described as simpler to predict and operate, but the source gives n... | / Cost / Usually simpler to predict and operate / Can increase model calls, tracing, evaluation, and maintenance costs / |
| EV_9 | Single-agent support automation:reliability | 1 | general | a single agent can often classify internally | This supports the plausible anchor: the approach can handle common requests and escalate, but the excerpt does not estab... | For a small team, a single agent can often classify internally and either answer from grounded knowledge or escalate. That reduces the number of handoffs that can fail. |
| EV_10 | Single-agent support automation:safeguards | 1 | general | A well-designed single-agent support system | This supports the plausible anchor by describing practical guardrails, logging, and escalation, but does not show that l... | A well-designed single-agent support system can retrieve from approved documentation, verify a customer identity, look up a customer record, apply policy, call a narrow tool, log the result, and escal... |
| EV_11 | Multi-agent support automation:reliability | 1 | general | If it sends a cancellation request to a generic FAQ agent | This supports the plausible anchor: routing errors are a notable failure case, but the source describes testing and fall... | But a router can also be wrong. If it sends a cancellation request to a generic FAQ agent, the customer gets delay rather than resolution. Routing therefore needs measurable test cases, fallback paths... |
| EV_12 | Multi-agent support automation:safeguards | 1 | general | Separate scopes can reduce blast radius | This supports the plausible anchor: scoped permissions can provide a useful guardrail, but identity and delegation contr... | Separate scopes can reduce blast radius, but require more identity and delegation controls |

Rejected candidates:

- CAND_1 `Single-agent support automation:implementation_complexity` (grounding): excerpt not found in source text
- CAND_9 `Single-agent support automation:implementation_complexity` (acceptance): approach identity: excerpt describes several alternatives without isolating this one
- CAND_10 `Single-agent support automation:reliability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_11 `Single-agent support automation:safeguards` (verification): verdict=partial: It recommends prompt-level behavioral guardrails for an agent generally, but does not attribute them specifically to single-agent support automation or e
- CAND_12 `Multi-agent support automation:implementation_complexity` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_13 `Multi-agent support automation:reliability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_14 `Multi-agent support automation:safeguards` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_15 `Single-agent support automation:implementation_complexity` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_19 `Multi-agent support automation:implementation_complexity` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_20 `Multi-agent support automation:total_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q4 r1 static - `EVAL_Q4_r1_static_20261030T050704_6d6d2a`

- Status `partial`, stop `budget_exhausted`, interval leader `Session-only memory` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only); differentiating cells lack strong support (single source or non-official): Session-only memory:retrieval_effectiveness, Persistent conversation-log retrieval:retrieval_effectiveness
- Mechanical: 12 cited evidence IDs, **0 invalid**; 11 accepted / 8 rejected (lexical 0, approach-identity 0); single-source cells: Session-only memory:retrieval_effectiveness, Session-only memory:privacy_protection, Session-only memory:retention_and_deletion_control, Persistent conversation-log retrieval:retrieval_effectiveness, Persistent conversation-log retrieval:privacy_protection, Persistent conversation-log retrieval:retention_and_deletion_control, Summarized customer-profile memory:privacy_protection, Summarized customer-profile memory:retention_and_deletion_control, Hybrid layered memory:privacy_protection
- AI-provisional flags: one source supports 3+ targets: SRC_1 (4); SRC_4 (4)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Session-only memory:retrieval_effectiveness | 2 | general | Within one active conversation | Strong for the approach’s intended short-term scope: the excerpt says the agent should remember everything already suppl... | Within one active conversation, the agent should remember everything the customer has already told it, without exception. Asking a customer for their order number twice in the same conversation is the... |
| EV_2 | Session-only memory:privacy_protection | 1 | general | Short-term memory, the context of the current conversation | Plausible: the excerpt supports limited persistence, but it does not describe enforceable controls over information used... | Short-term memory, the context of the current conversation, is rarely the source of privacy problems, because it lives and dies with the conversation and rarely persists in a form a customer would thi... |
| EV_3 | Session-only memory:retention_and_deletion_control | 1 | general | The boundary of session memory is the session itself. | Plausible: the excerpt defines a session boundary, but does not describe dependable correction, deletion, or expiration ... | The boundary of session memory is the session itself. Once a conversation genuinely ends, whether by explicit close or by a customer going quiet for an extended period, the design question shifts from... |
| EV_4 | Persistent conversation-log retrieval:retrieval_effectiveness | 1 | general | save each interaction into it | Plausible: it describes cross-session search and retrieval for customer support, but does not establish that retrieved c... | An AI support agent remembers customers across conversations when every ticket, chat and call is saved under one stable customer ID, and the relevant history is loaded before the agent replies. With a... |
| EV_5 | Persistent conversation-log retrieval:privacy_protection | 1 | general | A scoped API key can be limited to one namespace | Plausible: the excerpt describes access controls, but does not establish data minimization or comprehensive limits on wh... | Two controls matter for enterprise support: - Per-customer keys. A scoped API key can be limited to one namespace, or a fixed list of them, and requests outside it get a 403 (API keys docs). Writable ... |
| EV_6 | Persistent conversation-log retrieval:privacy_protection | 1 | general | Enforce authorization before memory reads, writes, exports a... | Plausible: it recommends explicit access controls, but does not show complete data-minimization or retention safeguards. | Make access and deletion testable A stable customer identifier supports continuity. It doesn't prove the caller is entitled to use that identity. Enforce authorization before memory reads, writes, exp... |
| EV_7 | Persistent conversation-log retrieval:retention_and_deletion_control | 1 | general | Define retention separately for transcripts, summaries, extr... | Plausible: the excerpt identifies lifecycle controls needed for stored conversation records, while noting that search re... | Define retention separately for transcripts, summaries, extracted facts, logs and backups. A deletion workflow should cover the copies your system actually keeps. Removing a result from search doesn't... |
| EV_8 | Summarized customer-profile memory:privacy_protection | 1 | general | prefer a compact, structured summary over a raw transcript | Plausible: the excerpt supports data minimization through summaries, but does not describe enforceable controls over wha... | A useful rule of thumb is to prefer a compact, structured summary over a raw transcript when carrying memory across sessions. A summary that says the customer had a billing dispute in March, resolved ... |
| EV_9 | Hybrid layered memory:privacy_protection | 1 | general | A shared store can hold all three if the data model and auth... | Plausible: the excerpt describes role separation and authorization rules, but does not establish comprehensive controls ... | Keep three kinds of context separate / Context / Example / How to use it / / --- / --- / --- / / Current business state / Subscription, permissions, open incident status / Fetch from the system of rec... |
| EV_10 | Summarized customer-profile memory:retention_and_deletion_control | 1 | general | Different memory categories may have different retention per... | This supports the plausible anchor: retention controls are available and can vary by memory category. The excerpt does n... | Every stored memory should have a time-to-live (TTL) that determines when it expires. Retention limits serve two purposes: they enforce the data minimization principle by removing data that is no long... |
| EV_11 | Summarized customer-profile memory:retention_and_deletion_control | 1 | general | remove the content, the embeddings, the graph connections, a... | This demonstrates defined expiration and thorough deletion controls, but does not describe correcting stored summaries o... | Run an expiration job daily that identifies and deletes memories past their TTL. The expiration process must be the same as a customer deletion request: remove the content, the embeddings, the graph c... |

Rejected candidates:

- CAND_8 `Summarized customer-profile memory:retrieval_effectiveness` (grounding): excerpt not found in source text
- CAND_10 `Summarized customer-profile memory:retention_and_deletion_control` (verification): verdict=partial: It addresses correcting and temporally distinguishing profile values, but not retention periods or deletion processes.
- CAND_11 `Hybrid layered memory:retrieval_effectiveness` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_14 `Persistent conversation-log retrieval:retrieval_effectiveness` (grounding): excerpt not found in source text
- CAND_13 `Session-only memory:retrieval_effectiveness` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_15 `Persistent conversation-log retrieval:retention_and_deletion_control` (verification): verdict=partial: The cap and FIFO eviction constrain retention, but the excerpt does not establish correction, expiration schedules, or dependable deletion.
- CAND_16 `Summarized customer-profile memory:retrieval_effectiveness` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_17 `Persistent conversation-log retrieval:privacy_protection` (grounding): excerpt not found in source text

## Q4 r1 adaptive - `EVAL_Q4_r1_adaptive_20261030T051000_398ba3`

- Status `partial`, stop `budget_exhausted`, interval leader `Session-only memory` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only); differentiating cells lack strong support (single source or non-official): Session-only memory:retrieval_effectiveness, Persistent conversation-log retrieval:retrieval_effectiveness
- Mechanical: 10 cited evidence IDs, **0 invalid**; 10 accepted / 4 rejected (lexical 0, approach-identity 0); single-source cells: Session-only memory:retrieval_effectiveness, Session-only memory:privacy_protection, Session-only memory:retention_and_deletion_control, Persistent conversation-log retrieval:retrieval_effectiveness, Persistent conversation-log retrieval:privacy_protection, Persistent conversation-log retrieval:retention_and_deletion_control, Summarized customer-profile memory:privacy_protection, Hybrid layered memory:privacy_protection, Hybrid layered memory:retention_and_deletion_control
- AI-provisional flags: one source supports 3+ targets: SRC_1 (4); SRC_4 (4)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Session-only memory:retrieval_effectiveness | 2 | general | Within one active conversation | Strong for the approach’s intended short-term scope: the excerpt says the agent should remember everything already suppl... | Within one active conversation, the agent should remember everything the customer has already told it, without exception. Asking a customer for their order number twice in the same conversation is the... |
| EV_2 | Session-only memory:privacy_protection | 1 | general | Short-term memory, the context of the current conversation | Plausible: the excerpt supports limited persistence, but it does not describe enforceable controls over information used... | Short-term memory, the context of the current conversation, is rarely the source of privacy problems, because it lives and dies with the conversation and rarely persists in a form a customer would thi... |
| EV_3 | Session-only memory:retention_and_deletion_control | 1 | general | The boundary of session memory is the session itself. | Plausible: the excerpt defines a session boundary, but does not describe dependable correction, deletion, or expiration ... | The boundary of session memory is the session itself. Once a conversation genuinely ends, whether by explicit close or by a customer going quiet for an extended period, the design question shifts from... |
| EV_4 | Persistent conversation-log retrieval:retrieval_effectiveness | 1 | general | save each interaction into it | Plausible: it describes cross-session search and retrieval for customer support, but does not establish that retrieved c... | An AI support agent remembers customers across conversations when every ticket, chat and call is saved under one stable customer ID, and the relevant history is loaded before the agent replies. With a... |
| EV_5 | Persistent conversation-log retrieval:privacy_protection | 1 | general | A scoped API key can be limited to one namespace | Plausible: the excerpt describes access controls, but does not establish data minimization or comprehensive limits on wh... | Two controls matter for enterprise support: - Per-customer keys. A scoped API key can be limited to one namespace, or a fixed list of them, and requests outside it get a 403 (API keys docs). Writable ... |
| EV_6 | Persistent conversation-log retrieval:privacy_protection | 1 | general | Enforce authorization before memory reads, writes, exports a... | Plausible: it recommends explicit access controls, but does not show complete data-minimization or retention safeguards. | Make access and deletion testable A stable customer identifier supports continuity. It doesn't prove the caller is entitled to use that identity. Enforce authorization before memory reads, writes, exp... |
| EV_7 | Persistent conversation-log retrieval:retention_and_deletion_control | 1 | general | Define retention separately for transcripts, summaries, extr... | Plausible: the excerpt identifies lifecycle controls needed for stored conversation records, while noting that search re... | Define retention separately for transcripts, summaries, extracted facts, logs and backups. A deletion workflow should cover the copies your system actually keeps. Removing a result from search doesn't... |
| EV_8 | Summarized customer-profile memory:privacy_protection | 1 | general | prefer a compact, structured summary over a raw transcript | Plausible: the excerpt supports data minimization through summaries, but does not describe enforceable controls over wha... | A useful rule of thumb is to prefer a compact, structured summary over a raw transcript when carrying memory across sessions. A summary that says the customer had a billing dispute in March, resolved ... |
| EV_9 | Hybrid layered memory:privacy_protection | 1 | general | A shared store can hold all three if the data model and auth... | Plausible: the excerpt describes role separation and authorization rules, but does not establish comprehensive controls ... | Keep three kinds of context separate / Context / Example / How to use it / / --- / --- / --- / / Current business state / Subscription, permissions, open incident status / Fetch from the system of rec... |
| EV_10 | Hybrid layered memory:retention_and_deletion_control | 1 | general | transient/working/durable controller | Plausible: the excerpt describes layered stores and inspectable lifecycle actions, indicating retention controls. It doe... | We instantiate this formulation in StageMem, a compact transient/working/durable controller that makes promotion, compression, and eviction decisions inspectable under bounded capacity. |

Rejected candidates:

- CAND_8 `Summarized customer-profile memory:retrieval_effectiveness` (grounding): excerpt not found in source text
- CAND_10 `Summarized customer-profile memory:retention_and_deletion_control` (verification): verdict=partial: It addresses correcting and temporally distinguishing profile values, but not retention periods or deletion processes.
- CAND_11 `Hybrid layered memory:retrieval_effectiveness` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_14 `Hybrid layered memory:retention_and_deletion_control` (verification): verdict=irrelevant: The excerpt discusses a hybrid of forgetting policies, not the hybrid layered memory approach described by the alternative.

## Q5 r1 static - `EVAL_Q5_r1_static_20261030T051103_6579a2`

- Status `partial`, stop `budget_exhausted`, interval leader `Managed vector database` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only)
- Mechanical: 9 cited evidence IDs, **0 invalid**; 21 accepted / 2 rejected (lexical 0, approach-identity 0); single-source cells: none
- AI-provisional flags: one source supports 3+ targets: SRC_2 (5); SRC_6 (5); SRC_8 (4); SRC_9 (3); SRC_10 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Managed vector database:operational_effort | 2 | general | Managed services usually handle infrastructure provisioning | Strong anchor: the excerpt describes the provider taking on routine operations and scaling work, which supports little o... | The biggest advantage is operational simplicity. Managed services usually handle infrastructure provisioning, routine maintenance, patching, availability architecture, scaling workflows, and parts of ... |
| EV_2 | Managed vector database:startup_cost | 1 | general | The Cost Tradeoff in Managed Services | Plausible anchor: the excerpt indicates that service costs may be justified by avoided staffing and engineering overhead... | That can be a good trade when the alternative is hiring or distracting engineers to manage the system. It becomes less attractive when a team has enough scale and expertise to operate the database eff... |
| EV_3 | Managed vector database:control_and_customization | 1 | general | managed services can limit certain choices | Plausible anchor: the excerpt supports adequate control for many common applications, while identifying provider-imposed... | The tradeoff is that managed services can limit certain choices. A team may have fewer options for low-level index tuning, infrastructure placement, deployment topology, private networking patterns, o... |
| EV_4 | Self-hosted vector database:operational_effort | 0 | general | Self-hosted vector databases | Poor anchor: the excerpt lists substantial ongoing infrastructure responsibilities that would be difficult to sustain wi... | Self-hosted vector databases give teams the most control over infrastructure, data placement, configuration, and long-term cost, but they also make the team responsible for deployment, scaling, monito... |
| EV_5 | Self-hosted vector database:control_and_customization | 2 | general | Self-hosting is attractive because it gives teams direct con... | Strong anchor: the excerpt explicitly describes direct control across a wide range of deployment and configuration choic... | Self-hosting is attractive because it gives teams direct control over the database environment. They can choose instance types, storage classes, regions, network topology, backup tooling, deployment c... |
| EV_6 | Managed vector database:operational_effort | 2 | general | Zilliz Cloud eliminates these concerns | Strong: automatic backups, patches, and scaling plus deployment in minutes support low operational effort for a small te... | Zilliz Cloud eliminates these concerns: deployment takes minutes through a web console, backups are automatic, patches are applied transparently, and scaling happens automatically. |
| EV_7 | Managed vector database:startup_cost | 2 | general | Zilliz Cloud is cheaper—you pay only for what you use | Strong: the excerpt describes an affordable, usage-based path specifically for low-volume pilots, aligning with modest e... | For low-query-volume agents (experimental systems, pilot projects), Zilliz Cloud is cheaper—you pay only for what you use. |
| EV_8 | Managed vector database:control_and_customization | 0 | general | Zilliz Cloud offers limited customization—you use the servic... | Poor: the excerpt directly indicates limited customization and little ability to alter the service. | Zilliz Cloud offers limited customization—you use the service as-is. |
| EV_9 | Self-hosted vector database:operational_effort | 0 | general | Self-hosted Milvus requires managing infrastructure | Poor: the excerpt explicitly characterizes the burden as substantial for small teams and requires DevOps expertise and o... | Self-hosted Milvus requires managing infrastructure: provisioning servers or Kubernetes clusters, configuring networking, setting up persistent storage, managing backups, monitoring performance, and a... |
| EV_10 | Self-hosted vector database:control_and_customization | 2 | general | Self-hosted Milvus offers maximum customization | Strong: the excerpt explicitly describes maximum customization across source code, configuration, and integration. | Self-hosted Milvus offers maximum customization: teams can modify source code, tune parameters for specific workloads, or integrate Milvus deeply with internal systems. |
| EV_11 | Managed vector database:operational_effort | 2 | general | Pinecone handles all operations, scaling, and maintenance. | Strong anchor: the excerpt explicitly says the provider handles operations, scaling, and maintenance, indicating little ... | Pinecone handles all operations, scaling, and maintenance. |
| EV_12 | Managed vector database:startup_cost | 1 | general | Pinecone's free tier covers 100K vectors. | Plausible anchor: a free entry tier offers an affordable start, but charges can become meaningful as usage grows. | Pinecone Starter: $0 to $70 per month. Pinecone's free tier covers 100K vectors. Beyond that, the Starter plan starts at roughly $70 per month for standard pod storage. |
| EV_13 | Self-hosted vector database:operational_effort | 1 | general | Self-hosted Qdrant requires initial setup | Plausible anchor: the excerpt describes recurring engineering attention, including 1 to 2 hours of monitoring per month,... | Engineering time varies dramatically by approach. Self-hosted Qdrant requires initial setup (1 to 2 hours), ongoing monitoring (1 to 2 hours per month), and occasional troubleshooting. |
| EV_14 | Self-hosted vector database:startup_cost | 1 | general | Self-hosted Qdrant: $20 to $50 per month. | Plausible anchor: the infrastructure price appears manageable at modest scale, but the excerpt does not quantify the mat... | Self-hosted Qdrant: $20 to $50 per month. A 4 GB RAM VPS from Hetzner, DigitalOcean, or Linode runs Qdrant comfortably for 200K to 500K vectors. An 8 GB instance handles up to 1 million vectors. |
| EV_15 | Self-hosted vector database:startup_cost | 1 | general | Self-hosting on a Hetzner CX33 is $9.99/month | Plausible anchor: the stated infrastructure charge is low, but the excerpt conditions it on the startup operating the da... | Self-hosting on a Hetzner CX33 is $9.99/month if you will operate Qdrant, Milvus, or pgvector. |
| EV_16 | Managed vector database:operational_effort | 2 | general | Managed vendors handle index lifecycle, replica placement, a... | Strong: the excerpt says the provider handles routine lifecycle and upgrade work, reducing direct engineering effort and... | Managed vendors handle index lifecycle, replica placement, and rolling upgrades, shifting the risk from engineering time to vendor bill. |
| EV_17 | Self-hosted vector database:operational_effort | 0 | general | If you choose to build, plan for three engineering phases | Poor: the excerpt describes substantial build, scaling, and resilience work and budgets for two SREs plus an ML infrastr... | If you choose to build, plan for three engineering phases: prototype (FAISS/pgvector, single-node), scale (distributed HNSW with autoscaling), and resilience (multi-AZ replication, snapshot catalog). ... |
| EV_18 | Managed vector database:startup_cost | 2 | general | Weaviate Flex: 1,536M dimensions × $0.00465 = $7.14 plus und... | Strong: the excerpt gives a clear, low minimum charge at modest pilot usage, supporting an affordable early-stage entry ... | Weaviate Flex: 1,536M dimensions × $0.00465 = $7.14 plus under $1 of storage, so the $45 minimum applies. |
| EV_19 | Self-hosted vector database:startup_cost | 0 | general | Self-hosting costs $26.8K with offshore operators | Poor: even the lowest modeled pilot cost is substantial for an early-stage workload, and the higher staffing-location es... | Self-hosting costs $26.8K with offshore operators, $36.9K nearshore and $52.0K with a US in-house team. |
| EV_20 | Managed vector database:control_and_customization | 1 | general | Weaviate Flex is a shared cluster with a 99.5% SLA. | Plausible: the excerpt shows some provider-tier constraints, but also identifies options for private networking and high... | Weaviate Flex is a shared cluster with a 99.5% SLA. A team that needs SSO, private networking or a higher SLA moves to Premium at $400/month or more. |
| EV_21 | Self-hosted vector database:control_and_customization | 2 | general | if you need custom similarity metrics | Strong: the excerpt explicitly describes customizing similarity behavior and choosing unique hardware in a build approac... | if you need custom similarity metrics, sub-10ms 99th-percentile latency at 1B vectors, or unique hardware (NVMe+GPU indexing), build and budget $1.2M+ over three years. |

Rejected candidates:

- CAND_5 `Self-hosted vector database:startup_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_11 `Self-hosted vector database:startup_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q5 r1 adaptive - `EVAL_Q5_r1_adaptive_20261030T051350_6f5523`

- Status `complete`, stop `stable`, interval leader `Managed vector database` (robust), recommendation `ready`
- Mechanical: 7 cited evidence IDs, **0 invalid**; 10 accepted / 2 rejected (lexical 0, approach-identity 1); single-source cells: Self-hosted vector database:startup_cost, Self-hosted vector database:control_and_customization
- AI-provisional flags: one source supports 3+ targets: SRC_2 (5); SRC_5 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Managed vector database:operational_effort | 2 | general | Managed services usually handle infrastructure provisioning | Strong anchor: the excerpt describes the provider taking on routine operations and scaling work, which supports little o... | The biggest advantage is operational simplicity. Managed services usually handle infrastructure provisioning, routine maintenance, patching, availability architecture, scaling workflows, and parts of ... |
| EV_2 | Managed vector database:startup_cost | 1 | general | The Cost Tradeoff in Managed Services | Plausible anchor: the excerpt indicates that service costs may be justified by avoided staffing and engineering overhead... | That can be a good trade when the alternative is hiring or distracting engineers to manage the system. It becomes less attractive when a team has enough scale and expertise to operate the database eff... |
| EV_3 | Managed vector database:control_and_customization | 1 | general | managed services can limit certain choices | Plausible anchor: the excerpt supports adequate control for many common applications, while identifying provider-imposed... | The tradeoff is that managed services can limit certain choices. A team may have fewer options for low-level index tuning, infrastructure placement, deployment topology, private networking patterns, o... |
| EV_4 | Self-hosted vector database:operational_effort | 0 | general | Self-hosted vector databases | Poor anchor: the excerpt lists substantial ongoing infrastructure responsibilities that would be difficult to sustain wi... | Self-hosted vector databases give teams the most control over infrastructure, data placement, configuration, and long-term cost, but they also make the team responsible for deployment, scaling, monito... |
| EV_5 | Self-hosted vector database:control_and_customization | 2 | general | Self-hosting is attractive because it gives teams direct con... | Strong anchor: the excerpt explicitly describes direct control across a wide range of deployment and configuration choic... | Self-hosting is attractive because it gives teams direct control over the database environment. They can choose instance types, storage classes, regions, network topology, backup tooling, deployment c... |
| EV_6 | Managed vector database:operational_effort | 2 | general | Pinecone — fully managed, no infrastructure to run | Strong anchor: the excerpt explicitly describes the managed option as zero-ops with no infrastructure to run, supporting... | Want zero ops / serverless? Pinecone — fully managed, no infrastructure to run. |
| EV_7 | Managed vector database:startup_cost | 1 | general | we ended up at ~$280/mo just for vectors | Plausible anchor: the excerpt gives a concrete monthly charge and notes additional redundancy and filtering costs, indic... | The s1.x1 pod sufficient for our index ran ~$70/mo per pod, and we needed 2 for redundancy. Add metadata filtering and we ended up at ~$280/mo just for vectors. |
| EV_8 | Managed vector database:control_and_customization | 0 | general | Data leaves your VPC (unless BYOC) | Poor anchor: the excerpt identifies a significant data-handling constraint for managed deployment, supporting limited co... | Data sovereignty / Data leaves your VPC (unless BYOC) / Full control |
| EV_9 | Self-hosted vector database:operational_effort | 0 | general | Cluster sizing was non-trivial | Poor anchor: the excerpt describes hands-on cluster sizing and repeated mistakes, evidence of substantial operational at... | Cluster sizing was non-trivial. The official guide assumes you understand HNSW parameters; we got it wrong twice. |
| EV_10 | Self-hosted vector database:startup_cost | 1 | general | ~$120/mo for a 2-node cluster with reasonable headroom | Plausible anchor: the excerpt gives a concrete infrastructure charge that may be manageable at modest scale, but does no... | Cost was middle-of-the-road: ~$120/mo for a 2-node cluster with reasonable headroom. |

Rejected candidates:

- CAND_5 `Self-hosted vector database:startup_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_12 `Self-hosted vector database:control_and_customization` (acceptance): approach identity: identification quote missing or not found verbatim in the source

## Q8 r1 static - `EVAL_Q8_r1_static_20261030T051457_95878b`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (None), recommendation `not_applicable`
- Mechanical: 12 cited evidence IDs, **0 invalid**; 19 accepted / 6 rejected (lexical 3, approach-identity 0); single-source cells: none
- AI-provisional flags: one source supports 3+ targets: SRC_2 (3); SRC_3 (3); SRC_5 (3); SRC_8 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | open_source_license | - | general | # confident-ai/deepeval |  | License: Apache License 2.0 |
| EV_2 | llm_evaluation_or_observability | - | general | Welcome to `prompttools` |  | This repo offers a set of open-source, self-hostable tools for experimenting with, testing, and evaluating LLMs, vector databases, and prompts. |
| EV_3 | self_hosting_support | - | general | Welcome to `prompttools` |  | This repo offers a set of open-source, self-hostable tools for experimenting with, testing, and evaluating LLMs, vector databases, and prompts. |
| EV_4 | open_source_license | - | general | # hegelai/prompttools |  | License: Apache License 2.0 |
| EV_5 | llm_evaluation_or_observability | - | general | Opik is the open-source LLM observability and evaluation pla... |  | Opik is the open-source LLM observability and evaluation platform for AI agent tracing, LLM evaluation, prompt management, and production monitoring. |
| EV_6 | open_source_license | - | general | Opik is Apache-2.0 licensed |  | Opik is Apache-2.0 licensed and free to self-host: the full platform, backend included, not just a client SDK. |
| EV_7 | self_hosting_support | - | general | the full platform, backend included |  | Opik is Apache-2.0 licensed and free to self-host: the full platform, backend included, not just a client SDK. |
| EV_8 | llm_evaluation_or_observability | - | general | OpenLLMetry is a set of extensions built on top of OpenTelem... |  | OpenLLMetry is a set of extensions built on top of OpenTelemetry that gives you complete observability over your LLM application. |
| EV_9 | open_source_license | - | general | OpenLLMetry is a set of extensions |  | It's built and maintained by Traceloop under the Apache 2.0 license. |
| EV_10 | llm_evaluation_or_observability | - | general | Langfuse is an **open source LLM engineering** platform |  | Langfuse is an **open source LLM engineering** platform. It helps teams collaboratively **develop, monitor, evaluate,** and **debug** AI applications. |
| EV_11 | open_source_license | - | general | This repository is MIT licensed |  | This repository is MIT licensed, except for the `ee` folders. See LICENSE and docs for more details. |
| EV_12 | self_hosting_support | - | general | Run Langfuse on your own infrastructure |  | Run Langfuse on your own infrastructure: - Local (docker compose): Run Langfuse on your own machine in 5 minutes using Docker Compose. |
| EV_13 | open_source_license | - | general | # evidentlyai/evidently |  | - License: Apache License 2.0 |
| EV_14 | self_hosting_support | - | general | Self-host the open-source version. |  | * Self-host the open-source version. |
| EV_15 | llm_evaluation_or_observability | - | general | Self-hosted LLM observability and evals. |  | **Self-hosted LLM observability and evals.** |
| EV_16 | open_source_license | - | general | License: MIT License |  | License: MIT License |
| EV_17 | self_hosting_support | - | general | docker compose up |  | **Zero-config deployment.** `docker compose up` gives you the API and UI on one port, with SQLite on a named volume. |
| EV_18 | open_source_license | - | general | License: Apache 2.0 |  | License: Apache 2.0 |
| EV_19 | self_hosting_support | - | general | Self-host with Docker Compose or Kubernetes Helm. |  | How do I deploy OpenLIT? Self-host with Docker Compose or Kubernetes Helm. |

Rejected candidates:

- CAND_1 `llm_evaluation_or_observability` (grounding): excerpt not found in source text
- CAND_14 `llm_evaluation_or_observability` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_15 `open_source_license` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_16 `self_hosting_support` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_17 `llm_evaluation_or_observability` (grounding): excerpt not found in source text
- CAND_23 `llm_evaluation_or_observability` (grounding): excerpt not found in source text

## Q8 r1 adaptive - `EVAL_Q8_r1_adaptive_20261030T051637_274f7f`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (None), recommendation `not_applicable`
- Mechanical: 11 cited evidence IDs, **0 invalid**; 15 accepted / 2 rejected (lexical 0, approach-identity 0); single-source cells: none
- AI-provisional flags: one source supports 3+ targets: SRC_2 (3); SRC_3 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | open_source_license | - | general | # confident-ai/deepeval |  | License: Apache License 2.0 |
| EV_2 | llm_evaluation_or_observability | - | general | Welcome to `prompttools` |  | This repo offers a set of open-source, self-hostable tools for experimenting with, testing, and evaluating LLMs, vector databases, and prompts. |
| EV_3 | self_hosting_support | - | general | Welcome to `prompttools` |  | This repo offers a set of open-source, self-hostable tools for experimenting with, testing, and evaluating LLMs, vector databases, and prompts. |
| EV_4 | open_source_license | - | general | # hegelai/prompttools |  | License: Apache License 2.0 |
| EV_5 | llm_evaluation_or_observability | - | general | Opik is the open-source LLM observability and evaluation pla... |  | Opik is the open-source LLM observability and evaluation platform for AI agent tracing, LLM evaluation, prompt management, and production monitoring. |
| EV_6 | open_source_license | - | general | Opik is Apache-2.0 licensed |  | Opik is Apache-2.0 licensed and free to self-host: the full platform, backend included, not just a client SDK. |
| EV_7 | self_hosting_support | - | general | the full platform, backend included |  | Opik is Apache-2.0 licensed and free to self-host: the full platform, backend included, not just a client SDK. |
| EV_8 | llm_evaluation_or_observability | - | general | OpenLLMetry is a set of extensions built on top of OpenTelem... |  | OpenLLMetry is a set of extensions built on top of OpenTelemetry that gives you complete observability over your LLM application. |
| EV_9 | open_source_license | - | general | OpenLLMetry is a set of extensions |  | It's built and maintained by Traceloop under the Apache 2.0 license. |
| EV_10 | llm_evaluation_or_observability | - | general | DeepEval is an open-source LLM evaluation framework |  | DeepEval is an open-source LLM evaluation framework for LLM applications. |
| EV_11 | self_hosting_support | - | general | DeepEval is local-first: your evaluations run in your own en... |  | DeepEval is local-first: your evaluations run in your own environment. |
| EV_12 | llm_evaluation_or_observability | - | general | Open-source observability for your LLM application |  | Open-source observability for your LLM application |
| EV_13 | open_source_license | - | general | OpenLLMetry is a set of extensions built on top of OpenTelem... |  | It's built and maintained by Traceloop under the Apache 2.0 license. |
| EV_14 | llm_evaluation_or_observability | - | general | OpenLLMetry is a set of extensions built on top of OpenTelem... |  | OpenLLMetry is a set of extensions built on top of OpenTelemetry that gives you complete observability over your LLM application. |
| EV_15 | open_source_license | - | general | under the Apache 2.0 license |  | It's built and maintained by Traceloop under the Apache 2.0 license. |

Rejected candidates:

- CAND_1 `llm_evaluation_or_observability` (grounding): excerpt not found in source text
- CAND_17 `self_hosting_support` (verification): verdict=partial: It mentions running the SDK locally, but does not establish self-hosting or deploying the tool on one's own infrastructure.

## Q1 r2 static - `EVAL_Q1_r2_static_20261030T051745_dc2ace`

- Status `partial`, stop `budget_exhausted`, interval leader `Weaviate` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only); differentiating cells lack strong support (single source or non-official): Milvus:filtering_capability
- Mechanical: 12 cited evidence IDs, **0 invalid**; 17 accepted / 7 rejected (lexical 1, approach-identity 0); single-source cells: Qdrant:filtering_capability, Qdrant:operational_effort, Weaviate:deployment_fit, Milvus:filtering_capability, Milvus:operational_effort
- AI-provisional flags: one source supports 3+ targets: SRC_3 (4)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Qdrant:deployment_fit | 2 | self_hosted | Qdrant’s quickstart | The one-command quickstart with a mounted volume is a clear, practical self-hosted setup path, matching the strong ancho... | Qdrant’s quickstart is one `docker run` with a mounted `qdrant_storage` volume. |
| EV_2 | Qdrant:deployment_fit | 1 | managed | Qdrant Cloud: 1 node, 0.5 vCPU, 1 GB RAM | The free managed tier provides a workable hosting choice, but its small resource limits and idle suspension are notable ... | Managed free tier / Qdrant Cloud: 1 node, 0.5 vCPU, 1 GB RAM, 4 GB disk, about 1M 768-dimension vectors, no card; suspended after 1 week idle, deleted after 4 (Cloud docs) |
| EV_3 | Qdrant:filtering_capability | 2 | general | Qdrant's ACORN approach | The excerpt describes filter-aware traversal and strong performance under highly selective filtering, directly supportin... | Qdrant's ACORN approach folds metadata filtering directly into the HNSW graph traversal instead of filtering after the search. That keeps queries fast even when a filter eliminates 99% of candidates, ... |
| EV_4 | Weaviate:deployment_fit | 2 | managed | Weaviate Cloud - From evaluation (free tier) to production | The managed cloud option spans evaluation through production and identifies provider-managed infrastructure, giving a sm... | Weaviate Cloud - From evaluation (free tier) to production - Shared Cloud (infrastructure managed by Weaviate) - (Optional) Data replication (high-availability) - (Optional) Zero-downtime updates |
| EV_5 | Weaviate:deployment_fit | 2 | self_hosted | experimenting on a small scale with Docker | The excerpt gives a concrete path to begin at small scale and move to Kubernetes as needs or familiarity grow, matching ... | If you are self-hosting, consider experimenting on a small scale with Docker and then transferring your configuration to Kubernetes Helm charts when you are more familiar with Weaviate. |
| EV_6 | Weaviate:filtering_capability | 2 | general | Weaviate pre-filters through its inverted index | The excerpt describes several integrated mechanisms for filtered retrieval, including a defined strategy for smaller res... | Weaviate pre-filters through its inverted index into an allow-list, walks HNSW with ACORN (default `filterStrategy` since v1.34), and uses brute force below `flatSearchCutoff` (default 40,000). |
| EV_7 | Milvus:filtering_capability | 1 | general | Milvus restricts the search scope to matching entities | The excerpt shows support for common filtering and complex expressions, but gives limited detail about flexibility or us... | Milvus restricts the search scope to matching entities before search, with iterative mode for complex expressions. |
| EV_8 | Milvus:deployment_fit | 1 | self_hosted | Milvus Standalone’s Docker requirements | The requirements show a workable self-hosted option, but its hardware, CPU-feature, and etcd storage prerequisites are n... | Milvus Standalone’s Docker requirements ask for at least 4 cores and 8 GB of RAM (16 GB recommended), a CPU with SSE4.2, AVX, AVX2 or AVX-512, and etcd on a disk with more than 500 IOPS and p99 fsync ... |
| EV_9 | Qdrant:deployment_fit | 1 | self_hosted | Qdrant Private Cloud | This establishes a flexible self-hosted deployment path, but does not describe setup ease or reduced operational commitm... | Qdrant Private Cloud allows you to manage Qdrant database clusters in any Kubernetes cluster on any infrastructure. |
| EV_10 | Qdrant:deployment_fit | 2 | managed | Qdrant fully manages your infrastructure | This directly supports a practical managed deployment path with minimal infrastructure setup for a small team, meeting t... | No Infrastructure Management / Qdrant fully manages your infrastructure, so you can focus on building your application. |
| EV_11 | Qdrant:operational_effort | 2 | managed | Qdrant fully manages your infrastructure | The excerpt explicitly says the managed service fully manages infrastructure, indicating low routine operational work fo... | No Infrastructure Management / Qdrant fully manages your infrastructure, so you can focus on building your application. |
| EV_12 | Qdrant:operational_effort | 1 | self_hosted | In self-hosted deployments | This identifies ongoing manual scaling work, indicating notable operational maintenance, though it does not establish th... | In self-hosted deployments, you must manually create or drop replicas and move shards between nodes as you scale. |
| EV_13 | Weaviate:filtering_capability | 2 | general | Weaviate provides powerful filtered vector search capabiliti... | Strong anchor: this directly describes filtered vector search combining vector similarity with structured conditions, a ... | Weaviate provides powerful filtered vector search capabilities, allowing you to combine vector searches with structured, scalar filters. This enables you to find the closest vectors to a query vector ... |
| EV_14 | Weaviate:filtering_capability | 2 | general | To filter with two or more conditions, use `And`, `Or` and `... | Strong anchor: explicit support for AND, OR, and NOT provides flexible composition of common metadata filters. | To filter with two or more conditions, use `And`, `Or` and `Not` to define the relationship between the conditions. |
| EV_15 | Milvus:deployment_fit | 2 | self_hosted | Milvus Lite itself or a combination of Milvus Lite and Milvu... | Strong anchor: the excerpt gives a practical, explicitly RAG-oriented path for prototyping with Milvus Lite and Standalo... | For Quick Prototyping If you would like to quickly build something as a prototype or for learning purposes, such as Retrieval Augmented Generation (RAG) demos, AI chatbots, multi-modality search, Milv... |
| EV_16 | Milvus:operational_effort | 1 | self_hosted | requiring much less DevOps than maintaining a K8s cluster | Plausible anchor: the excerpt indicates reduced operational work relative to Kubernetes, but does not establish that all... | For early-stage production, when the project is still seeking product-market fit and agility is more important than scalability, Milvus Standalone is the best choice. It can still scale up to 100M vec... |
| EV_17 | Milvus:operational_effort | 2 | managed | Zilliz Cloud is hassle-free, powered by Milvus | Strong anchor, with limited detail: the excerpt directly characterizes the managed Milvus-powered service as hassle-free... | Zilliz Cloud is hassle-free, powered by Milvus and 10x faster. |

Rejected candidates:

- CAND_4 `Qdrant:operational_effort` (acceptance): verifier attributes the excerpt to 'multiple', not Qdrant
- CAND_8 `Weaviate:operational_effort` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_9 `Weaviate:operational_effort` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_10 `Weaviate:operational_effort` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_15 `Qdrant:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_21 `Milvus:deployment_fit` (verification): verdict=partial: Standalone is recommended for early-stage production and needs much less DevOps than Kubernetes, but avoiding a Kubernetes cluster is not stated outright
- CAND_24 `Milvus:filtering_capability` (acceptance): lexical check: entity name/alias not found in excerpt context

## Q1 r2 adaptive - `EVAL_Q1_r2_adaptive_20261030T052052_62dd99`

- Status `partial`, stop `budget_exhausted`, interval leader `Qdrant` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only); differentiating cells lack strong support (single source or non-official): Qdrant:filtering_capability, Milvus:filtering_capability
- Mechanical: 17 cited evidence IDs, **0 invalid**; 19 accepted / 14 rejected (lexical 0, approach-identity 0); single-source cells: Qdrant:filtering_capability, Weaviate:deployment_fit, Milvus:filtering_capability, Milvus:operational_effort
- AI-provisional flags: one source supports 3+ targets: SRC_3 (4); SRC_6 (4); SRC_7 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Qdrant:deployment_fit | 2 | self_hosted | Qdrant’s quickstart | The one-command quickstart with a mounted volume is a clear, practical self-hosted setup path, matching the strong ancho... | Qdrant’s quickstart is one `docker run` with a mounted `qdrant_storage` volume. |
| EV_2 | Qdrant:deployment_fit | 1 | managed | Qdrant Cloud: 1 node, 0.5 vCPU, 1 GB RAM | The free managed tier provides a workable hosting choice, but its small resource limits and idle suspension are notable ... | Managed free tier / Qdrant Cloud: 1 node, 0.5 vCPU, 1 GB RAM, 4 GB disk, about 1M 768-dimension vectors, no card; suspended after 1 week idle, deleted after 4 (Cloud docs) |
| EV_3 | Qdrant:filtering_capability | 2 | general | Qdrant's ACORN approach | The excerpt describes filter-aware traversal and strong performance under highly selective filtering, directly supportin... | Qdrant's ACORN approach folds metadata filtering directly into the HNSW graph traversal instead of filtering after the search. That keeps queries fast even when a filter eliminates 99% of candidates, ... |
| EV_4 | Weaviate:deployment_fit | 2 | managed | Weaviate Cloud - From evaluation (free tier) to production | The managed cloud option spans evaluation through production and identifies provider-managed infrastructure, giving a sm... | Weaviate Cloud - From evaluation (free tier) to production - Shared Cloud (infrastructure managed by Weaviate) - (Optional) Data replication (high-availability) - (Optional) Zero-downtime updates |
| EV_5 | Weaviate:deployment_fit | 2 | self_hosted | experimenting on a small scale with Docker | The excerpt gives a concrete path to begin at small scale and move to Kubernetes as needs or familiarity grow, matching ... | If you are self-hosting, consider experimenting on a small scale with Docker and then transferring your configuration to Kubernetes Helm charts when you are more familiar with Weaviate. |
| EV_6 | Weaviate:filtering_capability | 2 | general | Weaviate pre-filters through its inverted index | The excerpt describes several integrated mechanisms for filtered retrieval, including a defined strategy for smaller res... | Weaviate pre-filters through its inverted index into an allow-list, walks HNSW with ACORN (default `filterStrategy` since v1.34), and uses brute force below `flatSearchCutoff` (default 40,000). |
| EV_7 | Milvus:filtering_capability | 1 | general | Milvus restricts the search scope to matching entities | The excerpt shows support for common filtering and complex expressions, but gives limited detail about flexibility or us... | Milvus restricts the search scope to matching entities before search, with iterative mode for complex expressions. |
| EV_8 | Milvus:deployment_fit | 1 | self_hosted | Milvus Standalone’s Docker requirements | The requirements show a workable self-hosted option, but its hardware, CPU-feature, and etcd storage prerequisites are n... | Milvus Standalone’s Docker requirements ask for at least 4 cores and 8 GB of RAM (16 GB recommended), a CPU with SSE4.2, AVX, AVX2 or AVX-512, and etcd on a disk with more than 500 IOPS and p99 fsync ... |
| EV_9 | Qdrant:deployment_fit | 1 | self_hosted | ### Qdrant: Fast, Lean, Needs a Driver | Plausible: Docker and Kubernetes Helm provide workable deployment paths, but the team must handle backups, monitoring, s... | Docker deployment is straightforward, Kubernetes helm charts work, but you're responsible for backups, monitoring, scaling, and recovering from failures. |
| EV_10 | Qdrant:operational_effort | 1 | self_hosted | ### Qdrant: Fast, Lean, Needs a Driver | Plausible: the excerpt identifies notable ongoing maintenance responsibilities and a less battle-tested distributed mode... | The trade-off: you're running it yourself. Docker deployment is straightforward, Kubernetes helm charts work, but you're responsible for backups, monitoring, scaling, and recovering from failures. The... |
| EV_11 | Qdrant:operational_effort | 1 | self_hosted | Qdrant self-hosted costs | Plausible: the excerpt quantifies notable ongoing maintenance and monitoring effort, without saying it is impossible for... | Note: self-hosted costs include compute only. Add 10-20 hours/month of engineering time for maintenance, monitoring, and the occasional 2 AM alert. |
| EV_12 | Weaviate:filtering_capability | 1 | general | the query latency with filtering shows more variance than I'... | Plausible: the excerpt indicates filtered queries work but reports a meaningful performance concern; it does not charact... | The trade-off: it's hungry for resources and the performance isn't quite in Qdrant's league. That 6.8 GB/million vectors adds up fast, and the query latency with filtering shows more variance than I'd... |
| EV_13 | Weaviate:operational_effort | 1 | self_hosted | That Weaviate memory number | Plausible: the excerpt documents significant troubleshooting in a self-hosted Kubernetes deployment, but also says the i... | That Weaviate memory number — 6.8 GB per million vectors — is what almost killed us. We had 8 million vectors and Weaviate was eating 54 GB of RAM. Our Kubernetes pods kept getting OOM-killed. We ende... |
| EV_14 | Weaviate:operational_effort | 1 | self_hosted | Weaviate is the most feature-dense of the open-source option... | Plausible: the excerpt identifies an operational complexity around scaling coupled workloads, but does not show that rou... | The same process that does ANN search also runs the embedding pipeline. In a production system I want those decoupled — embedding is a CPU/GPU-bound batch operation that should run on its own infrastr... |
| EV_15 | Milvus:deployment_fit | 0 | self_hosted | ## Milvus: too much complexity for my scale | Poor: the excerpt describes a substantial multi-service production deployment and explicitly calls it overkill at the st... | The minimum production deployment has, depending on how you count, six or seven separate services plus etcd plus MinIO or S3. For 40M vectors, this is overkill in the worst way: you pay the operationa... |
| EV_16 | Milvus:operational_effort | 0 | self_hosted | Milvus is the option for billion-vector workloads. | Poor: the excerpt describes multiple components that must all be operated, a substantial operational burden for a small ... | Milvus is the option for billion-vector workloads. The architecture is impressive — separate components for query nodes, data nodes, index nodes, root coordinator, an external object store for cold da... |
| EV_17 | Qdrant:deployment_fit | 1 | self_hosted | Deploy Qdrant on any infrastructure | Plausible anchor: there is a workable self-hosted deployment path with requirements and configuration guidance, though t... | Deploy Qdrant on any infrastructure. Get requirements, configuration options, and GPU setup guides. |
| EV_18 | Qdrant:operational_effort | 2 | managed | Qdrant fully manages your infrastructure | Strong anchor: the excerpt explicitly says Qdrant fully manages the infrastructure, reducing routine operational work fo... | No Infrastructure Management / Qdrant fully manages your infrastructure, so you can focus on building your application. |
| EV_19 | Qdrant:operational_effort | 1 | self_hosted | In self-hosted deployments, you must manually create or drop... | Plausible anchor: the excerpt identifies ongoing manual scaling tasks, indicating notable maintenance, but does not show... | In self-hosted deployments, you must manually create or drop replicas and move shards between nodes as you scale. |

Rejected candidates:

- CAND_4 `Qdrant:operational_effort` (acceptance): verifier attributes the excerpt to 'multiple', not Qdrant
- CAND_8 `Weaviate:operational_effort` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_9 `Weaviate:operational_effort` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_10 `Weaviate:operational_effort` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_13 `Qdrant:deployment_fit` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_14 `Qdrant:deployment_fit` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_15 `Qdrant:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_16 `Qdrant:operational_effort` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_18 `Qdrant:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_21 `Qdrant:operational_effort` (verification): verdict=irrelevant: The excerpt describes cluster features but does not identify the database as Qdrant.
- CAND_22 `Weaviate:deployment_fit` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_27 `Milvus:filtering_capability` (acceptance): verifier attributes the excerpt to 'multiple', not Milvus
- CAND_29 `Qdrant:deployment_fit` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_33 `Qdrant:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q2 r2 static - `EVAL_Q2_r2_static_20261030T052347_8454d4`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (None), recommendation `not_applicable`
- Mechanical: 24 cited evidence IDs, **0 invalid**; 31 accepted / 7 rejected (lexical 4, approach-identity 0); single-source cells: none
- AI-provisional flags: one source supports 3+ targets: SRC_1 (3); SRC_2 (4); SRC_5 (5); SRC_6 (5); SRC_7 (4); SRC_8 (4)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | india_based | - | general | FabHR HQ, 4th Floor, Indiranagar, Bengaluru, Karnataka 56003... |  | FabHR HQ, 4th Floor, Indiranagar, Bengaluru, Karnataka 560038, India |
| EV_2 | headquarters_evidence | - | general | Headquarters FabHR HQ, 4th Floor, Indiranagar, Bengaluru, Ka... |  | FabHR HQ, 4th Floor, Indiranagar, Bengaluru, Karnataka 560038, India |
| EV_3 | hr_technology | - | general | The AI-first HR operating system for modern teams. Hire fast... |  | The AI-first HR operating system for modern teams. Hire faster, pay smarter, build teams that thrive. |
| EV_4 | market_positioning_evidence | - | general | 450+ growing companies across India run their payroll, atten... |  | That is why 450+ growing companies across India run their payroll, attendance and hiring on FabHR month after month. |
| EV_5 | india_based | - | general | Headquartered in Bangalore, India |  | Headquartered in Bangalore, India |
| EV_6 | headquarters_evidence | - | general | Headquartered in Bangalore, India |  | Headquartered in Bangalore, India |
| EV_7 | hr_technology | - | general | replacing spreadsheets, disconnected tools, and manual proce... |  | Our Mission To make every HR professional's day easier by replacing spreadsheets, disconnected tools, and manual processes with one intelligent, beautifully simple platform. |
| EV_8 | market_positioning_evidence | - | general | an end-to-end HRMS that handles everything from the moment a... |  | In 2019, they left their high-paying jobs to build HRORA — an end-to-end HRMS that handles everything from the moment an offer letter is signed to the day an employee's full and final settlement is pr... |
| EV_9 | market_positioning_evidence | - | general | 500+ companies across India trust HRORA to manage their most... |  | Today, 500+ companies across India trust HRORA to manage their most important asset: their people. |
| EV_10 | india_based | - | general | CoreHRx is a product of THINKNEXT INNOVATIONS PRIVATE LIMITE... |  | CoreHRx is a product of THINKNEXT INNOVATIONS PRIVATE LIMITED, headquartered in Sector 63, Noida, Uttar Pradesh. |
| EV_11 | b2b_saas | - | general | India's fastest-growing HR SaaS product |  | Incubated at IIM Lucknow's EIC and recognised as India's fastest-growing HR SaaS product. We serve 1,000+ organisations across India and 10+ countries — helping HR teams, business owners, and employee... |
| EV_12 | hr_technology | - | general | future of workforce management |  | We're building the future of workforce management CoreHRx was born from a simple frustration — why is HR so complicated for small Indian businesses? We're here to fix that. |
| EV_13 | market_positioning_evidence | - | general | why is HR so complicated for small Indian businesses? |  | CoreHRx was born from a simple frustration — why is HR so complicated for small Indian businesses? We're here to fix that. |
| EV_14 | headquarters_evidence | - | general | headquartered in Sector 63, Noida, Uttar Pradesh |  | CoreHRx is a product of THINKNEXT INNOVATIONS PRIVATE LIMITED, headquartered in Sector 63, Noida, Uttar Pradesh. |
| EV_15 | india_based | - | general | headquartered at Plot No. 136, Rider House, Sector 44, Gurug... |  | Zimyo Consulting Pvt. Ltd. is headquartered at Plot No. 136, Rider House, Sector 44, Gurugram, Haryana 122003, India. |
| EV_16 | b2b_saas | - | general | HRTech SaaS startup Zimyo |  | HRTech SaaS startup Zimyo has been felicitated at the India AI Impact Summit 2026 by Software Technology Parks of India (STPI), recognizing its contribution to advancing AI-driven innovation in human ... |
| EV_17 | hr_technology | - | general | Zimyo is an AI-powered, end-to-end HRMS platform |  | Zimyo is an AI-powered, end-to-end HRMS platform trusted by 2,500+ organisations and more than a million employees, with global payroll support across 40+ countries - including India, the United State... |
| EV_18 | market_positioning_evidence | - | general | Why organisations choose Zimyo |  | Why organisations choose Zimyo Consolidating HR operations onto one intelligent platform helps organisations lift productivity, strengthen compliance, improve the employee experience, and make workfor... |
| EV_19 | headquarters_evidence | - | general | headquartered at Plot No. 136, Rider House, Sector 44, Gurug... |  | Zimyo Consulting Pvt. Ltd. is headquartered at Plot No. 136, Rider House, Sector 44, Gurugram, Haryana 122003, India. |
| EV_20 | headquarters_evidence | - | general | Grape Garden, #29 & 30, 17th Main, 6th Block, Koramangala, B... |  | Grape Garden, #29 & 30, 17th Main, 6th Block, Koramangala, Bengaluru - 560095 |
| EV_21 | b2b_saas | - | general | Starting at ₹2,495/month |  | Full-suite HR + payroll + AI. Starting at ₹2,495/month. Payroll, compliance, leave, attendance, ESS, and greytHR NAVOS — all included from ₹2,495/mo for up to 50 employees. |
| EV_22 | hr_technology | - | general | Plan, Recruit, Onboard, Pay, Manage, Upskill, Appraise and E... |  | Plan, Recruit, Onboard, Pay, Manage, Upskill, Appraise and Empower your people — all in one platform. |
| EV_23 | market_positioning_evidence | - | general | 33,000+ companies run People Operations on greytHR. |  | 33,000+ companies run People Operations on greytHR. Here's why they stay. Full-suite HR and payroll, with an AI agent built in, at a price point that makes the decision easy. |
| EV_24 | headquarters_evidence | - | general | Bengaluru +91 8688827973 |  | Bengaluru +91 8688827973 (+918688827973) |
| EV_25 | b2b_saas | - | general | Keka gives you enterprise scale and depth with the ease of a... |  | Keka gives you enterprise scale and depth with the ease of a modern platform. One interconnected, AI-native core runs your payroll, hiring, performance, time, attendance, shifts, and more. |
| EV_26 | hr_technology | - | general | runs your payroll, hiring, performance, time, attendance, sh... |  | Keka gives you enterprise scale and depth with the ease of a modern platform. One interconnected, AI-native core runs your payroll, hiring, performance, time, attendance, shifts, and more. |
| EV_27 | market_positioning_evidence | - | general | Modern HR & Payroll Software for Growing Enterprises |  | Modern HR & Payroll Software for Growing Enterprises / Keka HR |
| EV_28 | market_positioning_evidence | - | general | ZingHR's AI-powered Hire-to-ReHire platform |  | ZingHR / Enterprise HCM for the End of Transactional HR # The End of Transactional HR with the all new ZINGHR ZingHR's AI-powered Hire-to-ReHire platform permanently removes HR transactional layers fr... |
| EV_29 | b2b_saas | - | general | The revived cloud payroll system |  | Kantar Data Analytics & Market Research ZingHR have a great dedicated team who are well-equipped in handling payroll operations. The team is very courteous and understands your business requirements w... |
| EV_30 | market_positioning_evidence | - | general | India's leading HRMS & payroll software |  | HR & Payroll Software / One-Stop HRMS Solution / Timelabs # India's leading HRMS & payroll software Go Live in 45 Days, Not 3–6 Months. One HR platform built to connect everything, even the systems ot... |
| EV_31 | hr_technology | - | general | Timelabs is an HRMS and HR operating system |  | ### What is Timelabs? Timelabs is an HRMS and HR operating system that brings core HR, attendance, payroll, recruitment, employee self service, analytics, and workforce management together on one conn... |

Rejected candidates:

- CAND_4 `b2b_saas` (verification): verdict=partial: The excerpt supports recurring use of FabHR for business HR workflows, but does not explicitly establish a SaaS model.
- CAND_11 `india_based` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_12 `headquarters_evidence` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_23 `india_based` (verification): verdict=partial: The page lists a Bengaluru address, but does not identify it as greytHR’s headquarters or principal office.
- CAND_28 `india_based` (verification): verdict=partial: Bengaluru appears as one of several contact locations, but the excerpt does not identify it as the headquarters or principal office.
- CAND_35 `hr_technology` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_37 `b2b_saas` (acceptance): lexical check: entity name/alias not found in excerpt context

## Q2 r2 adaptive - `EVAL_Q2_r2_adaptive_20261030T052640_3a95bb`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (None), recommendation `not_applicable`
- Mechanical: 12 cited evidence IDs, **0 invalid**; 25 accepted / 5 rejected (lexical 3, approach-identity 0); single-source cells: none
- AI-provisional flags: one source supports 3+ targets: SRC_1 (3); SRC_2 (4); SRC_5 (4); SRC_9 (5); SRC_10 (5)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | india_based | - | general | FabHR HQ, 4th Floor, Indiranagar, Bengaluru, Karnataka 56003... |  | FabHR HQ, 4th Floor, Indiranagar, Bengaluru, Karnataka 560038, India |
| EV_2 | headquarters_evidence | - | general | Headquarters FabHR HQ, 4th Floor, Indiranagar, Bengaluru, Ka... |  | FabHR HQ, 4th Floor, Indiranagar, Bengaluru, Karnataka 560038, India |
| EV_3 | hr_technology | - | general | The AI-first HR operating system for modern teams. Hire fast... |  | The AI-first HR operating system for modern teams. Hire faster, pay smarter, build teams that thrive. |
| EV_4 | market_positioning_evidence | - | general | 450+ growing companies across India run their payroll, atten... |  | That is why 450+ growing companies across India run their payroll, attendance and hiring on FabHR month after month. |
| EV_5 | india_based | - | general | Headquartered in Bangalore, India |  | Headquartered in Bangalore, India |
| EV_6 | headquarters_evidence | - | general | Headquartered in Bangalore, India |  | Headquartered in Bangalore, India |
| EV_7 | hr_technology | - | general | replacing spreadsheets, disconnected tools, and manual proce... |  | Our Mission To make every HR professional's day easier by replacing spreadsheets, disconnected tools, and manual processes with one intelligent, beautifully simple platform. |
| EV_8 | market_positioning_evidence | - | general | an end-to-end HRMS that handles everything from the moment a... |  | In 2019, they left their high-paying jobs to build HRORA — an end-to-end HRMS that handles everything from the moment an offer letter is signed to the day an employee's full and final settlement is pr... |
| EV_9 | market_positioning_evidence | - | general | 500+ companies across India trust HRORA to manage their most... |  | Today, 500+ companies across India trust HRORA to manage their most important asset: their people. |
| EV_10 | b2b_saas | - | general | AI-First HRMS & HCM Platform for Modern Teams |  | FabHR blends intelligent automation with human-centric design — so you can hire faster, pay smarter, and build teams that thrive. From 10 to 2,000 employees, one platform does it all. |
| EV_11 | hr_technology | - | general | FabHR brings every part of the employee lifecycle into one i... |  | Everything HR. Beautifully unified. Stop stitching together 15 tools. FabHR brings every part of the employee lifecycle into one intelligent ecosystem — Core HR, Payroll, Talent, Performance and AI. |
| EV_12 | market_positioning_evidence | - | general | FabHR empowers businesses with more than HR technology |  | FabHR empowers businesses with more than HR technology. From AI-powered HRMS and payroll outsourcing to offshore development teams and workforce staffing, we help organizations build, manage and scale... |
| EV_13 | headquarters_evidence | - | general | Headquarters FabHR HQ, 4th Floor, Indiranagar, Bengaluru, Ka... |  | Headquarters FabHR HQ, 4th Floor, Indiranagar, Bengaluru, Karnataka 560038, India |
| EV_14 | hr_technology | - | general | HRORA unifies attendance, payroll, leave, documents and 17+ ... |  | HRORA unifies attendance, payroll, leave, documents and 17+ HR modules — powered by AI, available on Android & iOS, with geo-based attendance built in. |
| EV_15 | b2b_saas | - | general | Trusted by 500+ companies across India |  | Trusted by 500+ companies across India |
| EV_16 | b2b_saas | - | general | recognised as India's fastest-growing HR SaaS product |  | Incubated at IIM Lucknow's EIC and recognised as India's fastest-growing HR SaaS product. We serve 1,000+ organisations across India and 10+ countries — helping HR teams, business owners, and employee... |
| EV_17 | hr_technology | - | general | why is HR so complicated for small Indian businesses? |  | CoreHRx was born from a simple frustration — why is HR so complicated for small Indian businesses? We're here to fix that. |
| EV_18 | market_positioning_evidence | - | general | We serve 1,000+ organisations |  | We serve 1,000+ organisations across India and 10+ countries — helping HR teams, business owners, and employees work smarter from a single app. |
| EV_19 | india_based | - | general | CoreHRx is a product of THINKNEXT INNOVATIONS PRIVATE LIMITE... |  | CoreHRx is a product of THINKNEXT INNOVATIONS PRIVATE LIMITED, headquartered in Sector 63, Noida, Uttar Pradesh. |
| EV_20 | headquarters_evidence | - | general | headquartered in Sector 63, Noida, Uttar Pradesh |  | CoreHRx is a product of THINKNEXT INNOVATIONS PRIVATE LIMITED, headquartered in Sector 63, Noida, Uttar Pradesh. |
| EV_21 | b2b_saas | - | general | Best SaaS product of the year |  | Zimyo bagged the award for Best SaaS product of the year by Entrepreneurs Media Excellence Award in the HRMS category |
| EV_22 | hr_technology | - | general | end-to-end HRMS platform |  | Zimyo is an AI-powered, end-to-end HRMS platform trusted by 2,500+ organisations and more than a million employees, with global payroll support across 40+ countries - including India, the United State... |
| EV_23 | market_positioning_evidence | - | general | trusted by 2,500+ organisations |  | Zimyo is an AI-powered, end-to-end HRMS platform trusted by 2,500+ organisations and more than a million employees, with global payroll support across 40+ countries - including India, the United State... |
| EV_24 | india_based | - | general | Zimyo Consulting Pvt. Ltd. is headquartered at |  | Zimyo Consulting Pvt. Ltd. is headquartered at Plot No. 136, Rider House, Sector 44, Gurugram, Haryana 122003, India. |
| EV_25 | headquarters_evidence | - | general | Plot No. 136, Rider House, Sector 44, Gurugram |  | Zimyo Consulting Pvt. Ltd. is headquartered at Plot No. 136, Rider House, Sector 44, Gurugram, Haryana 122003, India. |

Rejected candidates:

- CAND_4 `b2b_saas` (verification): verdict=partial: The excerpt supports recurring use of FabHR for business HR workflows, but does not explicitly establish a SaaS model.
- CAND_11 `india_based` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_12 `headquarters_evidence` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_13 `india_based` (verification): verdict=irrelevant: It supports the stated employee-size range but provides no evidence about FabHR’s headquarters or location.
- CAND_20 `market_positioning_evidence` (acceptance): lexical check: entity name/alias not found in excerpt context

## Q3 r2 static - `EVAL_Q3_r2_static_20261030T052821_89c1ce`

- Status `partial`, stop `budget_exhausted`, interval leader `Single-agent support automation` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only)
- Mechanical: 10 cited evidence IDs, **0 invalid**; 10 accepted / 4 rejected (lexical 0, approach-identity 1); single-source cells: Single-agent support automation:safeguards, Multi-agent support automation:implementation_and_operational_complexit, Multi-agent support automation:reliability
- AI-provisional flags: one source supports 3+ targets: SRC_1 (5); SRC_5 (4)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Single-agent support automation:implementation_and_operational_complexit | 2 | general | Single‐agent systems consolidate all logic into a single age... | Strong anchor: the excerpt explicitly describes simpler implementation and reduced operational overhead, suggesting a st... | Single‐agent systems consolidate all logic into a single agent. This approach simplifies implementation, reduces operational overhead, and offers a more predictable execution model. |
| EV_2 | Single-agent support automation:total_cost | 1 | general | Single-agent designs reduce token usage and API calls | Plausible anchor: the excerpt identifies cost-reducing factors, but recommends validating the benefits, so the total cos... | Single-agent designs reduce token usage and API calls by maintaining context within one entity. Validate cost benefits through prototyping before adding orchestration overhead. |
| EV_3 | Single-agent support automation:reliability | 1 | general | even with single agents | Plausible anchor: the excerpt says workflows add structure for reliability, but does not establish consistent correctnes... | Single agents often respond directly to user requests without orchestration. Workflows provide essential structure for reliability and enterprise integration even with single agents. |
| EV_4 | Multi-agent support automation:implementation_and_operational_complexit | 1 | general | Each agent interaction requires protocol design | Plausible anchor: the excerpt establishes meaningful additional integration and monitoring work, but does not show that ... | Each agent interaction requires protocol design, error handling, and state synchronization. Every component needs separate prompt engineering, monitoring infrastructure, and debugging capabilities. |
| EV_5 | Multi-agent support automation:reliability | 1 | general | Manual chaining of agents creates brittle connections | Plausible anchor: reliability depends on careful workflow design; the excerpt identifies a failure risk in manual chaini... | Manual chaining of agents creates brittle connections that fail unpredictably. Workflows provide structured coordination that ensures reliable agent interaction. |
| EV_6 | Single-agent support automation:implementation_and_operational_complexit | 1 | general | Classifier → narrow intent agent | Plausible: the excerpt explicitly identifies added routing code, indicating meaningful implementation work, while also d... | Architecture / Classifier → narrow intent agent / More routing code; lower blast radius |
| EV_7 | Single-agent support automation:total_cost | 1 | general | ~$27k/month | Plausible: the excerpt gives an illustrative operating cost, but it is tied to assumed ticket volume and does not establ... | Takeaway: at ~$3–6 human cost/ticket, even 30% automation saves roughly $270k/month gross against ~$27k LLM. |
| EV_8 | Single-agent support automation:reliability | 2 | general | Handoff carries intent, facts, attempts, and a draft | Strong: the excerpt describes clear escalation conditions, a human handoff that preserves context, and measurement of re... | Escalate on low confidence, two failed tools, customer asks for a human (must work first try), angry sentiment, or gate reject. Handoff carries intent, facts, attempts, and a draft so the human starts... |
| EV_9 | Single-agent support automation:safeguards | 2 | general | The write gate is deterministic code | Strong: the excerpt specifies enforceable action limits and an authorization check outside the model, plus confirmation ... | The write gate is deterministic code before any payment call: amount ≤ $100 and ≤ order total; ≤ 2 refunds per customer per 90 days; ownership re-derived from session auth (never trust the agent's cla... |
| EV_10 | Single-agent support automation:safeguards | 2 | general | Audit every tool call | Strong: this directly supports auditability, one of the rubric's specified safeguards. | Audit every tool call — refunds are a financial record. |

Rejected candidates:

- CAND_4 `Single-agent support automation:safeguards` (acceptance): approach identity: identification quote missing or not found verbatim in the source
- CAND_6 `Multi-agent support automation:total_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_8 `Multi-agent support automation:safeguards` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_12 `Single-agent support automation:reliability` (grounding): excerpt not found in source text

## Q3 r2 adaptive - `EVAL_Q3_r2_adaptive_20261030T053046_85180d`

- Status `partial`, stop `budget_exhausted`, interval leader `Single-agent support automation` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only); differentiating cells lack strong support (single source or non-official): Single-agent support automation:implementation_and_operational_complexit, Multi-agent support automation:implementation_and_operational_complexit
- Mechanical: 7 cited evidence IDs, **0 invalid**; 5 accepted / 4 rejected (lexical 0, approach-identity 1); single-source cells: Single-agent support automation:implementation_and_operational_complexit, Single-agent support automation:total_cost, Single-agent support automation:reliability, Multi-agent support automation:implementation_and_operational_complexit, Multi-agent support automation:reliability
- AI-provisional flags: one source supports 3+ targets: SRC_1 (5)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Single-agent support automation:implementation_and_operational_complexit | 2 | general | Single‐agent systems consolidate all logic into a single age... | Strong anchor: the excerpt explicitly describes simpler implementation and reduced operational overhead, suggesting a st... | Single‐agent systems consolidate all logic into a single agent. This approach simplifies implementation, reduces operational overhead, and offers a more predictable execution model. |
| EV_2 | Single-agent support automation:total_cost | 1 | general | Single-agent designs reduce token usage and API calls | Plausible anchor: the excerpt identifies cost-reducing factors, but recommends validating the benefits, so the total cos... | Single-agent designs reduce token usage and API calls by maintaining context within one entity. Validate cost benefits through prototyping before adding orchestration overhead. |
| EV_3 | Single-agent support automation:reliability | 1 | general | even with single agents | Plausible anchor: the excerpt says workflows add structure for reliability, but does not establish consistent correctnes... | Single agents often respond directly to user requests without orchestration. Workflows provide essential structure for reliability and enterprise integration even with single agents. |
| EV_4 | Multi-agent support automation:implementation_and_operational_complexit | 1 | general | Each agent interaction requires protocol design | Plausible anchor: the excerpt establishes meaningful additional integration and monitoring work, but does not show that ... | Each agent interaction requires protocol design, error handling, and state synchronization. Every component needs separate prompt engineering, monitoring infrastructure, and debugging capabilities. |
| EV_5 | Multi-agent support automation:reliability | 1 | general | Manual chaining of agents creates brittle connections | Plausible anchor: reliability depends on careful workflow design; the excerpt identifies a failure risk in manual chaini... | Manual chaining of agents creates brittle connections that fail unpredictably. Workflows provide structured coordination that ensures reliable agent interaction. |

Rejected candidates:

- CAND_4 `Single-agent support automation:safeguards` (acceptance): approach identity: identification quote missing or not found verbatim in the source
- CAND_6 `Multi-agent support automation:total_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_8 `Multi-agent support automation:safeguards` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_9 `Multi-agent support automation:safeguards` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q4 r2 static - `EVAL_Q4_r2_static_20261030T053139_484ad1`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (undetermined), recommendation `none`
- Mechanical: 12 cited evidence IDs, **0 invalid**; 7 accepted / 12 rejected (lexical 0, approach-identity 0); single-source cells: Session-only context:short_term_continuity, Structured persistent customer profile:retrieval_quality, Structured persistent customer profile:long_term_continuity
- AI-provisional flags: none

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Session-only context:retrieval_quality | 0 | general | A stateless chatbot treats every message as if it were the f... | Meets the poor anchor: relevant prior-interaction context, including a prior promise or issue, is unavailable to the sta... | A stateless chatbot treats every message as if it were the first. It has no idea the customer asked about the same failed payment an hour ago, or that they are a ten-year enterprise account, or that t... |
| EV_2 | Session-only context:short_term_continuity | 2 | general | exists only for the length of the session | Meets the strong anchor for an active session: the excerpt says this context lets the agent handle a multi-turn exchange... | Short-term (working) memory. This is the current conversation: what the customer just said, the clarifying question the agent asked, the answer in progress. It lives largely in the model's context win... |
| EV_3 | Session-only context:long_term_continuity | 0 | general | The model keeps nothing between conversations. | Meets the poor anchor: the excerpt explicitly says nothing is kept between conversations, so the agent cannot carry cust... | The model keeps nothing between conversations. Anthropic's Messages API is stateless, so anything the agent knows about last week's ticket has to be loaded into this conversation. |
| EV_4 | Structured persistent customer profile:retrieval_quality | 1 | general | The profile filter keeps the customer's profile built from s... | Meets the plausible anchor: the excerpt shows a useful filtered profile lookup, but does not establish broad coverage or... | The profile filter keeps the customer's profile built from support tickets only, even if the same namespace also holds synced documents (user profiles docs). |
| EV_5 | Session-only context:retrieval_quality | 0 | general | do not retain prior context unless an external memory layer ... | Poor: relevant context from prior interactions is unavailable when the session ends, so retrieval depends on the current... | Across independent sessions, dialogue systems built on large language models do not retain prior context unless an external memory layer organizes and retrieves it. |
| EV_6 | Session-only context:long_term_continuity | 0 | general | do not retain prior context unless an external memory layer ... | Poor: the excerpt directly says prior context is not retained across independent sessions absent an external memory laye... | Across independent sessions, dialogue systems built on large language models do not retain prior context unless an external memory layer organizes and retrieves it. |
| EV_7 | Structured persistent customer profile:long_term_continuity | 1 | general | a key-value profile store for applications, indexed by custo... | Plausible: the excerpt describes a persistent, addressable profile with historical attributes and streaming updates, whi... | Golden profile: survivorship rules choose each attribute's value; dbt derives lifetime value, segments and propensities; history kept as SCD Type 2. 5. Serving: warehouse tables for analysts; a key-va... |

Rejected candidates:

- CAND_4 `Session-only context:retention_deletion_controls` (verification): verdict=partial: The excerpt establishes session-bounded duration but not retention management, updates, or deletion workflows.
- CAND_5 `Retrieval-augmented episodic memory:retrieval_quality` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_6 `Retrieval-augmented episodic memory:long_term_continuity` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_7 `Retrieval-augmented episodic memory:privacy_controls` (verification): verdict=partial: The excerpt recommends authorization and tenant scoping for memory generally, but does not attribute those safeguards specifically to episodic memory or 
- CAND_8 `Retrieval-augmented episodic memory:retention_deletion_controls` (verification): verdict=partial: The excerpt recommends category-specific retention and deletion coverage for memory generally, but does not establish these as capabilities of episodic m
- CAND_10 `Structured persistent customer profile:long_term_continuity` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_11 `Structured persistent customer profile:privacy_controls` (verification): verdict=irrelevant: The excerpt supports customer-level isolation for a namespace-based retrieval design, not specifically for a structured persistent customer profile.
- CAND_13 `Session-only context:short_term_continuity` (grounding): excerpt not found in source text
- CAND_15 `Retrieval-augmented episodic memory:retrieval_quality` (grounding): excerpt not found in source text
- CAND_16 `Retrieval-augmented episodic memory:retrieval_quality` (grounding): excerpt not found in source text
- CAND_17 `Retrieval-augmented episodic memory:retention_deletion_controls` (grounding): excerpt not found in source text
- CAND_18 `Retrieval-augmented episodic memory:short_term_continuity` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q4 r2 adaptive - `EVAL_Q4_r2_adaptive_20261030T053444_755f84`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (undetermined), recommendation `none`
- Mechanical: 5 cited evidence IDs, **0 invalid**; 4 accepted / 9 rejected (lexical 0, approach-identity 0); single-source cells: Session-only context:retrieval_quality, Session-only context:short_term_continuity, Session-only context:long_term_continuity, Structured persistent customer profile:retrieval_quality
- AI-provisional flags: none

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Session-only context:retrieval_quality | 0 | general | A stateless chatbot treats every message as if it were the f... | Meets the poor anchor: relevant prior-interaction context, including a prior promise or issue, is unavailable to the sta... | A stateless chatbot treats every message as if it were the first. It has no idea the customer asked about the same failed payment an hour ago, or that they are a ten-year enterprise account, or that t... |
| EV_2 | Session-only context:short_term_continuity | 2 | general | exists only for the length of the session | Meets the strong anchor for an active session: the excerpt says this context lets the agent handle a multi-turn exchange... | Short-term (working) memory. This is the current conversation: what the customer just said, the clarifying question the agent asked, the answer in progress. It lives largely in the model's context win... |
| EV_3 | Session-only context:long_term_continuity | 0 | general | The model keeps nothing between conversations. | Meets the poor anchor: the excerpt explicitly says nothing is kept between conversations, so the agent cannot carry cust... | The model keeps nothing between conversations. Anthropic's Messages API is stateless, so anything the agent knows about last week's ticket has to be loaded into this conversation. |
| EV_4 | Structured persistent customer profile:retrieval_quality | 1 | general | The profile filter keeps the customer's profile built from s... | Meets the plausible anchor: the excerpt shows a useful filtered profile lookup, but does not establish broad coverage or... | The profile filter keeps the customer's profile built from support tickets only, even if the same namespace also holds synced documents (user profiles docs). |

Rejected candidates:

- CAND_4 `Session-only context:retention_deletion_controls` (verification): verdict=partial: The excerpt establishes session-bounded duration but not retention management, updates, or deletion workflows.
- CAND_5 `Retrieval-augmented episodic memory:retrieval_quality` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_6 `Retrieval-augmented episodic memory:long_term_continuity` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_7 `Retrieval-augmented episodic memory:privacy_controls` (verification): verdict=partial: The excerpt recommends authorization and tenant scoping for memory generally, but does not attribute those safeguards specifically to episodic memory or 
- CAND_8 `Retrieval-augmented episodic memory:retention_deletion_controls` (verification): verdict=partial: The excerpt recommends category-specific retention and deletion coverage for memory generally, but does not establish these as capabilities of episodic m
- CAND_10 `Structured persistent customer profile:long_term_continuity` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_11 `Structured persistent customer profile:privacy_controls` (verification): verdict=irrelevant: The excerpt supports customer-level isolation for a namespace-based retrieval design, not specifically for a structured persistent customer profile.
- CAND_12 `Retrieval-augmented episodic memory:long_term_continuity` (verification): verdict=partial: It describes retrieval of relevant external information, but does not establish continuity of customer context across separate sessions or how stale reco
- CAND_13 `Retrieval-augmented episodic memory:privacy_controls` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q5 r2 static - `EVAL_Q5_r2_static_20261030T053614_c66d86`

- Status `partial`, stop `budget_exhausted`, interval leader `Managed vector database` (robust), recommendation `withheld` - withheld: differentiating cells lack strong support (single source or non-official): Managed vector database:total_cost, Self-hosted vector database:total_cost, Self-hosted vector database:operational_control
- Mechanical: 9 cited evidence IDs, **0 invalid**; 9 accepted / 4 rejected (lexical 0, approach-identity 0); single-source cells: Managed vector database:total_cost, Self-hosted vector database:total_cost, Self-hosted vector database:operational_control
- AI-provisional flags: one source supports 3+ targets: SRC_1 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Managed vector database:operational_effort | 2 | general | A managed service hands you an endpoint and credentials. | Strong: the provider takes on recurring operational work that would otherwise fall to a small in-house team, reducing th... | A managed service hands you an endpoint and credentials. The vendor provisions machines, applies upgrades, replaces failed nodes, runs backups and watches the system. |
| EV_2 | Managed vector database:operational_control | 1 | general | a managed service gives you most of the control you need wit... | Plausible: the excerpt says managed services provide most of the control needed in many cases, but does not establish ex... | In many cases, a managed service gives you most of the control you need with far less engineering effort. |
| EV_3 | Self-hosted vector database:operational_effort | 0 | general | Self-hosting requires DevOps or MLOps engineers | Poor: the excerpt describes substantial provisioning, patching, security, and monitoring responsibilities and suggests s... | Self-hosting requires DevOps or MLOps engineers to provision, configure, patch, secure, and monitor the database. For a high-growth SaaS startup, this may mean budgeting for one or two full-time senio... |
| EV_4 | Self-hosted vector database:operational_control | 2 | general | Self-hosting gives you direct authority over where data live... | Strong: the excerpt describes direct authority over data handling, security, and configuration through system tuning, su... | Self-hosting gives you direct authority over where data lives, how it is secured, and how the system is tuned. |
| EV_5 | Managed vector database:operational_effort | 2 | general | Databricks Vector Search automatically syncs indexes from De... | Strong: the excerpt explicitly says the service removes index and capacity operations from the team, minimizing recurrin... | Databricks Vector Search automatically syncs indexes from Delta tables and scales endpoints, removing index and capacity operations from the team. |
| EV_6 | Self-hosted vector database:total_cost | 0 | general | Self-hosting 50 million vectors costs about $1,533/month in ... | Poor for the modeled workload: the excerpt puts the engineer cost above the compute bill, suggesting comparatively high ... | Self-hosting 50 million vectors costs about $1,533/month in reserved compute and roughly $1,800/month in the engineer who runs it. |
| EV_7 | Self-hosted vector database:operational_effort | 0 | general | It is roughly six hours a week, and it buys: version upgrade... | Poor for a startup with one backend engineer and limited operations time: the excerpt describes recurring operational wo... | Fifteen percent is not a conservative estimate. It is roughly six hours a week, and it buys: version upgrades, index rebuilds after an embedding model change, capacity forecasting, snapshot verificati... |
| EV_8 | Managed vector database:total_cost | 1 | general | $45/month on Flex | Plausible: the stated Flex minimum is a manageable entry price, but the excerpt notes additional charges and does not es... | The minimum covers the baseline cluster cost and includes charges for Vector Dimensions and Storage: $45/month on Flex and from $400/month on Premium. Backups are charged on top, based on data volume ... |
| EV_9 | Managed vector database:operational_control | 1 | general | Choice of shared or dedicated deployment. | Plausible: a shared-versus-dedicated deployment choice provides some control over deployment, but the excerpt does not s... | Choice of shared or dedicated deployment. |

Rejected candidates:

- CAND_2 `Managed vector database:total_cost` (grounding): excerpt not found in source text
- CAND_5 `Self-hosted vector database:total_cost` (grounding): excerpt not found in source text
- CAND_10 `Self-hosted vector database:operational_control` (verification): verdict=partial: It demonstrates a meaningful storage-precision configuration choice, but does not establish the broader control described by the criterion.
- CAND_11 `Managed vector database:operational_effort` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q5 r2 adaptive - `EVAL_Q5_r2_adaptive_20261030T053916_a39ae4`

- Status `partial`, stop `budget_exhausted`, interval leader `Managed vector database` (robust), recommendation `withheld` - withheld: differentiating cells lack strong support (single source or non-official): Self-hosted vector database:operational_effort
- Mechanical: 6 cited evidence IDs, **0 invalid**; 8 accepted / 10 rejected (lexical 0, approach-identity 4); single-source cells: Self-hosted vector database:operational_effort
- AI-provisional flags: one source supports 3+ targets: SRC_1 (3); SRC_5 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Managed vector database:operational_effort | 2 | general | A managed service hands you an endpoint and credentials. | Strong: the provider takes on recurring operational work that would otherwise fall to a small in-house team, reducing th... | A managed service hands you an endpoint and credentials. The vendor provisions machines, applies upgrades, replaces failed nodes, runs backups and watches the system. |
| EV_2 | Managed vector database:operational_control | 1 | general | a managed service gives you most of the control you need wit... | Plausible: the excerpt says managed services provide most of the control needed in many cases, but does not establish ex... | In many cases, a managed service gives you most of the control you need with far less engineering effort. |
| EV_3 | Self-hosted vector database:operational_effort | 0 | general | Self-hosting requires DevOps or MLOps engineers | Poor: the excerpt describes substantial provisioning, patching, security, and monitoring responsibilities and suggests s... | Self-hosting requires DevOps or MLOps engineers to provision, configure, patch, secure, and monitor the database. For a high-growth SaaS startup, this may mean budgeting for one or two full-time senio... |
| EV_4 | Self-hosted vector database:operational_control | 2 | general | Self-hosting gives you direct authority over where data live... | Strong: the excerpt describes direct authority over data handling, security, and configuration through system tuning, su... | Self-hosting gives you direct authority over where data lives, how it is secured, and how the system is tuned. |
| EV_5 | Managed vector database:operational_effort | 2 | general | Pinecone (Months 1–2): The Easy Default | Strong: the excerpt directly describes near-zero operational work, matching the anchor for minimizing recurring infrastr... | Zero ops. Truly. We never touched a knob beyond pod count. |
| EV_6 | Managed vector database:operational_control | 1 | general | The metadata schema and the way you structure namespaces is ... | Plausible: the excerpt shows meaningful constraints in how data is structured and a costly migration path, but does not ... | Lock-in. The metadata schema and the way you structure namespaces is Pinecone-specific. Migrating out is a project. |
| EV_7 | Self-hosted vector database:operational_control | 1 | general | self-hosted on EKS | Plausible: the excerpt demonstrates control over some backup and replication capabilities, but does not establish extens... | Snapshots and replicas are first-class. |
| EV_8 | Managed vector database:operational_effort | 2 | general | Pinecone is genuinely zero-ops. | Meets the strong anchor: the excerpt explicitly describes minimal recurring infrastructure work and automatic scaling, w... | Pinecone is genuinely zero-ops. No capacity planning, no index tuning, no infrastructure management. Their serverless offering scales automatically and you pay per query. |

Rejected candidates:

- CAND_2 `Managed vector database:total_cost` (grounding): excerpt not found in source text
- CAND_5 `Self-hosted vector database:total_cost` (grounding): excerpt not found in source text
- CAND_8 `Managed vector database:total_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_10 `Self-hosted vector database:operational_effort` (acceptance): approach identity: identification quote missing or not found verbatim in the source
- CAND_11 `Self-hosted vector database:total_cost` (acceptance): approach identity: excerpt describes several alternatives without isolating this one
- CAND_14 `Managed vector database:total_cost` (acceptance): approach identity: excerpt describes several alternatives without isolating this one
- CAND_15 `Managed vector database:operational_control` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_16 `Self-hosted vector database:operational_effort` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_17 `Self-hosted vector database:total_cost` (acceptance): approach identity: excerpt describes several alternatives without isolating this one
- CAND_18 `Self-hosted vector database:operational_effort` (grounding): excerpt not found in source text

## Q8 r2 static - `EVAL_Q8_r2_static_20261030T054158_cde02f`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (None), recommendation `not_applicable`
- Mechanical: 18 cited evidence IDs, **0 invalid**; 21 accepted / 4 rejected (lexical 1, approach-identity 0); single-source cells: none
- AI-provisional flags: one source supports 3+ targets: SRC_1 (3); SRC_5 (3); SRC_6 (3); SRC_7 (3); SRC_9 (3); SRC_10 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | llm_evaluation_or_observability | - | general | Langfuse is an **open source LLM engineering** platform |  | Langfuse is an **open source LLM engineering** platform. It helps teams collaboratively **develop, monitor, evaluate,** and **debug** AI applications. |
| EV_2 | open_source_license | - | general | This repository is MIT licensed, except for the `ee` folders... |  | This repository is MIT licensed, except for the `ee` folders. See LICENSE and docs for more details. |
| EV_3 | self_hosting_support | - | general | Run Langfuse on your own infrastructure |  | Run Langfuse on your own infrastructure: - Local (docker compose): Run Langfuse on your own machine in 5 minutes using Docker Compose. |
| EV_4 | llm_evaluation_or_observability | - | general | Opik is the open-source LLM observability and evaluation pla... |  | Opik is the open-source LLM observability and evaluation platform for AI agent tracing, LLM evaluation, prompt management, and production monitoring. |
| EV_5 | open_source_license | - | general | Apache-2.0 licensed |  | Apache-2.0 licensed, free to self-host the full platform, with 20,000+ GitHub stars. |
| EV_6 | self_hosting_support | - | general | Opik can be deployed locally or in your own infrastructure |  | Yes. Opik can be deployed locally or in your own infrastructure using the documented self-hosting options. |
| EV_7 | llm_evaluation_or_observability | - | general | Trace, evaluate, guard, and improve AI agents and coding age... |  | Trace, evaluate, guard, and improve AI agents and coding agents with OpenTelemetry. |
| EV_8 | open_source_license | - | general | OpenLIT is free to self-host under Apache 2.0 |  | OpenLIT is free to self-host under Apache 2.0 and works with any model, framework, or harness: Claude Code, Codex, Cursor, OpenAI Agents SDK, LangGraph, CrewAI, and 70+ more integrations. |
| EV_9 | self_hosting_support | - | general | Run OpenLIT inside your own infrastructure using Docker or K... |  | Run OpenLIT inside your own infrastructure using Docker or Kubernetes. |
| EV_10 | llm_evaluation_or_observability | - | general | LangWatch is the open-source platform for AI in production |  | LangWatch is the open-source platform for AI in production: trace, test, route and govern every LLM call in your company, from the agents you build to the coding assistants your engineers use. |
| EV_11 | llm_evaluation_or_observability | - | general | Create simulation tests for evaluating or benchmarking your ... |  | Create simulation tests for evaluating or benchmarking your agents and voice agents |
| EV_12 | open_source_license | - | general | LangWatch is Apache 2.0. |  | LangWatch is Apache 2.0. |
| EV_13 | self_hosting_support | - | general | ### Self-host ``` npx @langwatch/server ``` |  | ### Self-host ``` npx @langwatch/server ``` Only Node.js 24 or newer required (macOS or glibc Linux). |
| EV_14 | open_source_license | - | general | License: Apache License 2.0 |  | License: Apache License 2.0 |
| EV_15 | self_hosting_support | - | general | Self-host the open-source version |  | You can choose: * Self-host the open-source version. Live demo. |
| EV_16 | llm_evaluation_or_observability | - | general | OpenLIT is an open-source agent harness engineering platform |  | OpenLIT is an open-source agent harness engineering platform: OpenTelemetry-native agent observability, evals, guardrails, prompt management, and cost and GPU monitoring for AI agents and coding agent... |
| EV_17 | open_source_license | - | general | License: Apache 2.0 |  | Free to self-host under Apache 2.0. |
| EV_18 | self_hosting_support | - | general | Self-host with Docker Compose or Kubernetes Helm. |  | How do I deploy OpenLIT? Self-host with Docker Compose or Kubernetes Helm. |
| EV_19 | llm_evaluation_or_observability | - | general | Self-hosted LLM observability and evals. |  | # LLMWatch **Self-hosted LLM observability and evals.** Log every model call with tokens, latency and cost, trace agent runs step by step, and compare models and prompts with evals that tell you wheth... |
| EV_20 | open_source_license | - | general | License: MIT License |  | # omer-ulucan/llmwatch - Stars: 0 - Forks: 0 - Watchers: 0 - Open issues: 0 - License: MIT License - Default branch: main - Created: 2026-03-07T21:52:58Z |
| EV_21 | self_hosting_support | - | general | docker compose up gives you the API and UI on one port |  | - **Zero-config deployment.** `docker compose up` gives you the API and UI on one port, with SQLite on a named volume. |

Rejected candidates:

- CAND_5 `open_source_license` (grounding): excerpt not found in source text
- CAND_6 `self_hosting_support` (grounding): excerpt not found in source text
- CAND_4 `llm_evaluation_or_observability` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_17 `llm_evaluation_or_observability` (grounding): excerpt not found in source text

## Q8 r2 adaptive - `EVAL_Q8_r2_adaptive_20261030T054339_1e3dad`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (None), recommendation `not_applicable`
- Mechanical: 13 cited evidence IDs, **0 invalid**; 16 accepted / 5 rejected (lexical 1, approach-identity 0); single-source cells: none
- AI-provisional flags: one source supports 3+ targets: SRC_1 (3); SRC_5 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | llm_evaluation_or_observability | - | general | Langfuse is an **open source LLM engineering** platform |  | Langfuse is an **open source LLM engineering** platform. It helps teams collaboratively **develop, monitor, evaluate,** and **debug** AI applications. |
| EV_2 | open_source_license | - | general | This repository is MIT licensed, except for the `ee` folders... |  | This repository is MIT licensed, except for the `ee` folders. See LICENSE and docs for more details. |
| EV_3 | self_hosting_support | - | general | Run Langfuse on your own infrastructure |  | Run Langfuse on your own infrastructure: - Local (docker compose): Run Langfuse on your own machine in 5 minutes using Docker Compose. |
| EV_4 | llm_evaluation_or_observability | - | general | Opik is the open-source LLM observability and evaluation pla... |  | Opik is the open-source LLM observability and evaluation platform for AI agent tracing, LLM evaluation, prompt management, and production monitoring. |
| EV_5 | open_source_license | - | general | Opik is licensed under Apache 2.0. |  | Opik is licensed under Apache 2.0. |
| EV_6 | self_hosting_support | - | general | Opik can be deployed locally or in your own infrastructure |  | Yes. Opik can be deployed locally or in your own infrastructure using the documented self-hosting options. |
| EV_7 | open_source_license | - | general | OpenLIT is free to self-host under Apache 2.0 |  | OpenLIT is free to self-host under Apache 2.0 and works with any model, framework, or harness: Claude Code, Codex, Cursor, OpenAI Agents SDK, LangGraph, CrewAI, and 70+ more integrations. |
| EV_8 | self_hosting_support | - | general | Run OpenLIT inside your own infrastructure using Docker or K... |  | Run OpenLIT inside your own infrastructure using Docker or Kubernetes. Your telemetry stays under your control. |
| EV_9 | llm_evaluation_or_observability | - | general | for the harness around their AI agents and coding agents |  | OpenLIT is an open-source agent harness engineering platform. It gives teams OpenTelemetry-native tracing, evaluations, guardrails, prompt and context management, and cost and GPU monitoring for the h... |
| EV_10 | self_hosting_support | - | general | self-hostable via Docker Compose or Helm |  | OpenLIT is fully open source under Apache 2.0 and self-hostable via Docker Compose or Helm, so your telemetry and prompts never have to leave your infrastructure. |
| EV_11 | llm_evaluation_or_observability | - | general | Langfuse is a self-hostable LLM engineering platform |  | Langfuse is a self-hostable LLM engineering platform for traces, sessions, evaluations, prompt management, datasets, annotations, and cost analytics, with hosted deployment also available. |
| EV_12 | self_hosting_support | - | general | Langfuse is a self-hostable |  | Langfuse is a self-hostable LLM engineering platform for traces, sessions, evaluations, prompt management, datasets, annotations, and cost analytics, with hosted deployment also available. |
| EV_13 | llm_evaluation_or_observability | - | general | Arize Phoenix is an open-source |  | Arize Phoenix is an open-source, OpenTelemetry-based observability and evaluation platform for LLM applications and agents, with trace exploration, datasets, experiments, and evaluators. |
| EV_14 | llm_evaluation_or_observability | - | general | Opik is Comet's open-source tracing and evaluation platform |  | Opik is Comet's open-source tracing and evaluation platform with a hosted service, datasets, experiments, prompt management, online scoring, dashboards, and agent-focused trace views. |
| EV_15 | llm_evaluation_or_observability | - | general | Helicone is an open-source observability platform |  | Helicone is an open-source observability platform and proxy for logging LLM requests, analyzing sessions, tracking cost and latency, collecting feedback, and running experiments. |
| EV_16 | llm_evaluation_or_observability | - | general | Laminar is an open-source platform for tracing, evaluating, ... |  | Laminar is an open-source platform for tracing, evaluating, and monitoring LLM applications and agents, with OpenTelemetry-based instrumentation, datasets, and browser-agent support. |

Rejected candidates:

- CAND_5 `open_source_license` (grounding): excerpt not found in source text
- CAND_6 `self_hosting_support` (grounding): excerpt not found in source text
- CAND_4 `llm_evaluation_or_observability` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_10 `llm_evaluation_or_observability` (grounding): excerpt not found in source text
- CAND_14 `open_source_license` (verification): verdict=partial: It names the Apache 2.0 license, but does not establish evidence from a repository or license file.

## Q1 r3 static - `EVAL_Q1_r3_static_20261030T054507_0a2006`

- Status `partial`, stop `budget_exhausted`, interval leader `Qdrant` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only)
- Mechanical: 9 cited evidence IDs, **0 invalid**; 10 accepted / 4 rejected (lexical 1, approach-identity 0); single-source cells: Qdrant:deployment_fit, Qdrant:operational_effort, Weaviate:filtering_capability, Milvus:deployment_fit
- AI-provisional flags: none

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Qdrant:deployment_fit | 2 | general | Run Qdrant as a managed service on AWS, GCP, or Azure | Strong (2): the excerpt identifies a managed service across AWS, GCP, and Azure and lists practical managed capabilities... | Managed Cloud — Run Qdrant as a managed service on AWS, GCP, or Azure with automatic scaling, backups, and zero-downtime upgrades. |
| EV_2 | Qdrant:operational_effort | 2 | managed | with automatic scaling, backups, and zero-downtime upgrades | Strong (2): the excerpt describes managed hosting with automation for scaling and backups and zero-downtime upgrades, su... | Managed Cloud — Run Qdrant as a managed service on AWS, GCP, or Azure with automatic scaling, backups, and zero-downtime upgrades. |
| EV_3 | Qdrant:deployment_fit | 2 | general | Qdrant supports multiple deployment models | Strong anchor: the excerpt identifies clear managed and self-hosted deployment paths, including Managed Cloud and Privat... | Qdrant supports multiple deployment models to match different infrastructure and operational needs. The right option depends on your security constraints and operational model: Qdrant-managed infrastr... |
| EV_4 | Qdrant:operational_effort | 2 | managed | Qdrant fully manages your infrastructure | Strong anchor: the deployment comparison explicitly says Qdrant fully manages the infrastructure; the row is the managed... | No Infrastructure Management / Qdrant fully manages your infrastructure, so you can focus on building your application. |
| EV_5 | Qdrant:operational_effort | 1 | self_hosted | In self-hosted deployments, you must manually create or drop... | Plausible anchor: the excerpt identifies hands-on scaling work for a self-hosted deployment, indicating operational effo... | In self-hosted deployments, you must manually create or drop replicas and move shards between nodes as you scale. |
| EV_6 | Weaviate:filtering_capability | 2 | general | Weaviate provides powerful filtered vector search capabiliti... | Meets the strong anchor: the excerpt directly describes structured filters integrated with vector retrieval, including p... | Weaviate provides powerful filtered vector search capabilities, allowing you to combine vector searches with structured, scalar filters. This enables you to find the closest vectors to a query vector ... |
| EV_7 | Milvus:deployment_fit | 2 | general | Milvus Standalone is the best choice | Strong anchor: the excerpt identifies a production-ready self-hosted option suited to early-stage projects and notes sub... | For early-stage production, when the project is still seeking product-market fit and agility is more important than scalability, Milvus Standalone is the best choice. It can still scale up to 100M vec... |
| EV_8 | Milvus:operational_effort | 2 | managed | Zilliz Cloud is hassle-free, powered by Milvus | Strong anchor: for the managed scope, the source explicitly characterizes the Milvus-powered service as hassle-free, ind... | Try Managed Milvus for Free Zilliz Cloud is hassle-free, powered by Milvus and 10x faster. |
| EV_9 | Milvus:operational_effort | 2 | self_hosted | Milvus Standalone is the best choice | Strong anchor for the self-hosted Standalone deployment: the excerpt explicitly says it requires much less DevOps than a... | It can still scale up to 100M vectors given enough machine resource, while requiring much less DevOps than maintaining a K8s cluster. |
| EV_10 | Milvus:operational_effort | 0 | self_hosted | operate the K8s cluster that runs Milvus Distributed | Poor anchor for the Distributed self-hosted deployment: the excerpt explicitly requires operating a Kubernetes cluster, ... | You can keep using Milvus Standalone for dev or staging environment for its convenience, and operate the K8s cluster that runs Milvus Distributed. |

Rejected candidates:

- CAND_3 `Qdrant:operational_effort` (verification): verdict=partial: The excerpt lists Qdrant configuration, monitoring, and tuning tasks, but does not identify them as self-hosted operations.
- CAND_4 `Qdrant:filtering_capability` (verification): verdict=partial: The excerpt supports integrated, adaptive filtering during vector search but does not establish expressive query conditions.
- CAND_6 `Qdrant:filtering_capability` (verification): verdict=partial: It shows filtering integrated into semantic retrieval, but does not establish the broader expressiveness or RAG suitability needed for the strong score.
- CAND_11 `Milvus:filtering_capability` (acceptance): lexical check: entity name/alias not found in excerpt context

## Q1 r3 adaptive - `EVAL_Q1_r3_adaptive_20261030T054711_d3bacc`

- Status `partial`, stop `budget_exhausted`, interval leader `Qdrant` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only)
- Mechanical: 5 cited evidence IDs, **0 invalid**; 5 accepted / 6 rejected (lexical 2, approach-identity 0); single-source cells: Qdrant:deployment_fit, Qdrant:operational_effort, Weaviate:deployment_fit, Milvus:operational_effort
- AI-provisional flags: none

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Qdrant:deployment_fit | 2 | general | Run Qdrant as a managed service on AWS, GCP, or Azure | Strong (2): the excerpt identifies a managed service across AWS, GCP, and Azure and lists practical managed capabilities... | Managed Cloud — Run Qdrant as a managed service on AWS, GCP, or Azure with automatic scaling, backups, and zero-downtime upgrades. |
| EV_2 | Qdrant:operational_effort | 2 | managed | with automatic scaling, backups, and zero-downtime upgrades | Strong (2): the excerpt describes managed hosting with automation for scaling and backups and zero-downtime upgrades, su... | Managed Cloud — Run Qdrant as a managed service on AWS, GCP, or Azure with automatic scaling, backups, and zero-downtime upgrades. |
| EV_3 | Milvus:operational_effort | 2 | managed | Zilliz Cloud sells the same engine | Meets the strong anchor for managed operations: the excerpt says operational decisions are taken off the table for the c... | Zilliz Cloud sells the same engine with those decisions taken off the table, and its pricing pages are explicit about what is metered. |
| EV_4 | Milvus:operational_effort | 0 | self_hosted | Self-hosting Milvus means owning | Meets the poor anchor: it identifies several substantial ongoing operational responsibilities for a self-hosting team. | Self-hosting Milvus means owning coordinator failover, replica placement, compaction behaviour and index-build capacity. |
| EV_5 | Weaviate:deployment_fit | 2 | general | deployment was easy with the provided Docker image | Meets the strong anchor by showing a practical self-hosted deployment option with no dependencies mentioned. | At least deployment was easy with the provided Docker image. There were no dependencies. |

Rejected candidates:

- CAND_3 `Qdrant:operational_effort` (verification): verdict=partial: The excerpt lists Qdrant configuration, monitoring, and tuning tasks, but does not identify them as self-hosted operations.
- CAND_4 `Qdrant:filtering_capability` (verification): verdict=partial: The excerpt supports integrated, adaptive filtering during vector search but does not establish expressive query conditions.
- CAND_9 `Qdrant:deployment_fit` (grounding): excerpt not found in source text
- CAND_5 `Milvus:deployment_fit` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_6 `Milvus:filtering_capability` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_10 `Qdrant:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q2 r3 static - `EVAL_Q2_r3_static_20261030T054836_aa03cf`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (None), recommendation `not_applicable`
- Mechanical: 19 cited evidence IDs, **0 invalid**; 26 accepted / 9 rejected (lexical 6, approach-identity 0); single-source cells: none
- AI-provisional flags: one source supports 3+ targets: SRC_3 (4); SRC_6 (4); SRC_7 (3); SRC_8 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | india_headquarters | - | general | Bengaluru-headquartered HR tech startup |  | In 2023, the Bengaluru-headquartered HR tech startup expanded into the UAE and Southeast Asia, acquired HR tech firms Troopers and MyRobin, and partnered with Microsoft to enhance its tech capabilitie... |
| EV_2 | b2b_saas | - | general | BetterPlace is Asia’s largest human capital SaaS solution |  | BetterPlace is Asia’s largest human capital SaaS solution that enables enterprises to manage the entire lifecycle of their frontline workers. |
| EV_3 | hr_technology | - | general | Betterplace streamlines HR functions |  | Betterplace streamlines HR functions via a unified, data-driven platform. From talent acquisition and onboarding to background verification, attendance tracking, and payroll processing, BetterPlace co... |
| EV_4 | market_positioning | - | general | Serving over 1,500 businesses |  | Serving over 1,500 businesses across 500 locations in APAC, India, and GCC, the startup competes with the likes of Zoho, Greythr, ZingHR, and Freshworks in the HRMS segment and competes with Apna, Gig... |
| EV_5 | hr_technology | - | general | the parent company of greytHR |  | Founded in 1994 by Grish Rowjee and Sayeed Anjum, GreyTip Software Private Limited, the parent company of greytHR, is a comprehensive HRMS platform that specialises in automating employee payroll serv... |
| EV_6 | market_positioning | - | general | strong adoption among SMEs and mid‐sized businesses |  | greytHR is one of India’s oldest and most trusted HRMS solutions with strong adoption among SMEs and mid‐sized businesses. It’s widely recognised for comprehensive payroll automation, statutory compli... |
| EV_7 | india_headquarters | - | general | Darwinbox is a Hyderabad-based |  | Darwinbox is a Hyderabad-based cloud HR technology platform that provides comprehensive solutions for recruitment, onboarding, payroll, travel, and people analytics. |
| EV_8 | b2b_saas | - | general | cloud HR technology platform |  | Darwinbox is a Hyderabad-based cloud HR technology platform that provides comprehensive solutions for recruitment, onboarding, payroll, travel, and people analytics. |
| EV_9 | hr_technology | - | general | Darwinbox’s cloud-based HRMS platform |  | Darwinbox’s cloud-based HRMS platform supports essential HR functions, including core HR, payroll, recruitment, performance management, and employee engagement. |
| EV_10 | market_positioning | - | general | employee lifecycle from hire to exit |  | Our comprehensive HR Tech 4.0 platform encompasses employee lifecycle from hire to exit, including Human Capital Management, Payroll, Talent Acquisition & Management, and Collaboration. |
| EV_11 | india_headquarters | - | general | CoreHRx is a product of THINKNEXT INNOVATIONS PRIVATE LIMITE... |  | CoreHRx is a product of THINKNEXT INNOVATIONS PRIVATE LIMITED, headquartered in Sector 63, Noida, Uttar Pradesh. |
| EV_12 | b2b_saas | - | general | India's fastest-growing HR SaaS product |  | Incubated at IIM Lucknow's EIC and recognised as India's fastest-growing HR SaaS product. |
| EV_13 | b2b_saas | - | general | We serve 1,000+ organisations |  | We serve 1,000+ organisations across India and 10+ countries — helping HR teams, business owners, and employees work smarter from a single app. |
| EV_14 | market_positioning | - | general | why is HR so complicated for small Indian businesses? We're ... |  | CoreHRx was born from a simple frustration — why is HR so complicated for small Indian businesses? We're here to fix that. |
| EV_15 | hr_technology | - | general | We're building the future of workforce management |  | We're building the future of workforce management |
| EV_16 | market_positioning | - | general | Automated processes linked directly to payroll |  | Automated processes linked directly to payroll — no guesswork. |
| EV_17 | b2b_saas | - | general | all included from ₹2,495/mo for up to 50 employees |  | Full-suite HR + payroll + AI. Starting at ₹2,495/month. Payroll, compliance, leave, attendance, ESS, and greytHR NAVOS — all included from ₹2,495/mo for up to 50 employees. |
| EV_18 | hr_technology | - | general | Plan, Recruit, Onboard, Pay, Manage, Upskill, Appraise and E... |  | Plan, Recruit, Onboard, Pay, Manage, Upskill, Appraise and Empower your people — all in one platform. |
| EV_19 | market_positioning | - | general | Full-suite HR and payroll, with an AI agent built in, at a p... |  | 33,000+ companies run People Operations on greytHR. Here's why they stay. Full-suite HR and payroll, with an AI agent built in, at a price point that makes the decision easy. |
| EV_20 | b2b_saas | - | general | Keka gives you enterprise scale and depth |  | Keka gives you enterprise scale and depth with the ease of a modern platform. One interconnected, AI-native core runs your payroll, hiring, performance, time, attendance, shifts, and more. |
| EV_21 | hr_technology | - | general | India payroll and compliance - HRIS - Hiring and onboarding ... |  | One platform to unify people, processes, and experiences - India payroll and compliance - HRIS - Hiring and onboarding - Time and attendance - Performance management - Project operations |
| EV_22 | market_positioning | - | general | One interconnected, AI-native core runs your payroll, hiring... |  | Keka gives you enterprise scale and depth with the ease of a modern platform. One interconnected, AI-native core runs your payroll, hiring, performance, time, attendance, shifts, and more. |
| EV_23 | market_positioning | - | general | Loved by 1200+ enterprises across Fortune 500s |  | Loved by 1200+ enterprises across Fortune 500s |
| EV_24 | hr_technology | - | general | AI driven HR & payroll software |  | Proudly made for the world by an 100% Indian homegrown company HRMantra is the world's most advanced AI driven HR & payroll software helping automate the most complicated hire-to-retire HR processes r... |
| EV_25 | market_positioning | - | general | off-the-shelf ready-to-use parameterized features |  | HRMantra is the world's most advanced AI driven HR & payroll software helping automate the most complicated hire-to-retire HR processes rapidly using its off-the-shelf ready-to-use parameterized featu... |
| EV_26 | market_positioning | - | general | Brands Happily Using HRMantra |  | Select Clientele #### Brands Happily Using HRMantra ##### Alpla ##### EagleBurgmann ##### Schneider ##### BHEL ##### Podar Education Network ##### LIC Housing Finance ##### POSCO Pune ##### Shinhan Ba... |

Rejected candidates:

- CAND_5 `india_headquarters` (verification): verdict=partial: The table associates greytHR with Bengaluru but does not specify that this is its headquarters.
- CAND_6 `b2b_saas` (verification): verdict=partial: It lists Greythr as an exact match with Bangalore, India as its recorded headquarters and calls it a full-suite HRMS platform, but does not explicitly id
- CAND_12 `market_positioning` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_13 `india_headquarters` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_14 `b2b_saas` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_15 `hr_technology` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_30 `hr_technology` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_31 `market_positioning` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_33 `b2b_saas` (verification): verdict=partial: The excerpt confirms cloud availability but does not establish that the cloud offering is SaaS.

## Q2 r3 adaptive - `EVAL_Q2_r3_adaptive_20261030T055134_ca429c`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (None), recommendation `not_applicable`
- Mechanical: 9 cited evidence IDs, **0 invalid**; 20 accepted / 8 rejected (lexical 3, approach-identity 0); single-source cells: none
- AI-provisional flags: one source supports 3+ targets: SRC_3 (4); SRC_6 (3); SRC_8 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | india_headquarters | - | general | Bengaluru-headquartered HR tech startup |  | In 2023, the Bengaluru-headquartered HR tech startup expanded into the UAE and Southeast Asia, acquired HR tech firms Troopers and MyRobin, and partnered with Microsoft to enhance its tech capabilitie... |
| EV_2 | b2b_saas | - | general | BetterPlace is Asia’s largest human capital SaaS solution |  | BetterPlace is Asia’s largest human capital SaaS solution that enables enterprises to manage the entire lifecycle of their frontline workers. |
| EV_3 | hr_technology | - | general | Betterplace streamlines HR functions |  | Betterplace streamlines HR functions via a unified, data-driven platform. From talent acquisition and onboarding to background verification, attendance tracking, and payroll processing, BetterPlace co... |
| EV_4 | market_positioning | - | general | Serving over 1,500 businesses |  | Serving over 1,500 businesses across 500 locations in APAC, India, and GCC, the startup competes with the likes of Zoho, Greythr, ZingHR, and Freshworks in the HRMS segment and competes with Apna, Gig... |
| EV_5 | hr_technology | - | general | the parent company of greytHR |  | Founded in 1994 by Grish Rowjee and Sayeed Anjum, GreyTip Software Private Limited, the parent company of greytHR, is a comprehensive HRMS platform that specialises in automating employee payroll serv... |
| EV_6 | market_positioning | - | general | strong adoption among SMEs and mid‐sized businesses |  | greytHR is one of India’s oldest and most trusted HRMS solutions with strong adoption among SMEs and mid‐sized businesses. It’s widely recognised for comprehensive payroll automation, statutory compli... |
| EV_7 | india_headquarters | - | general | Darwinbox is a Hyderabad-based |  | Darwinbox is a Hyderabad-based cloud HR technology platform that provides comprehensive solutions for recruitment, onboarding, payroll, travel, and people analytics. |
| EV_8 | b2b_saas | - | general | cloud HR technology platform |  | Darwinbox is a Hyderabad-based cloud HR technology platform that provides comprehensive solutions for recruitment, onboarding, payroll, travel, and people analytics. |
| EV_9 | hr_technology | - | general | Darwinbox’s cloud-based HRMS platform |  | Darwinbox’s cloud-based HRMS platform supports essential HR functions, including core HR, payroll, recruitment, performance management, and employee engagement. |
| EV_10 | b2b_saas | - | general | greytHR is delivered as cloud-hosted SaaS on a pay-per-use m... |  | greytHR is delivered as cloud-hosted SaaS on a pay-per-use model, with a free Starter tier for very small teams and mobile-first apps for both employees and managers on Android and iOS. |
| EV_11 | hr_technology | - | general | a full-suite, ‘hire-to-retire’ HRMS |  | Over three decades, greytHR has grown from a payroll-automation tool into a full-suite, ‘hire-to-retire’ HRMS for People Operations, with 50+ HR and payroll tools spanning recruitment, onboarding, eng... |
| EV_12 | market_positioning | - | general | built for businesses of all sizes - small, mid-sized and ent... |  | greytHR is a cloud-based, full-suite HRMS and payroll platform built for businesses of all sizes - small, mid-sized and enterprises. |
| EV_13 | b2b_saas | - | general | their fully integrated, comprehensive SaaS-based solutions |  | They enable businesses and HR departments of all shapes and sizes to leverage IT for both effectiveness and efficiency with their fully integrated, comprehensive SaaS-based solutions. |
| EV_14 | hr_technology | - | general | greytHR is an integrated cloud-based HR & Payroll software. |  | greytHR is an integrated cloud-based HR & Payroll software. |
| EV_15 | hr_technology | - | general | greytHR empowers employee self-service |  | greytHR empowers employee self-service and automates all HR processes including employee information management, leave and attendance, payroll, and much more. |
| EV_16 | market_positioning | - | general | we love entrepreneurs |  | If you started small and have big ambitions, that gives us something in common. |
| EV_17 | market_positioning | - | general | Their flagship product, greytHR |  | Their flagship product, greytHR, is India’s No. 1 cloud-based Payroll and HR Software serving 9000+ clients, 10 Lakhs+ users in 150+ cities. |
| EV_18 | market_positioning | - | general | businesses and HR departments of all shapes and sizes |  | They enable businesses and HR departments of all shapes and sizes to leverage IT for both effectiveness and efficiency with their fully integrated, comprehensive SaaS-based solutions. |
| EV_19 | hr_technology | - | general | greytHR offers 40+ tools for automating HR, payroll, leave &... |  | greytHR offers 40+ tools for automating HR, payroll, leave & attendance, and performance management, along with an employee self-service portal and mobile app. |
| EV_20 | market_positioning | - | general | Small and mid-sized companies are pillars of the economy |  | Small and mid-sized companies are pillars of the economy but have been underserved by legacy payroll and HCM solutions. greytHR enables businesses to save time and money by moving from complex and err... |

Rejected candidates:

- CAND_5 `india_headquarters` (verification): verdict=partial: The table associates greytHR with Bengaluru but does not specify that this is its headquarters.
- CAND_6 `b2b_saas` (verification): verdict=partial: It lists Greythr as an exact match with Bangalore, India as its recorded headquarters and calls it a full-suite HRMS platform, but does not explicitly id
- CAND_12 `market_positioning` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_13 `india_headquarters` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_17 `india_headquarters` (verification): verdict=partial: The profile lists Bangalore, India, but does not explicitly establish that this is the company’s headquarters.
- CAND_18 `b2b_saas` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_19 `b2b_saas` (verification): verdict=partial: It directly supports cloud-based HR and payroll software, but does not establish business customers or explicitly call it SaaS.
- CAND_26 `b2b_saas` (verification): verdict=partial: The context places greytHR in the cloud-based HR software market and identifies its customers, but does not directly state that its software is cloud-bas

## Q3 r3 static - `EVAL_Q3_r3_static_20261030T055323_5dd980`

- Status `partial`, stop `budget_exhausted`, interval leader `Single-agent support automation` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only)
- Mechanical: 12 cited evidence IDs, **0 invalid**; 8 accepted / 11 rejected (lexical 0, approach-identity 1); single-source cells: Single-agent support automation:reliability, Multi-agent support automation:total_cost, Multi-agent support automation:reliability
- AI-provisional flags: one source supports 3+ targets: SRC_5 (5)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Single-agent support automation:implementation_complexity | 2 | general | Single‐agent systems consolidate all logic into a single age... | Strong anchor: the excerpt directly says the design simplifies implementation and reduces operational overhead, supporti... | Single‐agent systems consolidate all logic into a single agent. This approach simplifies implementation, reduces operational overhead, and offers a more predictable execution model. |
| EV_2 | Multi-agent support automation:implementation_complexity | 0 | general | Each agent interaction requires protocol design, error handl... | Poor anchor: the excerpt describes several additional engineering and operational tasks across components and coordinati... | Each agent interaction requires protocol design, error handling, and state synchronization. Every component needs separate prompt engineering, monitoring infrastructure, and debugging capabilities. |
| EV_3 | Single-agent support automation:implementation_complexity | 2 | general | A single agent handles the entire conversation. | This describes one centralized agent and its workflow state rather than multiple coordinated components, which supports ... | A single agent handles the entire conversation. All tools, instructions, and state live in one place. |
| EV_4 | Single-agent support automation:reliability | 1 | general | A single very long instruction set degrades model reliabilit... | This identifies a reliability limitation as scope grows; reliability therefore depends on keeping instructions manageabl... | A single very long instruction set degrades model reliability |
| EV_5 | Multi-agent support automation:implementation_complexity | 0 | general | Multi-agent setups add real complexity | The excerpt identifies several coordination paths and additional ongoing maintenance and debugging, matching the poor an... | Multi-agent setups add real complexity — handoff logic, shared state, routing decisions — and that complexity has to be paid for in maintenance and debuggability. |
| EV_6 | Multi-agent support automation:total_cost | 1 | general | paid for in maintenance and debuggability | The excerpt supports added operational overhead, but does not quantify model or platform usage costs or establish that t... | Multi-agent setups add real complexity — handoff logic, shared state, routing decisions — and that complexity has to be paid for in maintenance and debuggability. |
| EV_7 | Multi-agent support automation:reliability | 1 | general | Handoff logic is a new failure surface | The excerpt identifies a coordination-related reliability risk, but does not say failures are difficult to detect or rec... | Handoff logic is a new failure surface |
| EV_8 | Multi-agent support automation:reliability | 1 | general | Routing errors can cause confusing user experiences | This identifies a potential inconsistency in user experience caused by coordination errors, but does not establish wheth... | Routing errors can cause confusing user experiences |

Rejected candidates:

- CAND_7 `Multi-agent support automation:reliability` (grounding): excerpt not found in source text
- CAND_2 `Single-agent support automation:total_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_3 `Single-agent support automation:reliability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_4 `Single-agent support automation:safeguards` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_6 `Multi-agent support automation:total_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_8 `Multi-agent support automation:safeguards` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_10 `Single-agent support automation:total_cost` (acceptance): approach identity: excerpt describes several alternatives without isolating this one
- CAND_11 `Single-agent support automation:reliability` (verification): verdict=partial: Centralizing behavior makes testing easier, but the excerpt does not address failure handling, escalation, or monitoring.
- CAND_17 `Multi-agent support automation:safeguards` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_18 `Single-agent support automation:reliability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_19 `Single-agent support automation:safeguards` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q3 r3 adaptive - `EVAL_Q3_r3_adaptive_20261030T055606_19d7b0`

- Status `partial`, stop `budget_exhausted`, interval leader `Single-agent support automation` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only); differentiating cells lack strong support (single source or non-official): Single-agent support automation:implementation_complexity, Multi-agent support automation:implementation_complexity
- Mechanical: 3 cited evidence IDs, **0 invalid**; 3 accepted / 7 rejected (lexical 0, approach-identity 0); single-source cells: Single-agent support automation:implementation_complexity, Multi-agent support automation:implementation_complexity, Multi-agent support automation:safeguards
- AI-provisional flags: none

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Single-agent support automation:implementation_complexity | 2 | general | Single‐agent systems consolidate all logic into a single age... | Strong anchor: the excerpt directly says the design simplifies implementation and reduces operational overhead, supporti... | Single‐agent systems consolidate all logic into a single agent. This approach simplifies implementation, reduces operational overhead, and offers a more predictable execution model. |
| EV_2 | Multi-agent support automation:implementation_complexity | 0 | general | Each agent interaction requires protocol design, error handl... | Poor anchor: the excerpt describes several additional engineering and operational tasks across components and coordinati... | Each agent interaction requires protocol design, error handling, and state synchronization. Every component needs separate prompt engineering, monitoring infrastructure, and debugging capabilities. |
| EV_3 | Multi-agent support automation:safeguards | 1 | general | several specialized agents coordinate to handle a customer i... | Plausible: the excerpt shows a policy check before execution, but does not establish clear permission boundaries, human ... | A retrieval agent gathers account context, a reasoning agent determines the appropriate resolution, a verification agent checks that resolution against policy, and an action agent executes it. |

Rejected candidates:

- CAND_7 `Multi-agent support automation:reliability` (grounding): excerpt not found in source text
- CAND_2 `Single-agent support automation:total_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_3 `Single-agent support automation:reliability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_4 `Single-agent support automation:safeguards` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_6 `Multi-agent support automation:total_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_8 `Multi-agent support automation:safeguards` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_9 `Multi-agent support automation:reliability` (grounding): excerpt not found in source text

## Q4 r3 static - `EVAL_Q4_r3_static_20261030T055711_56e79e`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (undetermined), recommendation `none`
- Mechanical: 3 cited evidence IDs, **0 invalid**; 3 accepted / 5 rejected (lexical 0, approach-identity 1); single-source cells: Session-only context-window memory:retrieval_usefulness, Session-only context-window memory:retention_and_deletion
- AI-provisional flags: none

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Session-only context-window memory:retrieval_usefulness | 1 | short_term | presence in the context window equals availability for recal... | Plausible: context-window information is available for the current inference, but the cited lost-in-the-middle limitatio... | Second, we revisit the "lost in the middle" phenomenon [5] and show that it is not merely a positional bias but a deeper indictment of the assumption that presence in the context window equals availab... |
| EV_2 | Session-only context-window memory:retrieval_usefulness | 0 | long_term | When a conversation ends and a new one begins, the context w... | Poor: the excerpt explicitly says the context resets between sessions, so it cannot make prior-session context available... | A context window exists only within a single inference call or, at most, a single session bounded by the model's maximum input length. When a conversation ends and a new one begins, the context window... |
| EV_3 | Session-only context-window memory:retention_and_deletion | 0 | short_term | There is no mechanism to revise a token in place | Poor: the excerpt explicitly identifies the lack of revision and deletion mechanisms, limiting reliable correction or re... | In a context window, information is represented as tokens at fixed positions. There is no mechanism to revise a token in place, to mark a previously presented fact as superseded, or to delete informat... |

Rejected candidates:

- CAND_5 `Retrieval-augmented episodic memory:retention_and_deletion` (grounding): excerpt not found in source text
- CAND_4 `Retrieval-augmented episodic memory:retrieval_usefulness` (acceptance): approach identity: identification quote missing or not found verbatim in the source
- CAND_6 `Retrieval-augmented episodic memory:privacy_controls` (grounding): excerpt not found in source text
- CAND_7 `Structured customer-profile memory:retention_and_deletion` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_8 `Structured customer-profile memory:retention_and_deletion` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q4 r3 adaptive - `EVAL_Q4_r3_adaptive_20261030T060017_40d637`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (undetermined), recommendation `none`
- Mechanical: 1 cited evidence IDs, **0 invalid**; 1 accepted / 0 rejected (lexical 0, approach-identity 0); single-source cells: Hybrid tiered memory:privacy_controls
- AI-provisional flags: none

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Hybrid tiered memory:privacy_controls | 1 | long_term | organizes episodic, semantic, social, and task memories as t... | Plausible: typed memory categories and sensitivity-aware retention provide some ability to limit sensitive data, and opt... | We present the Memory- Aware Retention Schema (MaRS), a cognitively inspired architecture that organizes episodic, semantic, social, and task memories as typed, provenance- tracked nodes with multiple... |

Rejected candidates:

- none

## Q5 r3 static - `EVAL_Q5_r3_static_20261030T060121_ab71c7`

- Status `partial`, stop `budget_exhausted`, interval leader `Managed vector database` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only)
- Mechanical: 6 cited evidence IDs, **0 invalid**; 16 accepted / 5 rejected (lexical 0, approach-identity 1); single-source cells: Self-hosted vector database:total_cost
- AI-provisional flags: one source supports 3+ targets: SRC_2 (4); SRC_6 (4); SRC_10 (5)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Managed vector database:operational_effort | 2 | general | Pinecone handles all operations, scaling, and maintenance. | Strong anchor: the excerpt explicitly says the provider handles all operations, scaling, and maintenance, leaving little... | Pinecone handles all operations, scaling, and maintenance. |
| EV_2 | Managed vector database:time_to_production | 2 | general | Managed services require initial setup (15 minutes) and zero... | Strong anchor: the stated 15-minute setup and zero maintenance support bringing the database into production quickly wit... | Managed services require initial setup (15 minutes) and zero maintenance. |
| EV_3 | Managed vector database:total_cost | 2 | general | a $70 per month managed database that saves 5 to 10 hours pe... | Strong anchor: the excerpt gives a clear monthly price and says the service saves substantial engineering time, describi... | For a two-person startup where every engineering hour counts, a $70 per month managed database that saves 5 to 10 hours per month of operations time is the cheapest option in practice. |
| EV_4 | Self-hosted vector database:operational_effort | 1 | general | Self-hosted Qdrant requires initial setup (1 to 2 hours), on... | Plausible anchor: the source describes recurring monitoring and occasional troubleshooting, but quantifies monitoring at... | Self-hosted Qdrant requires initial setup (1 to 2 hours), ongoing monitoring (1 to 2 hours per month), and occasional troubleshooting. |
| EV_5 | Managed vector database:operational_effort | 2 | general | A managed service hands you an endpoint and credentials. | Strong: routine infrastructure operations are handled by the vendor, leaving little ongoing operations work for the star... | A managed service hands you an endpoint and credentials. The vendor provisions machines, applies upgrades, replaces failed nodes, runs backups and watches the system. |
| EV_6 | Managed vector database:time_to_production | 2 | general | Managed services shorten time to production | Strong: the excerpt directly says managed services shorten time to production and include upgrades and backups, indicati... | Managed services shorten time to production, include upgrades and backups, and offer replication for high availability as an option. |
| EV_7 | Self-hosted vector database:operational_effort | 0 | general | Self-hosting moves upgrades, scaling, backups, monitoring an... | Poor: the excerpt assigns substantial recurring operational responsibilities to the team, which would strain a startup w... | Self-hosting moves upgrades, scaling, backups, monitoring and on-call duty to your team. |
| EV_8 | Self-hosted vector database:time_to_production | 0 | general | Each needs a plan before production, not after the first inc... | Poor: the excerpt lists substantial operational preparation that must be planned before production, rather than a quick ... | Self-hosting adds capacity planning, upgrades, scaling, backups, monitoring, security and on-call response to your team’s work. Each needs a plan before production, not after the first incident. |
| EV_9 | Self-hosted vector database:time_to_production | 1 | general | Self-hosted OSS: 45-minute setup | This supports the plausible anchor: the initial setup was quick, but tuning was still required. The excerpt does not est... | Self-hosted OSS: 45-minute setup but required tweaking `query_node.yaml` for optimal shard distribution |
| EV_10 | Self-hosted vector database:time_to_production | 0 | general | Realistic timeline: 3-6 weeks for an engineer with prior Kub... | This meets the poor anchor: the stated timeline involves substantial engineering work before production, even with relev... | Realistic timeline: 3-6 weeks for an engineer with prior Kubernetes/infra experience. Longer if they're learning as they go. |
| EV_11 | Self-hosted vector database:operational_effort | 0 | general | 0.25 FTE for ongoing operations of a small cluster | This meets the poor anchor for a startup with one backend engineer and limited operations time: the excerpt assigns a su... | Budget: 0.25 FTE for ongoing operations of a small cluster. 0.5-1 FTE for a big one. |
| EV_12 | Managed vector database:operational_effort | 2 | general | A managed vector database handles provisioning, scaling, bac... | Strong anchor: provisioning, scaling, backups, and index maintenance are handled by the provider, indicating little ongo... | A managed vector database handles provisioning, scaling, backups, and index maintenance, letting a team go from zero to a working retrieval pipeline in hours rather than days. |
| EV_13 | Managed vector database:time_to_production | 2 | general | letting a team go from zero to a working retrieval pipeline ... | Strong anchor: the excerpt explicitly describes reaching a working pipeline in hours rather than days and identifies min... | A managed vector database handles provisioning, scaling, backups, and index maintenance, letting a team go from zero to a working retrieval pipeline in hours rather than days. |
| EV_14 | Managed vector database:total_cost | 1 | general | managed pricing is typically built around a combination of s... | Plausible anchor: pricing is usage-based and the excerpt warns that costs can surprise teams as usage grows, suggesting ... | The tradeoff is cost that scales with usage in a way that can surprise a team once vector count and query volume both grow, since managed pricing is typically built around a combination of stored vect... |
| EV_15 | Self-hosted vector database:operational_effort | 0 | general | Self-hosting an open-source vector database | Poor anchor: the excerpt identifies multiple recurring infrastructure responsibilities and on-call ownership, a substant... | Self-hosting an open-source vector database trades a lower direct infrastructure bill for real, ongoing engineering time: index tuning, capacity planning, backup strategy, and on-call ownership for a ... |
| EV_16 | Self-hosted vector database:total_cost | 1 | general | the crossover point where self-hosting becomes clearly cheap... | Plausible anchor: the excerpt says costs can be manageable in some configurations but depend heavily on query volume and... | In our experience, the crossover point where self-hosting becomes clearly cheaper depends heavily on query volume, not just vector count — a large but rarely-queried index self-hosts cheaply, while a ... |

Rejected candidates:

- CAND_5 `Self-hosted vector database:time_to_production` (grounding): excerpt not found in source text
- CAND_6 `Self-hosted vector database:total_cost` (grounding): excerpt not found in source text
- CAND_14 `Managed vector database:operational_effort` (verification): verdict=partial: It contrasts Pinecone's invisible HA work with self-hosted HA engineering, but does not establish the broader routine-operations burden described by the 
- CAND_15 `Managed vector database:total_cost` (acceptance): approach identity: excerpt describes several alternatives without isolating this one
- CAND_16 `Self-hosted vector database:total_cost` (verification): verdict=partial: The excerpt supports the $3,530 total and $530 infrastructure figures, but the provided text does not identify them as the stated 10-million-vector Qdran

## Q5 r3 adaptive - `EVAL_Q5_r3_adaptive_20261030T060502_316282`

- Status `partial`, stop `budget_exhausted`, interval leader `Managed vector database` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only); differentiating cells lack strong support (single source or non-official): Self-hosted vector database:time_to_production
- Mechanical: 12 cited evidence IDs, **0 invalid**; 14 accepted / 6 rejected (lexical 0, approach-identity 0); single-source cells: Self-hosted vector database:time_to_production
- AI-provisional flags: one source supports 3+ targets: SRC_2 (4); SRC_5 (3); SRC_7 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Managed vector database:operational_effort | 2 | general | Pinecone handles all operations, scaling, and maintenance. | Strong anchor: the excerpt explicitly says the provider handles all operations, scaling, and maintenance, leaving little... | Pinecone handles all operations, scaling, and maintenance. |
| EV_2 | Managed vector database:time_to_production | 2 | general | Managed services require initial setup (15 minutes) and zero... | Strong anchor: the stated 15-minute setup and zero maintenance support bringing the database into production quickly wit... | Managed services require initial setup (15 minutes) and zero maintenance. |
| EV_3 | Managed vector database:total_cost | 2 | general | a $70 per month managed database that saves 5 to 10 hours pe... | Strong anchor: the excerpt gives a clear monthly price and says the service saves substantial engineering time, describi... | For a two-person startup where every engineering hour counts, a $70 per month managed database that saves 5 to 10 hours per month of operations time is the cheapest option in practice. |
| EV_4 | Self-hosted vector database:operational_effort | 1 | general | Self-hosted Qdrant requires initial setup (1 to 2 hours), on... | Plausible anchor: the source describes recurring monitoring and occasional troubleshooting, but quantifies monitoring at... | Self-hosted Qdrant requires initial setup (1 to 2 hours), ongoing monitoring (1 to 2 hours per month), and occasional troubleshooting. |
| EV_5 | Managed vector database:operational_effort | 2 | general | Pinecone — fully managed, no infrastructure to run | Strong: the excerpt explicitly describes a managed service as zero-ops with no infrastructure to run, indicating little ... | Want zero ops / serverless? Pinecone — fully managed, no infrastructure to run. |
| EV_6 | Managed vector database:time_to_production | 2 | general | Set up an index in 10 minutes, ship code | Strong: the excerpt describes a managed database index set up in 10 minutes, followed by shipping code, indicating quick... | Pinecone is the path of least resistance. Set up an index in 10 minutes, ship code, watch it work. |
| EV_7 | Managed vector database:total_cost | 1 | general | a managed service is almost always cheaper once engineering ... | Plausible: the excerpt says managed services are usually cheaper when engineering time is included for teams without ded... | If you have no dedicated infra/SRE capacity, a managed service is almost always cheaper once engineering time is priced in — until you reach a scale where per-vector pricing dominates. |
| EV_8 | Self-hosted vector database:operational_effort | 0 | general | Service was effectively down during that window | Poor: this self-hosted deployment experienced operational incidents, upgrade-related client breakage, and non-trivial cl... | Operational overhead is real. We hit two issues in 8 weeks: - A node restart caused index reload that took 6 minutes (memory-mapped files re-loading from disk). Service was effectively down during tha... |
| EV_9 | Self-hosted vector database:time_to_production | 1 | general | we got it wrong twice | Plausible: the excerpt indicates that production preparation involved meaningful infrastructure sizing and parameter wor... | Cluster sizing was non-trivial. The official guide assumes you understand HNSW parameters; we got it wrong twice. |
| EV_10 | Managed vector database:operational_effort | 2 | general | A managed vector database handles provisioning, scaling, bac... | Strong anchor: provisioning, scaling, backups, and index maintenance are handled by the provider, leaving little ongoing... | A managed vector database handles provisioning, scaling, backups, and index maintenance, letting a team go from zero to a working retrieval pipeline in hours rather than days. |
| EV_11 | Managed vector database:time_to_production | 2 | general | letting a team go from zero to a working retrieval pipeline ... | Strong anchor: the excerpt explicitly describes a fast path to a working pipeline and provider-managed infrastructure ta... | A managed vector database handles provisioning, scaling, backups, and index maintenance, letting a team go from zero to a working retrieval pipeline in hours rather than days. |
| EV_12 | Self-hosted vector database:operational_effort | 0 | general | index tuning, capacity planning, backup strategy, and on-cal... | Poor anchor: the excerpt identifies several substantial recurring operational responsibilities and cautions that their t... | Self-hosting an open-source vector database trades a lower direct infrastructure bill for real, ongoing engineering time: index tuning, capacity planning, backup strategy, and on-call ownership for a ... |
| EV_13 | Managed vector database:operational_effort | 2 | general | Pinecone is genuinely zero-ops. | Meets the strong anchor: the excerpt explicitly describes routine infrastructure and capacity work as handled without re... | Pinecone is genuinely zero-ops. No capacity planning, no index tuning, no infrastructure management. |
| EV_14 | Self-hosted vector database:operational_effort | 0 | general | Self-hosting means you own the operational burden | Meets the poor anchor: it lists several recurring operational responsibilities that would strain a startup with limited ... | Self-hosting means you own the operational burden: backups, monitoring, scaling, upgrades. |

Rejected candidates:

- CAND_5 `Self-hosted vector database:time_to_production` (grounding): excerpt not found in source text
- CAND_6 `Self-hosted vector database:total_cost` (grounding): excerpt not found in source text
- CAND_12 `Self-hosted vector database:total_cost` (verification): verdict=partial: It gives the cluster's monthly cost and characterizes it as middle-of-the-road, but does not establish startup-scale affordability or total cost includin
- CAND_15 `Managed vector database:total_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_17 `Self-hosted vector database:time_to_production` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_18 `Self-hosted vector database:total_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q8 r3 static - `EVAL_Q8_r3_static_20261030T060655_84dac1`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (None), recommendation `not_applicable`
- Mechanical: 13 cited evidence IDs, **0 invalid**; 21 accepted / 11 rejected (lexical 6, approach-identity 0); single-source cells: none
- AI-provisional flags: one source supports 3+ targets: SRC_2 (4); SRC_5 (4); SRC_8 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | llm_eval_or_observability | - | general | develop, monitor, evaluate, and debug AI applications |  | Litefuse is an **open source LLM engineering** platform. It helps teams collaboratively **develop, monitor, evaluate,** and **debug** AI applications. |
| EV_2 | open_source_license | - | general | This repository is MIT licensed. |  | This repository is MIT licensed. See LICENSE for details. |
| EV_3 | self_hosting_support | - | general | self-host on your own infrastructure |  | Two ways to run Litefuse: use the **managed cloud**, or **self-host** on your own infrastructure (Local, VM, Docker, Kubernetes via Helm, or Terraform on AWS / GCP / Azure). |
| EV_4 | license_and_deployment_evidence | - | general | This repository is MIT licensed. |  | This repository is MIT licensed. See LICENSE for details. |
| EV_5 | license_and_deployment_evidence | - | general | Run Litefuse on your own machine in 5 minutes using Docker C... |  | Run Litefuse on your own infrastructure: - Local (docker compose): Run Litefuse on your own machine in 5 minutes using Docker Compose. |
| EV_6 | llm_eval_or_observability | - | general | develop, monitor, evaluate, and debug AI applications |  | Langfuse is an open source LLM engineering platform. It helps teams collaboratively develop, monitor, evaluate, and debug AI applications. |
| EV_7 | self_hosting_support | - | general | Langfuse can be self-hosted in minutes |  | Langfuse can be self-hosted in minutes and is battle-tested. |
| EV_8 | self_hosting_support | - | general | Run Langfuse on your own machine in 5 minutes using Docker C... |  | Run Langfuse on your own infrastructure: - Local (docker compose): Run Langfuse on your own machine in 5 minutes using Docker Compose. |
| EV_9 | llm_eval_or_observability | - | general | Trace, evaluate, guard, and improve AI agents and coding age... |  | Trace, evaluate, guard, and improve AI agents and coding agents with OpenTelemetry. |
| EV_10 | open_source_license | - | general | License: Apache License 2.0 |  | License: Apache License 2.0 |
| EV_11 | self_hosting_support | - | general | Run OpenLIT inside your own infrastructure using Docker or K... |  | Run OpenLIT inside your own infrastructure using Docker or Kubernetes. Your telemetry stays under your control. |
| EV_12 | license_and_deployment_evidence | - | general | OpenLIT is free to self-host under Apache 2.0 |  | OpenLIT is free to self-host under Apache 2.0 |
| EV_13 | llm_eval_or_observability | - | general | Arize Phoenix is Arize's open-source AI observability platfo... |  | Arize Phoenix is Arize's open-source AI observability platform designed for experimentation, evaluation, and troubleshooting. |
| EV_14 | open_source_license | - | general | License: Apache License 2.0 |  | License: Apache License 2.0 |
| EV_15 | license_and_deployment_evidence | - | general | License: Apache License 2.0 |  | License: Apache License 2.0 |
| EV_16 | llm_eval_or_observability | - | general | trace, test, route and govern every LLM call |  | LangWatch is the open-source platform for AI in production: trace, test, route and govern every LLM call in your company, from the agents you build to the coding assistants your engineers use. |
| EV_17 | open_source_license | - | general | LangWatch is Apache 2.0. |  | LangWatch is Apache 2.0. |
| EV_18 | license_and_deployment_evidence | - | general | LangWatch is Apache 2.0. |  | LangWatch is Apache 2.0. |
| EV_19 | llm_eval_or_observability | - | general | open-source LLM observability |  | This guide shows you how to deploy open-source LLM observability with Docker, Kubernetes, or VMs on your own infrastructure. |
| EV_20 | self_hosting_support | - | general | Langfuse is open source and can be self-hosted using Docker ... |  | Langfuse is open source and can be self-hosted using Docker on your own infrastructure. |
| EV_21 | llm_eval_or_observability | - | general | Debug, evaluate, and monitor your LLM applications |  | opik / Debug, evaluate, and monitor your LLM applications, RAG systems, and agentic workflows with comprehensive tracing, automated evaluations, and production-ready dashboards. |

Rejected candidates:

- CAND_1 `llm_eval_or_observability` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_2 `open_source_license` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_3 `self_hosting_support` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_4 `license_and_deployment_evidence` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_18 `self_hosting_support` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_19 `llm_eval_or_observability` (grounding): excerpt not found in source text
- CAND_21 `self_hosting_support` (grounding): excerpt not found in source text
- CAND_23 `license_and_deployment_evidence` (grounding): excerpt not found in source text
- CAND_26 `self_hosting_support` (grounding): excerpt not found in source text
- CAND_28 `license_and_deployment_evidence` (grounding): excerpt not found in source text
- CAND_32 `self_hosting_support` (acceptance): lexical check: entity name/alias not found in excerpt context

## Q8 r3 adaptive - `EVAL_Q8_r3_adaptive_20261030T060902_086d45`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (None), recommendation `not_applicable`
- Mechanical: 7 cited evidence IDs, **0 invalid**; 18 accepted / 6 rejected (lexical 4, approach-identity 0); single-source cells: none
- AI-provisional flags: one source supports 3+ targets: SRC_2 (4); SRC_8 (3); SRC_10 (4)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | llm_eval_or_observability | - | general | develop, monitor, evaluate, and debug AI applications |  | Litefuse is an **open source LLM engineering** platform. It helps teams collaboratively **develop, monitor, evaluate,** and **debug** AI applications. |
| EV_2 | open_source_license | - | general | This repository is MIT licensed. |  | This repository is MIT licensed. See LICENSE for details. |
| EV_3 | self_hosting_support | - | general | self-host on your own infrastructure |  | Two ways to run Litefuse: use the **managed cloud**, or **self-host** on your own infrastructure (Local, VM, Docker, Kubernetes via Helm, or Terraform on AWS / GCP / Azure). |
| EV_4 | license_and_deployment_evidence | - | general | This repository is MIT licensed. |  | This repository is MIT licensed. See LICENSE for details. |
| EV_5 | license_and_deployment_evidence | - | general | Run Litefuse on your own machine in 5 minutes using Docker C... |  | Run Litefuse on your own infrastructure: - Local (docker compose): Run Litefuse on your own machine in 5 minutes using Docker Compose. |
| EV_6 | llm_eval_or_observability | - | general | develop, monitor, evaluate, and debug AI applications |  | Langfuse is an open source LLM engineering platform. It helps teams collaboratively develop, monitor, evaluate, and debug AI applications. |
| EV_7 | self_hosting_support | - | general | Langfuse can be self-hosted in minutes |  | Langfuse can be self-hosted in minutes and is battle-tested. |
| EV_8 | self_hosting_support | - | general | Run Langfuse on your own machine in 5 minutes using Docker C... |  | Run Langfuse on your own infrastructure: - Local (docker compose): Run Langfuse on your own machine in 5 minutes using Docker Compose. |
| EV_9 | llm_eval_or_observability | - | general | Langfuse provides comprehensive tracing capabilities |  | Langfuse provides comprehensive tracing capabilities that help you understand exactly what's happening in your application. |
| EV_10 | llm_eval_or_observability | - | general | Langfuse provides flexible evaluation tools |  | Evaluation is crucial for ensuring the quality and reliability of your LLM applications. Langfuse provides flexible evaluation tools that adapt to your specific needs, whether you're testing in develo... |
| EV_11 | self_hosting_support | - | general | self-hosted using Docker on your own infrastructure |  | Langfuse is open source and can be self-hosted using Docker on your own infrastructure. |
| EV_12 | llm_eval_or_observability | - | general | All core platform features and APIs (observability, evaluati... |  | - All core platform features and APIs (observability, evaluation, prompt management, datasets, etc.) |
| EV_13 | self_hosting_support | - | general | Use Docker Compose to run Langfuse locally, or use one of th... |  | Can I self-host Langfuse for free? Yes, Langfuse is open source and you can self-host it for free. Use Docker Compose to run Langfuse locally, or use one of the templates to self-host in production on... |
| EV_14 | license_and_deployment_evidence | - | general | Self-host all core Langfuse features for free without any li... |  | ### Open Source (Free) Self-host all core Langfuse features for free without any limitations. - MIT License - All core platform features and APIs (observability, evaluation, prompt management, dataset... |
| EV_15 | llm_eval_or_observability | - | general | We are building the platform to observe and improve LLM appl... |  | We are building the platform to observe and improve LLM applications. |
| EV_16 | open_source_license | - | general | all of which are now freely available to self-host under the... |  | Newly open sourced features include managed LLM-as-a-judge evaluations, annotation queues, prompt experiments and the playground, all of which are now freely available to self-host under the MIT licen... |
| EV_17 | self_hosting_support | - | general | freely available to self-host |  | Newly open sourced features include managed LLM-as-a-judge evaluations, annotation queues, prompt experiments and the playground, all of which are now freely available to self-host under the MIT licen... |
| EV_18 | license_and_deployment_evidence | - | general | all of which are now freely available to self-host under the... |  | Newly open sourced features include managed LLM-as-a-judge evaluations, annotation queues, prompt experiments and the playground, all of which are now freely available to self-host under the MIT licen... |

Rejected candidates:

- CAND_1 `llm_eval_or_observability` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_2 `open_source_license` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_3 `self_hosting_support` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_4 `license_and_deployment_evidence` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_16 `license_and_deployment_evidence` (verification): verdict=partial: The excerpt supports open-source status and self-hosting, but does not identify a specific license.
- CAND_18 `open_source_license` (verification): verdict=partial: It says evaluations and other capabilities are MIT licensed, but does not establish that the source code is publicly available.

