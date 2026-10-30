"""Evaluation protocol V2 (SYNTHETIC, offline record/replay): pairing, views, fairness, spend accounting."""

import json

from conftest import xy_plan

from pathfinder.config import Settings
from pathfinder.demo_fixtures import XY_QUESTION, xy_scenario
from pathfinder.evaluation import (
    FIELDS,
    config_fingerprint,
    plan_hash,
    run_pair,
    stop_index,
    store_spend,
    write_csv,
)
from pathfinder.replay import RecordingContents, RecordingLLM, RecordingSearch, SnapshotStore
from pathfinder.retry import ToolError

VOLATILE = {"run_id", "timestamp", "llm_model"}


def recorded(tmp_path, mode, inner=None, name="rep1"):
    store = SnapshotStore(tmp_path / f"{name}.json")
    inner = inner or (None, None, None)
    return (RecordingLLM(inner[0], store, mode, "fixture"), RecordingSearch(inner[1], store, mode),
            RecordingContents(inner[2], store, mode))


def stable(row):
    return {k: v for k, v in row.items() if k not in VOLATILE}


def pair(tmp_path, mode="record", fixture=None, out="o", **kw):
    fixture = fixture or (xy_scenario("flip", **kw) if mode == "record" else None)
    return run_pair(XY_QUESTION, "XY", xy_plan(), Settings(), lambda: recorded(tmp_path, mode, fixture),
                    1, tmp_path / out, synthetic=True, config_fp="fp")


def by(rows, arm, view):
    return next(r for r in rows if r["arm"] == arm and r["view"] == view)


def test_E01_replay_is_repeatable_and_matches_record(tmp_path):
    rec = pair(tmp_path, "record")
    rep1, rep2 = pair(tmp_path, "replay", out="r1"), pair(tmp_path, "replay", out="r2")
    assert [stable(r) for r in rep1] == [stable(r) for r in rep2] == [stable(r) for r in rec]


def test_replay_miss_is_an_error_not_a_network_call(tmp_path):
    _, search, _ = recorded(tmp_path, "replay")
    try:
        search.search("never recorded", 5, None, 1.0)
    except ToolError as e:
        assert e.kind == "replay_miss"
    else:
        raise AssertionError("expected replay_miss")


def test_E02_pair_shares_plan_round0_budget_and_has_both_views(tmp_path):
    rows = pair(tmp_path)
    assert {(r["arm"], r["view"]) for r in rows} == {(a, v) for a in ("static", "adaptive")
                                                     for v in ("common_stop", "full_budget")}
    assert len({r["plan_hash"] for r in rows}) == 1 and rows[0]["plan_hash"] == plan_hash(xy_plan())
    assert len({r["round0_hash"] for r in rows}) == 1 and "MISMATCH" not in rows[0]["stop_reason"]
    assert set(rows[0]) == set(FIELDS)


def test_E02_record_mode_gives_identical_round0_with_nondeterministic_llm(tmp_path):
    """Regression from live V1 Q2: record mode re-called the live LLM per arm and round 0 diverged."""
    fixture = xy_scenario("flip")
    extract = fixture[0].handlers["extract"]
    calls = {"n": 0}

    def drifting_extract(req):
        calls["n"] += 1
        out = extract(req)
        for it in out["items"]:
            it["claim"] = f"{it['claim']} (sample {calls['n']})"
        return out

    fixture[0].handlers["extract"] = drifting_extract
    rows = pair(tmp_path, fixture=fixture)
    assert len({r["round0_hash"] for r in rows}) == 1


def test_common_stop_view_is_an_exact_prefix_of_the_full_trajectory(tmp_path):
    rows = pair(tmp_path)
    traj = [json.loads(x) for x in (tmp_path / "o" / "trajectories.jsonl").read_text("utf-8").splitlines()]
    ad = next(t for t in traj if t["arm"] == "adaptive")["trajectory"]
    i = stop_index(ad)
    c = by(rows, "adaptive", "common_stop")
    assert (c["actions"], c["units_supported"], c["rounds"]) == (ad[i]["actions"], ad[i]["units_supported"],
                                                                  ad[i]["round"])
    f = by(rows, "adaptive", "full_budget")
    assert f["actions"] >= c["actions"]


