"""V01-V07: grounding is not support; verification fails closed (SYNTHETIC)."""

from conftest import run_xy

from pathfinder.demo_fixtures import Y_PRICING, Y_REVIEW, item
from pathfinder.retry import ToolError

NO_REVIEW = {Y_REVIEW: []}  # remove the independent review so only the page under test can fill Y:cost

PRICE = "VendorY (SYNTHETIC) pricing: the Starter plan costs $9 per month for the expected workload."


def y_cost(ctx):
    return ctx.cells()[("VendorY", "cost")]


def test_V01_grounded_but_unsupported_stays_unknown():
    ctx = run_xy("flip", items_override=NO_REVIEW,
                 verifier_rules={"Starter plan": {"verdict": "partial", "note": "price for other tier"}})
    # the excerpt exists verbatim (grounding passed) but support was not established: the cell is
    # `insufficient` (researched, unscorable), still the full interval [0, 2] and not supported
    cell = y_cost(ctx)
    assert (cell.state, cell.lower, cell.upper, cell.score) == ("insufficient", 0, 2, None)
    rej = [r for r in ctx.rejected if r.target_id == "VendorY:cost"]
    assert rej and rej[0].stage == "verification"
    # the rejected excerpt is kept for human review of wrongful rejections
    assert "Starter plan costs $9" in rej[0].excerpt and rej[0].proposed_score == 2 and rej[0].source_id
    assert any(e["event"] == "candidate_rejected" for e in ctx.telemetry.events)


def test_V02_contradicts_rejected_no_score_change():
    ctx = run_xy("flip", items_override=NO_REVIEW, verifier_rules={"Starter plan": {"verdict": "contradicts"}})
    assert y_cost(ctx).state == "unknown" and ctx.report.decision_flip_count == 0


def test_V03_two_verified_conflicting_scores_disputed():
    reseller = "A reseller lists VendorY at $400 per month for the same workload."
    ctx = run_xy("flip", text_override={Y_PRICING: f"{PRICE} {reseller}"},
                 items_override={Y_PRICING: [item("VendorY:cost", PRICE, "y cost $9", 2, 9, "USD/month"),
                                             item("VendorY:cost", reseller, "y cost $400", 0, 400, "USD/month")]})
    cell = y_cost(ctx)
    assert (cell.state, cell.lower, cell.upper) == ("disputed", 0, 2)
    assert ctx.report.recommended != "VendorY"  # conflict cannot produce a positive utility win
    assert ctx.report.decision_flip_count == 0
    # v3.1: both prices come from ONE page, so this is one internally inconsistent source, not two
    assert cell.dispute_kind == "source_inconsistent"
    assert any("Unresolved" in lim and "one source's own excerpts disagree" in lim for lim in ctx.report.limitations)


def test_V04_wrong_entity_rejected_by_verifier_and_lexical_check():
    # verifier flags wrong entity
    ctx = run_xy("flip", items_override=NO_REVIEW, verifier_rules={"Starter plan": {"mentions_alternative": False}})
    assert y_cost(ctx).state == "unknown"
    # verifier is fooled, but the lexical alias check still blocks an excerpt about another product
    other = "QuuxDB charges $9 per month for the Starter plan of the expected workload."
    ctx2 = run_xy("flip", text_override={Y_PRICING: other},
                  items_override={Y_PRICING: [item("VendorY:cost", other, "cheap", 2, 9, "USD/month")], **NO_REVIEW})
    assert any("lexical check" in r.reason for r in ctx2.rejected)
    assert y_cost(ctx2).state == "unknown"


def test_V05_verifier_failure_fails_closed():
    calls = {"n": 0}

    def broken(req):
        calls["n"] += 1
        return "this is not json"

    ctx = run_xy("flip", llm_overrides={"verify": broken})
    assert not ctx.evidence
    assert all("fail closed" in r.reason for r in ctx.rejected)
    assert calls["n"] >= 3  # bounded retries (1 + LLM_MAX_RETRIES) per verification call

    ctx = run_xy("flip", llm_overrides={"verify": lambda req: ToolError("timeout", "slow")})
    assert not ctx.evidence and ctx.report.status == "failed"


def test_V06_partial_is_note_not_progress():
    ctx = run_xy("flip", items_override=NO_REVIEW, verifier_rules={"Starter plan": {"verdict": "partial"}})
    assert ctx.report.stop_reason == "no_progress"


def test_V07_supported_but_score_not_justified_not_scored():
    ctx = run_xy("flip", verifier_rules={"single binary": {"justifies_proposed_score": False}})
    cell = ctx.cells()[("VendorY", "deployment")]
    assert (cell.state, cell.lower, cell.upper, cell.score) == ("insufficient", 0, 2, None)
    assert any("no derivable fit score" in r.reason for r in ctx.rejected)


def test_missing_verdict_for_candidate_rejected():
    def only_first(req):
        it = req.payload["items"][0]
        return {"verdicts": [{"candidate_id": it["candidate_id"], "verdict": "supports",
                              "mentions_alternative": True, "addresses_criterion": True,
                              "justifies_proposed_score": True, "note": ""}]}

    ctx = run_xy("flip", llm_overrides={"verify": only_first})
    assert any("no verdict returned" in r.reason for r in ctx.rejected)


def test_score_rejection_keeps_rationale_and_verifier_note_for_audit():
    """Diagnostic RUN_20261030T092400: 9 'no derivable fit score' rejections could not be audited because the
    record kept neither the extractor's rubric rationale nor the verifier's note. Logging only; acceptance is
    unchanged."""
    ctx = run_xy("flip", verifier_rules={"single binary": {"justifies_proposed_score": False,
                                                            "note": "deployment choice alone is not low effort"}})
    rej = [r for r in ctx.rejected if "no derivable fit score" in r.reason]
    assert rej and rej[0].rubric_rationale and rej[0].verifier_note == "deployment choice alone is not low effort"
