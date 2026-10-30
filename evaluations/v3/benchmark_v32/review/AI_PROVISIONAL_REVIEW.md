# AI-provisional review materials (V3.2)

> **AI-PROVISIONAL, NOT HUMAN EVALUATION.** These are mechanical checks computed from the run files, plus flags raised by the AI assistant. No score here is a human judgement. Human scores go in `HUMAN_REVIEW_WORKSHEET.csv`.

## Q1 r1 static - `EVAL_Q1_r1_static_20261030T091146_00e434`

- Status `partial`, stop `budget_exhausted`, interval leader `Weaviate` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only); critical criterion operational_effort (weight 5) has no supported score for Weaviate
- Mechanical: 6 cited evidence IDs, **0 invalid**; 6 accepted / 8 rejected (lexical 1, approach-identity 0); single-source cells: Qdrant:deployment_fit, Qdrant:operational_effort, Weaviate:deployment_fit, Weaviate:filtering_capability, Milvus:deployment_fit
- AI-provisional flags: none

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Weaviate:deployment_fit | 2 | general | Weaviate is available as a hosted service, Weaviate Cloud (W... | Strong: a small team can choose between hosted and self-managed options, with local and cloud hosting paths for self-man... | Weaviate is available as a hosted service, Weaviate Cloud (WCD), or as a self managed instance. If you manage your own instance, you can host it locally or with a cloud provider. |
| EV_2 | Qdrant:deployment_fit | 2 | general | Qdrant Cloud, which provides fully managed Qdrant databases | Meets the strong anchor: a small team can choose a fully managed deployment and get started with one-click installation,... | You can set up production with the Qdrant Cloud, which provides fully managed Qdrant databases. It provides horizontal and vertical scaling, one click installation and upgrades, monitoring, logging, a... |
| EV_3 | Qdrant:operational_effort | 2 | managed | one click installation and upgrades, monitoring, logging, as... | Meets the strong anchor for managed deployment: the excerpt describes a fully managed service and provides operational c... | You can set up production with the Qdrant Cloud, which provides fully managed Qdrant databases. It provides horizontal and vertical scaling, one click installation and upgrades, monitoring, logging, a... |
| EV_4 | Qdrant:operational_effort | 1 | self_hosted | Instead you must manage and set this up yourself. | Meets the plausible anchor: self-hosted routine operations involve meaningful work because the team must manage and set ... | While it is possible to deploy Qdrant in a distributed setup with the Helm chart, it does not come with the same level of features for zero-downtime upgrades, up and down-scaling, monitoring, logging,... |
| EV_5 | Weaviate:filtering_capability | 2 | general | Weaviate provides powerful filtered vector search capabiliti... | Strong: the excerpt explicitly describes combining vector search with structured filters to find matching nearest vector... | Weaviate provides powerful filtered vector search capabilities, allowing you to combine vector searches with structured, scalar filters. This enables you to find the closest vectors to a query vector ... |
| EV_6 | Milvus:deployment_fit | 2 | general | Milvus Lite itself or a combination of Milvus Lite and Milvu... | Strong: the excerpt directly recommends deployment options for RAG prototyping and identifies Standalone as appropriate ... | For Quick Prototyping If you would like to quickly build something as a prototype or for learning purposes, such as Retrieval Augmented Generation (RAG) demos, AI chatbots, multi-modality search, Milv... |

Rejected candidates:

- CAND_1 `Qdrant:deployment_fit` (acceptance): verifier attributes the excerpt to 'multiple', not Qdrant
- CAND_2 `Qdrant:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_4 `Weaviate:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_5 `Milvus:operational_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_6 `Milvus:deployment_fit` (acceptance): verifier attributes the excerpt to 'multiple', not Milvus
- CAND_7 `Milvus:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_13 `Milvus:filtering_capability` (verification): verdict=partial: The list includes vector search and metadata filtering, but the excerpt does not identify the three deployment modes by name.
- CAND_14 `Milvus:operational_effort` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q1 r1 v2_policy - `EVAL_Q1_r1_v2_policy_20261030T091146_335404`

- Status `partial`, stop `budget_exhausted`, interval leader `Milvus` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only)
- Mechanical: 5 cited evidence IDs, **0 invalid**; 5 accepted / 13 rejected (lexical 2, approach-identity 0); single-source cells: Weaviate:deployment_fit, Milvus:deployment_fit, Milvus:operational_effort
- AI-provisional flags: none

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Weaviate:deployment_fit | 2 | general | Weaviate is available as a hosted service, Weaviate Cloud (W... | Strong: a small team can choose between hosted and self-managed options, with local and cloud hosting paths for self-man... | Weaviate is available as a hosted service, Weaviate Cloud (WCD), or as a self managed instance. If you manage your own instance, you can host it locally or with a cloud provider. |
| EV_2 | Milvus:deployment_fit | 2 | general | Milvus Lite itself or a combination of Milvus Lite and Milvu... | The excerpt identifies Milvus Lite and Lite plus Standalone as suitable for RAG demos and describes notebook-based rapid... | For Quick Prototyping If you would like to quickly build something as a prototype or for learning purposes, such as Retrieval Augmented Generation (RAG) demos, AI chatbots, multi-modality search, Milv... |
| EV_3 | Milvus:deployment_fit | 2 | general | Milvus Standalone is the best choice | The excerpt recommends Standalone for early-stage production and contrasts it with Kubernetes-based operation, indicatin... | For early-stage production, when the project is still seeking product-market fit and agility is more important than scalability, Milvus Standalone is the best choice. It can still scale up to 100M vec... |
| EV_4 | Milvus:operational_effort | 1 | self_hosted | requiring much less DevOps than maintaining a K8s cluster | This supports the plausible anchor: routine effort is reduced relative to a Kubernetes cluster, but the excerpt does not... | For early-stage production, when the project is still seeking product-market fit and agility is more important than scalability, Milvus Standalone is the best choice. It can still scale up to 100M vec... |
| EV_5 | Milvus:operational_effort | 2 | managed | Zilliz Cloud is hassle-free | The excerpt describes the managed Milvus offering as hassle-free, which supports the strong anchor of little routine ope... | Try Managed Milvus for Free Zilliz Cloud is hassle-free, powered by Milvus and 10x faster. |

Rejected candidates:

- CAND_1 `Qdrant:deployment_fit` (acceptance): verifier attributes the excerpt to 'multiple', not Qdrant
- CAND_2 `Qdrant:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_4 `Weaviate:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_5 `Milvus:operational_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_6 `Milvus:deployment_fit` (acceptance): verifier attributes the excerpt to 'multiple', not Milvus
- CAND_7 `Milvus:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_12 `Weaviate:filtering_capability` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_13 `Weaviate:operational_effort` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_14 `Weaviate:deployment_fit` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_15 `Weaviate:deployment_fit` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_16 `Weaviate:filtering_capability` (acceptance): verifier attributes the excerpt to 'multiple', not Weaviate
- CAND_17 `Weaviate:operational_effort` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_18 `Weaviate:operational_effort` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q1 r1 adaptive - `EVAL_Q1_r1_adaptive_20261030T091146_6f51b6`

- Status `partial`, stop `budget_exhausted`, interval leader `Milvus` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only)
- Mechanical: 8 cited evidence IDs, **0 invalid**; 4 accepted / 9 rejected (lexical 3, approach-identity 0); single-source cells: Weaviate:deployment_fit, Milvus:deployment_fit, Milvus:operational_effort
- AI-provisional flags: none

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Weaviate:deployment_fit | 2 | general | Weaviate is available as a hosted service, Weaviate Cloud (W... | Strong: a small team can choose between hosted and self-managed options, with local and cloud hosting paths for self-man... | Weaviate is available as a hosted service, Weaviate Cloud (WCD), or as a self managed instance. If you manage your own instance, you can host it locally or with a cloud provider. |
| EV_2 | Milvus:deployment_fit | 2 | general | Milvus Standalone is the best choice | Strong: the excerpt identifies a deployment suited to an early-stage project and says it requires much less DevOps than ... | For early-stage production, when the project is still seeking product-market fit and agility is more important than scalability, Milvus Standalone is the best choice. It can still scale up to 100M vec... |
| EV_3 | Milvus:operational_effort | 1 | self_hosted | requiring much less DevOps than maintaining a K8s cluster | Plausible: the excerpt indicates reduced operational work compared with Kubernetes, but does not establish that routine ... | It can still scale up to 100M vectors given enough machine resource, while requiring much less DevOps than maintaining a K8s cluster. |
| EV_4 | Milvus:operational_effort | 2 | managed | Zilliz Cloud is hassle-free, powered by Milvus | Strong: the managed Milvus offering is explicitly described as hassle-free, indicating little operational effort for the... | Try Managed Milvus for Free Zilliz Cloud is hassle-free, powered by Milvus and 10x faster. |

Rejected candidates:

- CAND_1 `Qdrant:deployment_fit` (acceptance): verifier attributes the excerpt to 'multiple', not Qdrant
- CAND_2 `Qdrant:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_4 `Weaviate:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_5 `Milvus:operational_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_6 `Milvus:deployment_fit` (acceptance): verifier attributes the excerpt to 'multiple', not Milvus
- CAND_7 `Milvus:filtering_capability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_8 `Qdrant:operational_effort` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_10 `Milvus:filtering_capability` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_13 `Weaviate:operational_effort` (verification): verdict=partial: It supports lower resource-planning burden for small Weaviate projects, but does not establish low overall operational effort or specifically identify a 

## Q2 r1 static - `EVAL_Q2_r1_static_20261030T091146_522e62`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (None), recommendation `not_applicable`
- Mechanical: 17 cited evidence IDs, **0 invalid**; 28 accepted / 8 rejected (lexical 6, approach-identity 0); single-source cells: none
- AI-provisional flags: one source supports 3+ targets: SRC_6 (4); SRC_7 (3); SRC_8 (3); SRC_9 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | india_headquarters | - | general | Peoplestrong / Exact match / Gurgaon, India✓ HQ recorded |  | / 3 / Peoplestrong / Exact match / Gurgaon, India✓ HQ recorded Sep 29, 2026 |
| EV_2 | b2b_saas | - | general | PeopleStrong is Asia’s leading, and the most comprehensive H... |  | PeopleStrong is Asia’s leading, and the most comprehensive Human Capital Management SaaS platform. |
| EV_3 | hr_technology | - | general | PeopleStrong / 2005 / Gurugram / Enterprise HRMS |  | PeopleStrong / 2005 / Gurugram / Enterprise HRMS / Large organisations with complex HR processes / End-to-end HR lifecycle management including payroll and performance |
| EV_4 | market_positioning | - | general | trusted by 500+ major enterprises |  | PeopleStrong is one of Asia’s most widely adopted HRTech platforms, trusted by 500+ major enterprises and 2 million+ users across India and Asia‐Pacific. Its HR Tech 4.0 suite unifies recruitment, onb... |
| EV_5 | india_headquarters | - | general | Greythr / Exact match / Bangalore, India✓ HQ recorded |  | / 5 / Greythr / Exact match / Bangalore, India✓ HQ recorded Sep 29, 2026 |
| EV_6 | hr_technology | - | general | greytHR / 1994 / Bengaluru / Payroll & HR automation |  | greytHR / 1994 / Bengaluru / Payroll & HR automation / SMEs seeking simple, reliable HR software / Payroll processing, compliance, attendance management |
| EV_7 | market_positioning | - | general | strong adoption among SMEs and mid‐sized businesses |  | greytHR is one of India’s oldest and most trusted HRMS solutions with strong adoption among SMEs and mid‐sized businesses. It’s widely recognised for comprehensive payroll automation, statutory compli... |
| EV_8 | india_headquarters | - | general | Zinghr / Exact match / Mumbai, India✓ HQ recorded |  | / 9 / Zinghr / Exact match / Mumbai, India✓ HQ recorded Sep 29, 2026 |
| EV_9 | market_positioning | - | general | Loved by 1200+ enterprises across Fortune 500s |  | ## Loved by 1200+ enterprises across Fortune 500s |
| EV_10 | hr_technology | - | general | Our comprehensive HR Tech 4.0 platform |  | Our comprehensive HR Tech 4.0 platform encompasses employee lifecycle from hire to exit, including Human Capital Management, Payroll, Talent Acquisition & Management, and Collaboration. |
| EV_11 | market_positioning | - | general | modern talent-focused enterprises |  | We power the momentum of modern talent-focused enterprises We power the experience of your talent workforce, help you take data-driven decisions that impact your people, and bring agility to your busi... |
| EV_12 | india_headquarters | - | general | CoreHRx is a product of THINKNEXT INNOVATIONS PRIVATE LIMITE... |  | CoreHRx is a product of THINKNEXT INNOVATIONS PRIVATE LIMITED, headquartered in Sector 63, Noida, Uttar Pradesh. |
| EV_13 | b2b_saas | - | general | India's fastest-growing HR SaaS product |  | Incubated at IIM Lucknow's EIC and recognised as India's fastest-growing HR SaaS product. We serve 1,000+ organisations across India and 10+ countries — helping HR teams, business owners, and employee... |
| EV_14 | hr_technology | - | general | HR systems should be easy to use |  | HR systems should be easy to use. Every feature is built for the people who actually use it — not just the IT team. |
| EV_15 | market_positioning | - | general | why is HR so complicated for small Indian businesses? |  | CoreHRx was born from a simple frustration — why is HR so complicated for small Indian businesses? We're here to fix that. |
| EV_16 | b2b_saas | - | general | Full-suite HR + payroll + AI. |  | Full-suite HR + payroll + AI. Starting at ₹2,495/month. Payroll, compliance, leave, attendance, ESS, and greytHR NAVOS — all included from ₹2,495/mo for up to 50 employees. No per-module surprises. No... |
| EV_17 | hr_technology | - | general | all in one platform |  | Plan, Recruit, Onboard, Pay, Manage, Upskill, Appraise and Empower your people — all in one platform. |
| EV_18 | market_positioning | - | general | 33,000+ companies run People Operations on greytHR. |  | 33,000+ companies run People Operations on greytHR. Here's why they stay. Full-suite HR and payroll, with an AI agent built in, at a price point that makes the decision easy. |
| EV_19 | hr_technology | - | general | 247HRM runs HR and payroll |  | 247HRM runs HR and payroll for 1500+ companies across 30+ industries. |
| EV_20 | b2b_saas | - | general | Indian businesses paying for 247HRM |  | 1,500+ Active customers Indian businesses paying for 247HRM in May 2026 |
| EV_21 | market_positioning | - | general | From single-location startups to 5,000-employee multi-site g... |  | 247HRM runs payroll and HR for 32 industries. From single-location startups to 5,000-employee multi-site groups across 28 states. |
| EV_22 | b2b_saas | - | general | Launched India's 1st cloud-based HR & Payroll software |  | 2007 Launched India's 1st cloud-based HR & Payroll software across the country. |
| EV_23 | b2b_saas | - | general | at least 1 million businesses around the world having minimu... |  | Similarly, we have created HRMantra as a beautiful piece of art & a work of love after investing tens of thousands of person years since 1999 to make it desirable for at least 1 million businesses aro... |
| EV_24 | market_positioning | - | general | minimum double their features at less than 10% of their cost |  | HRMantra offers 2000 times better cost benefit ratio compared to the world's top 3 rated HRMS by giving minimum double their features at less than 10% of their cost! |
| EV_25 | hr_technology | - | general | HRMantra Human Capital Management software |  | The following are the major features of the HRMantra Human Capital Management software. ## Human Resource Management Create org hierarchies, personalize the home page & set form & report rights for ea... |
| EV_26 | hr_technology | - | general | preboarding processes, are fully automated here |  | ## Recruitment Management All hiring activities, including requisition management, connectivity to job sites, candidate Database, online test, interview, offer management, reference checking & preboar... |
| EV_27 | b2b_saas | - | general | 1000+ businesses choose Timelabs |  | See why 1000+ businesses choose Timelabs to simplify HR, connect everything, and get more done. |
| EV_28 | hr_technology | - | general | Timelabs is an HRMS and HR operating system |  | Timelabs is an HRMS and HR operating system that brings core HR, attendance, payroll, recruitment, employee self service, analytics, and workforce management together on one connected platform. |

Rejected candidates:

- CAND_6 `b2b_saas` (verification): verdict=partial: The excerpt supports greytHR’s HRMS product and the context records its Indian HQ, but neither establishes SaaS status.
- CAND_10 `b2b_saas` (verification): verdict=partial: The excerpt supports a cloud-based enterprise HCM platform, but does not establish SaaS status or the stated SaaS-listing claim.
- CAND_11 `hr_technology` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_13 `india_headquarters` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_14 `b2b_saas` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_32 `b2b_saas` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_35 `market_positioning` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_36 `market_positioning` (acceptance): lexical check: entity name/alias not found in excerpt context

## Q2 r1 v2_policy - `EVAL_Q2_r1_v2_policy_20261030T091146_ef5f40`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (None), recommendation `not_applicable`
- Mechanical: 14 cited evidence IDs, **0 invalid**; 18 accepted / 4 rejected (lexical 1, approach-identity 0); single-source cells: none
- AI-provisional flags: one source supports 3+ targets: SRC_6 (3); SRC_7 (3); SRC_10 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | india_headquarters | - | general | Peoplestrong / Exact match / Gurgaon, India✓ HQ recorded |  | / 3 / Peoplestrong / Exact match / Gurgaon, India✓ HQ recorded Sep 29, 2026 |
| EV_2 | b2b_saas | - | general | PeopleStrong is Asia’s leading, and the most comprehensive H... |  | PeopleStrong is Asia’s leading, and the most comprehensive Human Capital Management SaaS platform. |
| EV_3 | hr_technology | - | general | PeopleStrong / 2005 / Gurugram / Enterprise HRMS |  | PeopleStrong / 2005 / Gurugram / Enterprise HRMS / Large organisations with complex HR processes / End-to-end HR lifecycle management including payroll and performance |
| EV_4 | market_positioning | - | general | trusted by 500+ major enterprises |  | PeopleStrong is one of Asia’s most widely adopted HRTech platforms, trusted by 500+ major enterprises and 2 million+ users across India and Asia‐Pacific. Its HR Tech 4.0 suite unifies recruitment, onb... |
| EV_5 | india_headquarters | - | general | Greythr / Exact match / Bangalore, India✓ HQ recorded |  | / 5 / Greythr / Exact match / Bangalore, India✓ HQ recorded Sep 29, 2026 |
| EV_6 | hr_technology | - | general | greytHR / 1994 / Bengaluru / Payroll & HR automation |  | greytHR / 1994 / Bengaluru / Payroll & HR automation / SMEs seeking simple, reliable HR software / Payroll processing, compliance, attendance management |
| EV_7 | market_positioning | - | general | strong adoption among SMEs and mid‐sized businesses |  | greytHR is one of India’s oldest and most trusted HRMS solutions with strong adoption among SMEs and mid‐sized businesses. It’s widely recognised for comprehensive payroll automation, statutory compli... |
| EV_8 | india_headquarters | - | general | Zinghr / Exact match / Mumbai, India✓ HQ recorded |  | / 9 / Zinghr / Exact match / Mumbai, India✓ HQ recorded Sep 29, 2026 |
| EV_9 | market_positioning | - | general | Loved by 1200+ enterprises across Fortune 500s |  | ## Loved by 1200+ enterprises across Fortune 500s |
| EV_10 | india_headquarters | - | general | ZingHR, legally registered as Cynergis Infotec India Pvt Ltd |  | ZingHR, legally registered as Cynergis Infotec India Pvt Ltd, is an enterprise Human Capital Management (HCM) software company headquartered in Mumbai, India, founded in 2014. |
| EV_11 | b2b_saas | - | general | The business model is enterprise B2B SaaS subscription |  | The business model is enterprise B2B SaaS subscription with annual billing, supplemented by professional services for implementation and support. |
| EV_12 | market_positioning | - | general | ZingHR is an enterprise AI-powered HCM platform |  | ZingHR is an enterprise AI-powered HCM platform providing a unified Hire-to-ReHire suite of 35+ modules covering the full employee lifecycle for large enterprises and Fortune 500 companies across Indi... |
| EV_13 | b2b_saas | - | general | ZingHR platform offers a complete cloud-based, Hire to Rehir... |  | ZingHR platform offers a complete cloud-based, Hire to Rehire, HCM solution, helping enterprises in India build, operate and function key organizational outcomes through innovative HRTech. |
| EV_14 | hr_technology | - | general | ZingHR is an Emerging Technology leader in HR Tech and HRMS |  | ZingHR is an Emerging Technology leader in HR Tech and HRMS |
| EV_15 | market_positioning | - | general | We work with global enterprises and growth bound organizatio... |  | We work with global enterprises and growth bound organizations who believe that a well-designed HRMS fuels better outcomes and growth. |
| EV_16 | b2b_saas | - | general | 33,000+ companies run People Operations on greytHR |  | 33,000+ companies run People Operations on greytHR. Here's why they stay. Full-suite HR and payroll, with an AI agent built in, at a price point that makes the decision easy. |
| EV_17 | hr_technology | - | general | Full Suite HRMS |  | Plan, Recruit, Onboard, Pay, Manage, Upskill, Appraise and Empower your people — all in one platform. Get complex admin tasks done by AI, with simple language commands. |
| EV_18 | market_positioning | - | general | Whether you're replacing spreadsheets or outgrowing your cur... |  | Whether you're replacing spreadsheets or outgrowing your current HRMS, here's what changes on day one. ### Stop stitching together 5 tools for one employee lifecycle Recruitment, onboarding, payroll, ... |

Rejected candidates:

- CAND_6 `b2b_saas` (verification): verdict=partial: The excerpt supports greytHR’s HRMS product and the context records its Indian HQ, but neither establishes SaaS status.
- CAND_10 `b2b_saas` (verification): verdict=partial: The excerpt supports a cloud-based enterprise HCM platform, but does not establish SaaS status or the stated SaaS-listing claim.
- CAND_11 `hr_technology` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_15 `hr_technology` (grounding): excerpt not found in source text

## Q2 r1 adaptive - `EVAL_Q2_r1_adaptive_20261030T091146_23a2c5`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (None), recommendation `not_applicable`
- Mechanical: 14 cited evidence IDs, **0 invalid**; 18 accepted / 4 rejected (lexical 1, approach-identity 0); single-source cells: none
- AI-provisional flags: one source supports 3+ targets: SRC_6 (3); SRC_7 (3); SRC_10 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | india_headquarters | - | general | Peoplestrong / Exact match / Gurgaon, India✓ HQ recorded |  | / 3 / Peoplestrong / Exact match / Gurgaon, India✓ HQ recorded Sep 29, 2026 |
| EV_2 | b2b_saas | - | general | PeopleStrong is Asia’s leading, and the most comprehensive H... |  | PeopleStrong is Asia’s leading, and the most comprehensive Human Capital Management SaaS platform. |
| EV_3 | hr_technology | - | general | PeopleStrong / 2005 / Gurugram / Enterprise HRMS |  | PeopleStrong / 2005 / Gurugram / Enterprise HRMS / Large organisations with complex HR processes / End-to-end HR lifecycle management including payroll and performance |
| EV_4 | market_positioning | - | general | trusted by 500+ major enterprises |  | PeopleStrong is one of Asia’s most widely adopted HRTech platforms, trusted by 500+ major enterprises and 2 million+ users across India and Asia‐Pacific. Its HR Tech 4.0 suite unifies recruitment, onb... |
| EV_5 | india_headquarters | - | general | Greythr / Exact match / Bangalore, India✓ HQ recorded |  | / 5 / Greythr / Exact match / Bangalore, India✓ HQ recorded Sep 29, 2026 |
| EV_6 | hr_technology | - | general | greytHR / 1994 / Bengaluru / Payroll & HR automation |  | greytHR / 1994 / Bengaluru / Payroll & HR automation / SMEs seeking simple, reliable HR software / Payroll processing, compliance, attendance management |
| EV_7 | market_positioning | - | general | strong adoption among SMEs and mid‐sized businesses |  | greytHR is one of India’s oldest and most trusted HRMS solutions with strong adoption among SMEs and mid‐sized businesses. It’s widely recognised for comprehensive payroll automation, statutory compli... |
| EV_8 | india_headquarters | - | general | Zinghr / Exact match / Mumbai, India✓ HQ recorded |  | / 9 / Zinghr / Exact match / Mumbai, India✓ HQ recorded Sep 29, 2026 |
| EV_9 | market_positioning | - | general | Loved by 1200+ enterprises across Fortune 500s |  | ## Loved by 1200+ enterprises across Fortune 500s |
| EV_10 | india_headquarters | - | general | ZingHR, legally registered as Cynergis Infotec India Pvt Ltd |  | ZingHR, legally registered as Cynergis Infotec India Pvt Ltd, is an enterprise Human Capital Management (HCM) software company headquartered in Mumbai, India, founded in 2014. |
| EV_11 | b2b_saas | - | general | The business model is enterprise B2B SaaS subscription |  | The business model is enterprise B2B SaaS subscription with annual billing, supplemented by professional services for implementation and support. |
| EV_12 | market_positioning | - | general | ZingHR is an enterprise AI-powered HCM platform |  | ZingHR is an enterprise AI-powered HCM platform providing a unified Hire-to-ReHire suite of 35+ modules covering the full employee lifecycle for large enterprises and Fortune 500 companies across Indi... |
| EV_13 | b2b_saas | - | general | ZingHR platform offers a complete cloud-based, Hire to Rehir... |  | ZingHR platform offers a complete cloud-based, Hire to Rehire, HCM solution, helping enterprises in India build, operate and function key organizational outcomes through innovative HRTech. |
| EV_14 | hr_technology | - | general | ZingHR is an Emerging Technology leader in HR Tech and HRMS |  | ZingHR is an Emerging Technology leader in HR Tech and HRMS |
| EV_15 | market_positioning | - | general | We work with global enterprises and growth bound organizatio... |  | We work with global enterprises and growth bound organizations who believe that a well-designed HRMS fuels better outcomes and growth. |
| EV_16 | b2b_saas | - | general | 33,000+ companies run People Operations on greytHR |  | 33,000+ companies run People Operations on greytHR. Here's why they stay. Full-suite HR and payroll, with an AI agent built in, at a price point that makes the decision easy. |
| EV_17 | hr_technology | - | general | Full Suite HRMS |  | Plan, Recruit, Onboard, Pay, Manage, Upskill, Appraise and Empower your people — all in one platform. Get complex admin tasks done by AI, with simple language commands. |
| EV_18 | market_positioning | - | general | Whether you're replacing spreadsheets or outgrowing your cur... |  | Whether you're replacing spreadsheets or outgrowing your current HRMS, here's what changes on day one. ### Stop stitching together 5 tools for one employee lifecycle Recruitment, onboarding, payroll, ... |

Rejected candidates:

- CAND_6 `b2b_saas` (verification): verdict=partial: The excerpt supports greytHR’s HRMS product and the context records its Indian HQ, but neither establishes SaaS status.
- CAND_10 `b2b_saas` (verification): verdict=partial: The excerpt supports a cloud-based enterprise HCM platform, but does not establish SaaS status or the stated SaaS-listing claim.
- CAND_11 `hr_technology` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_15 `hr_technology` (grounding): excerpt not found in source text

## Q3 r1 static - `EVAL_Q3_r1_static_20261030T091146_5ce955`

- Status `partial`, stop `budget_exhausted`, interval leader `Single-agent support automation` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only); Single-agent support automation:total_cost includes cost evidence whose dimension (infrastructure, labour, total, ...) cannot be determined
- Mechanical: 8 cited evidence IDs, **0 invalid**; 4 accepted / 14 rejected (lexical 0, approach-identity 0); single-source cells: Single-agent support automation:implementation_complexity, Single-agent support automation:total_cost, Single-agent support automation:safeguards, Multi-agent support automation:safeguards
- AI-provisional flags: one source supports 3+ targets: SRC_1 (4)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Single-agent support automation:implementation_complexity | 2 | general | Single-agent architectures | This meets the strong anchor: the source explicitly says implementation and governance are simplified and that the desig... | Single-agent architectures consolidate logic, context, and tool execution into one entity. This consolidation reduces design complexity, simplifies implementation, and streamlines governance. Organiza... |
| EV_2 | Single-agent support automation:total_cost | 1 | general | Single-agent designs reduce token usage and API calls | This supports the plausible anchor: usage-related costs can be lower, but the source recommends validating the savings, ... | Single-agent designs reduce token usage and API calls by maintaining context within one entity. Validate cost benefits through prototyping before adding orchestration overhead. |
| EV_3 | Single-agent support automation:safeguards | 1 | general | workflow automation around single agents | This meets the plausible anchor: practical approval and audit controls are available, but the excerpt says they are impl... | Governance and compliance. Implement logging, approval gates, and audit trails through workflow capabilities. These controls satisfy regulatory requirements and provide operational visibility into age... |
| EV_4 | Multi-agent support automation:safeguards | 1 | general | Build multiple agents when regulations or policies mandate s... | This supports the plausible anchor by describing data isolation and least-privilege boundaries, but it does not show app... | Build multiple agents when regulations or policies mandate strict data isolation. Different security classifications need independent processing environments that single agents can't provide. This lea... |