def test_both_arms_use_the_same_stopping_rule_and_static_is_not_adaptive(tmp_path):
    rows = pair(tmp_path)
    s, a = by(rows, "static", "common_stop"), by(rows, "adaptive", "common_stop")
    # static targets follow the fixed round-robin schedule, independent of findings
    assert s["targeted_actions"].split(" | ")[0] == "VendorX:cost"
    assert a["targeted_actions"].split(" | ")[0] == "VendorY:cost"
    # the common rule is evaluated identically: both views carry an explicit stop reason
    assert s["stop_reason"] and a["stop_reason"]


def test_metrics_use_spent_counts_and_flip_is_counted(tmp_path):
    rows = pair(tmp_path)
    a = by(rows, "adaptive", "full_budget")
    assert int(a["actions"]) == int(a["search_calls"]) + int(a["content_pages"])
    assert a["flips"] == 1 and a["interval_leader"] == "VendorY" and a["recommendation"] == "ready"


def test_config_fingerprint_separates_budget_settings_and_protocol():
    fp8, _ = config_fingerprint(Settings(max_content_pages=8))
    fp12, cfg = config_fingerprint(Settings(max_content_pages=12))
    assert fp8 != fp12 and cfg["max_content_pages"] == 12 and cfg["protocol"] == "v3.2"  # earlier protocols' recordings are never reused
    assert config_fingerprint(Settings(max_content_pages=12, exa_api_key="k"))[0] == fp12  # keys excluded


def test_provider_costs_are_captured_and_survive_record_replay(tmp_path):
    llm, search, contents = xy_scenario("flip")
    search.last_cost_usd = 0.007
    contents.last_cost_usd = 0.001
    rows = pair(tmp_path, fixture=(llm, search, contents))
    rep = pair(tmp_path, "replay", out="r")
    a, ar = by(rows, "adaptive", "full_budget"), by(rep, "adaptive", "full_budget")
    assert a["exa_cost_usd"] == ar["exa_cost_usd"] and a["exa_cost_usd"] > 0
    spend = store_spend([tmp_path / "rep1.json"])
    assert spend["recorded_calls"] > 0 and spend["total_reported_usd"] == spend["exa_cost_usd"]


def test_eval_report_and_review_from_recorded_runs(tmp_path):
    from pathfinder.eval_report import build, load_rows, replay_diff

    def one(mode, folder):
        rows = pair(tmp_path, mode, out=folder)
        out = tmp_path / folder
        write_csv(rows, out / "results.csv")
        (out / "config.json").write_text(json.dumps({"protocol": "v2", "mode": mode, "config_fp": "fp",
                                                     "settings": {}, "question_ids": ["XY"], "repeat": 1,
                                                     "started": "t"}))
        return out

    rec, rep = one("record", "rec"), one("replay", "rep")
    assert replay_diff(load_rows(rec), load_rows(rep)) == []
    build(rec, rep, tmp_path / "REPORT.md", tmp_path / "review")
    report = (tmp_path / "REPORT.md").read_text("utf-8")
    review = (tmp_path / "review" / "AI_PROVISIONAL_REVIEW.md").read_text("utf-8")
    worksheet = (tmp_path / "review" / "HUMAN_REVIEW_WORKSHEET.csv").read_text("utf-8").splitlines()
    assert "all 4 rows identical" in report  # 2 arms x 2 views and "Targeting value" in report and "Stopping value" in report
    assert "AI-PROVISIONAL, NOT HUMAN EVALUATION" in review and "**0 invalid**" in review
    assert len(worksheet) == 3 and worksheet[1].endswith("," * 14)  # 2 runs, human columns blank


def test_equal_incomplete_coverage_is_not_reported_as_a_benefit():
    from pathfinder.eval_report import classify

    s = {"coverage": "0.2", "actions": "15"}
    assert classify(s, {"coverage": "0.2", "actions": "12"}) == \
        "NO coverage benefit (equal, incomplete); adaptive fewer actions"
    assert classify({"coverage": "0.5", "actions": "15"}, {"coverage": "0.2", "actions": "12"}) == \
        "adaptive WORSE coverage"
    assert classify({"coverage": "1.0", "actions": "15"}, {"coverage": "1.0", "actions": "6"}) == \
        "equal full coverage, adaptive fewer actions"


# ---------------------------------------------------------------------------------------- protocol V3


