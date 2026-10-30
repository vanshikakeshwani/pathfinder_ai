"""Shared offline helpers. All data here is SYNTHETIC."""

from __future__ import annotations

import pytest

from pathfinder.config import Settings
from pathfinder.demo_fixtures import XY_QUESTION, xy_plan_draft, xy_scenario
from pathfinder.planner import normalize_plan
from pathfinder.runner import make_context, run


def no_sleep(_seconds: float) -> bool:
    return False


def test_settings(**overrides) -> Settings:
    return Settings(**overrides)


test_settings.__test__ = False  # not a test


def build_ctx(llm, search, contents, settings: Settings | None = None, **kw):
    return make_context(kw.pop("question", XY_QUESTION), settings or Settings(), llm, search, contents,
                        sleeper=no_sleep, synthetic=True, **kw)


def run_xy(variant: str = "flip", settings: Settings | None = None, **kw):
    scenario_kw = {k: kw.pop(k) for k in ("cost_weight", "verifier_rules", "llm_overrides", "items_override",
                                          "text_override") if k in kw}
    llm, search, contents = xy_scenario(variant, **scenario_kw)
    ctx = build_ctx(llm, search, contents, settings, **kw)
    run(ctx)
    return ctx


def xy_plan(cost_weight: int = 5, deploy_weight: int = 3):
    return normalize_plan(XY_QUESTION, xy_plan_draft(cost_weight, deploy_weight), {}, 2)[0]


@pytest.fixture
def plan():
    return xy_plan()
