"""Discovery/coverage mode. Never invents a winner; tracks which facets have verified evidence.

Entity mode (target_entity_count > 0): an entity counts as verified only when EVERY facet has
verified evidence for that entity. Topic mode (target_entity_count == 0): each facet needs
`required_count` verified evidence items. Unknown stays missing, never assumed false.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field

from pathfinder.models import Evidence, Facet, ResearchAction, ResearchPlan
from pathfinder.queries import build_discovery_query

_SUFFIXES = re.compile(r"\b(inc|ltd|llc|corp|corporation|pvt|private|limited|technologies|technology|"
                       r"labs|software|co)\b")
MAX_ATTEMPTS_PER_TARGET = 2


def entity_key(name: str) -> str:
    low = _SUFFIXES.sub(" ", name.lower())
    return re.sub(r"[^a-z0-9]", "", low) or re.sub(r"[^a-z0-9]", "", name.lower())


@dataclass
class EntityRecord:
    key: str
    name: str
    facets: dict[str, list[str]] = field(default_factory=dict)  # facet_id -> evidence ids

    def verified(self, facet_ids: list[str]) -> bool:
        return all(self.facets.get(f) for f in facet_ids)


@dataclass
class Coverage:
    required_units: int
    verified_units: int
    entities: dict[str, EntityRecord]
    facet_status: dict[str, str]  # facet_id -> covered | partial | missing
    facet_evidence: dict[str, list[str]]
    covered_pairs: set[tuple[str, str]]

    @property
    def progress(self) -> float:
        return 1.0 if self.required_units == 0 else min(1.0, self.verified_units / self.required_units)

    @property
    def complete(self) -> bool:
        return self.verified_units >= self.required_units

    def as_json(self, plan: ResearchPlan) -> dict:
        ids = [f.facet_id for f in plan.facets]
        return {
            "required_units": self.required_units, "verified_units": self.verified_units,
            "progress": round(self.progress, 3), "facet_status": self.facet_status,
            "facet_evidence": self.facet_evidence,
            "entities": [{"name": e.name, "verified": e.verified(ids), "facets": e.facets}
                         for e in self.entities.values()],
        }


def compute_coverage(plan: ResearchPlan, evidence: list[Evidence]) -> Coverage:
    facet_ids = [f.facet_id for f in plan.facets]
    entities: dict[str, EntityRecord] = {}
    facet_evidence: dict[str, list[str]] = {f: [] for f in facet_ids}
    for e in evidence:
        if e.target_id not in facet_evidence:
            continue
        facet_evidence[e.target_id].append(e.evidence_id)
        key = entity_key(e.entity)
        rec = entities.setdefault(key, EntityRecord(key=key, name=e.entity))
        rec.facets.setdefault(e.target_id, []).append(e.evidence_id)
    pairs = {(k, f) for k, r in entities.items() for f in r.facets}

    if plan.target_entity_count > 0:
        verified = sum(1 for r in entities.values() if r.verified(facet_ids))
        required = plan.target_entity_count
        status = {}
        for f in facet_ids:
            n = sum(1 for r in entities.values() if r.facets.get(f))
            status[f] = "covered" if n >= required else "partial" if n else "missing"
    else:
        required = sum(f.required_count for f in plan.facets)
        verified = sum(min(len(facet_evidence[f.facet_id]), f.required_count) for f in plan.facets)
        status = {f.facet_id: ("covered" if len(facet_evidence[f.facet_id]) >= f.required_count
                               else "partial" if facet_evidence[f.facet_id] else "missing")
                  for f in plan.facets}
    return Coverage(required, min(verified, required), entities, status, facet_evidence, pairs)


def progress_units(before: Coverage, after: Coverage, plan: ResearchPlan) -> int:
    if plan.target_entity_count > 0:
        return len(after.covered_pairs - before.covered_pairs)
    return after.verified_units - before.verified_units


def choose_next_discovery(plan: ResearchPlan, cov: Coverage, attempts: Mapping[str, int],
                          action_no: int) -> ResearchAction | None:
    if cov.complete:
        return None
    facets = {f.facet_id: f for f in plan.facets}

    # (-priority, n_evidence, target, facet, entity, why); queries come from the shared builder
    candidates: list[tuple[float, int, str, Facet | None, str | None, str]] = []
    if plan.target_entity_count > 0:
        partial = [r for r in cov.entities.values() if not r.verified(list(facets))]
        for r in partial:
            for fid, f in facets.items():
                if r.facets.get(fid):
                    continue
                candidates.append((-float(f.importance), 0, f"{r.name}|{fid}", f, r.name,
                                   f"{r.name} is missing verified evidence for '{f.description}' "
                                   f"(importance {f.importance})."))
        known = sum(1 for r in cov.entities.values() if r.verified(list(facets))) + len(partial)
        if known < plan.target_entity_count:
            top = max(plan.facets, key=lambda f: f.importance)
            candidates.append((-float(top.importance) + 0.5, 0, "new_entities", top, None,
                               f"Only {known} candidate entities known; {plan.target_entity_count} required."))
    else:
        for f in plan.facets:
            missing = f.required_count - len(cov.facet_evidence[f.facet_id])
            if missing > 0:
                candidates.append((-float(f.importance * missing), len(cov.facet_evidence[f.facet_id]),
                                   f.facet_id, f, None,
                                   f"Facet '{f.facet_id}' has {len(cov.facet_evidence[f.facet_id])}/"
                                   f"{f.required_count} verified items (importance {f.importance})."))

    for neg_priority, _, target, facet, entity, why in sorted(candidates, key=lambda c: (c[0], c[1], c[2])):
        tried = attempts.get(target, 0)
        if tried >= MAX_ATTEMPTS_PER_TARGET:
            continue
        query = build_discovery_query(plan, facet, entity, tried)
        if tried:
            why += " Retry with a broadened query."
        return ResearchAction(action_id=f"ACT_{action_no}", target_id=target, queries=[query],
                              predicted_gain=-neg_priority, estimated_cost_units=2.0,
                              action_score=-neg_priority / 2.0, why_selected=why)
    return None
