"""Optional deep-research configuration (.env.deep.example): valid, internally consistent, opt-in only."""

from pathlib import Path

from dotenv import dotenv_values

from pathfinder.config import Settings, load_settings

ROOT = Path(__file__).resolve().parents[1]
DEEP = {k.lower(): v for k, v in dotenv_values(ROOT / ".env.deep.example").items()}


def test_deep_example_parses_into_valid_settings():
    s = Settings(**DEEP)
    assert (s.max_research_rounds, s.max_search_calls, s.max_content_pages, s.max_llm_calls, s.max_seconds,
            s.max_no_progress) == (5, 8, 16, 20, 360.0, 2)


def test_deep_budget_is_internally_consistent():
    s = Settings(**DEEP)
    searches_needed = s.max_initial_queries + s.max_research_rounds  # round 0 + one search per targeted round
    assert searches_needed <= s.max_search_calls
    assert searches_needed * s.pages_per_search <= s.max_content_pages
    # plan + (rounds + 1) x (extract + verify) + report, before retries, fits under the LLM cap
    assert 1 + (s.max_research_rounds + 1) * 2 + 1 <= s.max_llm_calls


def test_deep_mode_is_opt_in_and_defaults_are_unchanged():
    d = Settings()
    assert (d.max_research_rounds, d.max_search_calls, d.max_content_pages, d.max_no_progress,
            d.max_llm_calls, d.max_seconds) == (3, 6, 8, 2, None, None)
    # request-level timeouts and retries are not part of the deep profile
    assert not {"llm_request_timeout_s", "exa_request_timeout_s", "llm_max_retries", "exa_max_retries"} & set(DEEP)


def test_process_environment_overrides_dotenv(tmp_path, monkeypatch):
    env = tmp_path / ".env"
    env.write_text("MAX_RESEARCH_ROUNDS=3\nMAX_SEARCH_CALLS=6\n", encoding="utf-8")
    monkeypatch.setenv("MAX_RESEARCH_ROUNDS", "5")
    monkeypatch.setenv("MAX_SEARCH_CALLS", "8")
    s = load_settings(str(env))
    assert (s.max_research_rounds, s.max_search_calls) == (5, 8)


def test_deep_settings_run_the_full_loop_offline():
    """SYNTHETIC fixture: the graph accepts the deep limits and still stops with an explicit reason."""
    from conftest import build_ctx

    from pathfinder.demo_fixtures import xy_scenario
    from pathfinder.runner import run

    ctx = build_ctx(*xy_scenario("irrelevant"), Settings(**DEEP))
    run(ctx)
    assert ctx.stop_reason in ("no_progress", "budget_exhausted", "stable", "insufficient_evidence")
    assert ctx.budget.search_calls <= 8 and ctx.budget.content_pages <= 16 and ctx.budget.llm_calls <= 20
