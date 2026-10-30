# Demo video script (4 minutes)

Record the screen in PowerShell from the project folder. Label the synthetic part on screen as **SYNTHETIC**. Have these files open in an editor beforehand:
- `samples\EVAL_Q5_r1_adaptive_…\report.md`
- `evaluations\v2\EVALUATION_ANALYSIS.md`
- `evaluations\v3\pilot_v31\PILOT_V31_ANALYSIS.md`

| Time | Say | Show / run |
|---|---|---|
| 0:00–0:25 | **The problem:** a fixed research plan spends searches on facts that cannot change the decision. Pathfinder asks which missing fact could change, or make defensible, the recommendation, and only recommends when the evidence supports it. | README title and the "How it works" section |
| 0:25–0:55 | **The architecture:** one LangGraph agent with 8 nodes. Exa Search and Get Contents are separate tools. Grounding (a verbatim excerpt) is separate from verification (does it support the score). There are hard budgets. | The graph line in README, then `pathfinder\graph.py` (`build_graph`) |
| 0:55–1:50 | **SYNTHETIC demo:** X = [11,11], Y = [6,16]. Y's cost is the only cell that can change the leader (priority 10). The flip case changes the leader, the confirm case keeps it, and the no-progress case rejects an irrelevant page and stops. | `.\.venv\Scripts\python.exe -m pathfinder.cli demo-fixture --case all` |
| 1:50–2:50 | **Live run:** GPT-6 Luna and Exa. Point at the targeted rounds and their reasons (decision factor, reachability), the cited findings, and why the recommendation is withheld. | `.\.venv\Scripts\python.exe -m pathfinder.cli run --question "Compare Qdrant, Weaviate, and Milvus for a small team building RAG; consider deployment, filtering and operational effort."` then open `outputs\RUN_…\report.md`. If time or network is short, open the saved real sample in `samples\` instead and say it is a recorded live run. |
| 2:50–3:35 | **Honest evaluation:**<br>• V2: with a fair round-robin baseline and the same stop rule, adaptive did **not** beat static (69 vs 70 cells).<br>• The V3 pilots found and fixed a scoring defect (disputes could never resolve).<br>• V3.1 pilot: all 8 correctness checks passed; 22 vs 21 vs 18 cells over three questions, descriptive only.<br>• The V3.2 benchmark was stopped early for the deadline. | `evaluations\v2\EVALUATION_ANALYSIS.md` (headline table), `evaluations\v3\pilot_v31\PILOT_V31_ANALYSIS.md` (section 2), `evaluations\v3\benchmark_v32\` |
| 3:35–4:00 | **Limits:**<br>• scores are rubric judgements;<br>• the verifier is the same model family;<br>• source and cost-dimension detection are heuristics;<br>• no human review yet;<br>• "consensus" is not proof. | `docs\tradeoffs.md` |

Questions to rehearse:
- Why was cost researched next in the demo?
- What changes if its weight is 1?
- What makes the agent stop, and why is the rule the same for every strategy?
- Why isn't the priority a probability?
- Why isn't grounding the same as support?
- Why was the recommendation withheld?
- Why didn't adaptive beat static in V2, and what did V3 change?
