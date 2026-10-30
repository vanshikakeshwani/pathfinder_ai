"""Runtime settings loaded from the environment (.env supported).

Keys are held as SecretStr so they never appear in reprs, logs or outputs.
Optional caps (MAX_LLM_CALLS, MAX_SECONDS) are disabled when empty.
"""

from __future__ import annotations

import os
from typing import Literal

from pydantic import BaseModel, Field, SecretStr, field_validator

StructuredMode = Literal["json_schema", "json_object", "prompt"]


class Settings(BaseModel):
    # LLM gateway
    llm_provider: str = "experiential"
    llm_model: str = "gpt-6-luna"
    llm_base_url: str = "https://api.experientiallabs.ai/v1"
    explabs_api_key: SecretStr | None = None
    llm_request_timeout_s: float = Field(default=60.0, gt=0)
    llm_max_retries: int = Field(default=2, ge=0, le=5)
    llm_temperature: float | None = 0.0
    llm_structured_mode: StructuredMode = "json_schema"

    # Research tools
    exa_api_key: SecretStr | None = None
    exa_request_timeout_s: float = Field(default=20.0, gt=0)
    exa_max_retries: int = Field(default=2, ge=0, le=5)

    # Research-action budget (always enforced)
    max_search_calls: int = Field(default=6, ge=1, le=50)
    max_content_pages: int = Field(default=8, ge=1, le=100)
    max_research_rounds: int = Field(default=3, ge=0, le=20)
    # 2, not the blueprint's 1: in the first live Q1 run a single failed target ended the run with
    # 7/9 cells unknown and half the search budget unused (see docs/tradeoffs.md).
    max_no_progress: int = Field(default=2, ge=1, le=10)
    max_evidence_per_round: int = Field(default=12, ge=1, le=50)
    max_initial_queries: int = Field(default=2, ge=1, le=5)
    results_per_search: int = Field(default=5, ge=1, le=10)
    pages_per_search: int = Field(default=2, ge=1, le=5)

    # Optional caps
    max_llm_calls: int | None = Field(default=None, ge=1)
    max_seconds: float | None = Field(default=None, gt=0)

    output_dir: str = "outputs"

    @field_validator("max_llm_calls", "max_seconds", "llm_temperature", "explabs_api_key",
                     "exa_api_key", mode="before")
    @classmethod
    def _empty_is_none(cls, v):
        if isinstance(v, str) and not v.strip():
            return None
        return v

    def secret_values(self) -> list[str]:
        """Secret strings that must never appear in any output file."""
        return [s.get_secret_value() for s in (self.explabs_api_key, self.exa_api_key)
                if s is not None and s.get_secret_value()]


_ENV_FIELDS = [name for name in Settings.model_fields]


def load_settings(env_file: str | None = ".env", **overrides) -> Settings:
    if env_file and os.path.exists(env_file):
        from dotenv import load_dotenv

        load_dotenv(env_file, override=False)
    values: dict = {}
    for name in _ENV_FIELDS:
        raw = os.environ.get(name.upper())
        if raw is not None:
            values[name] = raw
    values.update(overrides)
    return Settings(**values)
