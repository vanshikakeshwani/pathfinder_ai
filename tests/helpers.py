"""Builders for evidence/cells used by matrix, policy, readiness and flip tests (SYNTHETIC)."""

from __future__ import annotations

from pathfinder.matrix import build_cells
from pathfinder.models import Evidence

_counter = {"n": 0}


def ev(target: str, score: int | None, source: str = "SRC_1", entity: str | None = None,
       excerpt: str | None = None, scope: str = "general") -> Evidence:
    _counter["n"] += 1
    n = _counter["n"]
    return Evidence(evidence_id=f"EV_T{n}", candidate_id=f"C{n}", source_id=source,
                    excerpt=excerpt or f"synthetic excerpt number {n}", start=0, end=10, target_id=target,
                    entity=entity or target.split(":")[0], claim="synthetic claim", score=score,
                    score_basis="verified_proposal" if score is not None else "none", scope=scope,
                    rubric_rationale="synthetic rationale" if score is not None else "")


DOMAINS = {"SRC_1": "vendorx.example", "SRC_2": "vendory.example", "SRC_3": "thirdparty.example",
           "SRC_4": "another.example", "SRC_5": "third.example"}
PUBLISHED: dict[str, str | None] = {k: None for k in DOMAINS}


def cells(plan, evidence):
    return build_cells(plan, evidence, DOMAINS, PUBLISHED)


def round0_evidence():
    """PF-1 state: X cost=1, X deploy=2, Y deploy=2, Y cost unknown."""
    return [ev("VendorX:cost", 1, "SRC_1"), ev("VendorX:deployment", 2, "SRC_1"),
            ev("VendorY:deployment", 2, "SRC_2")]
