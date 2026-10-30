# Pathfinder AI V3: what changed, why, and the intended causal effect

> **Status:** implemented and tested offline only. **No live V3 run has been made.** Nothing here is evidence of live performance. Each claim about an intended effect is a hypothesis for the controlled pilot and benchmark (`PREREGISTRATION.md`).
> **Unchanged:**
> - the architecture: 8 LangGraph nodes plus the `decide` router;
> - the providers: GPT-6 Luna through the Experiential Labs gateway, plus Exa Search and Get Contents;
> - provenance, grounding and verification;
> - Pydantic validation, the injection defences and the CLI;
> - the planner, extraction and verifier prompts;
> - the budgets;
> - the static baseline's schedule and queries.
>
> V2 stays reproducible with its frozen code: `python evaluations/v2/replay_v2.py` gives 0 differences.

Root causes R1–R10 are in `DIAGNOSIS_V2.md`.

## 1. Decision-aware acquisition (`pathfinder/acquisition.py`, adaptive arm only) — R2, R3, R5

```
priority = weight × uncertainty × decision_factor × exploration_factor × retry_factor / cost_units   (cost_units = 2)
```

| Term | Definition | Interpretation |
|---|---|---|
| weight | criterion weight 1–5 (user > inferred > default 3) | importance |
| uncertainty | cell interval width (unknown/insufficient 2, disputed max−min); 1 for a corroboration target | how much the cell's score can still move |
| decision_factor | **2.0** if resolving this cell **alone** can change the leader, break a tie or make the leader interval-robust, or it is the only readiness blocker of a robust leader. **1 + 1/k** if it belongs to a *minimal group* of k ≥ 2 cells that can jointly do so, or is one of k readiness blockers. **1.25** if it can rule out another alternative. **1.0** for coverage only. **0.5** for coverage only on an alternative already ruled out. | potential effect on a defensible decision |
| exploration_factor | 1 / (1 + 0.5·n), where n = rounds among the last two spent on this alternative while others still have valuable targets; ×1.2 for an alternative never targeted | balance across alternatives |
| retry_factor | 0.5^failures | redundancy risk after misses |

How the decision factor is computed:
- **Counterfactuals:** each open cell is pinned to every score its interval allows (0/1/2, or the observed range of a dispute), and the deterministic outcome is recorded: leader, stability and alternatives ruled out. Criterion directions and the rubric are already in the 0–2 fit scores.
- **Groups:** an exact search over combinations of 2–4 open cells finds the smallest groups that can *jointly* change the leader or make it robust. It is minimal by construction: no group is reported when a single cell suffices.
- **Recorded:** every action stores the full calculation in `analysis` (bounds, counterfactual values, groups, readiness blockers, the top 6 candidates with all factors, skipped targets with reasons) plus a plain-English `why_selected`.
- **Not probabilities:** a counterfactual says what *could* change, never how likely it is.

Intended effect: stop spending rounds on cells that cannot matter, and stop treating jointly decisive cells as irrelevant.

## 2. Retry policy (adaptive arm; discovery too) — R1, R10

- **Failure memory:** a target *fails* when its round yields no new verified evidence for that target. For corroboration, failure means no new independent source and no change to the cell.
- **Cool-down:** a target that failed in the previous round is skipped while other eligible targets exist.
- **Bounded retry:** an immediate retry is allowed once, only for a uniquely decisive target (factor 2, and no other eligible target with factor ≥ 1.5), and always with a different, broadened query.
- **No permanent blacklist:** a failed target may be revisited later at half priority per failure. Its label depends on why: `targeted` when its decision value grew since the failure (new information), otherwise `fallback_exploration`.
- **Query ladder:** at most 3 attempts per target, each with a distinct query variant:
  - attempt 0: official documentation, or "trade-offs" for approach alternatives;
  - attempt 1: "independent review comparison";
  - attempt 2: keywords from the criterion's description;
  - conflicts get their own "detailed evidence version differences" wording.

  Near-duplicates (token Jaccard ≥ 0.8 with an issued query) are skipped.
- **Unusable pages** stay remembered and are never refetched, as in V2.
- **Labels:** each action is tagged `first_exploration`, `targeted`, `corroboration`, `conflict_resolution`, `bounded_retry`, `fallback_exploration`, or `static_schedule` for the baseline.

Intended effect: recover from a miss by moving to the next valuable target instead of repeating it (V2: 10 of 11 repeats followed a failure, and only 3 succeeded).

## 3. Disagreements (`pathfinder/matrix.py`, scoring for both arms) — R4

| State | Meaning | Interval | Counts as supported? |
|---|---|---|---|
| unknown | no verified evidence | [0, 2] | no |
| **insufficient** (new) | researched; on-target candidates could not justify a score (verdict `partial`, or no derivable score) | [0, 2] | no |
| supported | consistent verified evidence | [s, s] | yes |
| scope_dependent | consistent within each context, but the contexts differ | [min, max] | yes (as in V2) |
| disputed | comparable (same-context) sources disagree | **[min, max] of the verified scores** (V2: [0, 2]) | **no** |

