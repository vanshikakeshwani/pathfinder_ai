"""Grounding gate and registry: F08, F09, X03, X05, X07 (SYNTHETIC)."""

from conftest import run_xy

from pathfinder.demo_fixtures import Y_DOCS, Y_DOCS_TEXT, Y_PRICING, ScriptedExtractor, item
from pathfinder.grounding import Registry, normalize, registrable_domain
from pathfinder.models import ExtractionCandidate
from pathfinder.tools.base import PageContent


def page(url="https://docs.example.com/a",
         text="Alpha supports filtering by metadata fields. Filters combine with vector search in one query."):
    return PageContent(url=url, title="t", text=text)


def cand(reg, **kw):
    base = {"candidate_id": reg.next_candidate_id(), "source_id": "SRC_1",
            "excerpt": "supports filtering by metadata", "target_id": "Alpha:filtering", "entity": "Alpha",
            "claim": "Alpha supports filtering"}
    base.update(kw)
    return ExtractionCandidate(**base)


def test_exact_offsets_accepted_and_wrong_offsets_corrected():
    reg = Registry()
    src, status = reg.add_page(page())
    assert status == "new" and src.source_id == "SRC_1"
    i = src.content.find("supports filtering by metadata")
    g, s = reg.ground(cand(reg, start=i, end=i + 30))
    assert s == "ok" and (g.start, g.end) == (i, i + 30)
    g, s = reg.ground(cand(reg, start=0, end=5))
    assert s == "offsets_corrected" and src.content[g.start:g.end] == g.excerpt


def test_excerpt_not_in_source_rejected():
    reg = Registry()
    reg.add_page(page())
    g, s = reg.ground(cand(reg, excerpt="Alpha is free forever for every team"))
    assert g is None and "not found" in s


def test_X07_unknown_source_id_rejected():
    reg = Registry()
    reg.add_page(page())
    g, s = reg.ground(cand(reg, source_id="SRC_999"))
    assert g is None and "unknown source id" in s


def test_X05_F09_duplicate_urls_registered_once():
    reg = Registry()
    a, s1 = reg.add_page(page("https://docs.example.com/a/"))
    b, s2 = reg.add_page(page("https://DOCS.example.com/a#section"))
    assert s1 == "new" and s2 == "duplicate" and a.source_id == b.source_id
    assert len(reg.sources) == 1


def test_X03_empty_content_not_registered():
    reg = Registry()
    src, status = reg.add_page(page(text="   "))
    assert src is None and status == "empty"


def test_X03_redirect_and_error_stubs_are_unusable():
    """Regression from live Q1: Exa returned milvus.io pages as '302 Found nginx/1.22.1' with status success."""
    reg = Registry()
    for text in ["\n 302 Found \n \n 302 Found \n nginx/1.22.1 \n \n \n",
                 "404 Not Found - the page you requested could not be found on this server, sorry.",
                 "Just a moment... Checking your browser before accessing the site. This may take a few seconds.",
                 "Short page."]:
        src, status = reg.add_page(page(url=f"https://x.example/{len(reg.sources)}{len(text)}", text=text))
        assert src is None and status.startswith(("unusable", "empty")), (text, status)
    assert not reg.sources
    # regression from live Q1: an unusable URL must count as already seen, so it is never fetched again
    stub = "https://milvus.io/docs/install-overview.md"
    reg.add_page(page(url=stub, text="302 Found nginx/1.22.1"))
    assert reg.known_url(stub) and reg.known_url(stub + "/")
    src, status = reg.add_page(page(text="Milvus supports a 302-style redirect config for its proxy, "
                                         "documented in the deployment guide."))
    assert status == "new"  # a number inside normal prose is fine


def test_normalization_and_domains():
    assert normalize("a  b\n\nc") == "a b c"
    assert registrable_domain("https://www.docs.qdrant.tech/x") == "qdrant.tech"
    assert registrable_domain("https://shop.example.co.uk/") == "example.co.uk"


def test_F08_fake_evidence_ids_in_report_are_rejected():
    """The report LLM cites EV_999: the finding is dropped and logged; valid findings remain."""

    def report(req):
        return {"short_answer": "s", "next_steps": [],
                "findings": [{"text": "fabricated", "evidence_ids": ["EV_999"]},
                             {"text": "real", "evidence_ids": [req.payload["evidence"][0]["evidence_id"]]}]}

    ctx = run_xy("flip", llm_overrides={"report": report})
    texts = [f.text for f in ctx.report.findings]
    assert texts == ["real"]
    assert any(e["event"] == "finding_rejected" and e["ids"] == ["EV_999"] for e in ctx.telemetry.events)


def test_F08_fake_source_id_from_extractor_leaves_cell_unknown():
    extractor = ScriptedExtractor({Y_DOCS: [item("VendorY:deployment", Y_DOCS_TEXT, "deploy", 2)]},
                                  extra=[{**item("VendorY:cost", "VendorY costs nothing at all", "free", 2),
                                          "source_id": "SRC_999"}])
    ctx = run_xy("irrelevant", llm_overrides={"extract": extractor})
    assert ctx.cells()[("VendorY", "cost")].state == "unknown"
    assert any(r.reason.startswith("unknown source id SRC_999") for r in ctx.rejected)


def test_F09_same_url_not_refetched_or_double_counted():
    from conftest import build_ctx

    from pathfinder.config import Settings
    from pathfinder.demo_fixtures import X_DOCS, xy_scenario
    from pathfinder.runner import run
    from pathfinder.tools.base import SearchHit
    from pathfinder.tools.fixture_adapter import keyword_search

    # every VendorY query returns the same pricing page, so later rounds hit an already-registered URL
    llm, search, contents = xy_scenario("irrelevant")
    search.handler = keyword_search([(("vendory",), [SearchHit(url=Y_PRICING)]), (("vendorx",), [SearchHit(url=X_DOCS)])])
    ctx = build_ctx(llm, search, contents, Settings(max_no_progress=2))
    run(ctx)
    fetched = [u for call in ctx.tools.contents_client.calls for u in call]
    assert len(fetched) == len(set(fetched))
    assert fetched.count(Y_PRICING) == 1
    assert any(e["event"] == "search_result" and e["duplicates_skipped"] > 0 for e in ctx.telemetry.events)
    # V3: after Y:cost fails, the policy moves to the other decisive VendorY cell instead of repeating it;
    # that search returns the same (already registered) page, which is skipped, not refetched
    assert ctx.attempts["VendorY:cost"] == 1 and ctx.attempts["VendorY:deployment"] == 1
