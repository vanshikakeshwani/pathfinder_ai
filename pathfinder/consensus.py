"""Source-family evidence aggregation and conservative consensus (protocol v3.1).

Pipeline for one matrix cell (all verified, grounded, scorable evidence for one alternative x criterion):

1. Documents and source families
   - a document is one fetched page (source_id): several excerpts from it are ONE dependent unit;
   - a source family is a publisher: the registrable domain, or the full host on multi-tenant platforms
     (github.io, medium.com, ...), where independence is marked `uncertain` rather than assumed;
   - families whose excerpts are copies of each other (identical normalised text) are merged: syndicated or
     copied text never counts twice.
2. Family assessment
   - consistent: every excerpt in the family implies the same score;
   - internally inconsistent: the family's excerpts imply different scores. It is recorded as ONE family with
     an unresolved interval [min, max], never as disagreement between independent sources, and it never
     contributes whichever score helps an alternative. If the documents carry different publication dates,
     the newer one is noted as a *possible* supersession, which is never assumed.
3. Context split
   - scoped criteria: per declared context, as before (managed / self_hosted ...);
   - cost-like criteria: per cost dimension inferred deterministically from the recorded unit, claim and
     excerpt (recurring infrastructure, one-time setup, engineering labour, total cost of ownership,
     licence or subscription). Incompatible dimensions are never pooled into one vote.
   Differing consistent contexts give `scope_dependent` (a contradiction is not invented); evidence with no
   specific context applies to every context.
4. Consensus inside one context
   - all families agree: `supported`;
   - a single family that is internally inconsistent: `disputed` (kind `source_inconsistent`);
   - otherwise the prevailing score s (most consistent families; no tie) becomes `consensus` (qualified
     consensus, dissent disclosed) only if ALL of these hold:
       C1 at least two supporting families with certain independence;
       C2 supporting families >= 2 x dissenting families (an inconsistent family whose range excludes s
          dissents; one whose range includes s is recorded but counts neither way);
       C3 no dissent at the opposite end of the rubric (0 vs 2 is a material contradiction);
       C4 no authoritative dissent: a first-party (the alternative's own domain) family rating the
          alternative WORSE than s, or a dissent scored from a measured value (threshold basis) against
          judgement-based support;
       C5 no version-specific dissent (the dissenting excerpt names a version and the support does not).
     Otherwise `disputed`, with the reasons recorded. Consensus is an eligibility rule, not proof of truth.
   - consensus strength: `strong` if >= 3 certain supporting families, >= 3:1 against the dissent, and the
     dissent is only adjacent-score rubric judgement; otherwise `weak`. Factual confidence: strong -> high,
     weak -> moderate (so a weak consensus can never satisfy readiness on a differentiating criterion).

Authority: first-party pages are good evidence of what a product offers, poor evidence of how good it is.
They count as one family like any other; their dissent AGAINST their own product is treated as material,
their dissent in their own favour is not. Unsupported scoring interpretations never reach this module: the
verifier must accept the rubric rationale before a score exists.
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from urllib.parse import urlparse

from pathfinder.models import Evidence

MULTI_TENANT = {"github.io", "medium.com", "substack.com", "blogspot.com", "wordpress.com", "dev.to", "hashnode.dev",
                "notion.site", "gitbook.io", "readthedocs.io", "vercel.app", "netlify.app", "pages.dev",
                "linkedin.com", "reddit.com", "quora.com", "youtube.com", "github.com", "gitlab.io"}
COST_WORDS = ("cost", "price", "pricing", "spend", "budget", "tco", "fee", "billing", "expense")
_VERSION = re.compile(r"\b(?:v\d+(?:\.\d+)+|v\d+\b|version\s+\d+(?:\.\d+)*|release\s+\d+(?:\.\d+)*)", re.I)

# v3.2 cost-dimension patterns: WORD-BOUNDED regexes (v3.1 used substrings, so "after" matched "fte").
_TCO = re.compile(
    r"\b(?:total[- ]cost[- ]of[- ]ownership|tco|total[- ]costs?|real[- ]costs?|true[- ]costs?|actual[- ]costs?|"
    r"all[- ]in(?:[- ]costs?)?|fully[- ]loaded|overall[- ]costs?|effective[- ]costs?|hidden[- ]costs?)\b"
    r"|\binclud\w*\s+(?:the\s+|all\s+)?(?:engineering|engineers?|staff|operational|operations|ops|labou?r|people|"
    r"personnel|maintenance|salar\w*)"
    r"|\b(?:engineering|engineer|staff|labou?r|ops)\s+(?:time|costs?|hours)\s+(?:is\s+|are\s+)?"
    r"(?:included|priced\s+in|factored\s+in|counted|added)"
    r"|\bbeyond\s+(?:the\s+)?infrastructure"
    r"|\b(?:infrastructure|hosting|servers?|cloud)\s+(?:spend\s+|costs?\s+|bills?\s+)?(?:plus|and|\+)\s+(?:the\s+)?"
    r"(?:engineering|engineers?|staff|labou?r|ops|operational|operations|people)", re.I)
_LABOUR = re.compile(r"\b(?:engineer(?:s|ing)?(?:[- ](?:weeks?|months?|days?|hours?|time))?|ftes?|salar(?:y|ies)|"
                     r"total[- ]comp|headcount|sres?|staff(?:[- ]time)?|person[- ]hours|man[- ]hours|hours\s+of\s+work|"
                     r"devops\s+time)\b", re.I)
_ONE_TIME = re.compile(r"\b(?:up[- ]?front|one[- ]time|one[- ]off|setup\s+(?:costs?|fees?)|initial\s+"
                       r"(?:build|costs?|setup|investment))\b", re.I)
_LICENCE = re.compile(r"\b(?:licen[cs]es?|licen[cs]ing|per[- ]seat|per[- ]user|seats?)\b", re.I)
_INFRA_COMPONENT = re.compile(r"\b(?:infrastructure|vps|instances?|servers?|hosting|clusters?|pods?|nodes?|storage|"
                              r"compute|bills?|free[- ]tier|subscription|plans?)\b", re.I)
_PERIOD = re.compile(r"(?:/\s?mo\b|/month\b|\bper\s+month\b|\ba\s+month\b|\bmonthly\b|/\s?yr\b|/year\b|\bper\s+year\b|"
                     r"\bannually\b)", re.I)
_AMOUNT = re.compile(r"\$?\s?(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)\s?([kKmM])?\b")
_SENTENCE = re.compile(r"(?<=[.!?;])\s+|\s*[•·�]\s*")


def classify_cost_text(text: str) -> str | None:
    """Cost dimension of ONE piece of text. Precedence: total cost (explicit wording, or infrastructure AND
    labour components together) > engineering labour > one-time setup > licence > recurring infrastructure."""
    if not text:
        return None
    if _TCO.search(text):
        return "total_cost_of_ownership"
    labour = bool(_LABOUR.search(text))
    infra = bool(_INFRA_COMPONENT.search(text))
    if labour and infra:  # the quantity covers both components
        return "total_cost_of_ownership"
    if labour:
        return "engineering_labour"
    if _ONE_TIME.search(text):
        return "one_time_setup"
    if _LICENCE.search(text):
        return "license_or_subscription"
    if infra or _PERIOD.search(text):
        return "recurring_infrastructure"
    return None


# Capitalised words that are ordinary vocabulary, not product names (v3.2 product-mention heuristic).
_NOT_PRODUCTS = {
    "the", "a", "an", "if", "for", "when", "at", "in", "on", "of", "to", "and", "but", "or", "it", "its", "this",
    "that", "these", "those", "however", "managed", "self", "cost", "costs", "initial", "minimum", "add", "our", "we",
    "you", "your", "they", "their", "cloud", "flex", "serverless", "pro", "enterprise", "starter", "standard", "plus",
    "free", "tier", "pricing", "price", "database", "databases", "vector", "vectors", "search", "memory", "session",
    "hosted", "hybrid", "persistent", "summarized", "teams", "team", "small", "large", "startups", "startup", "note",
    "example", "see", "also", "with", "without", "once", "then", "than", "some", "most", "all", "each", "both", "one",
    "two", "three", "use", "using", "is", "are", "be", "as", "by", "from", "here", "there", "why", "what", "how",
    "which", "who", "more", "less", "yes", "no", "not", "only", "just", "so", "because", "while", "after", "before",
    "per", "month", "year", "day", "week", "hour", "real", "true", "total", "infrastructure", "pilot", "production",
    "experimental", "ops", "operations", "engineering", "build", "storage", "dimensions", "zero", "truly",
    "operational", "overhead", "sla", "usd"}
_CAPWORD = re.compile(r"\b[A-Z][A-Za-z0-9]*[a-z][A-Za-z0-9]*\b")


def product_mentions(text: str, exclude: set[str] | None = None) -> set[str]:
    """Capitalised, non-acronym words that are not ordinary vocabulary: a heuristic for named products,
    vendors and plans (e.g. Zilliz, Qdrant, Weaviate, Pinecone, Hetzner). Recorded for audit."""
    exclude = {w.lower() for w in (exclude or set())}
    return {w for w in _CAPWORD.findall(text) if w.lower() not in _NOT_PRODUCTS and w.lower() not in exclude}


def heterogeneous_products(evs: list[Evidence], fams: list[Family], exclude: set[str]) -> dict[str, list[str]]:
    """Families (with >= 1 named product) whose named products differ: product-specific prices cannot establish
    one category-level cost. Returns {family: products} when heterogeneous, else {}."""
    by_id = {e.evidence_id: e for e in evs}
    named = {}
    for f in fams:
        names = set()
        for i in f.evidence_ids:
            names |= product_mentions(by_id[i].excerpt, exclude)
        if names:
            named[f.family_id] = names
    sets = list(named.values())
    disjoint = any(a.isdisjoint(b) for i, a in enumerate(sets) for b in sets[i + 1:])
    return {k: sorted(v) for k, v in named.items()} if len(sets) >= 2 and disjoint else {}


def _amount_sentence(excerpt: str, value: float) -> str | None:
    """The sentence of the excerpt that states `value` (the verified raw value), if it can be located."""
    for sentence in _SENTENCE.split(excerpt):
        for m in _AMOUNT.finditer(sentence):
            num = float(m.group(1).replace(",", ""))
            suffix = (m.group(2) or "").lower()
            num *= 1000 if suffix == "k" else 1_000_000 if suffix == "m" else 1
            if value and abs(num - value) <= max(0.01 * abs(value), 0.005):
                return sentence
    return None


def normalize_excerpt(text: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text.lower()).split())


def is_cost_like(criterion_id: str, description: str = "") -> bool:
    text = f"{criterion_id} {description}".lower()
    return any(w in text for w in COST_WORDS)


def cost_dimension(e: Evidence) -> str | None:
    """Deterministic cost-dimension label of the quantity that SUPPORTS the score, or None if undeterminable.

    v3.2: a passage can state several amounts ("infrastructure $530/month; real cost $3,530/month"), so the
    focus is, in order: (1) the unit plus the sentence stating the verified raw value; (2) the unit plus the
    verified claim; (3) the unit plus the whole excerpt. The first focus that names a dimension decides.
    A monthly amount is not assumed to be infrastructure when its sentence says it is a total.
    """
    unit = e.raw_unit or ""
    focuses = []
    if e.raw_value is not None:
        sentence = _amount_sentence(e.excerpt, e.raw_value)
        if sentence:
            focuses.append(f"{unit} {sentence}")
    focuses += [f"{unit} {e.claim}", f"{unit} {e.excerpt}"]
    for text in focuses:
        dim = classify_cost_text(text)
        if dim:
            return dim
    return None


def version_specific(e: Evidence) -> bool:
    return bool(_VERSION.search(e.excerpt))


def _host(url: str | None) -> str | None:
    if not url:
        return None
    return (urlparse(url).hostname or "").lower().removeprefix("www.") or None


@dataclass
class Family:
    family_id: str
    domains: list[str]
    documents: list[str]
    evidence_ids: list[str]
    scores: list[int]
    independence: str  # certain | uncertain
    first_party: bool
    measured: bool  # some score comes from a measured value (threshold basis)
    version_specific: bool
    published: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def consistent(self) -> bool:
        return len(self.scores) == 1

    @property
    def low(self) -> int:
        return min(self.scores)

    @property
    def high(self) -> int:
        return max(self.scores)

    def brief(self) -> dict:
        return {"family": self.family_id, "scores": self.scores, "documents": self.documents,
                "evidence_ids": self.evidence_ids, "independence": self.independence,
                "first_party": self.first_party, "measured": self.measured,
                "version_specific": self.version_specific, **({"notes": self.notes} if self.notes else {})}


def build_families(evs: list[Evidence], source_domains: Mapping[str, str], source_urls: Mapping[str, str],
                   official: list[str], published: Mapping[str, str | None]) -> list[Family]:
    keys: dict[str, str] = {}  # evidence_id -> family key
    uncertain: set[str] = set()
    for e in evs:
        domain = source_domains[e.source_id]
        if domain in MULTI_TENANT:
            host = _host(source_urls.get(e.source_id)) or domain
            keys[e.evidence_id] = host
            uncertain.add(host)
        else:
            keys[e.evidence_id] = domain
    # merge families that share an identical (normalised) excerpt: copies are one source
    parent: dict[str, str] = {k: k for k in keys.values()}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    by_text: dict[str, str] = {}
    copied: set[str] = set()
    for e in evs:
        norm = normalize_excerpt(e.excerpt)
        k = keys[e.evidence_id]
        if norm in by_text and find(by_text[norm]) != find(k):
            a, b = sorted((find(by_text[norm]), find(k)))
            parent[b] = a
            copied.update((a, b))
        by_text.setdefault(norm, k)
    groups: dict[str, list[Evidence]] = {}
    for e in evs:
        groups.setdefault(find(keys[e.evidence_id]), []).append(e)
    fams = []
    for root, members in sorted(groups.items()):
        domains = sorted({keys[e.evidence_id] for e in members})
        fam = Family(
            family_id="+".join(domains), domains=domains, documents=sorted({e.source_id for e in members}),
            evidence_ids=[e.evidence_id for e in members], scores=sorted({e.score for e in members}),  # type: ignore[misc]
            independence="uncertain" if any(d in uncertain for d in domains) else "certain",
            first_party=any(source_domains[e.source_id] in official for e in members),
            measured=any(e.score_basis == "threshold" for e in members),
            version_specific=any(version_specific(e) for e in members),
            published=sorted({p for e in members if (p := published.get(e.source_id))}))
        if len(domains) > 1 or root in copied:
            fam.notes.append("copied/syndicated text merged into one family")
        if not fam.consistent:
            fam.notes.append("internally inconsistent: its own excerpts imply different scores")
            by_doc = {}
            for e in members:
                by_doc.setdefault(e.source_id, set()).add(e.score)
            dated = [(published.get(d), d) for d in by_doc if published.get(d)]
            if len(by_doc) > 1 and len({p for p, _ in dated}) > 1:
                newest = max(dated)
                fam.notes.append(f"documents have different dates; the newest ({newest[1]}, {newest[0]}) may "
                                 "supersede older ones, but supersession is not assumed")
        if fam.independence == "uncertain":
            fam.notes.append("multi-tenant host: independence from other families uncertain")
        fams.append(fam)
    return fams


@dataclass
class Aggregate:
    state: str  # unknown | supported | consensus | disputed
    lower: int
    upper: int
    score: int | None
    kind: str | None = None  # dispute or consensus detail
    record: dict = field(default_factory=dict)
    heterogeneous: bool = False  # v3.2: contributing families describe different named products


def aggregate_context(evs: list[Evidence], source_domains: Mapping[str, str], source_urls: Mapping[str, str],
                      official: list[str], published: Mapping[str, str | None],
                      product_check: set[str] | None = None) -> Aggregate:
    """Consensus inside ONE comparable context (same criterion definition, scope and dimension).

    product_check (v3.2): set for cost criteria of approach-type alternatives (the set holds words of the
    alternative's own name, which are not product names). If the contributing families name DIFFERENT products,
    the result is marked heterogeneous: a consensus becomes kind `heterogeneous` (never strong), a supported
    cell is flagged, and the record lists the products; nothing is merged or suppressed."""
    agg = _aggregate_context(evs, source_domains, source_urls, official, published)
    if product_check is None or agg.state not in ("supported", "consensus", "disputed"):
        return agg
    fams = build_families(evs, source_domains, source_urls, official, published)
    contributing = fams
    if agg.state == "consensus":
        supporting = set(agg.record.get("supporting", []))
        contributing = [f for f in fams if f.family_id in supporting] + \
            [f for f in fams if f.family_id in set(agg.record.get("dissenting", []))]
    het = heterogeneous_products(evs, contributing, product_check)
    if het:
        agg.record["heterogeneous_products"] = het
        agg.record["heterogeneity_note"] = ("families describe different named products/plans; product-specific "
                                            "prices are examples, not one category-level cost")
        agg.heterogeneous = True
        if agg.state == "consensus":
            agg.kind = "heterogeneous"
            agg.record["strength"] = "weak (heterogeneous products)"
    return agg


def _aggregate_context(evs: list[Evidence], source_domains: Mapping[str, str], source_urls: Mapping[str, str],
                       official: list[str], published: Mapping[str, str | None]) -> Aggregate:
    if not evs:
        return Aggregate("unknown", 0, 2, None)
    fams = build_families(evs, source_domains, source_urls, official, published)
    all_scores = sorted({s for f in fams for s in f.scores})
    rec: dict = {"families": [f.brief() for f in fams], "family_count": len(fams),
                 "certain_families": sum(1 for f in fams if f.independence == "certain")}
    if len(all_scores) == 1:
        s = all_scores[0]
        return Aggregate("supported", s, s, s, None, {**rec, "prevailing_score": s, "decision": "all families agree"})
    lo, hi = all_scores[0], all_scores[-1]
    consistent = [f for f in fams if f.consistent]
    if len(fams) == 1 or not consistent:
        rec.update(decision="not resolved: the only assessment(s) are internally inconsistent source families",
                   disagreement="source_inconsistency", remaining_uncertainty=f"score in [{lo}, {hi}]")
        return Aggregate("disputed", lo, hi, None, "source_inconsistent", rec)
    counts: dict[int, int] = {}
    for f in consistent:
        counts[f.scores[0]] = counts.get(f.scores[0], 0) + 1
    top = max(counts.values())
    leaders = [s for s, n in counts.items() if n == top]
    if len(leaders) > 1:
        rec.update(decision=f"not resolved: families tie between scores {sorted(leaders)}",
                   disagreement=_kind_of_disagreement(fams), remaining_uncertainty=f"score in [{lo}, {hi}]")
        return Aggregate("disputed", lo, hi, None, "independent_disagreement", rec)
    s = leaders[0]
    support = [f for f in consistent if f.scores[0] == s]
    partial = [f for f in fams if not f.consistent and f.low <= s <= f.high]
    dissent = [f for f in fams if all(f is not g for g in support) and all(f is not g for g in partial)]
    certain_support = [f for f in support if f.independence == "certain"]
    reasons, blocks = [], []
    if len(certain_support) < 2:
        blocks.append(f"C1: {len(certain_support)} supporting family(ies) with certain independence (need 2)")
    if len(support) < 2 * len(dissent):
        blocks.append(f"C2: {len(support)} supporting vs {len(dissent)} dissenting families (need 2:1)")
    opposite = [f for f in dissent if abs(f.low - s) == 2 or abs(f.high - s) == 2]
    if opposite:
        blocks.append("C3: material contradiction at the opposite end of the rubric from "
                      + ", ".join(f.family_id for f in opposite))
    judged = all(not f.measured for f in support)
    authoritative = [f for f in dissent if (f.first_party and f.low < s) or (f.measured and judged)]
    if authoritative:
        blocks.append("C4: authoritative dissent (first-party against its own product, or a measured value) "
                      "from " + ", ".join(f.family_id for f in authoritative))
    versioned = [f for f in dissent if f.version_specific and not any(g.version_specific for g in support)]
    if versioned:
        blocks.append("C5: version-specific dissent from " + ", ".join(f.family_id for f in versioned)
                      + "; check whether a version or scope separates the claims")
    rec.update(prevailing_score=s, supporting=[f.family_id for f in support], dissenting=[f.family_id for f in dissent],
               inconsistent_including_prevailing=[f.family_id for f in partial],
               supporting_certain=len(certain_support), disagreement=_kind_of_disagreement(fams),
               source_quality=_quality_notes(fams))
    if blocks:
        kind = ("authoritative_dissent" if authoritative else "material_contradiction" if opposite
                else "version_specific" if versioned
                # no family dissents: the only disagreement is inside an internally inconsistent source
                else "source_inconsistent" if not dissent else "independent_disagreement")
        rec.update(decision="not resolved: " + "; ".join(blocks), remaining_uncertainty=f"score in [{lo}, {hi}]")
        return Aggregate("disputed", lo, hi, None, kind, rec)
    adjacent_only = all(abs(f.low - s) <= 1 and abs(f.high - s) <= 1 for f in dissent + partial)
    strong = (len(certain_support) >= 3 and len(support) >= 3 * max(1, len(dissent)) and adjacent_only
              and not any(f.measured for f in dissent))
    reasons.append(f"qualified consensus: {len(support)} supporting vs {len(dissent)} dissenting families "
                   f"({len(certain_support)} with certain independence); dissent retained")
    rec.update(decision="; ".join(reasons), strength="strong" if strong else "weak",
               remaining_uncertainty=("dissenting families: " + ", ".join(f.family_id for f in dissent + partial))
               or "none")
    return Aggregate("consensus", s, s, s, "strong" if strong else "weak", rec)


def _kind_of_disagreement(fams: list[Family]) -> str:
    scores = sorted({s for f in fams for s in f.scores})
    if any(not f.consistent for f in fams) and len([f for f in fams if f.consistent]) <= 1:
        return "source_inconsistency"
    if any(f.measured for f in fams):
        return "factual (a measured value is involved)"
    return "rubric_interpretation" if scores[-1] - scores[0] == 1 else "substantive (opposite rubric ends)"


def _quality_notes(fams: list[Family]) -> list[str]:
    notes = []
    if any(f.first_party for f in fams):
        notes.append("first-party family present: evidence of what is offered, not of how good it is")
    if any(f.independence == "uncertain" for f in fams):
        notes.append("multi-tenant host families: independence uncertain, not counted toward C1")
    if any(f.measured for f in fams):
        notes.append("measured (threshold-scored) evidence present")
    return notes


@dataclass
class CellAggregate:
    state: str
    lower: int
    upper: int
    score: int | None
    scope_scores: dict[str, int]
    kind: str | None
    records: dict[str, dict]
    families: int
    certain_families: int
    dimension_mismatch: bool
    contexts: list[str]
    heterogeneous: bool = False
    ambiguous_dimension: bool = False  # cost criterion with scoring evidence of undeterminable dimension


def aggregate_cell(evs: list[Evidence], scoped: bool, cost_like: bool, source_domains: Mapping[str, str],
                   source_urls: Mapping[str, str], official: list[str],
                   published: Mapping[str, str | None], approach_name: str | None = None) -> CellAggregate:
    """approach_name: the alternative's name when it is an approach-type (conceptual) alternative."""
    if not evs:
        return CellAggregate("unknown", 0, 2, None, {}, None, {}, 0, 0, False, [])
    product_check = (set(re.findall(r"[A-Za-z0-9]+", approach_name)) if (approach_name and cost_like) else None)
    agg = _aggregate_cell(evs, scoped, cost_like, source_domains, source_urls, official, published, product_check)
    agg.heterogeneous = any(r.get("heterogeneous_products") for r in agg.records.values())
    agg.ambiguous_dimension = cost_like and any(cost_dimension(e) is None for e in evs)
    return agg


def _aggregate_cell(evs, scoped, cost_like, source_domains, source_urls, official, published,
                    product_check) -> CellAggregate:
    scopes = sorted({e.scope for e in evs} - {"general"}) if scoped else []
    scope_ctx = scopes if len(scopes) >= 2 else ["*"]
    leaves: dict[str, list[Evidence]] = {}
    dim_split = False
    for sc in scope_ctx:
        in_scope = [e for e in evs if sc == "*" or e.scope in (sc, "general")]
        dims = sorted({d for e in in_scope if (d := cost_dimension(e))}) if cost_like else []
        if len(dims) >= 2:
            dim_split = True
            for d in dims:
                leaves[f"{sc}|{d}"] = [e for e in in_scope if cost_dimension(e) in (d, None)]
        else:
            leaves[f"{sc}|*"] = in_scope
    results = {k: aggregate_context(v, source_domains, source_urls, official, published, product_check)
               for k, v in leaves.items()}
    all_fams = build_families(evs, source_domains, source_urls, official, published)
    fam_n, certain_n = len(all_fams), sum(1 for f in all_fams if f.independence == "certain")
    records = {k: {**r.record, "state": r.state} for k, r in results.items()}
    labels = {k: k.replace("*|", "").replace("|*", "").replace("*", "general") for k in results}
    if len(results) == 1:
        r = next(iter(results.values()))
        return CellAggregate(r.state, r.lower, r.upper, r.score, {}, r.kind, records, fam_n, certain_n, False,
                             list(labels.values()))
    disputed = {k: r for k, r in results.items() if r.state == "disputed"}
    if disputed:
        lo = min(r.lower for r in results.values())
        hi = max(r.upper for r in results.values())
        kind = next(iter(disputed.values())).kind
        return CellAggregate("disputed", lo, hi, None, {}, kind, records, fam_n, certain_n, dim_split,
                             list(labels.values()))
    vals = {labels[k]: r.score for k, r in results.items()}
    if len(set(vals.values())) > 1:  # cell-level summary (kept last; per-context records stay authoritative)
        what = "cost evidence measures different dimensions" if dim_split else "contexts differ"
        records["summary"] = {"state": "summary", "decision": f"{what}: " + ", ".join(
            f"{k}={v}" for k, v in vals.items()) + "; not pooled into one score"}
    if len(set(vals.values())) == 1:
        s = next(iter(vals.values()))
        state = "consensus" if any(r.state == "consensus" for r in results.values()) else "supported"
        kind = next((r.kind for r in results.values() if r.state == "consensus"), None)
        return CellAggregate(state, s, s, s, {}, kind, records, fam_n, certain_n, False, list(labels.values()))
    return CellAggregate("scope_dependent", min(vals.values()), max(vals.values()), None,  # type: ignore[type-var]
                         vals, "dimension_mismatch" if dim_split else "scope", records, fam_n, certain_n, dim_split,
                         list(labels.values()))


# ------------------------------------------------------------------------------- reachable outcomes (v3.1)

def _blocked_for(score: int, support: list[dict], dissent: list[dict]) -> str | None:
    """Why NO amount of new agreeing evidence can create a consensus on `score` (None if it could)."""
    if any(abs(x - score) == 2 for f in dissent for x in f["scores"]):
        return "material contradiction (opposite rubric end) stays"
    judged = all(not f.get("measured") for f in support)
    if any((f.get("first_party") and min(f["scores"]) < score) or (f.get("measured") and judged) for f in dissent):
        return "authoritative dissent (first-party or measured) stays"
    if any(f.get("version_specific") for f in dissent) and not any(f.get("version_specific") for f in support):
        return "version-specific dissent: needs version/scope clarification"
    return None


def reachability(cell, remaining_searches: int) -> dict:
    """What more research can still achieve for a cell under the implemented aggregation rules.

    Assumption (disclosed): one search adds AT MOST ONE new independent agreeing family, and agreement is never
    guaranteed; k is the minimum number of such families needed, not a prediction that they exist.
    Classes: resolvable_by_one_source | needs_multiple_sources | unlikely_within_budget |
             needs_scope_or_authority_clarification | unresolvable_by_more_evidence | not_applicable.
    """
    state = cell.state
    if state in ("unknown", "insufficient"):
        return {"class": "resolvable_by_one_source", "k": 1, "reachable": {s: 1 for s in range(0, 3)}}
    if state == "scope_dependent":
        return {"class": "needs_scope_or_authority_clarification", "k": None, "reachable": {},
                "why": "contexts or cost dimensions differ; more evidence cannot choose the user's context"}
    if getattr(cell, "heterogeneous", False):  # v3.2: more product-specific prices cannot make one category cost
        return {"class": "needs_scope_or_authority_clarification", "k": None, "reachable": {},
                "why": "families describe different products; needs a product- or plan-specific criterion"}
    if state == "supported":
        need = max(1, 2 - cell.certain_families) if cell.factual_confidence != "high" else 0
        return {"class": "resolvable_by_one_source" if need == 1 else
                "needs_multiple_sources" if need else "not_applicable", "k": need or None,
                "reachable": {cell.score: need} if need else {}}
    record = next((r for r in cell.consensus.values() if r.get("state") in ("disputed", "consensus")), None)
    if record is None:
        return {"class": "not_applicable", "k": None, "reachable": {}}
    fams = record.get("families", [])
    if state == "consensus":  # corroborating a weak consensus into a strong one
        s = cell.score
        support = [f for f in fams if f["scores"] == [s]]
        dissent = [f for f in fams if f["scores"] != [s]]
        certain = sum(1 for f in support if f["independence"] == "certain")
        if any(f.get("measured") for f in dissent) or any(abs(x - s) > 1 for f in dissent for x in f["scores"]):
            return {"class": "unresolvable_by_more_evidence", "k": None, "reachable": {},
                    "why": "dissent prevents a strong consensus whatever is added"}
        k = max(3 - certain, 3 * max(1, len(dissent)) - len(support), 1 if cell.dispute_kind == "weak" else 0)
        if k == 0:
            return {"class": "not_applicable", "k": None, "reachable": {}}
        return {"class": _cls(k, remaining_searches), "k": k, "reachable": {s: k}}
    reachable, why = {}, {}
    for s in range(cell.lower, cell.upper + 1):
        support = [f for f in fams if f["scores"] == [s]]
        partial = [f for f in fams if len(f["scores"]) > 1 and min(f["scores"]) <= s <= max(f["scores"])]
        dissent = [f for f in fams if f not in support and f not in partial]
        blocked = _blocked_for(s, support, dissent)
        if blocked:
            why[s] = blocked
            continue
        certain = sum(1 for f in support if f["independence"] == "certain")
        # k new agreeing families: C1 needs certain + k >= 2; C2 needs support + k >= 2 * dissent
        reachable[s] = max(2 - certain, 2 * len(dissent) - len(support), 1)
    if not reachable:
        clar = any("version" in w or "authoritative" in w for w in why.values())
        return {"class": "needs_scope_or_authority_clarification" if clar else "unresolvable_by_more_evidence",
                "k": None, "reachable": {}, "why": why}
    kmin = min(reachable.values())
    return {"class": _cls(kmin, remaining_searches), "k": kmin, "reachable": reachable, "why": why}


def _cls(k: int, remaining: int) -> str:
    if k <= 1:
        return "resolvable_by_one_source"
    return "needs_multiple_sources" if k <= remaining else "unlikely_within_budget"


def audit_cell(cell) -> list[str]:
    """Mechanical integrity check of a cell's aggregation record (empty list = OK): every scoring excerpt sits
    in exactly one family per context, documents and publishers are not split across families, and every
    evidence id is kept (dissent is never dropped)."""
    problems = []
    for ctx, rec in cell.consensus.items():
        if rec.get("state") == "summary":
            continue
        fams = rec.get("families", [])
        ev_ids = [e for f in fams for e in f["evidence_ids"]]
        if len(ev_ids) != len(set(ev_ids)):
            problems.append(f"{ctx}: an excerpt is counted in two families")
        docs = [d for f in fams for d in f["documents"]]
        if len(docs) != len(set(docs)):
            problems.append(f"{ctx}: a document is split across families")
        pubs = [p for f in fams for p in f["family"].split("+")]
        if len(pubs) != len(set(pubs)):
            problems.append(f"{ctx}: a publisher is split across families")
        missing = set(ev_ids) - set(cell.evidence_ids)
        if missing:
            problems.append(f"{ctx}: record cites evidence not in the cell: {sorted(missing)}")
    recorded = {e for r in cell.consensus.values() for f in r.get("families", []) for e in f["evidence_ids"]}
    if cell.evidence_ids and set(cell.evidence_ids) - recorded:
        problems.append(f"evidence missing from the record (dropped?): {sorted(set(cell.evidence_ids) - recorded)}")
    return problems
