CONTRIBUTING.md
=================

Purpose
-------

This document describes the standard adapter pattern, naming conventions, testing rules, and CI/platform notes for adding TA-Lib-backed overlap indicators to this repository.

Backend
-------

- Use the Python bindings `ta-lib` (ta-lib-python) as the computation backend.
- Reference links:
  - TA-Lib C library: https://ta-lib.org/
  - ta-lib-python: https://github.com/TA-Lib/ta-lib-python

Files & Naming
---------------

- Indicator adapter files: `src/mcp_talib/indicators/<short_name>.py` (e.g., `bbands.py`).
- Adapter class: `<CamelName>Indicator` inheriting `BaseIndicator` (`src/mcp_talib/indicators/base.py`).
- Registry: register in `src/mcp_talib/indicators/__init__.py` via
  `registry.register("<short_name>", <CamelName>Indicator)`.
- MCP tool wrapper name: `calculate_<short_name>` in `src/mcp_talib/core/server.py`.
- Tests:
  - Unit: `tests/unit/test_<short_name>.py`
  - Integration: `tests/integration/<short_name>_tool_call.py`

Adapter Pattern
---------------

Each adapter should be a thin wrapper around the corresponding `ta` function.

1. `input_schema` — provide a Pydantic-style schema (or dict) indicating required arrays (`close`, `high`, `low`, etc.) and parameters. Enforce `high`/`low` where TA-Lib requires them (SAR, SAREXT, MIDPRICE).

2. `async calculate(self, market_data: MarketData, **params)` — implementation steps:
   - Convert input arrays to `numpy` arrays.
   - Call the corresponding TA-Lib function (e.g., `ta.BBANDS(...)`).
   - Map TA-Lib outputs into an `IndicatorResult`-compatible dict using TA-Lib default output names for multi-output functions.
   - Populate `metadata` with input params and output lengths.
   - Return a dict: `{ "success": True, "values": { ... }, "metadata": { ... } }` or an `IndicatorResult` instance if that is the repo pattern.

3. Error handling: raise or return `success: False` with `error_message` for invalid inputs, exceptions, or TA-Lib errors.

Testing (TDD)
-------------

- Write unit tests first. Unit tests should call TA-Lib directly to compute expected values and assert adapter output equality using `numpy.testing.assert_allclose` with sensible tolerances (e.g., `rtol=1e-6, atol=1e-8`).
- Include edge-case tests: empty input, short input, mismatched lengths, invalid params.
- Integration tests should exercise MCP tool exposure via stdio client (existing test patterns) and assert `success` + expected keys and lengths.

MCP / HTTP / CLI Exposure
-------------------------

- MCP tool wrappers in `src/mcp_talib/core/server.py` should forward `ToolRequest` fields to the registry executor. No changes to `http_api.py` are required unless strict per-indicator validation is desired.
- CLI uses `src/mcp_talib/cli_tools.py` existing helper to call MCP tools; no CLI changes required beyond testable parameter exposure.

CI & Platform Notes
-------------------

- The `ta-lib` Python package requires the native TA-Lib C library to be present on the system. CI must install the TA-Lib system package before installing Python deps. See:
  - https://ta-lib.org/ (official site and build instructions)
  - https://github.com/TA-Lib/ta-lib-python (Python bindings)
- Suggested CI steps: install system `ta-lib` (or use manylinux wheels), then `pip install TA-Lib` (or add `TA-Lib` to `pyproject.toml`). Document commands in `README.md`.

Multi-output naming
-------------------

- Use TA-Lib default output names (for example `upperband`, `middleband`, `lowerband`, `mama`, `fama`). Return multi-output results as a dict keyed by those names.

How to add a new indicator (summary)
-----------------------------------

1. Write unit tests under `tests/unit/` that compute expected results using `ta` directly.
2. Add `src/mcp_talib/indicators/<short_name>.py` implementing the adapter with `input_schema` and `calculate`.
3. Register adapter in `src/mcp_talib/indicators/__init__.py`.
4. Add MCP wrapper `calculate_<short_name>` in `src/mcp_talib/core/server.py` following existing patterns.
5. Add integration test under `tests/integration/`.
6. Update `tasks.md` status.

Notes
-----

- Prefer thin adapters and re-use utility functions (numpy conversion, validation) where available.
- Keep numeric tolerance assertions in tests to avoid fragile tests across platforms.
