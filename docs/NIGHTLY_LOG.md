# Nightly Build Log

Add one entry per nightly run.

## Template
- Date:
- Built:
- Why this step:
- Key technical concepts:
- Files changed:
- Risks/limitations:
- Next step:

---

- Date: 2026-02-17
- Built: Initial FastAPI skeleton with application factory and `/health` endpoint, plus pinned runtime deps and a health endpoint test scaffold.
- Why this step: It is the top-priority item in `NEXT_STEPS.md` and creates a runnable API foundation for all upcoming LLM integration work.
- Key technical concepts:
  - FastAPI app factory (`create_app`) for easier testing and future config injection.
  - Liveness probe pattern via lightweight `/health` endpoint.
  - Dependency pinning (`requirements.txt`) to reduce environment drift.
  - Test-first API contract setup with `fastapi.testclient.TestClient`.
- Files changed:
  - `app/main.py`
  - `tests/test_health.py`
  - `requirements.txt`
- Risks/limitations:
  - Runtime test execution not performed yet because dependencies are not installed in this environment.
  - No startup config/env handling yet.
- Next step: Implement an OpenRouter client wrapper with clean interface, timeout handling, and basic error mapping.

- Date: 2026-02-17
- Built: Added a minimal OpenRouter client wrapper (`OpenRouterClient`) with env-based config loading, timeout/error mapping, and focused unit tests for success + failure paths.
- Why this step: It was the highest-priority remaining item and unlocks safe model-call plumbing before adding `/analyze`.
- Key technical concepts:
  - API client wrapper pattern to isolate third-party integration details.
  - Environment-driven secrets/config (`OPENROUTER_API_KEY`, timeout override).
  - Error taxonomy (`ConfigError`, `RequestError`, `TimeoutError`) so API routes can map failures cleanly.
  - Dependency injection in tests via monkeypatching `httpx.Client` to keep tests deterministic.
- Files changed:
  - `app/openrouter_client.py`
  - `tests/test_openrouter_client.py`
  - `requirements.txt`
- Risks/limitations:
  - Sanity check command `pytest -q` is currently blocked in this environment (`pytest: command not found`) until dependencies are installed.
  - Wrapper currently returns raw completion JSON; response normalization is not implemented yet.
- Next step: Add first `/analyze` endpoint with deterministic mock + response schema, then swap in OpenRouter behind the same contract.