Rejected candidates:

- CAND_3 `Single-agent support automation:reliability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_5 `Multi-agent support automation:implementation_complexity` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_6 `Multi-agent support automation:total_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_7 `Multi-agent support automation:reliability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_14 `Multi-agent support automation:reliability` (grounding): excerpt not found in source text
- CAND_9 `Single-agent support automation:implementation_complexity` (verification): verdict=partial: The guide calls the setup fast to build and iterate, but does not address integration, monitoring, or ongoing maintenance.
- CAND_10 `Single-agent support automation:total_cost` (verification): verdict=partial: It supports avoiding handoff maintenance, but provides no basis for judging total implementation and operating costs.
- CAND_11 `Single-agent support automation:reliability` (verification): verdict=partial: The excerpt identifies easier testing and a reliability drawback, but does not establish overall support accuracy or recovery performance.
- CAND_12 `Multi-agent support automation:implementation_complexity` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_13 `Multi-agent support automation:total_cost` (verification): verdict=partial: It identifies maintenance and debuggability as added cost drivers, but gives no overall cost estimate or evidence for a low-cost score.
- CAND_15 `Multi-agent support automation:safeguards` (verification): verdict=partial: It describes sub-agent capability isolation, but does not establish the broader safeguards or auditability in the criterion.
- CAND_16 `Single-agent support automation:implementation_complexity` (grounding): excerpt not found in source text
- CAND_18 `Single-agent support automation:safeguards` (grounding): excerpt not found in source text
- CAND_17 `Single-agent support automation:reliability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q3 r1 v2_policy - `EVAL_Q3_r1_v2_policy_20261030T091146_ec3f70`

