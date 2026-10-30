# Gateway compatibility (smoke test)

- Run at: 2026-10-29T23:33:37+00:00
- Base URL: https://api.experientiallabs.ai/v1
- Model: gpt-6-luna
- Recommended `LLM_STRUCTURED_MODE`: **json_schema**

| Check | OK | Detail | ms |
|---|---|---|---|
| basic_completion | yes | {"model": "gpt-6-luna", "usage": {"completion_tokens": 82, "prompt_tokens": 23, "total_tokens": 105, "completion_tokens_details": {"accepted_prediction_tokens": null, "audio_tokens": null, "reasoning_ | 3594 |
| strict_json_schema | yes | "validated against Pydantic schema" | 2823 |
| json_object_mode | NO | "ValidationError: 3 validation errors for _Probe\ncity\n  Field required [type=missing, input_value={'properties': {'city': {...robe', 'type': 'object'}, input_type=dict]\n    For further information  | 3325 |
| temperature_seed | yes | "accepted temperature=0 and seed=7" | 3580 |
| error_shape | yes | "PermissionDeniedError status=403" | 313 |
