# Human review rubric

Fill this in only from real runs (`evaluate --record`). Score each item **0** (absent or incorrect), **1** (partial) or **2** (clear or strong). An LLM self-rating is never the only evaluation.

| # | Dimension |
|---|---|
| 1 | Answers the question that was asked |
| 2 | Covers the required criteria, facets or entities |
| 3 | Factual claims have inspectable sources and actual excerpts |
| 4 | The excerpts genuinely support the claims they're attached to (check `verification_log.jsonl` for wrongly accepted or wrongly rejected items) |
| 5 | Uncertainty, assumptions and missing information are stated honestly |
| 6 | Tool choices advance the task (`decision_trace.jsonl` → `action_selected` reasons) |
| 7 | No fabricated citation IDs or unsupported claims |
| 8 | Useful next actions and a clear structure |

## Per-run sheet

| Run ID | Q | Arm | Reviewer | Date | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Wrongly rejected evidence | Notes / corrections |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

## Coverage audit (for the coverage metrics)

For each required criterion or facet, mark whether **real** supporting evidence exists. Ignore whether the answer merely sounds complete.

| Run ID | Requirement unit | Supported? (y/n) | Evidence IDs | Reviewer note |
|---|---|---|---|---|

## Fault fixtures

Fault fixtures are scored as binary assertions by `pytest`: safe stop, no unauthorized calls, no false support. They are not scored here.
