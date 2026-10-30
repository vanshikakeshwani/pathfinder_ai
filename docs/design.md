# Pathfinder AI: design and mechanics

Pathfinder is a CLI research agent. For a comparison question it builds an alternatives × criteria matrix, represents unknowns as score **intervals**, and spends each next search on the missing fact that **could change the recommendation**. It stops when more research can't change the result under the stated rubric, or when a budget or progress limit is hit. For list or overview questions it tracks facet coverage instead and never invents a winner.

> Detailed design notes (moved from the README). Status, setup and results: `README.md`; version history: `evaluations/`.

## Why an agent, and why a graph

A fixed list of searches often gathers content that cannot change the answer. Pathfinder re-plans after every round. It asks which unknown cell could flip the leader, and whether there is still budget to find out. That loop has branches: search → nothing new, page empty, evidence rejected, stop or continue. A small LangGraph `StateGraph` makes each of these transitions explicit and inspectable:

```
START → plan → choose_action → search → retrieve → extract → verify → update_state ─(decide)→ choose_action …
                                                                                            └→ report → END
```

There are 8 nodes, plus a `decide` router on the edge after `update_state`. Plain Python guards every edge: budgets, round counts, no-progress, cancellation. The LangGraph recursion limit is only a backstop. The agent is a single agent with no memory database and no UI.

## Tools

| Tool | Operation | Why it is separate |
|---|---|---|
| **Exa Search** | `Exa.search(query, contents=False, …)` → URLs and titles | Cheap discovery of candidate pages, optionally restricted to official domains |
| **Exa Get Contents** | `Exa.get_contents(urls, text={max_characters})` → page text | Only fetches the pages the policy chose. Text becomes registered, citable sources. |
| LLM (Experiential Labs gateway, `gpt-6-luna`) | Planning, extraction, support verification, report prose | Model infrastructure, not a research tool. Every output is Pydantic-validated. |

Signatures were checked against `exa-py 2.26.0`. Only these two research operations exist. The LLM never chooses a tool by name, so retrieved text can't add tools.

## How a decision is made

**Scoring rules (per criterion).** Each criterion records its direction (`lower_is_better` for cost, effort and latency), a weight from 1 to 5 with its source (`user` from `--weights` or the question, `inferred`, or `default` = 3, logged as an assumption), and anchors that define fit scores 0, 1 and 2. **2 is always the best fit.** If the user gave numeric limits (e.g. "≤ $20/month is strong"), **the code** computes the score from the verified raw value, not the LLM.

**Cells and intervals.** Cells are built from *verified* evidence only:

