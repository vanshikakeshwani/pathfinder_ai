"""Typed domain models.

Two families:
* Application models (ResearchPlan, Source, Evidence, ...) - validated strictly, IDs allocated by the app.
* LLM output models (PlanDraft, ExtractionBatch, VerdictBatch, ReportProse) - what the model may return.
  They avoid dict-typed fields so they work with strict JSON-schema structured outputs.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, model_validator


class Mode(StrEnum):
    COMPARISON = "comparison"
    DISCOVERY = "discovery"


class Direction(StrEnum):
    HIGHER_IS_BETTER = "higher_is_better"
    LOWER_IS_BETTER = "lower_is_better"


StopReason = Literal[
    "stable", "budget_exhausted", "no_progress", "insufficient_evidence", "error", "cancelled"
]
RunStatus = Literal["complete", "partial", "failed"]
# scope_dependent: consistent verified evidence per context, but the contexts differ (e.g. managed 2 vs
# self-hosted 0) and the user has not chosen one; the interval spans the per-scope scores. Not a dispute.
# disputed: comparable (same-context) verified evidence implies different scores; interval = [min, max] of
# the verified scores (V3; V2 used [0, 2]). Never counted as supported.
# insufficient: no scorable evidence, but the cell WAS researched and on-target candidates were rejected
# because they could not justify a score (verdict partial / no derivable score). Interval [0, 2].
# consensus (v3.1): qualified consensus with disclosed dissent - independent source families meet the
# conservative eligibility rules in pathfinder.consensus; interval [s, s]; dissent kept in `consensus`.
CellState = Literal["supported", "consensus", "scope_dependent", "disputed", "insufficient", "unknown"]
RESOLVED_STATES = ("supported", "consensus", "scope_dependent")
SCORED_STATES = ("supported", "consensus")  # a single prevailing score exists
OPEN_STATES = ("unknown", "insufficient", "disputed")
# Why a research action was taken (trace label). static_schedule: the fixed baseline's next target.
ActionKind = Literal["first_exploration", "targeted", "corroboration", "conflict_resolution", "bounded_retry",
                     "fallback_exploration", "static_schedule"]
Stability = Literal["robust", "provisional", "undetermined"]
FactualConfidence = Literal["high", "moderate", "low", "n.a."]
Confidence = Literal["high", "moderate", "low"]
Verdict = Literal["supports", "partial", "contradicts", "irrelevant"]


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


# --------------------------------------------------------------------------- plan


class Anchors(Strict):
    """Text definitions of the 0/1/2 fit scores. 2 is always the best fit."""

    poor: str
    plausible: str
    strong: str


class Thresholds(Strict):
    """Numeric cut-offs from user constraints, interpreted with the criterion's direction.

    lower_is_better: value <= strong -> 2, value <= plausible -> 1, else 0.
    higher_is_better: value >= strong -> 2, value >= plausible -> 1, else 0.
    """

    strong: float
    plausible: float
    unit: str = ""


class Criterion(Strict):
    criterion_id: str = Field(pattern=r"^[a-z0-9_]{1,40}$")
    description: str
    direction: Direction = Direction.HIGHER_IS_BETTER
    weight: int = Field(ge=1, le=5)
    weight_source: Literal["user", "inferred", "default"] = "default"
    anchors: Anchors
    thresholds: Thresholds | None = None
    time_sensitive: bool = False  # e.g. pricing: undated official sources lower factual confidence
    # Comparable contexts for this criterion (e.g. ["managed", "self_hosted"]). Evidence is tagged with one
    # of these (or "general"); alternatives are only compared within the same context.
    scopes: list[str] = Field(default_factory=list)
    # The context the user's constraints point to; when set, only that context (or "general") scores.
    preferred_scope: str | None = None

    @model_validator(mode="after")
    def _threshold_order(self) -> Criterion:
        t = self.thresholds
        if t is not None:
            if self.direction == Direction.LOWER_IS_BETTER and t.strong > t.plausible:
                raise ValueError("lower_is_better thresholds need strong <= plausible")
            if self.direction == Direction.HIGHER_IS_BETTER and t.strong < t.plausible:
                raise ValueError("higher_is_better thresholds need strong >= plausible")
        if self.preferred_scope is not None and self.preferred_scope not in self.scopes:
            raise ValueError("preferred_scope must be one of scopes")
        return self


class Alternative(Strict):
    name: str = Field(min_length=1, max_length=80)
    aliases: list[str] = Field(default_factory=list)
    official_domains: list[str] = Field(default_factory=list)  # planner assumption, logged
    # named: a product/company/project; exact identity matters (lexical check on name/alias).
    # approach: a conceptual option; identified semantically via a grounded identification quote.
    kind: Literal["named", "approach"] = "named"
    defining_features: list[str] = Field(default_factory=list)  # approach: what distinguishes it


class Facet(Strict):
    facet_id: str = Field(pattern=r"^[a-z0-9_]{1,40}$")
    description: str
    importance: int = Field(ge=1, le=5)
    required_count: int = Field(default=1, ge=1, le=10)
    search_terms: str = ""  # short keywords for queries (descriptions are often full sentences)


class ResearchPlan(Strict):
    question: str
    mode: Mode
    alternatives: list[Alternative] = Field(default_factory=list)
    criteria: list[Criterion] = Field(default_factory=list)
    facets: list[Facet] = Field(default_factory=list)
    # Discovery: number of distinct entities that must satisfy every facet (0 = topic coverage).
    target_entity_count: int = Field(default=0, ge=0, le=10)
    assumptions: list[str] = Field(min_length=1)
    initial_queries: list[str] = Field(min_length=1, max_length=5)
    search_context: str = ""  # short topic phrase added to discovery queries (same builder for both arms)

    @model_validator(mode="after")
    def _mode_shape(self) -> ResearchPlan:
        if self.mode == Mode.COMPARISON:
            if not 2 <= len(self.alternatives) <= 4:
                raise ValueError("comparison needs 2-4 alternatives")
            if not 2 <= len(self.criteria) <= 5:
                raise ValueError("comparison needs 2-5 criteria")
            names = [a.name.lower() for a in self.alternatives]
            if len(set(names)) != len(names):
                raise ValueError("duplicate alternatives")
            ids = [c.criterion_id for c in self.criteria]
            if len(set(ids)) != len(ids):
                raise ValueError("duplicate criterion ids")
        else:
            if not 1 <= len(self.facets) <= 6:
                raise ValueError("discovery needs 1-6 facets")
            ids = [f.facet_id for f in self.facets]
            if len(set(ids)) != len(ids):
                raise ValueError("duplicate facet ids")
        return self

    def criterion(self, criterion_id: str) -> Criterion:
        return next(c for c in self.criteria if c.criterion_id == criterion_id)

    def alternative(self, name: str) -> Alternative:
        return next(a for a in self.alternatives if a.name == name)


# ----------------------------------------------------------------------- evidence


class Source(Strict):
    source_id: str
    url: HttpUrl
    domain: str
    title: str
    retrieved_at: str
    content: str
    published_at: str | None = None


class ExtractionCandidate(Strict):
    """An LLM-proposed piece of evidence. Not trusted until grounded and verified."""

    candidate_id: str
    source_id: str
    excerpt: str
    start: int | None = None
    end: int | None = None
    target_id: str  # "Alternative:criterion_id" (comparison) or facet_id (discovery)
    entity: str  # alternative name, or the discovered entity name
    claim: str
    raw_value: float | None = None
    raw_unit: str | None = None
    proposed_score: int | None = Field(default=None, ge=0, le=2)
    scope: str = "general"  # comparable context the excerpt is about (criterion.scopes or "general")
    rubric_rationale: str = ""  # why the excerpt meets the proposed score's anchor
    round: int = 0


class SupportVerdict(Strict):
    candidate_id: str
    verdict: Verdict
    mentions_alternative: bool
    addresses_criterion: bool
    justifies_proposed_score: bool
    note: str = ""
    # Which alternative the excerpt is actually about: an alternative name, "multiple" or "none".
    applies_to: str = ""
    # Verbatim phrase from the excerpt/context that identifies the subject (checked by code).
    identification_quote: str = ""
    # The excerpt is about the candidate's stated scope (e.g. managed vs self-hosted).
    scope_matches: bool = True


class Evidence(Strict):
    """Verified evidence: grounded excerpt + passing support verdict + deterministic checks."""

    evidence_id: str
    candidate_id: str
    source_id: str
    excerpt: str
    start: int
    end: int
    target_id: str
    entity: str
    claim: str
    score: int | None = Field(default=None, ge=0, le=2)  # derived fit score (comparison)
    score_basis: Literal["threshold", "verified_proposal", "none"] = "none"
    raw_value: float | None = None
    raw_unit: str | None = None
    scope: str = "general"
    rubric_rationale: str = ""
    identification_quote: str = ""
    round: int = 0

    @model_validator(mode="after")
    def _offsets(self) -> Evidence:
        if self.end <= self.start or self.start < 0:
            raise ValueError("evidence needs 0 <= start < end")
        return self


class RejectedCandidate(Strict):
    candidate_id: str
    target_id: str
    stage: Literal["grounding", "verification", "acceptance"]
    reason: str
    round: int = 0
    # kept so a human reviewer can check for wrongly rejected evidence
    source_id: str = ""
    excerpt: str = ""
    claim: str = ""
    proposed_score: int | None = None
    scope: str = ""


class Finding(Strict):
    text: str
    evidence_ids: list[str] = Field(min_length=1)


# ----------------------------------------------------------------- decision state


class MatrixCell(Strict):
    alternative: str
    criterion_id: str
    state: CellState
    lower: int
    upper: int
    score: int | None = None
    evidence_ids: list[str] = Field(default_factory=list)
    factual_confidence: FactualConfidence = "n.a."
    independent_sources: int = 0  # distinct domains with distinct excerpts (repeats are not corroboration)
    scopes: list[str] = Field(default_factory=list)  # contexts of the scoring evidence
    scope_scores: dict[str, int] = Field(default_factory=dict)  # per-context score (scope_dependent cells)
    excluded_evidence_ids: list[str] = Field(default_factory=list)  # verified, but other scope: not scored
    observed_scores: list[int] = Field(default_factory=list)  # distinct verified scores (disputes keep all)
    self_reported_only: bool = False  # every scoring excerpt is a judgement from the alternative's own domain
    # v3.1 source-family aggregation (pathfinder.consensus)
    families: int = 0  # source families (documents -> publishers, copies merged)
    certain_families: int = 0  # families whose independence is established (not multi-tenant hosts)
    dispute_kind: str | None = None  # source_inconsistent | independent_disagreement | material_contradiction |
    #                                  authoritative_dissent | version_specific; consensus: strong | weak;
    #                                  scope_dependent: scope | dimension_mismatch
    dimension_mismatch: bool = False  # cost evidence measures incompatible dimensions
    dimensions: list[str] = Field(default_factory=list)  # cost dimensions of the scoring evidence
    consensus: dict = Field(default_factory=dict)  # per-context aggregation record (families, decision, ...)


class DecisionState(Strict):
    recommended: str | None
    stability: Stability


class DecisionChange(Strict):
    round: int
    kind: Literal["leader_changed", "became_robust", "lost_robustness", "stability_changed"]
    before: DecisionState
    after: DecisionState
    evidence_ids: list[str]


class ResearchAction(Strict):
    action_id: str
    target_id: str
    queries: list[str] = Field(min_length=1)
    include_domains: list[str] = Field(default_factory=list)
    predicted_gain: float
    estimated_cost_units: float
    action_score: float
    flip_relevant: bool = False
    why_selected: str
    action_kind: ActionKind = "targeted"
    # the deterministic calculations behind the choice (counterfactuals, factors, rejected alternatives)
    analysis: dict = Field(default_factory=dict)


# -------------------------------------------------------------------- LLM outputs


class CriterionDraft(Strict):
    criterion_id: str
    description: str
    direction: Direction
    weight: int | None
    weight_source: Literal["user", "inferred", "default"]
    anchors: Anchors
    thresholds: Thresholds | None
    time_sensitive: bool
    scopes: list[str]
    preferred_scope: str | None


class FacetDraft(Strict):
    facet_id: str
    description: str
    importance: int
    required_count: int
    search_terms: str


class AlternativeDraft(Strict):
    name: str
    aliases: list[str]
    official_domains: list[str]
    kind: Literal["named", "approach"]
    defining_features: list[str]


class PlanDraft(Strict):
    mode: Mode
    alternatives: list[AlternativeDraft]
    criteria: list[CriterionDraft]
    facets: list[FacetDraft]
    target_entity_count: int
    assumptions: list[str]
    initial_queries: list[str]
    search_context: str


class ExtractionItem(Strict):
    source_id: str
    excerpt: str
    start: int | None
    end: int | None
    target_id: str
    entity: str
    claim: str
    raw_value: float | None
    raw_unit: str | None
    proposed_score: int | None
    scope: str | None
    rubric_rationale: str | None


class ExtractionBatch(Strict):
    items: list[ExtractionItem]


class VerdictBatch(Strict):
    verdicts: list[SupportVerdict]


class ReportProse(Strict):
    short_answer: str
    findings: list[Finding]
    next_steps: list[str]


# ------------------------------------------------------------------------- report


class ResearchReport(Strict):
    run_id: str
    question: str
    mode: Mode
    short_answer: str
    findings: list[Finding]
    sources: list[dict]
    confidence: Confidence
    confidence_rule: str
    factual_confidence: FactualConfidence
    decision_stability: Stability | None  # mathematical interval stability under the rubric
    recommended: str | None  # set ONLY when recommendation_status == "ready"
    # Interval outcome kept for inspectability even when no recommendation is made.
    interval_leader: str | None = None
    recommendation_status: Literal["ready", "withheld", "none", "not_applicable"] = "not_applicable"
    recommendation_withheld_reasons: list[str] = Field(default_factory=list)
    comparability_issues: list[str] = Field(default_factory=list)
    single_source_cells: list[str] = Field(default_factory=list)
    requirement_coverage: dict = Field(default_factory=dict)
    assumptions: list[str]
    limitations: list[str]
    next_steps: list[str]
    stop_reason: StopReason
    status: RunStatus
    decision_changes: list[DecisionChange]
    decision_flip_count: int  # V2 definition (preserved): every counted leader_changed event
    status_change_count: int
    strong_flip_count: int = 0  # V3 stricter metric: real leader -> different real leader (no tie involved)
    research_budget_spent: dict
    synthetic: bool = False
