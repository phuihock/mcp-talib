# TA-Lib Overlap Studies — Tasks

Notes:
- Backend: `ta-lib` (ta-lib-python). See `CONTRIBUTING.md` for CI/platform steps.
- Naming: MCP tools are `calculate_<short_name>`, adapter classes `<CamelName>Indicator`.
- Tests: follow TDD (unit using `ta`, integration via MCP stdio client).

- [ ] BBANDS (`bbands.py`) — Medium
  - [x] Add unit tests `tests/unit/test_bbands.py` (TDD)
  - [x] Implement `src/mcp_talib/indicators/bbands.py` → `BBANDSIndicator`
  - [x] Register in `src/mcp_talib/indicators/__init__.py`
  - [x] Add MCP wrapper `calculate_bbands` in `src/mcp_talib/core/server.py`
  - [x] Add integration test `tests/integration/bbands_tool_call.py`

- [ ] DEMA (`dema.py`) — Medium
  - [ ] unit tests
  - [ ] adapter `DEMAIndicator`
  - [ ] register, MCP wrapper, integration test

- [x] EMA (`ema.py`) — (already implemented)
  - [ ] verify TA-Lib adapter parity / tests

- [ ] HT_TRENDLINE (`ht_trendline.py`) — High
  - [ ] unit tests (compare to `ta.HT_TRENDLINE`)
  - [ ] adapter, register, MCP, integration

- [ ] KAMA (`kama.py`) — Medium

- [ ] MA (`ma.py`) — Medium
  - [ ] expose `matype` param to select underlying MA type

 - [x] MAMA (`mama.py`) — High (multi-output: `mama`, `fama`)
  - [x] unit tests
  - [x] Implemented adapter
  - [x] Registered
  - [x] MCP wrapper

- [ ] MAVP (`mavp.py`) — Medium

- [ ] MIDPOINT (`midpoint.py`) — Low

- [ ] MIDPRICE (`midprice.py`) — Low (requires `high` and `low`)

 - [x] SAR (`sar.py`) — Medium (requires `high` and `low`)
  - [x] unit tests
  - [x] Implemented adapter
  - [x] Registered
  - [x] MCP wrapper

- [ ] SAREXT (`sarext.py`) — High (many params, complex behavior)

- [x] SMA (`sma.py`) — (already implemented)
  - [ ] verify tests exist / TA-Lib parity

- [ ] T3 (`t3.py`) — High

- [ ] TEMA (`tema.py`) — Medium

- [ ] TRIMA (`trima.py`) — Medium

- [ ] WMA (`wma.py`) — Low

General checklist for each indicator:
- [ ] Write unit tests first (compare adapter to `ta` outputs)
- [ ] Implement adapter under `src/mcp_talib/indicators/`
- [ ] Register in `src/mcp_talib/indicators/__init__.py`
- [ ] Add MCP wrapper in `src/mcp_talib/core/server.py`
- [ ] Add integration test (stdio client)
- [ ] Update `tasks.md` (mark done)

Estimated effort keys: Low / Medium / High shown per indicator.