- **What stays the same:**
  - a dispute never counts as covered;
  - its factual confidence is `low`;
  - scores are not averaged and no credible source is dropped;
  - copies of the same excerpt count once;
  - 0-vs-2 is still [0, 2].
- **What changes:** a 1-vs-2 dispute keeps the information that every verified source said "at least 1".
- **Why the narrowing is justified:** the lower bound is the *lowest* verified score, so no source is overruled.
- **New metrics:** supported, disputed, unknown, insufficient and evidenced (supported + disputed) are reported separately. Also reported: disputes seen and resolved, and *consequential* disputes (decision-relevant when they arose) and how many of those were resolved.
- **Adaptive only:** conflict-directed research. A disputed cell is a `conflict_resolution` target, valued by its counterfactual effect like any other cell.

Intended effect: more evidence no longer erases information, and the metrics no longer reward finding fewer contradicting sources.

## 4. Recommendation readiness (`pathfinder/readiness.py`, both arms) — R5

Interval leader, interval robustness, factual confidence and readiness stay separate. `ready` still requires all of these:
- an interval-robust leader;
- no comparability issue on a differentiating criterion;
- every differentiating cell with high factual confidence.

New named blockers, all of which withhold the recommendation:
- `leader_disputed`: the leader's own score on a criterion is disputed;
- `critical_unsupported`: a criterion with weight ≥ 4 has no supported score for the leader;
- `self_reported`: the leader's advantage on a differentiating criterion is an evaluative judgement taken only from the leader's own domain. Threshold-scored facts such as prices are exempt.

The adaptive policy targets blockers at **any** stability, not only once robust. The factor is 2 (or 1 + 1/k) for a robust leader, and 1 + 1/(k + 1) for a provisional one.

**Corroboration is never assumed to succeed:** a disagreeing new source makes the cell disputed, and the recommendation stays withheld (tested).

## 5. Planning and baseline fairness (`pathfinder/evaluation.py`) — R8

- **Fixed plans:** one plan per question, reused by every repetition and arm (`--plans-dir evaluations/v3/plans`). The six plans are the V2 repetition-1 plans, regenerated **offline** from the recorded planner responses (byte-identical hashes; `freeze_plans.py`; provenance and validation in each file).
- **Retrieval still varies:** each repetition has its own snapshot store.
- **Shared within a repetition:** every arm uses the same plan, an identical round 0 (checked by hash), the same budgets, query builder, verifier, scoring and stop rule. The only intended difference is which target is researched next.
- **Static unchanged:** the same diagonal round-robin and attempt-0 queries as V2 (test `test_static_schedule_is_unchanged_by_v3`). It does not skip cells that are already supported, which would be adaptive behaviour.
- **No look-ahead:** the adaptive policy sees only its own past state. The offline test `test_reconstruction_reproduces_every_live_v3_decision` rebuilds every live V3 decision from earlier-round evidence alone.
- **Ablation arms:**
  - `v2_policy`: the unchanged V2 policy under V3 scoring and stopping, i.e. the controlled V2-vs-V3 policy comparison;
  - `no_retry`, `no_decision`, `no_readiness`, `no_conflict`, `no_exploration`: one component switched off each.
- **Protocol `v3`:** a new snapshot fingerprint, so V2 recordings are never mixed in.

## 6. Common stopping rule (`pathfinder/graph.py`, identical for every arm) — R6, R7

- Round 0 no longer counts toward `no_progress`. It was already exempt from triggering a stop; now it is also not counted.
- A round with a tool or LLM failure (timeout, verifier unavailable) that makes no progress is logged as `provider_failure_round` and not counted.
- `no_progress` is deferred while any decision-relevant open cell has never been attempted by this run. Budgets and round caps still bound the run.
- `stable` still requires robust **and** ready.
- Evaluation still runs to the full budget and reports both views, so stopping value stays separate from targeting value.

Intended effect: no premature stops from empty or failed rounds. Trade-off: fewer actions saved by stopping. Re-evaluated offline on the V2 trajectories, the V3 rule saves 3 actions instead of 30 and loses 0 units instead of 7.

## 7. Flip metrics — R9

- The V2 definition of a counted flip (`leader_changed`) is **preserved**, and V2's historical count (1) is untouched.
- V3 adds `strong_flips`: a real leader replaced by a different real leader, with no tie on either side. `tie_flips` is the remainder. Both are reported; neither replaces the other.

## Files

| Kind | Files |
|---|---|
| New | `pathfinder/acquisition.py`, `pathfinder/trace_replay.py`; `evaluations/v3/` (`diagnose_v2.py`, `freeze_plans.py`, `offline_policy_comparison.py`, `plans/`, docs); `evaluations/v2/` (`code_snapshot/` plus checksums, `replay_v2.py`, archived reports) |
| Changed | `models.py` (states, action kind, analysis), `matrix.py`, `readiness.py`, `queries.py` (variants 2+, conflict wording, near-duplicates; attempts 0/1 unchanged), `coverage.py`, `graph.py`, `policy.py` (`is_strong_flip`), `reports.py`, `evaluation.py`, `eval_report.py`, `cli.py`, `pyproject.toml` (Ruff excludes the frozen snapshot) |
