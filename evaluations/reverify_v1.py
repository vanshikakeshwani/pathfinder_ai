"""Re-run frozen V1 Q3-Q5 candidates through the V2 acceptance layer (Phase 1 check).

Input: evaluations/v1/frozen_candidates_Q3_Q5.jsonl, dumped by replaying the V1 recordings with the V1 code
(identical excerpts, contexts, V1 verdicts and V1 outcomes). V1 recordings are not modified.
The V1 plans have no alternative kinds, so one live call per question annotates kinds and defining features
with the V2 planner rules; then the V2 verifier and acceptance rule run on the same excerpts and contexts.

  python evaluations/reverify_v1.py  ->  evaluations/v2/reverify_Q3_Q5.jsonl + summary on stdout
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from pydantic import BaseModel

from pathfinder.config import load_settings
from pathfinder.grounding import Registry
from pathfinder.llm import GatewayLLM, StructuredLLM
from pathfinder.models import AlternativeDraft, ExtractionCandidate, ResearchPlan
from pathfinder.retry import CancelToken
from pathfinder.telemetry import Budget, Telemetry
from pathfinder.tools.base import PageContent
from pathfinder.verification import acceptance_failure, verify

IN = Path("evaluations/v1/frozen_candidates_Q3_Q5.jsonl")
OUT = Path("evaluations/v2/reverify_Q3_Q5.jsonl")

ANNOTATE_SYSTEM = """For each listed comparison alternative, set kind = "named" for a specific product,
company or project, or "approach" for a conceptual option or architecture pattern. For approaches give 2-4
defining_features that distinguish it from the other alternatives in ordinary text. Keep names unchanged;
aliases [] and official_domains [] for approaches."""


class Annotations(BaseModel):
    alternatives: list[AlternativeDraft]


def main() -> int:
    s = load_settings()
    budget = Budget.from_settings(s)
    tel = Telemetry("REVERIFY", s.secret_values())
    llm = StructuredLLM(GatewayLLM(s), s, budget, tel, CancelToken())
    records = [json.loads(x) for x in IN.read_text("utf-8").splitlines() if x.strip()]
    out = []
    for qid in ("Q3", "Q4", "Q5"):
        recs = [r for r in records if r["qid"] == qid]
        alts = recs[0]["plan_alternatives"]
        ann = llm.call("annotate", ANNOTATE_SYSTEM, {"question": recs[0]["question"],
                                                     "alternatives": [a["name"] for a in alts]}, Annotations)
        kinds = {a.name: a for a in ann.alternatives}
        for a in alts:
            k = kinds.get(a["name"])
            a["kind"] = k.kind if k else "named"
            a["defining_features"] = k.defining_features if k else []
        plan = ResearchPlan(question=recs[0]["question"], mode="comparison", alternatives=alts,
                            criteria=recs[0]["plan_criteria"], assumptions=["V1 plan, kinds annotated for V2"],
                            initial_queries=["n/a"])
        print(qid, "kinds:", {a.name: a.kind for a in plan.alternatives})
        reg = Registry()
        cands = []
        for i, r in enumerate(recs):
            c = r["candidate"]
            context = r["context"]
            src, _ = reg.add_page(PageContent(url=f"https://frozen.v1.example/{qid}/{i}", title="frozen", text=context))
            start = src.content.find(c["excerpt"])
            cand = ExtractionCandidate(**{**c, "start": max(start, 0), "end": max(start, 0) + len(c["excerpt"]),
                                          "source_id": src.source_id, "scope": "general",
                                          "rubric_rationale": c.get("rubric_rationale") or ""})
            cands.append((r, cand))
        verdicts = {}
        for b in range(0, len(cands), 10):  # verifier batches of 10
            batch = [c for _, c in cands[b:b + 10]]
            verdicts.update(verify(llm, plan, reg, batch).verdicts)
        for r, c in cands:
            v = verdicts.get(c.candidate_id)
            ctx_text = reg.context_window(c.source_id, c.start or 0, c.end or 0)
            full = acceptance_failure(plan, c, v, ctx_text)
            # V1 candidates were extracted before rubric_rationale existed: also report the outcome with only
            # that rule waived, which isolates the identity/support layers that Phase 1 changed.
            no_rat = acceptance_failure(plan, c, v, ctx_text, require_rationale=False)
            out.append({"qid": qid, "target_id": c.target_id, "entity_kind": plan.alternative(c.entity).kind,
                        "excerpt": c.excerpt, "claim": c.claim, "proposed_score": c.proposed_score,
                        "v1_outcome": r["v1_outcome"], "v1_reason": r["v1_reason"],
                        "v2_outcome": "accepted" if full is None else "rejected", "v2_reason": full or "",
                        "v2_identity_layer_outcome": "accepted" if no_rat is None else "rejected",
                        "v2_identity_layer_reason": no_rat or "",
                        "v2_verdict": v.model_dump() if v else None})
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(json.dumps(o, ensure_ascii=False) for o in out) + "\n", encoding="utf-8")

    def bucket(reason: str) -> str:
        if not reason:
            return "accepted"
        for key in ("lexical", "approach identity", "verdict=partial", "verdict=irrelevant", "verdict=contradicts",
                    "no derivable", "rubric rationale", "not about this", "does not address", "instruction-like"):
            if key in reason:
                return key
        return reason[:40]

    print("\ntransitions V1 -> V2 identity/support layer (rationale rule waived for V1 candidates):")
    for (q, v1, v2), n in sorted(Counter((o["qid"], bucket(o["v1_reason"] or ""),
                                          bucket(o["v2_identity_layer_reason"])) for o in out).items()):
        print(f"  {q}: {v1:20} -> {v2:22} x{n}")
    print("\nfull V2 rule (includes the rationale requirement V1 candidates cannot meet):",
          dict(Counter(o["v2_outcome"] for o in out)))
    usage = [c["usage"] for c in tel.llm_calls if c.get("usage")]
    print("\nLLM requests:", len(tel.llm_calls), "tokens:", sum(u.get("total_tokens", 0) for u in usage),
          "reported cost:", round(sum(u.get("cost", 0) or 0 for u in usage), 6))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