- Status `partial`, stop `budget_exhausted`, interval leader `Single-agent support automation` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only); Single-agent support automation:total_cost includes cost evidence whose dimension (infrastructure, labour, total, ...) cannot be determined
- Mechanical: 12 cited evidence IDs, **0 invalid**; 9 accepted / 16 rejected (lexical 0, approach-identity 2); single-source cells: Single-agent support automation:implementation_complexity, Single-agent support automation:total_cost, Single-agent support automation:safeguards, Multi-agent support automation:total_cost
- AI-provisional flags: one source supports 3+ targets: SRC_1 (4); SRC_5 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Single-agent support automation:implementation_complexity | 2 | general | Single-agent architectures | This meets the strong anchor: the source explicitly says implementation and governance are simplified and that the desig... | Single-agent architectures consolidate logic, context, and tool execution into one entity. This consolidation reduces design complexity, simplifies implementation, and streamlines governance. Organiza... |
| EV_2 | Single-agent support automation:total_cost | 1 | general | Single-agent designs reduce token usage and API calls | This supports the plausible anchor: usage-related costs can be lower, but the source recommends validating the savings, ... | Single-agent designs reduce token usage and API calls by maintaining context within one entity. Validate cost benefits through prototyping before adding orchestration overhead. |
| EV_3 | Single-agent support automation:safeguards | 1 | general | workflow automation around single agents | This meets the plausible anchor: practical approval and audit controls are available, but the excerpt says they are impl... | Governance and compliance. Implement logging, approval gates, and audit trails through workflow capabilities. These controls satisfy regulatory requirements and provide operational visibility into age... |
| EV_4 | Multi-agent support automation:safeguards | 1 | general | Build multiple agents when regulations or policies mandate s... | This supports the plausible anchor by describing data isolation and least-privilege boundaries, but it does not show app... | Build multiple agents when regulations or policies mandate strict data isolation. Different security classifications need independent processing environments that single agents can't provide. This lea... |
| EV_5 | Single-agent support automation:implementation_complexity | 2 | general | single-agent architecture | This directly supports the strong anchor: implementation and maintenance are described as easier, with no additional orc... | It's easier to design, implement, test, and maintain. |
| EV_6 | Single-agent support automation:total_cost | 1 | general | no need for inter-agent communication | This supports a plausible cost advantage through lower resource overhead, but does not establish total implementation an... | There's no need for inter-agent communication, so computational and networking overhead is lower. |
| EV_7 | Multi-agent support automation:total_cost | 1 | general | Multiple agents can use more computing and communication res... | This indicates added resource costs, but does not quantify them or establish that they are uncontrolled; it supports a p... | Higher resource consumption/ Multiple agents can use more computing and communication resources. |
| EV_8 | Multi-agent support automation:total_cost | 1 | general | For teams running thousands of tasks per day, they are a rea... | Plausible: costs may be minor at low volume but become a real budget line at high volume, so they depend on usage and re... | For low-volume prototypes, these differences are trivial. For teams running thousands of tasks per day, they are a real budget line. At 100,000 research tasks per month, the difference between LangGra... |
| EV_9 | Multi-agent support automation:safeguards | 1 | general | human-in-the-loop interrupts | Plausible: native human-in-the-loop support and per-step inspection enable practical review and auditability, but the ex... | LangGraph’s native support for state persistence (via checkpointers), human-in-the-loop interrupts, and cyclic graphs means you are not bolting on these capabilities from third-party packages. The deb... |

