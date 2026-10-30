# Research report - EVAL_Q4_r1_adaptive_20261030T051000_398ba3

**Question:** Compare approaches to short-term and long-term memory in customer-support AI agents, including retrieval, privacy and retention.

**Short answer:** Session-only memory leads provisionally, but score intervals overlap (Session-only memory [12,12], Persistent conversation-log retrieval [9,9], Summarized customer-profile memory [3,15], Hybrid layered memory [6,12]); current evidence does not force a unique recommendation. The main trade-off is immediate continuity within a conversation versus cross-session personalization that requires deliberate access, retention, and deletion controls. The evidence describes design properties more than measured retrieval quality, and it leaves retention periods and some lifecycle guarantees unspecified.

| Mode | Status | Stop reason | Confidence | Factual confidence | Decision stability |
|---|---|---|---|---|---|
| comparison | partial | budget_exhausted | moderate | moderate | provisional |

_Confidence rule: confidence = min(interval stability, lowest factual confidence among the leader's supported/disputed cells); robust/high=high, provisional/moderate=moderate, otherwise low. A withheld recommendation caps confidence at moderate, and at low when the withholding is due to non-comparable evidence._

**Requirement coverage:** 9/12 units with verified support.

## Recommendation readiness

- Interval leader: Session-only memory (provisional)
- Recommendation: **withheld**
  - withheld because: score intervals overlap (provisional leader only)
  - withheld because: differentiating cells lack strong support (single source or non-official): Session-only memory:retrieval_effectiveness, Persistent conversation-log retrieval:retrieval_effectiveness

## Decision matrix

_Cell = score (evidence; independent sources; scope)._

| Alternative | retrieval_effectiveness (w3, default) | privacy_protection (w3, default) | retention_and_deletion_control (w3, default) | LB | UB |
|---|---|---|---|---|---|
| Session-only memory (approach) | 2 (EV_1; 1 src) | 1 (EV_2; 1 src) | 1 (EV_3; 1 src) | 12 | 12 |
| Persistent conversation-log retrieval (approach) | 1 (EV_4; 1 src) | 1 (EV_5, EV_6; 1 src) | 1 (EV_7; 1 src) | 9 | 9 |
| Summarized customer-profile memory (approach) | unknown [0,2] | 1 (EV_8; 1 src) | unknown [0,2] | 3 | 15 |
| Hybrid layered memory (approach) | unknown [0,2] | 1 (EV_9; 1 src) | 1 (EV_10; 1 src) | 6 | 12 |

### Scoring rules

- **retrieval_effectiveness** (higher_is_better, weight 3 [default]): 0 = Cannot reliably surface useful context for the user's short-term and long-term support needs.; 1 = Supports useful context within its memory scope, but has notable limits in cross-session recall, relevance, or freshness.; 2 = Reliably surfaces relevant, current context across the short- and long-term memory needs the approach is designed to address.
- **privacy_protection** (higher_is_better, weight 3 [default]): 0 = Retains or exposes substantial customer information without clear limits on what is stored or retrieved.; 1 = Offers some data minimization or access controls, but privacy protections are incomplete or difficult to apply consistently.; 2 = Supports data minimization and clear, enforceable controls over what customer information is stored and made available to the agent.
- **retention_and_deletion_control** (higher_is_better, weight 3 [default]): 0 = Retention is difficult to limit, and correcting or deleting stored memories is unreliable.; 1 = Some retention and deletion controls are available, but lifecycle management may be manual or incomplete.; 2 = Retention can be defined for relevant memory types, with dependable correction, expiration, and deletion processes.

## Findings

- Session-only memory uses information from the active conversation to avoid repeated questions, and its boundary is the end of that conversation; cross-session recall is a separate design choice. Its short-lived scope is described as limiting ongoing privacy exposure. [EV_1, EV_2, EV_3]
  - EV_1 (SRC_1, chars 4392-4795, score 2 via verified_proposal): "Within one active conversation, the agent should remember everything the customer has already told it, without exception. Asking a customer for their order number twice in the same conversation is the exact failure this guide is trying to prevent, and it needs no special justification: the customer volunteered the information moments ago, in the same thread, for the purpose of getting help right now."
    - rubric rationale: Strong for the approach’s intended short-term scope: the excerpt says the agent should remember everything already supplied in the active conversation and gives a concrete service benefit.
  - EV_2 (SRC_1, chars 3057-3273, score 1 via verified_proposal): "Short-term memory, the context of the current conversation, is rarely the source of privacy problems, because it lives and dies with the conversation and rarely persists in a form a customer would think to ask about."
    - rubric rationale: Plausible: the excerpt supports limited persistence, but it does not describe enforceable controls over information used within the session.
  - EV_3 (SRC_1, chars 5560-5858, score 1 via verified_proposal): "The boundary of session memory is the session itself. Once a conversation genuinely ends, whether by explicit close or by a customer going quiet for an extended period, the design question shifts from within-session recall, which is essentially unconditional, to cross-session recall, which is not."
    - rubric rationale: Plausible: the excerpt defines a session boundary, but does not describe dependable correction, deletion, or expiration mechanisms.
- Persistent conversation-log retrieval can load and search prior interactions before responding, but it requires controls beyond a stable customer identifier: scoped access, authorization across reads and deletion, and tenant-aware handling of caches and background work. Retention should be specified separately for transcripts and derived data, and deletion should cover retained copies. [EV_4, EV_5, EV_6, EV_7]
  - EV_4 (SRC_4, chars 126-519, score 1 via verified_proposal): "An AI support agent remembers customers across conversations when every ticket, chat and call is saved under one stable customer ID, and the relevant history is loaded before the agent replies. With a memory layer such as supermemory, that means one namespace per customer: you save each interaction into it, and before each reply you load the customer's profile and search their past tickets."
    - rubric rationale: Plausible: it describes cross-session search and retrieval for customer support, but does not establish that retrieved context is reliably accurate or current.
  - EV_5 (SRC_4, chars 3055-3370, score 1 via verified_proposal): "Two controls matter for enterprise support: - Per-customer keys. A scoped API key can be limited to one namespace, or a fixed list of them, and requests outside it get a 403 (API keys docs). Writable scoped keys can still update and delete inside their namespace, so give read-only keys to anything that only reads."
    - rubric rationale: Plausible: the excerpt describes access controls, but does not establish data minimization or comprehensive limits on what customer information is stored and retrieved.
  - EV_6 (SRC_4, chars 7696-7999, score 1 via verified_proposal): "Make access and deletion testable A stable customer identifier supports continuity. It doesn't prove the caller is entitled to use that identity. Enforce authorization before memory reads, writes, exports and deletion, and include the tenant scope in caches and background jobs as well as live searches."
    - rubric rationale: Plausible: it recommends explicit access controls, but does not show complete data-minimization or retention safeguards.
  - EV_7 (SRC_4, chars 8000-8253, score 1 via verified_proposal): "Define retention separately for transcripts, summaries, extracted facts, logs and backups. A deletion workflow should cover the copies your system actually keeps. Removing a result from search doesn't necessarily remove its source or every derived copy."
    - rubric rationale: Plausible: the excerpt identifies lifecycle controls needed for stored conversation records, while noting that search removal alone may not delete all copies.
- Summarized profile memory is presented as a way to retain useful support context while omitting unnecessary transcript detail, including sensitive information. The evidence does not specify its retrieval performance or retention and deletion procedures. [EV_8]
  - EV_8 (SRC_1, chars 7251-7651, score 1 via verified_proposal): "A useful rule of thumb is to prefer a compact, structured summary over a raw transcript when carrying memory across sessions. A summary that says the customer had a billing dispute in March, resolved with a partial refund, carries the useful signal without retaining every word of a conversation that included payment details, an address, or other information beyond what the next conversation needs."
    - rubric rationale: Plausible: the excerpt supports data minimization through summaries, but does not describe enforceable controls over what is stored or made available.
- Hybrid layered memory distinguishes current business state, interaction history, and customer preferences, with separate intended uses and authorization rules. Its controller makes promotion, compression, and eviction inspectable under bounded capacity, but the evidence does not establish retention periods or reliable correction and deletion. [EV_9, EV_10]
  - EV_9 (SRC_4, chars 4535-5146, score 1 via verified_proposal): "Keep three kinds of context separate | Context | Example | How to use it | | --- | --- | --- | | Current business state | Subscription, permissions, open incident status | Fetch from the system of record when the answer depends on it | | Interaction history | Error code, attempted fix, unresolved question | Retrieve relevant events with timestamps and source references | | Customer preferences | Preferred language or level of technical detail | Apply a current preference within its intended scope | A shared store can hold all three if the data model and authorization rules preserve their different roles."
    - rubric rationale: Plausible: the excerpt describes role separation and authorization rules, but does not establish comprehensive controls or data minimization.
  - EV_10 (SRC_5, chars 5920-6105, score 1 via verified_proposal): "We instantiate this formulation in StageMem, a compact transient/working/durable controller that makes promotion, compression, and eviction decisions inspectable under bounded capacity."
    - rubric rationale: Plausible: the excerpt describes layered stores and inspectable lifecycle actions, indicating retention controls. It does not establish defined retention periods or dependable correction, expiration, and deletion processes.

## Decision changes (attributed to newly verified evidence)

- Round 0: stability_changed None/undetermined -> Session-only memory/provisional via EV_1, EV_2, EV_3, EV_4, EV_5, EV_6, EV_7, EV_8, EV_9

Decision flips: 0; status changes: 1

## Sources

- SRC_1: [Conversation memory for a support agent: what to keep and forget - Blog · Communicate](https://communicate.so/blog/conversation-memory-support-agent) - retrieved 2026-10-30T05:10:00+00:00, published 2026-08-30T00:00:00.000Z
- SRC_4: [AI Memory for Customer Support Agents: A Practical Architecture](https://supermemory.ai/blog/ai-memory-customer-support-agents/) - retrieved 2026-10-30T05:10:00+00:00
- SRC_5: [Retention Consequence in Lifecycle Memory Control](https://arxiv.org/html/2604.16774) - retrieved 2026-10-30T05:10:02+00:00, published 2026-05-27T00:00:00.000Z

## Assumptions

- The comparison is about general memory architectures for customer-support AI agents, not specific vendors or products.
- No jurisdiction, regulatory regime, data sensitivity level, or retention period was specified.
- No deployment model, technical stack, or customer-support channel was specified.
- The requested comparison should cover both within-session context and cross-session memory where an approach supports it.
- No stated priority for retrieval_effectiveness, privacy_protection, retention_and_deletion_control: equal default weight 3.

## Limitations

- Fit scores (0/1/2) are model-assisted assessments under the disclosed rubric and weights, not measurements.
- Support verification uses the same model family as extraction; it is not ground truth and needs human audit.
- 'Robust' means interval dominance under the chosen criteria and weights, not that the option is factually best.
- Single-source support (one independent source): Session-only memory:retrieval_effectiveness, Session-only memory:privacy_protection, Session-only memory:retention_and_deletion_control, Persistent conversation-log retrieval:retrieval_effectiveness, Persistent conversation-log retrieval:privacy_protection, Persistent conversation-log retrieval:retention_and_deletion_control, Summarized customer-profile memory:privacy_protection, Hybrid layered memory:privacy_protection, Hybrid layered memory:retention_and_deletion_control.
- Unknown (no verified evidence, interval [0,2]): Summarized customer-profile memory:retrieval_effectiveness, Summarized customer-profile memory:retention_and_deletion_control, Hybrid layered memory:retrieval_effectiveness.
- 4 extracted candidate(s) were rejected by grounding/verification (see verification_log.jsonl).
- Stopped: budget_exhausted (MAX_RESEARCH_ROUNDS=3 reached).

## Next steps

- Compare retrieval accuracy and failure rates across the approaches on representative support tasks, including whether relevant history is surfaced without stale or irrelevant context.
- Specify retention periods and end-to-end deletion behavior for transcripts, summaries, extracted facts, logs, backups, and caches.
- Validate authorization and tenant isolation for retrieval, updates, exports, deletion, and background processing.
- Test how summarized and hybrid memories are corrected when customer details change or stored context is inaccurate.

## Budget

Searches 5/6, content pages 10/12, LLM requests 7, elapsed 52.72 s. LLM: gpt-6-luna (record).
