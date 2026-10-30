"""Deterministic scoring rules: direction, thresholds, weights and the confidence rules.

Fit scores are always oriented so 2 = best fit. Direction only changes how a raw value maps to fit.
"""

from __future__ import annotations

from pathfinder.models import (
    Confidence,
    Criterion,
    Direction,
    Evidence,
    ExtractionCandidate,
    FactualConfidence,
    Stability,
    SupportVerdict,
)

DEFAULT_WEIGHT = 3
_FACT_RANK = {"high": 3, "moderate": 2, "low": 1, "n.a.": 1}
_STAB_RANK = {"robust": 3, "provisional": 2, "undetermined": 1}
_RANK_CONF: dict[int, Confidence] = {3: "high", 2: "moderate", 1: "low"}

CONFIDENCE_RULE_COMPARISON = (
    "confidence = min(interval stability, lowest factual confidence among the leader's supported/disputed "
    "cells); robust/high=high, provisional/moderate=moderate, otherwise low. A withheld recommendation caps "
    "confidence at moderate, and at low when the withholding is due to non-comparable evidence.")
CONFIDENCE_RULE_DISCOVERY = (
    "confidence = coverage 100% -> lowest factual confidence of counted evidence; coverage >= 60% -> "
    "at most moderate; otherwise low.")


def threshold_score(criterion: Criterion, value: float) -> int | None:
    t = criterion.thresholds
    if t is None:
        return None
    if criterion.direction == Direction.LOWER_IS_BETTER:
        return 2 if value <= t.strong else 1 if value <= t.plausible else 0
    return 2 if value >= t.strong else 1 if value >= t.plausible else 0


def derive_score(criterion: Criterion, cand: ExtractionCandidate,
                 verdict: SupportVerdict) -> tuple[int, str] | None:
    """Fit score for a verified comparison candidate, or None if no score is derivable.

    Thresholds + a verified raw value: the code computes the score (any LLM proposal is ignored).
    Otherwise the extractor's proposed score is used only if the verifier says the excerpt justifies it.
    """
    if criterion.thresholds is not None and cand.raw_value is not None:
        score = threshold_score(criterion, cand.raw_value)
        if score is not None:
            return score, "threshold"
    if cand.proposed_score is not None and verdict.justifies_proposed_score:
        return cand.proposed_score, "verified_proposal"
    return None


def parse_weights(spec: str | None) -> dict[str, int]:
    """Parse `--weights cost=5,deployment=3`."""
    out: dict[str, int] = {}
    if not spec:
        return out
    for part in spec.split(","):
        if not part.strip():
            continue
        key, _, val = part.partition("=")
        weight = int(val)
        if not 1 <= weight <= 5:
            raise ValueError(f"weight for {key!r} must be 1-5")
        out[key.strip().lower()] = weight
    return out


def factual_confidence(state: str, evidence: list[Evidence], domains: dict[str, str],
                       published: dict[str, str | None], official_domains: list[str],
                       time_sensitive: bool) -> FactualConfidence:
    """How well-sourced a cell's fact is (independent of whether it decides anything).

    domains/published map source_id -> registrable domain / published date.
    """
    if state == "unknown" or not evidence:
        return "n.a."
    if state == "disputed":
        return "low"
    # repeated passages are not corroboration: count each distinct excerpt's domain once
    by_excerpt = {" ".join(e.excerpt.lower().split()): domains[e.source_id] for e in evidence}
    if len(set(by_excerpt.values())) >= 2:
        return "high"
    official = [e for e in evidence if domains[e.source_id] in official_domains]
    if official:
        if time_sensitive and all(published.get(e.source_id) is None for e in official):
            return "moderate"
        return "high"
    return "moderate"


def comparison_confidence(stability: Stability, recommended_cell_confidences: list[FactualConfidence]
                          ) -> Confidence:
    if not recommended_cell_confidences:
        return "low"
    factual = min(_FACT_RANK[c] for c in recommended_cell_confidences)
    return _RANK_CONF[min(_STAB_RANK[stability], factual)]


def discovery_confidence(progress: float, counted_confidences: list[FactualConfidence]) -> Confidence:
    factual = min((_FACT_RANK[c] for c in counted_confidences), default=1)
    if progress >= 1.0:
        return _RANK_CONF[factual]
    if progress >= 0.6:
        return _RANK_CONF[min(2, factual)]
    return "low"


def min_factual(levels: list[FactualConfidence]) -> FactualConfidence:
    if not levels:
        return "n.a."
    return min(levels, key=lambda c: _FACT_RANK[c] if c != "n.a." else 0)