Rejected candidates:

- CAND_3 `Single-agent support automation:reliability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_5 `Multi-agent support automation:implementation_complexity` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_6 `Multi-agent support automation:total_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_7 `Multi-agent support automation:reliability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_11 `Single-agent support automation:reliability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_12 `Multi-agent support automation:implementation_complexity` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_14 `Multi-agent support automation:total_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_15 `Multi-agent support automation:reliability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_16 `Multi-agent support automation:reliability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_17 `Multi-agent support automation:safeguards` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_18 `Multi-agent support automation:safeguards` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_19 `Single-agent support automation:implementation_complexity` (acceptance): approach identity: excerpt describes several alternatives without isolating this one
- CAND_20 `Multi-agent support automation:implementation_complexity` (acceptance): approach identity: excerpt describes several alternatives without isolating this one
- CAND_21 `Multi-agent support automation:implementation_complexity` (verification): verdict=partial: It supports the stated learning and integration effort for LangGraph, but does not tie that workflow to multi-agent support automation.
- CAND_23 `Multi-agent support automation:reliability` (verification): verdict=partial: The guidance names pause, resume, and recovery needs, but does not establish that the approach provides those capabilities or reliable support outcomes.
- CAND_25 `Multi-agent support automation:reliability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q3 r1 adaptive - `EVAL_Q3_r1_adaptive_20261030T091146_0dff60`

- Status `partial`, stop `budget_exhausted`, interval leader `Single-agent support automation` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only); differentiating cells lack strong support (single source or non-official): Single-agent support automation:implementation_complexity, Multi-agent support automation:implementation_complexity; Single-agent support automation:total_cost includes cost evidence whose dimension (infrastructure, labour, total, ...) cannot be determined
- Mechanical: 19 cited evidence IDs, **0 invalid**; 17 accepted / 12 rejected (lexical 0, approach-identity 1); single-source cells: Single-agent support automation:implementation_complexity, Single-agent support automation:total_cost, Single-agent support automation:reliability, Single-agent support automation:safeguards, Multi-agent support automation:implementation_complexity, Multi-agent support automation:total_cost
- AI-provisional flags: one source supports 3+ targets: SRC_1 (4); SRC_7 (7); SRC_8 (4)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Single-agent support automation:implementation_complexity | 2 | general | Single-agent architectures | This meets the strong anchor: the source explicitly says implementation and governance are simplified and that the desig... | Single-agent architectures consolidate logic, context, and tool execution into one entity. This consolidation reduces design complexity, simplifies implementation, and streamlines governance. Organiza... |
| EV_2 | Single-agent support automation:total_cost | 1 | general | Single-agent designs reduce token usage and API calls | This supports the plausible anchor: usage-related costs can be lower, but the source recommends validating the savings, ... | Single-agent designs reduce token usage and API calls by maintaining context within one entity. Validate cost benefits through prototyping before adding orchestration overhead. |
| EV_3 | Single-agent support automation:safeguards | 1 | general | workflow automation around single agents | This meets the plausible anchor: practical approval and audit controls are available, but the excerpt says they are impl... | Governance and compliance. Implement logging, approval gates, and audit trails through workflow capabilities. These controls satisfy regulatory requirements and provide operational visibility into age... |
| EV_4 | Multi-agent support automation:safeguards | 1 | general | Build multiple agents when regulations or policies mandate s... | This supports the plausible anchor by describing data isolation and least-privilege boundaries, but it does not show app... | Build multiple agents when regulations or policies mandate strict data isolation. Different security classifications need independent processing environments that single agents can't provide. This lea... |
| EV_5 | Single-agent support automation:reliability | 1 | general | constrain the agent’s autonomy | Plausible: the excerpt describes improved reliability for constrained tasks, with resolution rates potentially in the hi... | That said, the results suggest that if we constrain the agent’s autonomy and frame each task as a simple, well-structured instruction—minimising ambiguity and room for interpretation—we might be able ... |
| EV_6 | Single-agent support automation:implementation_complexity | 2 | general | single-agent architecture | Strong anchor: the excerpt directly describes lower design, testing, and maintenance effort. | It's easier to design, implement, test, and maintain. |
| EV_7 | Single-agent support automation:total_cost | 1 | general | single-agent architecture | Plausible anchor: it identifies a source of lower operating overhead, but does not establish total cost or cost predicta... | There's no need for inter-agent communication, so computational and networking overhead is lower. |
| EV_8 | Single-agent support automation:reliability | 1 | general | single-agent architecture | Plausible anchor: fewer unexpected interactions may support consistency, but the excerpt does not establish failure reco... | There are fewer sources of randomness and unexpected interactions. |
| EV_9 | Multi-agent support automation:implementation_complexity | 1 | general | challenges in multi-agent architectures | Plausible anchor: these are meaningful integration and operational challenges, but the excerpt does not show that they e... | There are challenges in multi-agent architectures, though. For example, it can be complex to share context between agents, and to coordinate and delegate between agents. Also, small changes to orchest... |
| EV_10 | Multi-agent support automation:implementation_complexity | 1 | general | We built the orchestrator before the specialists were stable... | Plausible anchor: the excerpt shows ongoing integration and debugging effort, without establishing that the effort is be... | We built the orchestrator before the specialists were stable. When a specialist regresses, the orchestrator inherits the regression and it's hard to localize. |
| EV_11 | Multi-agent support automation:total_cost | 1 | general | Drawbacks of multi-agent architecture | Plausible anchor: the excerpt identifies potential additional operating costs, but gives no dollar amount or evidence th... | Multiple agents can use more computing and communication resources. |
| EV_12 | Multi-agent support automation:total_cost | 1 | general | specialists running in parallel dominate | Plausible anchor: costs depend on multiple model calls and can require active optimization, although the excerpt describ... | The triage call is the cheapest; specialists running in parallel dominate; the reviewer is a small overhead. Caching account-context templates and specialist prompts cut cost by another ~30%. |
| EV_13 | Multi-agent support automation:reliability | 1 | general | handle individual agent failures | Plausible anchor: the excerpt supports a fault-tolerance benefit, but does not establish failure detection, recovery pro... | The system can handle individual agent failures, so it's more robust. |
| EV_14 | Multi-agent support automation:reliability | 2 | general | Reviewer failures send the ticket to the human queue | Strong anchor: the excerpt describes a failure check and an explicit human recovery path for failed drafts. | Reviewer failures send the ticket to the human queue with the draft attached for editing. Reviewer passes send the draft into the user-facing reply pipeline. |
| EV_15 | Multi-agent support automation:safeguards | 1 | general | Agent autonomy is limited by roles, permissions | Plausible anchor: the excerpt describes practical permission and domain boundaries, but not approval gates, audit trails... | Agent autonomy is limited by roles, permissions, and assigned domains or tasks. |
| EV_16 | Multi-agent support automation:safeguards | 1 | general | Each agent has the minimum tools it needs. | Plausible anchor: the excerpt demonstrates least-privilege tool and data boundaries, but does not establish audit trails... | Strict tool boundaries. Each agent has the minimum tools it needs. Billing specialist cannot reset an integration. Integration specialist cannot view invoice line items. |
| EV_17 | Multi-agent support automation:safeguards | 1 | general | The agents propose; the user confirms; code executes. | Plausible anchor: the excerpt supports an explicit approval gate, but does not establish auditability or the full set of... | The agents propose; the user confirms; code executes. This is the single most important design rule in the system. |

Rejected candidates:

- CAND_3 `Single-agent support automation:reliability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_5 `Multi-agent support automation:implementation_complexity` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_6 `Multi-agent support automation:total_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_7 `Multi-agent support automation:reliability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_22 `Single-agent support automation:implementation_complexity` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_23 `Single-agent support automation:total_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_24 `Single-agent support automation:reliability` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_25 `Single-agent support automation:safeguards` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_26 `Multi-agent support automation:implementation_complexity` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_27 `Multi-agent support automation:total_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_28 `Multi-agent support automation:reliability` (acceptance): approach identity: identification quote missing or not found verbatim in the source
- CAND_29 `Multi-agent support automation:safeguards` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q4 r1 static - `EVAL_Q4_r1_static_20261030T091146_dd8873`

- Status `partial`, stop `budget_exhausted`, interval leader `Hybrid layered memory` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only); differentiating cells lack strong support (single source or non-official): Hybrid layered memory:privacy_protection, Session-only memory:privacy_protection, Summarized customer-profile memory:privacy_protection
- Mechanical: 13 cited evidence IDs, **0 invalid**; 14 accepted / 6 rejected (lexical 0, approach-identity 1); single-source cells: Session-only memory:privacy_protection, Persistent conversation-log retrieval:retention_and_deletion_control, Summarized customer-profile memory:privacy_protection, Hybrid layered memory:privacy_protection, Hybrid layered memory:retention_and_deletion_control
- AI-provisional flags: one source supports 3+ targets: SRC_1 (4); SRC_4 (3); SRC_6 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Session-only memory:retrieval_effectiveness | 1 | general | Within one active conversation | Plausible: the excerpt describes useful recall within the active session, but this approach does not provide cross-sessi... | Within one active conversation, the agent should remember everything the customer has already told it, without exception. Asking a customer for their order number twice in the same conversation is the... |
| EV_2 | Session-only memory:privacy_protection | 1 | general | Short-term memory, the context of the current conversation | Plausible: the excerpt indicates limited persistence, but does not establish enforceable controls over what information ... | Short-term memory, the context of the current conversation, is rarely the source of privacy problems, because it lives and dies with the conversation and rarely persists in a form a customer would thi... |
| EV_3 | Persistent conversation-log retrieval:retrieval_effectiveness | 1 | general | keeping the history outside the conversation and loading onl... | Plausible: the excerpt describes relevant, selective retrieval for a current ticket, but does not establish reliable rec... | Memory solves both by keeping the history outside the conversation and loading only what the current ticket needs. |
| EV_4 | Persistent conversation-log retrieval:retention_and_deletion_control | 1 | general | treat raw transcripts and interaction records as transient | Plausible: the excerpt recommends a retention limit, but does not establish reliable correction, expiration, and deletio... | First, treat raw transcripts and interaction records as transient. Don't persist them beyond your operational retention window. If you're keeping voice call recordings for 30 days for quality purposes... |
| EV_5 | Summarized customer-profile memory:retrieval_effectiveness | 1 | general | A short, structured summary is faster and more reliable for ... | Plausible: summaries can provide useful context more reliably than long transcripts, but the excerpt does not address ho... | This preference for summaries over transcripts also has a practical retrieval benefit, separate from the privacy argument. A short, structured summary is faster and more reliable for a model to reason... |
| EV_6 | Summarized customer-profile memory:privacy_protection | 1 | general | without retaining every word of a conversation | Plausible: the excerpt describes data minimization through summaries, but does not provide clear enforceable access or s... | A useful rule of thumb is to prefer a compact, structured summary over a raw transcript when carrying memory across sessions. A summary that says the customer had a billing dispute in March, resolved ... |
| EV_7 | Summarized customer-profile memory:retention_and_deletion_control | 1 | general | the difference between "the current value" and "what was tru... | Plausible: the excerpt addresses correction and historical values, but does not describe a dependable expiration or dele... | Handle corrections and stale information If a customer changes their contact preference from phone to email, the agent should use email from now on. It may still need the earlier preference when expla... |
| EV_8 | Hybrid layered memory:privacy_protection | 2 | general | tags each memory unit with its source channel, its sensitivi... | Strong: the excerpt describes differentiated policies and explicit metadata for sensitivity, retention, and consent, sup... | The right approach is channel-aware memory scoping: different memory policies for different interaction types, with clear disclosure at the point of interaction about what will and won't be retained a... |
| EV_9 | Hybrid layered memory:retention_and_deletion_control | 1 | general | Define retention separately for transcripts, summaries, extr... | Plausible: the excerpt describes layer-specific retention and a deletion workflow, while noting that deletion from searc... | Define retention separately for transcripts, summaries, extracted facts, logs and backups. A deletion workflow should cover the copies your system actually keeps. Removing a result from search doesn't... |
| EV_10 | Session-only memory:retrieval_effectiveness | 1 | general | In-Context Windowing (ICW) | Plausible: the approach can use recent interaction context, but its recency window prevents reliable recall of older ses... | In-Context Windowing (ICW) : retains the most recent $k$ tokens in the context window, discarding older turns via a sliding window or recency-based truncation Beltagy et al. (2020). |
| EV_11 | Persistent conversation-log retrieval:retrieval_effectiveness | 2 | general | EKV dominates on every quality axis | Strong: the excerpt reports the highest macro-averaged Recall@5 and a measurable long-range recall result where other li... | Our measured results show that (1) EKV dominates on every quality axis, achieving the highest macro-averaged Recall@5 ($0.792$), MRR ($0.677$), Answer F1 ($0.156$), and Faithfulness ($0.354$); (2) lon... |
| EV_12 | Summarized customer-profile memory:retrieval_effectiveness | 1 | general | CBS is the clear runner-up on retrieval (macro $0.556$) | Plausible: the reported retrieval result indicates useful recall from compressed context, but it is below the leading st... | (3) CBS is the clear runner-up on retrieval (macro $0.556$) by inheriting the provenance of the turns it compresses; |
| EV_13 | Summarized customer-profile memory:retention_and_deletion_control | 1 | general | "consolidated": { "ttl_days": 730, "description": "Merged su... | This supports the plausible anchor: retention periods are defined by memory category, but this excerpt alone does not es... | Different memory categories may have different retention periods based on their utility and sensitivity. `RETENTION_POLICIES = { "episodic": { "ttl_days": 180, "description": "Specific interaction rec... |
| EV_14 | Summarized customer-profile memory:retention_and_deletion_control | 1 | general | Run an expiration job daily that identifies and deletes memo... | This supports the plausible anchor through an automated expiration process and broad deletion instructions. The excerpt ... | Run an expiration job daily that identifies and deletes memories past their TTL. The expiration process must be the same as a customer deletion request: remove the content, the embeddings, the graph c... |

Rejected candidates:

- CAND_3 `Session-only memory:retention_and_deletion_control` (verification): verdict=partial: It specifies session duration and automatic disposal, but does not establish correction, deletion, or a complete lifecycle process.
- CAND_5 `Persistent conversation-log retrieval:privacy_protection` (acceptance): approach identity: excerpt describes several alternatives without isolating this one
- CAND_10 `Hybrid layered memory:retrieval_effectiveness` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_14 `Session-only memory:retention_and_deletion_control` (verification): verdict=partial: Automatic removal of older context provides a retention limit, but the excerpt does not establish defined retention periods or correction and deletion pr
- CAND_16 `Persistent conversation-log retrieval:retention_and_deletion_control` (verification): verdict=partial: The cap and FIFO eviction provide some retention control, but do not demonstrate correction or dependable deletion processes.
- CAND_18 `Persistent conversation-log retrieval:privacy_protection` (verification): verdict=irrelevant: The excerpt describes general privacy-defense limitations but does not connect them to persistent conversation-log retrieval or stored memories.

## Q4 r1 v2_policy - `EVAL_Q4_r1_v2_policy_20261030T091146_286248`

- Status `partial`, stop `budget_exhausted`, interval leader `Hybrid layered memory` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only); differentiating cells lack strong support (single source or non-official): Hybrid layered memory:privacy_protection, Session-only memory:privacy_protection, Persistent conversation-log retrieval:privacy_protection, Summarized customer-profile memory:privacy_protection
- Mechanical: 10 cited evidence IDs, **0 invalid**; 10 accepted / 4 rejected (lexical 0, approach-identity 1); single-source cells: Session-only memory:retrieval_effectiveness, Session-only memory:privacy_protection, Persistent conversation-log retrieval:retrieval_effectiveness, Persistent conversation-log retrieval:privacy_protection, Persistent conversation-log retrieval:retention_and_deletion_control, Summarized customer-profile memory:retrieval_effectiveness, Summarized customer-profile memory:privacy_protection, Summarized customer-profile memory:retention_and_deletion_control, Hybrid layered memory:privacy_protection, Hybrid layered memory:retention_and_deletion_control
- AI-provisional flags: one source supports 3+ targets: SRC_1 (4); SRC_4 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Session-only memory:retrieval_effectiveness | 1 | general | Within one active conversation | Plausible: the excerpt describes useful recall within the active session, but this approach does not provide cross-sessi... | Within one active conversation, the agent should remember everything the customer has already told it, without exception. Asking a customer for their order number twice in the same conversation is the... |
| EV_2 | Session-only memory:privacy_protection | 1 | general | Short-term memory, the context of the current conversation | Plausible: the excerpt indicates limited persistence, but does not establish enforceable controls over what information ... | Short-term memory, the context of the current conversation, is rarely the source of privacy problems, because it lives and dies with the conversation and rarely persists in a form a customer would thi... |
| EV_3 | Persistent conversation-log retrieval:retrieval_effectiveness | 1 | general | keeping the history outside the conversation and loading onl... | Plausible: the excerpt describes relevant, selective retrieval for a current ticket, but does not establish reliable rec... | Memory solves both by keeping the history outside the conversation and loading only what the current ticket needs. |
| EV_4 | Persistent conversation-log retrieval:retention_and_deletion_control | 1 | general | treat raw transcripts and interaction records as transient | Plausible: the excerpt recommends a retention limit, but does not establish reliable correction, expiration, and deletio... | First, treat raw transcripts and interaction records as transient. Don't persist them beyond your operational retention window. If you're keeping voice call recordings for 30 days for quality purposes... |
| EV_5 | Summarized customer-profile memory:retrieval_effectiveness | 1 | general | A short, structured summary is faster and more reliable for ... | Plausible: summaries can provide useful context more reliably than long transcripts, but the excerpt does not address ho... | This preference for summaries over transcripts also has a practical retrieval benefit, separate from the privacy argument. A short, structured summary is faster and more reliable for a model to reason... |
| EV_6 | Summarized customer-profile memory:privacy_protection | 1 | general | without retaining every word of a conversation | Plausible: the excerpt describes data minimization through summaries, but does not provide clear enforceable access or s... | A useful rule of thumb is to prefer a compact, structured summary over a raw transcript when carrying memory across sessions. A summary that says the customer had a billing dispute in March, resolved ... |
| EV_7 | Summarized customer-profile memory:retention_and_deletion_control | 1 | general | the difference between "the current value" and "what was tru... | Plausible: the excerpt addresses correction and historical values, but does not describe a dependable expiration or dele... | Handle corrections and stale information If a customer changes their contact preference from phone to email, the agent should use email from now on. It may still need the earlier preference when expla... |
| EV_8 | Hybrid layered memory:privacy_protection | 2 | general | tags each memory unit with its source channel, its sensitivi... | Strong: the excerpt describes differentiated policies and explicit metadata for sensitivity, retention, and consent, sup... | The right approach is channel-aware memory scoping: different memory policies for different interaction types, with clear disclosure at the point of interaction about what will and won't be retained a... |
| EV_9 | Hybrid layered memory:retention_and_deletion_control | 1 | general | Define retention separately for transcripts, summaries, extr... | Plausible: the excerpt describes layer-specific retention and a deletion workflow, while noting that deletion from searc... | Define retention separately for transcripts, summaries, extracted facts, logs and backups. A deletion workflow should cover the copies your system actually keeps. Removing a result from search doesn't... |
| EV_10 | Persistent conversation-log retrieval:privacy_protection | 0 | general | extracted from users' dialogues | The excerpt describes persistent dialogue-derived memories being reused and says users may not understand what is collec... | The "black box" nature of LLMs exacerbates this issue, leaving users unable to fully understand the scope of data being collected in memories or the associated privacy risks. Specifically, for RAG-bas... |

Rejected candidates:

- CAND_3 `Session-only memory:retention_and_deletion_control` (verification): verdict=partial: It specifies session duration and automatic disposal, but does not establish correction, deletion, or a complete lifecycle process.
- CAND_5 `Persistent conversation-log retrieval:privacy_protection` (acceptance): approach identity: excerpt describes several alternatives without isolating this one
- CAND_10 `Hybrid layered memory:retrieval_effectiveness` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_13 `Hybrid layered memory:retrieval_effectiveness` (verification): verdict=partial: It supports the temporal-semantic organization and query-dependent retrieval claim, but does not establish the session-plus-persistent layers that define

## Q4 r1 adaptive - `EVAL_Q4_r1_adaptive_20261030T091146_eb62c4`

- Status `partial`, stop `budget_exhausted`, interval leader `Hybrid layered memory` (provisional), recommendation `withheld` - withheld: score intervals overlap (provisional leader only); differentiating cells lack strong support (single source or non-official): Hybrid layered memory:privacy_protection, Session-only memory:privacy_protection, Persistent conversation-log retrieval:privacy_protection, Summarized customer-profile memory:privacy_protection
- Mechanical: 10 cited evidence IDs, **0 invalid**; 10 accepted / 5 rejected (lexical 0, approach-identity 1); single-source cells: Session-only memory:retrieval_effectiveness, Session-only memory:privacy_protection, Persistent conversation-log retrieval:retrieval_effectiveness, Persistent conversation-log retrieval:privacy_protection, Persistent conversation-log retrieval:retention_and_deletion_control, Summarized customer-profile memory:retrieval_effectiveness, Summarized customer-profile memory:privacy_protection, Summarized customer-profile memory:retention_and_deletion_control, Hybrid layered memory:privacy_protection, Hybrid layered memory:retention_and_deletion_control
- AI-provisional flags: one source supports 3+ targets: SRC_1 (4); SRC_4 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Session-only memory:retrieval_effectiveness | 1 | general | Within one active conversation | Plausible: the excerpt describes useful recall within the active session, but this approach does not provide cross-sessi... | Within one active conversation, the agent should remember everything the customer has already told it, without exception. Asking a customer for their order number twice in the same conversation is the... |
| EV_2 | Session-only memory:privacy_protection | 1 | general | Short-term memory, the context of the current conversation | Plausible: the excerpt indicates limited persistence, but does not establish enforceable controls over what information ... | Short-term memory, the context of the current conversation, is rarely the source of privacy problems, because it lives and dies with the conversation and rarely persists in a form a customer would thi... |
| EV_3 | Persistent conversation-log retrieval:retrieval_effectiveness | 1 | general | keeping the history outside the conversation and loading onl... | Plausible: the excerpt describes relevant, selective retrieval for a current ticket, but does not establish reliable rec... | Memory solves both by keeping the history outside the conversation and loading only what the current ticket needs. |
| EV_4 | Persistent conversation-log retrieval:retention_and_deletion_control | 1 | general | treat raw transcripts and interaction records as transient | Plausible: the excerpt recommends a retention limit, but does not establish reliable correction, expiration, and deletio... | First, treat raw transcripts and interaction records as transient. Don't persist them beyond your operational retention window. If you're keeping voice call recordings for 30 days for quality purposes... |
| EV_5 | Summarized customer-profile memory:retrieval_effectiveness | 1 | general | A short, structured summary is faster and more reliable for ... | Plausible: summaries can provide useful context more reliably than long transcripts, but the excerpt does not address ho... | This preference for summaries over transcripts also has a practical retrieval benefit, separate from the privacy argument. A short, structured summary is faster and more reliable for a model to reason... |
| EV_6 | Summarized customer-profile memory:privacy_protection | 1 | general | without retaining every word of a conversation | Plausible: the excerpt describes data minimization through summaries, but does not provide clear enforceable access or s... | A useful rule of thumb is to prefer a compact, structured summary over a raw transcript when carrying memory across sessions. A summary that says the customer had a billing dispute in March, resolved ... |
| EV_7 | Summarized customer-profile memory:retention_and_deletion_control | 1 | general | the difference between "the current value" and "what was tru... | Plausible: the excerpt addresses correction and historical values, but does not describe a dependable expiration or dele... | Handle corrections and stale information If a customer changes their contact preference from phone to email, the agent should use email from now on. It may still need the earlier preference when expla... |
| EV_8 | Hybrid layered memory:privacy_protection | 2 | general | tags each memory unit with its source channel, its sensitivi... | Strong: the excerpt describes differentiated policies and explicit metadata for sensitivity, retention, and consent, sup... | The right approach is channel-aware memory scoping: different memory policies for different interaction types, with clear disclosure at the point of interaction about what will and won't be retained a... |
| EV_9 | Hybrid layered memory:retention_and_deletion_control | 1 | general | Define retention separately for transcripts, summaries, extr... | Plausible: the excerpt describes layer-specific retention and a deletion workflow, while noting that deletion from searc... | Define retention separately for transcripts, summaries, extracted facts, logs and backups. A deletion workflow should cover the copies your system actually keeps. Removing a result from search doesn't... |
| EV_10 | Persistent conversation-log retrieval:privacy_protection | 0 | general | RAG-based memories, they were usually extracted from users' ... | The excerpt describes persistent dialogue-derived memories being reused and says users may not understand what is collec... | The "black box" nature of LLMs exacerbates this issue, leaving users unable to fully understand the scope of data being collected in memories or the associated privacy risks. Specifically, for RAG-bas... |

Rejected candidates:

- CAND_3 `Session-only memory:retention_and_deletion_control` (verification): verdict=partial: It specifies session duration and automatic disposal, but does not establish correction, deletion, or a complete lifecycle process.
- CAND_5 `Persistent conversation-log retrieval:privacy_protection` (acceptance): approach identity: excerpt describes several alternatives without isolating this one
- CAND_10 `Hybrid layered memory:retrieval_effectiveness` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_13 `Hybrid layered memory:retrieval_effectiveness` (verification): verdict=partial: It supports the temporal-semantic organization and query-dependent retrieval claim, but does not establish the session-plus-persistent layers that define
- CAND_14 `Session-only memory:retention_and_deletion_control` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q5 r1 static - `EVAL_Q5_r1_static_20261030T091146_0de7c2`

- Status `partial`, stop `budget_exhausted`, interval leader `Managed vector database` (robust), recommendation `withheld` - withheld: startup_cost: Managed vector database scored from ['recurring_infrastructure'] cost evidence but Self-hosted vector database from ['total_cost_of_ownership']; different cost dimensions are not comparable; differentiating cells lack strong support (single source or non-official): Self-hosted vector database:startup_cost; Managed vector database:startup_cost rests on a weak qualified consensus (dissent disclosed; needs more independent agreement); Managed vector database's own score on control_and_customization is disputed (verified scores [0, 1]); Managed vector database:startup_cost rests on prices of different named products/plans; they are examples, not one comparable category-level cost; Managed vector database:startup_cost includes cost evidence whose dimension (infrastructure, labour, total, ...) cannot be determined
- Mechanical: 10 cited evidence IDs, **0 invalid**; 15 accepted / 7 rejected (lexical 0, approach-identity 4); single-source cells: Self-hosted vector database:startup_cost, Self-hosted vector database:control_and_customization
- AI-provisional flags: comparability: startup_cost: Managed vector database scored from ['recurring_infrastructure'] cost evidence but Self-hosted vector database from ['total_cost_of_ownership']; different cost dimensions are not comparable; one source supports 3+ targets: SRC_2 (3); SRC_6 (4); SRC_10 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Managed vector database:operational_effort | 2 | general | Managed services usually handle infrastructure provisioning | Strong anchor: the provider handles many recurring operational tasks, reducing the attention required from a small engin... | The biggest advantage is operational simplicity. Managed services usually handle infrastructure provisioning, routine maintenance, patching, availability architecture, scaling workflows, and parts of ... |
| EV_2 | Managed vector database:startup_cost | 1 | general | Managed services convert large and unpredictable infrastruct... | Plausible anchor: costs are described as predictable but usage-based, with no evidence that the service is clearly affor... | Managed services convert large and unpredictable infrastructure expenses into a more predictable operational expense. Pricing is typically based on: • Data storage • Indexing hours • Query volume • Th... |
| EV_3 | Managed vector database:control_and_customization | 1 | general | managed services can limit certain choices | Plausible anchor: the excerpt describes provider constraints on some choices while noting they are acceptable for most a... | The tradeoff is that managed services can limit certain choices. A team may have fewer options for low-level index tuning, infrastructure placement, deployment topology, private networking patterns, o... |
| EV_4 | Self-hosted vector database:operational_effort | 0 | general | Self-hosting requires DevOps or MLOps engineers | Poor anchor: provisioning, patching, security, and monitoring require substantial hands-on work, potentially demanding o... | Self-hosting requires DevOps or MLOps engineers to provision, configure, patch, secure, and monitor the database. For a high-growth SaaS startup, this may mean budgeting for one or two full-time senio... |
| EV_5 | Self-hosted vector database:control_and_customization | 2 | general | direct control over the database environment | Strong anchor: the excerpt describes extensive control over deployment environment and configuration choices. | Self-hosting is attractive because it gives teams direct control over the database environment. They can choose instance types, storage classes, regions, network topology, backup tooling, deployment c... |
| EV_6 | Managed vector database:operational_effort | 2 | general | Zilliz Cloud eliminates these concerns | Strong: automatic backups, patches, and scaling reduce routine operations work, while deployment takes minutes. | Zilliz Cloud eliminates these concerns: deployment takes minutes through a web console, backups are automatic, patches are applied transparently, and scaling happens automatically. |
| EV_7 | Managed vector database:startup_cost | 1 | general | Zilliz Cloud is cheaper—you pay only for what you use | Plausible: the excerpt supports manageable costs for modest usage, but gives no price or broader cost predictability. | For low-query-volume agents (experimental systems, pilot projects), Zilliz Cloud is cheaper—you pay only for what you use. |
| EV_8 | Managed vector database:control_and_customization | 0 | general | Zilliz Cloud offers limited customization—you use the servic... | Poor: the excerpt explicitly describes limited customization and use of the service as-is. | Zilliz Cloud offers limited customization—you use the service as-is. For standard agent use cases, Zilliz Cloud's defaults are excellent. |
| EV_9 | Self-hosted vector database:operational_effort | 0 | general | Self-hosted Milvus requires managing infrastructure | Poor: the excerpt explicitly characterizes the burden as substantial for small teams and says it requires DevOps experti... | Self-hosted Milvus requires managing infrastructure: provisioning servers or Kubernetes clusters, configuring networking, setting up persistent storage, managing backups, monitoring performance, and a... |
| EV_10 | Managed vector database:operational_effort | 2 | general | Pinecone handles all operations, scaling, and maintenance. | Strong anchor: the excerpt says the provider handles core operational work, supporting little ongoing attention from the... | Pinecone handles all operations, scaling, and maintenance. |
| EV_11 | Self-hosted vector database:operational_effort | 1 | general | Self-hosted Qdrant requires initial setup (1 to 2 hours) | Plausible anchor: the excerpt describes recurring but limited monitoring effort, alongside initial setup and occasional ... | Engineering time varies dramatically by approach. Self-hosted Qdrant requires initial setup (1 to 2 hours), ongoing monitoring (1 to 2 hours per month), and occasional troubleshooting. |
| EV_12 | Managed vector database:operational_effort | 2 | general | Managed vendors handle index lifecycle, replica placement, a... | Strong: the excerpt describes the provider taking on routine operational responsibilities, which supports low ongoing op... | Managed vendors handle index lifecycle, replica placement, and rolling upgrades, shifting the risk from engineering time to vendor bill. |
| EV_13 | Managed vector database:startup_cost | 0 | general | Pinecone implemented a $50 monthly minimum across paid Stand... | Poor: the excerpt documents a fixed monthly minimum that affects smaller workloads, indicating a potentially high or inf... | The most visible signal came in October, when Pinecone implemented a $50 monthly minimum across paid Standard plans. For organizations already spending well above that level, the change barely registe... |
| EV_14 | Self-hosted vector database:operational_effort | 0 | general | require you to provide the distributed orchestration, shardi... | Poor: the excerpt describes substantial infrastructure responsibilities that would be difficult for one backend engineer... | FAISS and Annoy are libraries for custom index builds and require you to provide the distributed orchestration, sharding, and recovery. |
| EV_15 | Self-hosted vector database:startup_cost | 0 | general | Budget at least $600k over 18 months | Poor: the stated staffing and infrastructure budget is substantial relative to an early-stage startup's likely needs. | If you choose to build, plan for three engineering phases: prototype (FAISS/pgvector, single-node), scale (distributed HNSW with autoscaling), and resilience (multi-AZ replication, snapshot catalog). ... |

Rejected candidates:

- CAND_5 `Self-hosted vector database:startup_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_11 `Self-hosted vector database:startup_cost` (acceptance): approach identity: excerpt describes several alternatives without isolating this one
- CAND_12 `Self-hosted vector database:control_and_customization` (acceptance): approach identity: excerpt describes several alternatives without isolating this one
- CAND_14 `Managed vector database:startup_cost` (acceptance): approach identity: excerpt describes several alternatives without isolating this one
- CAND_15 `Self-hosted vector database:startup_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_19 `Managed vector database:control_and_customization` (acceptance): approach identity: excerpt describes several alternatives without isolating this one
- CAND_22 `Self-hosted vector database:control_and_customization` (verification): verdict=partial: The excerpt establishes responsibility for orchestration and recovery, but does not directly show extensive control or choices over them.

## Q5 r1 v2_policy - `EVAL_Q5_r1_v2_policy_20261030T091146_15bb2c`

- Status `partial`, stop `budget_exhausted`, interval leader `Managed vector database` (robust), recommendation `withheld` - withheld: differentiating cells lack strong support (single source or non-official): Managed vector database:operational_effort; Managed vector database's own score on control_and_customization is disputed (verified scores [0, 1])
- Mechanical: 5 cited evidence IDs, **0 invalid**; 9 accepted / 6 rejected (lexical 0, approach-identity 0); single-source cells: Managed vector database:operational_effort, Managed vector database:startup_cost, Self-hosted vector database:control_and_customization
- AI-provisional flags: one source supports 3+ targets: SRC_2 (3); SRC_6 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Managed vector database:operational_effort | 2 | general | Managed services usually handle infrastructure provisioning | Strong anchor: the provider handles many recurring operational tasks, reducing the attention required from a small engin... | The biggest advantage is operational simplicity. Managed services usually handle infrastructure provisioning, routine maintenance, patching, availability architecture, scaling workflows, and parts of ... |
| EV_2 | Managed vector database:startup_cost | 1 | general | Managed services convert large and unpredictable infrastruct... | Plausible anchor: costs are described as predictable but usage-based, with no evidence that the service is clearly affor... | Managed services convert large and unpredictable infrastructure expenses into a more predictable operational expense. Pricing is typically based on: • Data storage • Indexing hours • Query volume • Th... |
| EV_3 | Managed vector database:control_and_customization | 1 | general | managed services can limit certain choices | Plausible anchor: the excerpt describes provider constraints on some choices while noting they are acceptable for most a... | The tradeoff is that managed services can limit certain choices. A team may have fewer options for low-level index tuning, infrastructure placement, deployment topology, private networking patterns, o... |
| EV_4 | Self-hosted vector database:operational_effort | 0 | general | Self-hosting requires DevOps or MLOps engineers | Poor anchor: provisioning, patching, security, and monitoring require substantial hands-on work, potentially demanding o... | Self-hosting requires DevOps or MLOps engineers to provision, configure, patch, secure, and monitor the database. For a high-growth SaaS startup, this may mean budgeting for one or two full-time senio... |
| EV_5 | Self-hosted vector database:control_and_customization | 2 | general | direct control over the database environment | Strong anchor: the excerpt describes extensive control over deployment environment and configuration choices. | Self-hosting is attractive because it gives teams direct control over the database environment. They can choose instance types, storage classes, regions, network topology, backup tooling, deployment c... |
| EV_6 | Managed vector database:operational_effort | 2 | general | Managed (Pinecone, Qdrant Cloud, Weaviate Cloud, Zilliz) | Strong anchor: the excerpt explicitly describes the managed service's operations burden as near-zero. | Ops burden / Near-zero / You own upgrades, backups, scaling |
| EV_7 | Managed vector database:control_and_customization | 0 | general | Managed (Pinecone, Qdrant Cloud, Weaviate Cloud, Zilliz) | Poor anchor: the excerpt identifies a constraint on data-handling and deployment choices for the managed approach, with ... | Data sovereignty / Data leaves your VPC (unless BYOC) / Full control |
| EV_8 | Self-hosted vector database:operational_effort | 0 | general | Self-hosted (pgvector, Milvus, Qdrant, Chroma, Vespa) | Poor anchor: the excerpt places ongoing infrastructure responsibilities on the team, a substantial burden given one back... | Ops burden / Near-zero / You own upgrades, backups, scaling |
| EV_9 | Self-hosted vector database:operational_effort | 0 | general | Self-hosting means you own the operational burden | This meets the poor anchor: the team owns several ongoing infrastructure duties—backups, monitoring, scaling, and upgrad... | Self-hosting means you own the operational burden: backups, monitoring, scaling, upgrades. |

Rejected candidates:

- CAND_5 `Self-hosted vector database:startup_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_8 `Managed vector database:startup_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_11 `Self-hosted vector database:startup_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_12 `Self-hosted vector database:control_and_customization` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_13 `Self-hosted vector database:operational_effort` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_14 `Self-hosted vector database:control_and_customization` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q5 r1 adaptive - `EVAL_Q5_r1_adaptive_20261030T091146_c8ad1a`

- Status `partial`, stop `budget_exhausted`, interval leader `Managed vector database` (robust), recommendation `withheld` - withheld: differentiating cells lack strong support (single source or non-official): Managed vector database:operational_effort; Managed vector database's own score on control_and_customization is disputed (verified scores [0, 1])
- Mechanical: 3 cited evidence IDs, **0 invalid**; 9 accepted / 6 rejected (lexical 0, approach-identity 0); single-source cells: Managed vector database:operational_effort, Managed vector database:startup_cost, Self-hosted vector database:control_and_customization
- AI-provisional flags: one source supports 3+ targets: SRC_2 (3); SRC_6 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | Managed vector database:operational_effort | 2 | general | Managed services usually handle infrastructure provisioning | Strong anchor: the provider handles many recurring operational tasks, reducing the attention required from a small engin... | The biggest advantage is operational simplicity. Managed services usually handle infrastructure provisioning, routine maintenance, patching, availability architecture, scaling workflows, and parts of ... |
| EV_2 | Managed vector database:startup_cost | 1 | general | Managed services convert large and unpredictable infrastruct... | Plausible anchor: costs are described as predictable but usage-based, with no evidence that the service is clearly affor... | Managed services convert large and unpredictable infrastructure expenses into a more predictable operational expense. Pricing is typically based on: • Data storage • Indexing hours • Query volume • Th... |
| EV_3 | Managed vector database:control_and_customization | 1 | general | managed services can limit certain choices | Plausible anchor: the excerpt describes provider constraints on some choices while noting they are acceptable for most a... | The tradeoff is that managed services can limit certain choices. A team may have fewer options for low-level index tuning, infrastructure placement, deployment topology, private networking patterns, o... |
| EV_4 | Self-hosted vector database:operational_effort | 0 | general | Self-hosting requires DevOps or MLOps engineers | Poor anchor: provisioning, patching, security, and monitoring require substantial hands-on work, potentially demanding o... | Self-hosting requires DevOps or MLOps engineers to provision, configure, patch, secure, and monitor the database. For a high-growth SaaS startup, this may mean budgeting for one or two full-time senio... |
| EV_5 | Self-hosted vector database:control_and_customization | 2 | general | direct control over the database environment | Strong anchor: the excerpt describes extensive control over deployment environment and configuration choices. | Self-hosting is attractive because it gives teams direct control over the database environment. They can choose instance types, storage classes, regions, network topology, backup tooling, deployment c... |
| EV_6 | Managed vector database:operational_effort | 2 | general | Managed (Pinecone, Qdrant Cloud, Weaviate Cloud, Zilliz) | Strong anchor: the excerpt explicitly describes the managed service's operations burden as near-zero. | Ops burden / Near-zero / You own upgrades, backups, scaling |
| EV_7 | Managed vector database:control_and_customization | 0 | general | Managed (Pinecone, Qdrant Cloud, Weaviate Cloud, Zilliz) | Poor anchor: the excerpt identifies a constraint on data-handling and deployment choices for the managed approach, with ... | Data sovereignty / Data leaves your VPC (unless BYOC) / Full control |
| EV_8 | Self-hosted vector database:operational_effort | 0 | general | Self-hosted (pgvector, Milvus, Qdrant, Chroma, Vespa) | Poor anchor: the excerpt places ongoing infrastructure responsibilities on the team, a substantial burden given one back... | Ops burden / Near-zero / You own upgrades, backups, scaling |
| EV_9 | Self-hosted vector database:operational_effort | 0 | general | Self-hosting means you own the operational burden | Meets the poor anchor: the excerpt assigns several ongoing infrastructure responsibilities to the team, which could be d... | Self-hosting means you own the operational burden: backups, monitoring, scaling, upgrades. Their managed cloud offering mitigates this but is still newer and less battle-tested than Pinecone's. |

Rejected candidates:

- CAND_5 `Self-hosted vector database:startup_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_8 `Managed vector database:startup_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_11 `Self-hosted vector database:startup_cost` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_12 `Self-hosted vector database:control_and_customization` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)
- CAND_14 `Managed vector database:control_and_customization` (verification): verdict=partial: It confirms that replacing the data source permits changing the embedding model and chunking, but does not establish that the database is resident or Dat
- CAND_15 `Managed vector database:control_and_customization` (acceptance): no derivable fit score (no thresholds+value, and proposed score not justified)

## Q8 r1 static - `EVAL_Q8_r1_static_20261030T091146_5ac52b`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (None), recommendation `not_applicable`
- Mechanical: 16 cited evidence IDs, **0 invalid**; 16 accepted / 5 rejected (lexical 3, approach-identity 0); single-source cells: none
- AI-provisional flags: one source supports 3+ targets: SRC_2 (3); SRC_6 (3); SRC_7 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | open_source_license | - | general | # confident-ai/deepeval |  | License: Apache License 2.0 |
| EV_2 | llm_evaluation_or_observability | - | general | Opik is the open-source LLM observability and evaluation pla... |  | Opik is the open-source LLM observability and evaluation platform for AI agent tracing, LLM evaluation, prompt management, and production monitoring. |
| EV_3 | open_source_license | - | general | Opik is Apache-2.0 licensed |  | Opik is Apache-2.0 licensed and free to self-host: the full platform, backend included, not just a client SDK. |
| EV_4 | self_hosting_support | - | general | Opik can be deployed locally or in your own infrastructure |  | Yes. Opik can be deployed locally or in your own infrastructure using the documented self-hosting options. |
| EV_5 | llm_evaluation_or_observability | - | general | Langfuse is an open source LLM engineering platform |  | Langfuse is an open source LLM engineering platform. It helps teams collaboratively develop, monitor, evaluate, and debug AI applications. |
| EV_6 | self_hosting_support | - | general | Run Langfuse on your own infrastructure |  | Run Langfuse on your own infrastructure: - Local (docker compose): Run Langfuse on your own machine in 5 minutes using Docker Compose. |
| EV_7 | llm_evaluation_or_observability | - | general | Trace, evaluate, and improve AI agents with Phoenix. |  | Trace, evaluate, and improve AI agents with Phoenix. |
| EV_8 | self_hosting_support | - | general | Run locally or self-host in your environment. |  | Run locally or self-host in your environment. |
| EV_9 | llm_evaluation_or_observability | - | general | Evidently is ​​an open-source ML and LLM observability frame... |  | Evidently is ​​an open-source ML and LLM observability framework. Evaluate, test, and monitor any AI-powered system or data pipeline. |
| EV_10 | open_source_license | - | general | License: Apache License 2.0 |  | License: Apache License 2.0 |
| EV_11 | self_hosting_support | - | general | Self-host the open-source version. |  | You can choose: * Self-host the open-source version. Live demo. |
| EV_12 | llm_evaluation_or_observability | - | general | Self-hosted LLM observability and evals. |  | **Self-hosted LLM observability and evals.** Log every model call with tokens, latency and cost, trace agent runs step by step, and compare models and prompts with evals that tell you whether a differ... |
| EV_13 | open_source_license | - | general | License: MIT License |  | License: MIT License |
| EV_14 | self_hosting_support | - | general | docker compose up |  | **Zero-config deployment.** `docker compose up` gives you the API and UI on one port, with SQLite on a named volume. |
| EV_15 | llm_evaluation_or_observability | - | general | OpenLIT is an open-source agent harness engineering platform |  | OpenLIT is an open-source agent harness engineering platform: OpenTelemetry-native agent observability, evals, guardrails, prompt management, and cost and GPU monitoring for AI agents and coding agent... |
| EV_16 | open_source_license | - | general | License: Apache 2.0 |  | License: Apache 2.0 |

Rejected candidates:

- CAND_1 `llm_evaluation_or_observability` (grounding): excerpt not found in source text
- CAND_8 `llm_evaluation_or_observability` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_9 `open_source_license` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_10 `self_hosting_support` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_21 `self_hosting_support` (grounding): excerpt not found in source text

## Q8 r1 v2_policy - `EVAL_Q8_r1_v2_policy_20261030T091147_130113`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (None), recommendation `not_applicable`
- Mechanical: 12 cited evidence IDs, **0 invalid**; 12 accepted / 5 rejected (lexical 4, approach-identity 0); single-source cells: none
- AI-provisional flags: one source supports 3+ targets: SRC_2 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | open_source_license | - | general | # confident-ai/deepeval |  | License: Apache License 2.0 |
| EV_2 | llm_evaluation_or_observability | - | general | Opik is the open-source LLM observability and evaluation pla... |  | Opik is the open-source LLM observability and evaluation platform for AI agent tracing, LLM evaluation, prompt management, and production monitoring. |
| EV_3 | open_source_license | - | general | Opik is Apache-2.0 licensed |  | Opik is Apache-2.0 licensed and free to self-host: the full platform, backend included, not just a client SDK. |
| EV_4 | self_hosting_support | - | general | Opik can be deployed locally or in your own infrastructure |  | Yes. Opik can be deployed locally or in your own infrastructure using the documented self-hosting options. |
| EV_5 | llm_evaluation_or_observability | - | general | Langfuse is an open source LLM engineering platform |  | Langfuse is an open source LLM engineering platform. It helps teams collaboratively develop, monitor, evaluate, and debug AI applications. |
| EV_6 | self_hosting_support | - | general | Run Langfuse on your own infrastructure |  | Run Langfuse on your own infrastructure: - Local (docker compose): Run Langfuse on your own machine in 5 minutes using Docker Compose. |
| EV_7 | llm_evaluation_or_observability | - | general | DeepEval is an open-source LLM evaluation framework |  | DeepEval is an open-source LLM evaluation framework for LLM applications. |
| EV_8 | self_hosting_support | - | general | DeepEval is local-first: your evaluations run in your own en... |  | DeepEval is local-first: your evaluations run in your own environment. |
| EV_9 | llm_evaluation_or_observability | - | general | Open source LLM engineering platform: LLM Observability, met... |  | 🪢 Open source LLM engineering platform: LLM Observability, metrics, evals, prompt management, playground, datasets. |
| EV_10 | open_source_license | - | general | All product capabilities—tracing, evaluations, prompt manage... |  | All product capabilities—tracing, evaluations, prompt management, experiments, annotation, the playground, and more—are MIT licensed without any usage limits. |
| EV_11 | self_hosting_support | - | general | Self-host it on your own infrastructure. |  | Self-host it on your own infrastructure. |
| EV_12 | llm_evaluation_or_observability | - | general | Trace, evaluate, and improve AI agents with Phoenix. |  | Trace, evaluate, and improve AI agents with Phoenix. |

Rejected candidates:

- CAND_1 `llm_evaluation_or_observability` (grounding): excerpt not found in source text
- CAND_13 `llm_evaluation_or_observability` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_14 `open_source_license` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_15 `self_hosting_support` (acceptance): lexical check: entity name/alias not found in excerpt context
- CAND_17 `self_hosting_support` (acceptance): lexical check: entity name/alias not found in excerpt context

## Q8 r1 adaptive - `EVAL_Q8_r1_adaptive_20261030T091147_0272b9`

- Status `partial`, stop `budget_exhausted`, interval leader `None` (None), recommendation `not_applicable`
- Mechanical: 16 cited evidence IDs, **0 invalid**; 22 accepted / 2 rejected (lexical 0, approach-identity 0); single-source cells: none
- AI-provisional flags: one source supports 3+ targets: SRC_2 (3); SRC_8 (3)

| EV | target | score | scope | identification quote | rubric rationale | excerpt |
|---|---|---|---|---|---|---|
| EV_1 | open_source_license | - | general | # confident-ai/deepeval |  | License: Apache License 2.0 |
| EV_2 | llm_evaluation_or_observability | - | general | Opik is the open-source LLM observability and evaluation pla... |  | Opik is the open-source LLM observability and evaluation platform for AI agent tracing, LLM evaluation, prompt management, and production monitoring. |
| EV_3 | open_source_license | - | general | Opik is Apache-2.0 licensed |  | Opik is Apache-2.0 licensed and free to self-host: the full platform, backend included, not just a client SDK. |
| EV_4 | self_hosting_support | - | general | Opik can be deployed locally or in your own infrastructure |  | Yes. Opik can be deployed locally or in your own infrastructure using the documented self-hosting options. |
| EV_5 | llm_evaluation_or_observability | - | general | Langfuse is an open source LLM engineering platform |  | Langfuse is an open source LLM engineering platform. It helps teams collaboratively develop, monitor, evaluate, and debug AI applications. |
| EV_6 | self_hosting_support | - | general | Run Langfuse on your own infrastructure |  | Run Langfuse on your own infrastructure: - Local (docker compose): Run Langfuse on your own machine in 5 minutes using Docker Compose. |
| EV_7 | llm_evaluation_or_observability | - | general | DeepEval is an open-source LLM evaluation framework |  | DeepEval is an open-source LLM evaluation framework for LLM applications. |
| EV_8 | self_hosting_support | - | general | DeepEval is local-first: your evaluations run in your own en... |  | DeepEval is local-first: your evaluations run in your own environment. |
| EV_9 | llm_evaluation_or_observability | - | general | Open source LLM engineering platform: LLM Observability, met... |  | 🪢 Open source LLM engineering platform: LLM Observability, metrics, evals, prompt management, playground, datasets. |
| EV_10 | open_source_license | - | general | All product capabilities—tracing, evaluations, prompt manage... |  | All product capabilities—tracing, evaluations, prompt management, experiments, annotation, the playground, and more—are MIT licensed without any usage limits. |
| EV_11 | self_hosting_support | - | general | Self-host it on your own infrastructure. |  | Self-host it on your own infrastructure. |
| EV_12 | llm_evaluation_or_observability | - | general | Langfuse |  | / 🔵 Langfuse / 36.5k / MIT (open-core) / AI engineering platform: tracing, evals, prompt mgmt, playground. The most widely adopted OSS LLM-obs platform. / |
| EV_13 | open_source_license | - | general | MIT (open-core) |  | / 🔵 Langfuse / 36.5k / MIT (open-core) / AI engineering platform: tracing, evals, prompt mgmt, playground. The most widely adopted OSS LLM-obs platform. / |
| EV_14 | self_hosting_support | - | general | / Langfuse / ✅ / MIT / |  | / Langfuse / ✅ / MIT / ✅ / ✅ / ✅ / ✅ / |
| EV_15 | llm_evaluation_or_observability | - | general | OpenTelemetry-native AI observability & evaluation |  | / 🟢 Arize Phoenix / 12.0k / Elastic v2 / OpenTelemetry-native AI observability & evaluation; runs locally or self-hosted. / |
| EV_16 | open_source_license | - | general | Elastic v2 |  | / 🟢 Arize Phoenix / 12.0k / Elastic v2 / OpenTelemetry-native AI observability & evaluation; runs locally or self-hosted. / |
| EV_17 | self_hosting_support | - | general | runs locally or self-hosted |  | / 🟢 Arize Phoenix / 12.0k / Elastic v2 / OpenTelemetry-native AI observability & evaluation; runs locally or self-hosted. / |
| EV_18 | llm_evaluation_or_observability | - | general | Trace, evaluate & monitor LLM/RAG/agent apps |  | / 🟢 Comet Opik / 22.9k / Apache-2.0 / Trace, evaluate & monitor LLM/RAG/agent apps; automated prompt optimization. / |
| EV_19 | open_source_license | - | general | Apache-2.0 |  | / 🟢 Comet Opik / 22.9k / Apache-2.0 / Trace, evaluate & monitor LLM/RAG/agent apps; automated prompt optimization. / |
| EV_20 | self_hosting_support | - | general | / Comet Opik / ✅ / Apache-2.0 / |  | / Comet Opik / ✅ / Apache-2.0 / ✅ / ✅ / ✅ / ✅ / |
| EV_21 | llm_evaluation_or_observability | - | general | One-line **proxy** observability |  | / 🟢 Helicone / 6.2k / Apache-2.0 / One-line **proxy** observability - change the base URL, log every request/cost/error. / |
| EV_22 | open_source_license | - | general | Apache-2.0 |  | / 🟢 Helicone / 6.2k / Apache-2.0 / One-line **proxy** observability - change the base URL, log every request/cost/error. / |

Rejected candidates:

- CAND_1 `llm_evaluation_or_observability` (grounding): excerpt not found in source text
- CAND_24 `self_hosting_support` (grounding): excerpt not found in source text

