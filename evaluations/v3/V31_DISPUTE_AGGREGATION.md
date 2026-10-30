# V3.1: source-family consensus aggregation and reachable counterfactuals

> **Status:** implemented and tested offline only (202 tests). No paid call has been made since the pilot.
> **Historical results are unchanged:**
> - all 446 V1, V2 and V3-pilot artifacts match `pilot/HISTORICAL_ARTIFACTS_SHA256.txt`;
> - V2 and the pilot still replay exactly with their frozen code (`evaluations/v2/replay_v2.py`, `evaluations/v3/pilot/replay_pilot.py`; 0 differences);
> - the new protocol is `v3.1`, with its own snapshot fingerprint.

## 1. Root cause (pilot rules, `matrix.cell_state`)

The pilot aggregated a cell as follows: one distinct verified score gives `supported`; two or more distinct scores in one context give `disputed` [min, max], whatever their source or number. Consequences:
- a dispute could only grow, because adding evidence adds scores and never removes one;
- the V3 counterfactuals pinned disputed cells to scores that no evidence could reach;
- `independent_sources` counted domains for *display*, but the dispute rule ignored sources entirely.

Pilot evidence, 33 cells with ≥ 2 scored excerpts across the 9 runs (the categories overlap):

| Distinction | Observed | How v3.1 treats it |
|---|---|---|
| 1. Repeated copies of one passage | 0 in these 33 cells | Identical normalised excerpts merge their families into one |
| 2. Several excerpts from one document | 7 cells (e.g. Q1 Weaviate:deployment_fit, one weaviate.io source scored 1 and 2) | One document, one family; if it implies two scores, that family is **internally inconsistent**, never two votes |
| 3. Two or more independent families | 27 cells | Counted by publisher (registrable domain, or the full host with *uncertain* independence on multi-tenant platforms) |
| 4. Rubric-interpretation differences (adjacent scores, judgement-based) | 21 of 24 cells with a disagreement | Eligible for qualified consensus under the 2:1 family rule |
| 5. Context or dimension differences | 3 cells (incl. Q5 Self-hosted:startup_cost: a $20/month VPS vs $9–18k engineering time) | Split by declared scope and inferred cost dimension, never pooled |
| 6. Direct contradictions at opposite rubric ends | 2 cells (Q5 Managed:startup_cost: free tier vs price increases) | Material: never resolved by majority |
| 7. Unsupported or misattributed evidence | 14 candidates rejected (lexical, approach identity, "multiple") | Never reaches aggregation (verification is unchanged) |

## 2. Scoring rules implemented (`pathfinder/consensus.py`)

Per cell, using only verified, grounded, scorable evidence:

1. **Families:**
   - a document is one fetched page;
   - a family is its publisher (registrable domain). On multi-tenant hosts (github.io, medium.com, …) the family is the full host, and its independence is marked `uncertain`;
   - families sharing an identical normalised excerpt are merged as copies.
2. **Family assessment:**
   - *consistent* if all its excerpts imply one score;
   - otherwise *internally inconsistent*, with an unresolved interval. It is never resolved to the score that suits an alternative.
   - Different publication dates inside a family are noted as a *possible* supersession, never assumed.
3. **Contexts:**
   - split by declared scope (as before) and, for cost-like criteria, by an inferred cost dimension: recurring infrastructure, one-time setup, engineering labour, total cost of ownership, or licence/subscription;
   - the dimension is inferred deterministically from the recorded unit, the claim and the excerpt;
   - evidence with no specific context applies to all contexts;
   - consistent but different contexts give `scope_dependent` (dimension mismatch: `dimension_mismatch=True`).
4. **Consensus inside one context:** all families agree → `supported`. Only inconsistent families → `disputed`, labelled source-inconsistent. Otherwise the prevailing score s (most consistent families, with no tie) becomes **`consensus`** only if all of these hold:

   | Condition | Rule |
   |---|---|
   | C1 | ≥ 2 supporting families of *certain* independence |
   | C2 | supporting families ≥ 2 × dissenting families. An inconsistent family whose range excludes s dissents; one whose range includes s is recorded but counts neither way. |
   | C3 | no dissent at the opposite rubric end (0 vs 2 is material) |
   | C4 | no authoritative dissent: a first-party family rating its own product *worse*, or a measured (threshold-scored) value against judgement-based support |
   | C5 | no version-specific dissent that the support does not share |

   Otherwise the cell is `disputed`. Its kind is one of `source_inconsistent`, `independent_disagreement`, `material_contradiction`, `authoritative_dissent` or `version_specific`, and the interval is [min, max]. Every outcome records:
   - the prevailing score;
   - supporting, dissenting and inconsistent family IDs;
   - certain-family counts;
   - source-quality notes;
   - the type of disagreement: rubric interpretation, factual, substantive, or source inconsistency;
   - the remaining uncertainty;
   - the reasons for accepting or rejecting consensus.

   Dissent is never deleted.
5. **Consensus strength and confidence:**
   - *strong* means ≥ 3 certain supporting families, at least 3:1 against the dissent, and only adjacent, judgement-based dissent. Factual confidence `high`.
   - Every other consensus is *weak*, with factual confidence `moderate`.
   - Consensus is an eligibility rule, not proof of truth.