def test_v3_arms_share_plan_and_round0_and_ablation_names_are_validated(tmp_path):
    import pytest

    from pathfinder.evaluation import arm_policy

    fixture = xy_scenario("flip")
    rows = run_pair(XY_QUESTION, "XY", xy_plan(), Settings(), lambda: recorded(tmp_path, "record", fixture), 1,
                    tmp_path / "o", synthetic=True, config_fp="fp",
                    arms=("static", "adaptive", "v2_policy", "no_retry"))
    assert {r["arm"] for r in rows} == {"static", "adaptive", "v2_policy", "no_retry"}
    assert len({r["round0_hash"] for r in rows}) == 1 and len({r["plan_hash"] for r in rows}) == 1
    assert {r["policy"] for r in rows if r["arm"] == "adaptive"} == {"v3"}
    with pytest.raises(ValueError):
        arm_policy("best_policy_ever")


def _eval_args(tmp_path, **kw):
    import argparse

    q = tmp_path / "queries.json"
    q.write_text(json.dumps({"questions": [{"id": "XY", "mode": "comparison", "required": True,
                                            "question": XY_QUESTION}]}), encoding="utf-8")
    base = dict(queries=str(q), ids=None, snapshots=str(tmp_path / "snaps"), record=True, replay=False, repeat=2,
                max_usd=None, output_dir=str(tmp_path / "out"), arms=None, plans_dir=None)
    base.update(kw)
    return argparse.Namespace(**base)


def test_v3_one_fixed_plan_per_question_is_reused_by_every_repetition(tmp_path, monkeypatch):
    import pathfinder.runner as runner_mod
    from pathfinder.evaluation import evaluate

    monkeypatch.setattr(runner_mod, "live_clients", lambda settings: xy_scenario("flip"))
    assert evaluate(_eval_args(tmp_path), Settings()) == 0
    out = next((tmp_path / "out").iterdir())
    rows = list(__import__("csv").DictReader((out / "results.csv").open(encoding="utf-8")))
    assert {r["repeat"] for r in rows} == {"1", "2"} and len({r["plan_hash"] for r in rows}) == 1
    fp_dir = next((tmp_path / "snaps" / "XY").iterdir())
    names = {p.name for p in fp_dir.iterdir()}
    assert "plan_fixed.json" in names and not any(n.startswith("plan_rep") for n in names)
    assert {"rep1.json", "rep2.json"} <= names  # retrieval still recorded independently per repetition
    assert (out / "plans" / "XY.json").exists()


def test_v3_frozen_plan_file_is_used_without_a_planner_call(tmp_path, monkeypatch):
    import pathfinder.runner as runner_mod
    from pathfinder.evaluation import evaluate, load_frozen_plan

    frozen = tmp_path / "plans"
    frozen.mkdir()
    (frozen / "XY.json").write_text(json.dumps({"plan": xy_plan().model_dump(mode="json"),
                                                "provenance": {"note": "test"}}), encoding="utf-8")
    assert load_frozen_plan(frozen / "XY.json") == xy_plan()
    monkeypatch.setattr(runner_mod, "live_clients", lambda settings: xy_scenario("flip"))
    assert evaluate(_eval_args(tmp_path, plans_dir=str(frozen), repeat=1), Settings()) == 0
    fp_dir = next((tmp_path / "snaps" / "XY").iterdir())
    assert not (fp_dir / "plan_fixed.json").exists()
    out = next((tmp_path / "out").iterdir())
    cfg = json.loads((out / "config.json").read_text("utf-8"))
    assert cfg["plans"]["XY"]["plan_hash"] == plan_hash(xy_plan()) and cfg["arms"] == ["static", "adaptive"]


def test_static_schedule_is_unchanged_by_v3():
    """Fairness guard: the static arm's targets and queries are exactly the V2 round-robin schedule."""
    from pathfinder.planner import static_queue

    q = static_queue(xy_plan())
    assert [t for t, _, _ in q] == ["VendorX:cost", "VendorY:deployment", "VendorX:deployment", "VendorY:cost"]
    assert q[0][1] == "VendorX cost pricing plans official documentation"


def test_eval_report_handles_discovery_rows_with_blank_cell_metrics(tmp_path):
    """Regression (V3.2 benchmark): discovery rows have blank cell-level metrics; the report must not crash."""
    from pathfinder.eval_report import _num, _paired

    assert _num("") is None and _paired([]) == "n/a"