| State | Condition | Interval |
|---|---|---|
| unknown | no verified evidence | [0, 2] |
| supported | all verified evidence implies the same score `s` | [s, s] |
| insufficient (V3) | researched, but on-target candidates could not justify a score | [0, 2] |
| scope_dependent | consistent within each declared context (e.g. managed 2, self-hosted 0), but the contexts differ and the user chose none | [min, max] |
| consensus (v3.1) | independent source families agree under conservative rules (≥ 2 certain families, ≥ 2:1, no material/authoritative/version dissent); dissent disclosed | [s, s]; weak consensus caps confidence at moderate |
| disputed | comparable sources disagree without a qualified consensus; labelled by kind (one source's own excerpts, independent disagreement, material, authoritative, version-specific) | [min, max] of the verified scores (V2: [0, 2]); never counted as supported |

A repeated excerpt on several domains counts as **one** independent source.

`LB(a) = Σ weight × lower` and `UB(a) = Σ weight × upper`. An option is **interval-robust** if its LB is strictly greater than every other option's UB. The midpoint is used only to rank investigation priority and is never presented as a score.

**Why pricing gets researched next (synthetic example, cost weight 5, deployment weight 3).** After round 0, X = [11, 11] and Y = [6, 16], so there is no robust winner. For each open cell the policy pins it to 0 and then to 2. If the leader differs between the two, the cell is **flip-relevant**.

```
V3: priority = weight × uncertainty × decision_factor × exploration × retry / cost_units   →   Y:cost = 5 × 2 × 2 × 1 × 1 / 2 = 10
```

(V2 used `weight × width × flip_factor / cost_units`, which gives the same 10 here.) V3's decision factor is 2 for a cell that can change the leader, break a tie or make the leader robust *alone*, 1 + 1/k for a cell in a minimal group of k cells that can do so *jointly*, and lower values for coverage-only cells. Every factor is recorded in the trace (`evaluations/v3/V3_CHANGES.md`).

Y's deployment is already supported, so Y:cost is the only target. If Y's cost is verified as 2, Y becomes [16, 16] and wins: a **leader change**. If it is verified as 0, X becomes robust: a **status change**, with the same leader.

**What changes if cost weight = 1?** X = [7, 7] and Y = [6, 8]. Y:cost is still flip-relevant, but its priority drops from 10 to 2. Test `S04` covers this.

**Why it isn't a probability.** `flip_factor` and `cost_units = 2` are transparent policy constants. This is a value-of-information *proxy*, not Bayesian expected information gain, and the score is not calibrated.

**Three separate measures** appear in every report:
- *factual confidence*: how well-sourced the facts are (number of distinct domains, official source, whether time-sensitive data is dated);
- *decision stability*: `robust`, `provisional` or `undetermined`;
- *flip relevance*: computed per open cell.

The report's overall `confidence` is derived deterministically from these, and the rule is printed in the report.

## Grounding is not support

```
extract (LLM proposes) → grounding (excerpt must exist verbatim; offsets checked/corrected)
                       → verification (separate LLM call, fail-closed) → acceptance rule → matrix
```

A candidate becomes evidence only if **all** of these hold:
- it is grounded;
- the verdict is `supports`;
- the verifier confirms it is about the right entity (`mentions_alternative`) and the right criterion (`addresses_criterion`);
- **identity, by alternative kind:**
  - *named* product: the name or an alias appears in the excerpt's context;
  - *approach* (conceptual option): the verifier attributes the excerpt to this approach (not `multiple` or another alternative), and its identification quote is found verbatim in the source by code;
- for scoped criteria, the excerpt's context (scope) matches;
- for comparisons, a fit score can be derived: either from thresholds on a verified number, or from a model-proposed score whose **rubric rationale** the verifier accepts.

`partial`, `contradicts` and `irrelevant` verdicts are logged and never change a cell. Malformed output, refusals or timeouts from the verifier reject the whole batch. Limitation: the verifier is the same model family, so it isn't ground truth. Human audit is still needed (`evaluations/rubric.md`).

## Interval result vs recommendation (readiness)

The interval outcome (`robust`, `provisional` or `undetermined`) is always computed and traced. A **recommendation** is only made (`ready`) if all of these hold:
- the leader is interval-robust;
- every *differentiating* cell has strong support (more than one independent source, or official);
- no differentiating criterion compares different contexts, such as managed docs vs self-hosting complaints.

Otherwise the report says "Interval result: … Recommendation withheld: <reasons>", and adaptive researches the blocking cells (`#corroborate`).

## What counts as a decision flip

A change is recorded only when this round's **newly verified evidence** changes the recommended option (`leader_changed`, counted in `decision_flip_count`) or its supported status (`became_robust`, `lost_robustness`, `stability_changed`, counted in `status_change_count`). It must also pass a counterfactual check: recomputing without the new evidence restores the previous state.

These are **not counted**: researching a new topic, a narrower interval, a changed score, or a leader that only appears or moves while the state stays `undetermined` (a tie-break artifact). Weight or rubric edits are also not counted.

V3 keeps this definition unchanged and also reports **strong flips** separately: a real leader replaced by a different real leader. A move into or out of a tie counts under the V2 rule but is reported as tie-related.

## What stops the agent

| Stop reason | When |
|---|---|
| `stable` | Comparison: interval-robust winner **with the recommendation ready** (robust but withheld only after corroboration attempts are used up). Discovery: all required units are covered. |
| `no_progress` | `MAX_NO_PROGRESS` (default 2) consecutive targeted rounds with no newly verified cell or facet, or every open target is exhausted. V3: the shared round 0 and provider-failure rounds are not counted, and the stop is deferred while a decision-relevant cell has never been attempted. |
| `budget_exhausted` | `MAX_RESEARCH_ROUNDS`, the search budget or the content-page budget is reached, or an optional `MAX_LLM_CALLS` / `MAX_SECONDS` cap is set and hit |
| `insufficient_evidence` | A run would stop on budget or no-progress with no verified evidence at all |
| `error` | Authentication or configuration failure, or invalid plan output |
| `cancelled` | Ctrl+C or the cancel token. The report is rendered deterministically with no further API calls. |

There is no default LLM-call or wall-clock cap. The run is still bounded: rounds are capped and every call has bounded retries. Worst case is `(1 plan + (R+1) × (extract + verify) + 1 report) × (1 + LLM_MAX_RETRIES)` LLM requests, which is 30 with the defaults (test `G05`).

## Reliability and safety

- Per-request timeouts for the LLM and Exa, and bounded exponential backoff with jitter. `Retry-After` is honoured up to a 60 s ceiling. 401/403 errors stop the run immediately. Every attempt is logged.
- https-only URLs. Localhost, private, loopback and link-local addresses are blocked. Query length and result count are capped.
- Retrieved text is wrapped as `<untrusted_source>` data with the closing tag defanged. LLM output schemas reject unknown fields. Prompt-injection fixtures prove that injected pages can't add tools, leak keys or change decisions (`F13/X06`).
- Keys are held as `SecretStr` and scrubbed from every output file (`G06`). `.env` is gitignored.

## Evaluation (V2 detail; later versions in `evaluations/v3/`)

V3 has no live results yet. Its pilot and benchmark are pre-registered in `evaluations/v3/PREREGISTRATION.md` and wait for spending approval.

**V2 measured result** (3 paired repetitions × 6 questions; descriptive, no significance claims):

| | Static | Adaptive |
|---|---|---|
| Units supported, common-stop view (of 142) | 70 | 69 |
| Units supported, full-budget view (of 142) | 75 | 71 |
| Pairs where adaptive had better / equal / worse coverage (common-stop) | — | 5 / 7 / 6 |
| Research actions (common-stop) | 254 | 245 |

- **Variance:** repetition-to-repetition variance exceeds the arm difference on every question.
- **Recommendations:** 1 ready recommendation in 36 runs.
- **Decision flips:** 1 counted. It was weak: the round ended in a tie.
- **Cost:** provider-reported total $1.37. Estimated $1.52, because 130 gateway calls reported cost 0.
- **Why adaptive didn't help:** see `evaluations/EVALUATION_ANALYSIS.md`. In short:
  - 29% of adaptive rounds retried the same target;
  - flip-relevant cells were rare;
  - more evidence created disputes, which lowered measured coverage.

### Protocol

`evaluations/queries.json` holds the shared benchmark with its wording preserved:
- comparisons: Q1, Q3, Q4 and Q5;
- discovery: Q2, plus the project-added **Q8**, because the blueprint requires two discovery questions;
- optional: Q6 and Q7.

**Pairing.** Each repetition freezes one plan. Both arms share that plan and an identical round 0, with identical budgets and identical extraction, verification and scoring code.

**Static baseline.** A fixed round-robin over alternatives × criteria, using the **same query builder** as adaptive. The only policy difference is which target comes next.

**Stopping.** Both arms use one common stop rule. Each run goes to the full budget and is reported twice: `common_stop` (the prefix where the rule fires) and `full_budget`. This separates targeting value from stopping value.

**Replay and costs.**
- Record/replay makes runs repeatable. Snapshots are keyed by a config fingerprint plus the protocol version.
- Costs are provider-reported (Exa `cost_dollars`, gateway `usage.cost`), not an invoice.
- Elapsed time isn't comparable, because the second arm reuses the cached round 0.

```bash
python -m pathfinder.cli evaluate --record --repeat 3 --max-usd 1.60   # live, spend-guarded
python -m pathfinder.cli evaluate --replay --repeat 3                  # no network
python -m pathfinder.eval_report outputs/<record_dir> --replay outputs/<replay_dir>
```

## Known limitations

- Scores are model-assisted assessments under an LLM-drafted rubric. The planner can miss a decisive criterion.
- Flip relevance tests one cell at a time. Joint uncertainty across several cells isn't modelled.
- V2: disputed cells fell back to [0, 2] even for close conflicts (1 vs 2), so more sources could *lower* coverage (V2 analysis §4.3). V3 keeps the verified range [min, max]; disputes are still never counted as supported.
- Approach identity relies on the verifier plus a verbatim quote. The quote proves grounding, not meaning.
- The gateway's `usage.cost` was 0 for some calls that used tokens, so LLM cost is under-reported. The evaluation adds an estimate and the spend guard uses it.
- Factual confidence uses domain diversity as a proxy for independence. Two domains can still copy each other.
- The deterministic findings list is one finding per evidence item. The LLM prose summary is optional and its citations are validated.
- Replays reproduce results exactly except run IDs, timestamps and latencies.

## Project layout

```
pathfinder/   config, models, llm (gateway + fixture), tools/ (Exa + fixtures), grounding, verification,
              scoring, matrix, readiness, policy (V2), acquisition (V3), queries, coverage, planner,
              extraction, graph, reports, replay, trace_replay, evaluation, eval_report, cli
tests/        offline suite: F01–F16, X01–X10, PF-1–3, V/S/D/G/E series
evaluations/  queries.json, rubric.md, EVALUATION_REPORT.md + EVALUATION_ANALYSIS.md (V2), review/, v1/ (archived),
              v2/ (archive + frozen code + replay_v2.py), v3/ (diagnosis, changes, plans, offline comparison)
samples/      3 real V2 runs (+ v1/ archived)
docs/         architecture.md, tradeoffs.md, demo-script.md, submission-readiness.md
```

AI assistance: this repository was implemented with an AI coding assistant (Claude Code) from the candidate's specification. Disclose this if the programme's policy requires it.
