"""SYNTHETIC fixtures: fictional VendorX / VendorY, fictional prices, scripted LLM outputs.

Nothing here is a live research result. Used by `demo-fixture` and the offline test suite.

PF-1: cost weight 5, deployment weight 3. After round 0: X cost=1, deploy=2 -> [11,11];
      Y cost unknown, deploy=2 -> [6,16]. No interval-robust winner.
PF-2: the policy targets Y:cost. "flip": Y cost verified 2 -> Y [16,16] wins (leader changes).
      "confirm": Y cost verified 0 -> Y [6,6], X becomes robust.
      Either way the decisive cost cells rest on single, undated official pricing pages, so the
      recommendation is first WITHHELD; adaptive then corroborates them from independent (synthetic)
      reviews, after which the recommendation becomes ready.
PF-3: "irrelevant": the targeted pages do not address cost -> verifier rejects -> no_progress stop.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from pathfinder.llm import FixtureLLM, LLMRequest
from pathfinder.models import (
    AlternativeDraft,
    Anchors,
    CriterionDraft,
    Direction,
    PlanDraft,
    ReportProse,
    Thresholds,
)
from pathfinder.tools.base import PageContent, SearchHit
from pathfinder.tools.fixture_adapter import FixtureContents, FixtureSearch, keyword_search

XY_QUESTION = ("[SYNTHETIC] Choose between VendorX and VendorY for a small team: cost matters most (weight 5), "
               "deployment flexibility second (weight 3).")

X_DOCS = "https://docs.vendorx.example/overview"
Y_DOCS = "https://docs.vendory.example/deploy"
Y_PRICING = "https://vendory.example/pricing"
X_REVIEW = "https://reviews.example.org/vendorx-pricing"
Y_REVIEW = "https://reviews.example.org/vendory-pricing"

X_DOCS_TEXT = ("VendorX (SYNTHETIC) offers a managed cloud service and a self-hosted Docker deployment. "
               "VendorX pricing: the Team plan costs $60 per month for the expected workload.")
Y_DOCS_TEXT = "VendorY (SYNTHETIC) can be deployed as a managed service or self-hosted with a single binary."
Y_PRICING_TEXT = {
    "flip": "VendorY (SYNTHETIC) pricing: the Starter plan costs $9 per month for the expected workload.",
    "confirm": "VendorY (SYNTHETIC) pricing: the Starter plan costs $400 per month for the expected workload.",
    "irrelevant": "VendorY (SYNTHETIC) company news: the whole team enjoyed the annual summer picnic.",
}
X_REVIEW_TEXT = "An independent review (SYNTHETIC) measured VendorX at $60 per month for a comparable workload."
Y_REVIEW_TEXT = {
    "flip": "An independent review (SYNTHETIC) measured VendorY at $9 per month for a comparable workload.",
    "confirm": "An independent review (SYNTHETIC) measured VendorY at $400 per month for a comparable workload.",
    "irrelevant": "An independent review (SYNTHETIC) of VendorY's office catering and the annual picnic menu.",
}


def xy_plan_draft(cost_weight: int = 5, deploy_weight: int = 3) -> PlanDraft:
    return PlanDraft(
        mode="comparison",
        alternatives=[AlternativeDraft(name="VendorX", aliases=[], official_domains=["vendorx.example"],
                                       kind="named", defining_features=[]),
                      AlternativeDraft(name="VendorY", aliases=[], official_domains=["vendory.example"],
                                       kind="named", defining_features=[])],
        criteria=[
            CriterionDraft(criterion_id="cost", description="monthly cost for the expected workload",
                           direction=Direction.LOWER_IS_BETTER, weight=cost_weight, weight_source="user",
                           anchors=Anchors(poor="over $100/month", plausible="$21-$100/month",
                                           strong="$20/month or less"),
                           thresholds=Thresholds(strong=20, plausible=100, unit="USD/month"), time_sensitive=True,
                           scopes=[], preferred_scope=None),
            CriterionDraft(criterion_id="deployment", description="deployment options (managed and self-hosted)",
                           direction=Direction.HIGHER_IS_BETTER, weight=deploy_weight, weight_source="user",
                           anchors=Anchors(poor="one rigid option", plausible="managed only or self-hosted only",
                                           strong="both managed and self-hosted"),
                           thresholds=None, time_sensitive=False, scopes=[], preferred_scope=None),
        ],
        facets=[], target_entity_count=0,
        assumptions=["SYNTHETIC scenario: vendors, prices and pages are fictional."],
        initial_queries=["VendorX deployment pricing", "VendorY deployment options"],
        search_context="",
    )


def item(target: str, excerpt: str, claim: str, score: int | None = None, raw: float | None = None,
         unit: str | None = None, entity: str = "", scope: str | None = None,
         rationale: str | None = "scripted rubric rationale") -> dict:
    return {"target_id": target, "excerpt": excerpt, "claim": claim, "proposed_score": score,
            "raw_value": raw, "raw_unit": unit, "entity": entity or target.split(":")[0],
            "start": None, "end": None, "scope": scope, "rubric_rationale": rationale if score is not None else None}


@dataclass
class ScriptedExtractor:
    """Returns pre-scripted items for each supplied source, keyed by URL."""

    by_url: dict[str, list[dict]]
    extra: list[dict] = field(default_factory=list)  # raw items appended (e.g. fake source ids)

    def __call__(self, req: LLMRequest) -> dict:
        items = []
        for src in req.payload["sources"]:
            for it in self.by_url.get(src["url"], []):
                items.append({"source_id": src["source_id"], **it})
        return {"items": items + self.extra}


@dataclass
class ScriptedVerifier:
    """Default verdict: supports, attributed to the candidate's own entity, all flags true.
    `rules` maps an excerpt substring to field overrides (e.g. a wrong applies_to)."""

    rules: dict[str, dict] = field(default_factory=dict)

    def __call__(self, req: LLMRequest) -> dict:
        out = []
        for it in req.payload["items"]:
            v = {"candidate_id": it["candidate_id"], "verdict": "supports", "mentions_alternative": True,
                 "addresses_criterion": True, "justifies_proposed_score": it.get("proposed_score") is not None,
                 "note": "scripted fixture verdict", "applies_to": it["entity"], "identification_quote": "",
                 "scope_matches": True}
            for needle, override in self.rules.items():
                if needle in it["excerpt"]:
                    v.update(override)
            out.append(v)
        return {"verdicts": out}


def evidence_report(req: LLMRequest) -> ReportProse:
    ev = req.payload["evidence"]
    return ReportProse(short_answer="(Synthetic summary of verified fixture evidence.)",
                       findings=[{"text": f"{e['entity']}: {e['claim']}", "evidence_ids": [e["evidence_id"]]}
                                 for e in ev],
                       next_steps=["Replace synthetic vendors with a real question for a live run."])


def xy_scenario(variant: str = "flip", cost_weight: int = 5,
                verifier_rules: dict[str, dict] | None = None,
                llm_overrides: dict[str, Callable[[LLMRequest], Any]] | None = None,
                items_override: dict[str, list[dict]] | None = None,
                text_override: dict[str, str] | None = None,
                ) -> tuple[FixtureLLM, FixtureSearch, FixtureContents]:
    """`items_override` replaces the scripted extraction items for a URL; `text_override` replaces
    a page's text (tests use both to build conflicts, wrong-entity pages, injections, ...)."""
    if variant not in Y_PRICING_TEXT:
        raise ValueError(f"unknown variant {variant}")
    texts = {X_DOCS: X_DOCS_TEXT, Y_DOCS: Y_DOCS_TEXT, Y_PRICING: Y_PRICING_TEXT[variant],
             X_REVIEW: X_REVIEW_TEXT, Y_REVIEW: Y_REVIEW_TEXT[variant]}
    texts.update(text_override or {})
    titles = {X_DOCS: "VendorX overview", Y_DOCS: "VendorY deployment", Y_PRICING: "VendorY pricing",
              X_REVIEW: "VendorX independent review", Y_REVIEW: "VendorY independent review"}
    pages = {u: PageContent(url=u, title=f"{titles[u]} (synthetic)", text=t) for u, t in texts.items()}
    search = FixtureSearch(keyword_search([
        (("vendorx", "independent"), [SearchHit(url=X_REVIEW, title=titles[X_REVIEW])]),
        (("vendory", "independent"), [SearchHit(url=Y_REVIEW, title=titles[Y_REVIEW])]),
        (("vendory", "pricing"), [SearchHit(url=Y_PRICING, title=titles[Y_PRICING])]),
        (("vendory",), [SearchHit(url=Y_DOCS, title=titles[Y_DOCS])]),
        (("vendorx",), [SearchHit(url=X_DOCS, title=titles[X_DOCS])]),
    ]))
    contents = FixtureContents(pages)
    y_price = {"flip": item("VendorY:cost", Y_PRICING_TEXT["flip"], "VendorY Starter costs $9/month",
                            2, 9, "USD/month"),
               "confirm": item("VendorY:cost", Y_PRICING_TEXT["confirm"], "VendorY Starter costs $400/month",
                               0, 400, "USD/month"),
               "irrelevant": item("VendorY:cost", Y_PRICING_TEXT["irrelevant"], "VendorY is inexpensive", 2)}
    y_review = {"flip": [item("VendorY:cost", Y_REVIEW_TEXT["flip"], "Review: VendorY costs $9/month", 2, 9,
                              "USD/month")],
                "confirm": [item("VendorY:cost", Y_REVIEW_TEXT["confirm"], "Review: VendorY costs $400/month", 0,
                                 400, "USD/month")],
                "irrelevant": []}
    by_url = {
        X_DOCS: [item("VendorX:deployment", "VendorX (SYNTHETIC) offers a managed cloud service and a self-hosted "
                      "Docker deployment.", "VendorX offers managed and self-hosted deployment", 2),
                 item("VendorX:cost", "VendorX pricing: the Team plan costs $60 per month for the expected workload.",
                      "VendorX Team plan costs $60/month", 1, 60, "USD/month")],
        Y_DOCS: [item("VendorY:deployment", Y_DOCS_TEXT, "VendorY offers managed and self-hosted deployment", 2)],
        Y_PRICING: [y_price[variant]],
        X_REVIEW: [item("VendorX:cost", X_REVIEW_TEXT, "Review: VendorX costs $60/month", 1, 60, "USD/month")],
        Y_REVIEW: y_review[variant],
    }
    by_url.update(items_override or {})
    extractor = ScriptedExtractor(by_url)
    rules = {"picnic": {"verdict": "irrelevant", "addresses_criterion": False,
                        "justifies_proposed_score": False, "note": "excerpt is about a company event, not cost"}}
    rules.update(verifier_rules or {})
    handlers: dict[str, Callable[[LLMRequest], Any]] = {
        "plan": lambda req: xy_plan_draft(cost_weight),
        "extract": extractor,
        "verify": ScriptedVerifier(rules),
        "report": evidence_report,
    }
    handlers.update(llm_overrides or {})
    return FixtureLLM(handlers), search, contents
