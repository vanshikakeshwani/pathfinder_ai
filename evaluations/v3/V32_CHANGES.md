# V3.2: pre-benchmark scoring corrections (offline only)

> Made after the V3.1 live pilot (`pilot_v31/PILOT_V31_ANALYSIS.md`). No paid call has been made since that pilot.
> **Unchanged:**
> - all historical artifacts (571 hash-verified files);
> - V2, the V3 pilot and the V3.1 pilot each replay exactly with their frozen code (0 differences);
> - plans, budgets, the static schedule, queries, extraction and verification prompts, and the stop rule.

## Defects fixed

| # | Defect | Evidence | Fix | Applies to |
|---|---|---|---|---|
| 1 | Cost dimension misclassified when a passage has several amounts | "The infrastructure is $530/month. The real cost is $3,530/month." The score (0) is for the $3,530 total, but v3.1 filed it as recurring infrastructure, which created a false dispute in Q5 V3.1 | `cost_dimension` now classifies the **scored quantity**: unit plus the sentence stating the verified raw value, then unit plus the verified claim, then the excerpt | scoring, all arms |
| 2 | Total-cost wording not recognised | "real/true/total/actual/overall/all-in cost", "including engineering/staff/ops", "engineering time is priced in", "beyond infrastructure", "infrastructure plus engineering" | Explicit total-cost-of-ownership patterns. A quantity naming **both** an infrastructure component and a labour component is total cost. A monthly amount is no longer assumed to be infrastructure ("0.15 FTE costs $2,428 a month" is labour). | scoring, all arms |
| 3 | **Substring matching** (found while fixing 1) | v3.1 matched "fte" inside "af**te**r", filing Pinecone's "$280/mo just for vectors" as engineering labour | Word-bounded regular expressions | scoring, all arms |
| 4 | Product heterogeneity inside conceptual alternatives | Q5 static Managed:startup_cost was a 2-vs-1 "consensus" over Zilliz, Qdrant/Pinecone and Weaviate prices | For **cost** criteria of **approach-type** alternatives, contributing families that name disjoint products mark the cell `heterogeneous`:<br>• the products are listed in the record;<br>• a consensus becomes kind `heterogeneous` (never strong);<br>• factual confidence is capped at moderate;<br>• reachability is "needs product/plan-specific criterion".<br>Nothing is merged or suppressed. Non-cost properties shown by several products (independent examples of an approach-level property) and named alternatives are not flagged. | scoring and readiness, all arms |
| 5 | Ambiguous cost dimension could support readiness | e.g. "Zilliz Cloud is cheaper" (no measurable dimension) | `ambiguous_dimension` flag on cost cells | readiness, all arms |
| 6 | **v2_policy arm used V3 retry logic in discovery mode** (found while preparing the benchmark; no effect on the pilots, which had only comparison questions) | `coverage.choose_next_discovery` checked only `retry_handling` | The legacy V2 arm now keeps V2 discovery behaviour exactly (test `test_v2_policy_arm_uses_v2_discovery_behaviour`) | v2_policy arm |

New readiness blockers (shared by all arms):
- `heterogeneous_products`: a differentiating or leader cost cell rests on prices of different products.
- `ambiguous_cost_dimension`: a differentiating or leader cost cell includes evidence whose dimension can't be determined.

All earlier safeguards remain: citation, independence, authority, dispute, reachability and scope.

**Reporting:** `units_strict_supported` (state `supported` only) is reported in every table next to `units_consensus` and the total. The report has its own paired-difference line for strictly supported coverage. `units_heterogeneous` and `units_ambiguous_dimension` are also reported.

**Protocol:** `v3.2`, which gives a new snapshot fingerprint.

## Files changed

| Kind | Files |
|---|---|
| Changed | `pathfinder/consensus.py` (dimension classifier, product heterogeneity, reachability), `pathfinder/models.py` (`heterogeneous`, `ambiguous_dimension`), `pathfinder/matrix.py` (approach flag, confidence cap), `pathfinder/readiness.py` (two blockers), `pathfinder/coverage.py` (V2 discovery fairness), `pathfinder/graph.py` and `pathfinder/evaluation.py` (v3.2 metrics, protocol), `pathfinder/eval_report.py` (strict vs consensus columns and paired line), `tests/test_eval.py` (protocol v3.2) |
| New | `tests/test_cost_and_products.py` (22 tests), one test in `tests/test_retry_policy.py`; `evaluations/v3/pilot_v31/` (`code_snapshot/` with checksums, `replay_pilot_v31.py`, `rescoring_baseline_v31_rules.json`, `rescore_pilot_v32.py`, `RESCORING_V32.md` / `.json`) |

## Retrospective (V3.1 pilot evidence, offline; `pilot_v31/RESCORING_V32.md`)

- **8 evidence-level dimension changes, all in Q5:**
  - the known $3,530 total-cost excerpt;
  - Pinecone's $280/month (labour → infrastructure; the substring bug), in V3.1 and v2_policy;
  - "infrastructure spend and staff time" (labour → total cost), in all three arms;
  - "once engineering time is priced in" (labour → total cost), in V3.1 and v2_policy.
- **2 cells changed state or kind:**
  - Q5 V3.1 Self-hosted:startup_cost: *disputed* → *dimension split* (recurring infrastructure 1, total cost 0), removing the false dispute;
  - Q5 static Managed:startup_cost: weak consensus → *heterogeneous* consensus. It also gained an ambiguous-dimension flag from the Zilliz excerpt.
- **4 other cells** changed only their dimension labels.
- **No change** to supported, strictly supported or consensus counts, leaders, stability or recommendations. Static Q5 gained two additional withholding reasons; it was already withheld.