6. **Authority:**
   - first-party pages count as one family like any other;
   - they are good evidence of *what* a product offers, weak evidence of *how good* it is;
   - their dissent *against* their own product is material, their dissent in its favour is not;
   - unsupported scoring interpretations never get here, because the verifier must accept the rubric rationale first.

Test cases A–E from the specification are covered by `tests/test_consensus.py`:

| Case | Evidence | Result |
|---|---|---|
| A | 3 vs 1 | strong consensus, dissent disclosed |
| A | 2 vs 1 | weak consensus |
| B | one document scored two ways | one inconsistent family |
| C | 1 vs 1 or 2 vs 2 | unresolved |
| D | version-specific dissent | not outvoted |
| E | newer document | noted, not assumed to supersede |

## 3. Recommendation readiness (`pathfinder/readiness.py`, all arms)

The interval leader, interval robustness, evidence confidence and readiness stay separate. New or changed blockers:
- **`weak_consensus`:** a differentiating cell rests on a weak consensus.
- **`incomparable_dimensions`:** the leader's own cost cell mixes dimensions. A differentiating cost criterion whose alternatives were scored from disjoint dimensions is a comparability issue.
- **Consensus cells count as differentiating**, so they are subject to every blocker.
- **Kept from V3:**
  - `leader_disputed` (now including authoritative, material and source-inconsistent disputes);
  - `weak_support`, `comparability`, `self_reported` and `critical_unsupported`.

Readiness still requires a robust leader and no blocker. On the pilot evidence the stricter rules produce **0 ready recommendations** (none before either).

## 4. Reachable counterfactuals (`consensus.reachability`, `acquisition.py`, adaptive arm)

For each cell, `reachability` asks what more research can still achieve under the rules above:
- **Disputed cell:** for each score s, find the minimum number k of *new agreeing, independent* families needed for C1 and C2. A score is unreachable when C3, C4 or C5 would block consensus however many sources agree.
- **Corroboration target:** k is the number of families needed to reach high confidence (2 certain families), or a *strong* consensus.
- **Assumption, disclosed:** one search adds at most one new family, and agreement is never assumed.

| Class | Effect on the V3 policy |
|---|---|
| `resolvable_by_one_source` (k = 1) | counterfactual pins restricted to reachable scores; factor unchanged |
| `needs_multiple_sources` (k ≤ remaining searches) | decision factor divided by k |
| `unlikely_within_budget` (k > remaining) | not pinned; factor 0.5, labelled |
| `needs_scope_or_authority_clarification` (version, authority or dimension issues) | not pinned; factor 0.5, labelled |
| `unresolvable_by_more_evidence` | not pinned; factor 0.5, labelled |

- Group analysis and the common stop rule's "decision-relevant cell" test use only reachable pins.
- Every action records `reach = {class, k, reachable_scores}`.
- Remaining searches are passed from the graph: rounds left, capped by the search budget.

On the 9 pilot decision points, v3.1 makes **the same choices** as the pilot V3: every chosen target was reachable with k = 1. The change only matters for disputes that are blocked or need several sources, and none arose at those points. It is a correctness fix, not a demonstrated improvement.

## 5. Fairness and metrics

- **Same for every arm:** aggregation, readiness and stopping. Aggregation has no strategy input (test `test_aggregation_is_identical_for_every_arm`). Static scheduling and queries are unchanged.
- **Supported coverage (v3.1):** supported + consensus + scope_dependent, *excluding* dimension-mismatch cells, which have no comparable score.
- **Reported separately:** consensus, disputed (by kind), dimension mismatches, source-inconsistent cells, unknown and insufficient.

## 6. Retrospective re-scoring of the pilot

Full detail is in `pilot/RESCORING_V31.md`. It is **not** a new live benchmark: the trajectories were chosen under the pilot rules.

| Arm | Supported cells, pilot rules → v3.1 |
|---|---|
| static | 16 → 17 |
| v2_policy | 17 → 20 |
| V3 | 17 → 19 |

- **Q5 only:**
  - majority cells became qualified consensus (strong: Managed ops 4 vs 1, Self-hosted ops 3 vs 1 in static; weak elsewhere);
  - Self-hosted startup cost became a dimension mismatch;
  - V3 and v2_policy became interval-robust, but recommendations stay withheld (weak consensus, and the leader's own disputed cells).
- **Q1:** the same-page Weaviate cell is relabelled as source-inconsistent in all arms. Leaders unchanged.
- **Q4:** no change.
- **No recommendation became ready.**

## 7. Limitations

- **Families:** registrable domain plus copy detection. Reworded syndication, or one author publishing on several sites, is not detected. Multi-tenant hosts are marked uncertain instead.
- **Cost dimensions and versions:** inferred by keywords and regex. They can miss or mislabel, and they are recorded for audit.
- **First-party detection** depends on each plan's `official_domains`. Approach alternatives have none.
- **Thresholds:** 2:1 for consensus and 3 families / 3:1 for strong consensus are conservative policy constants, not calibrated.
- **One family per search** is an assumption. Agreement of new sources is never predicted.
- **Human review:** no human has reviewed the evidence.
