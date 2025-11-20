import json

from fastapi.testclient import TestClient

from mcp_talib.http_api_server import create_http_api_app
from mcp_talib import indicators


class FakeIndicator:
    async def calculate(self, market_data, params):
        class Result:
            def __init__(self):
                self.success = True
                self.values = [1.0, 2.0, 3.0]
                self.metadata = {"timeperiod": params.get("timeperiod")}

        return Result()


def test_list_tools(monkeypatch):
    def fake_list():
        return ["sma", "ema", "rsi"]

    monkeypatch.setattr(indicators.registry, "list_indicators", fake_list, raising=False)

    app = create_http_api_app()
    client = TestClient(app)

    r = client.get("/api/tools")
    assert r.status_code == 200
    data = r.json()
    assert "tools" in data
    assert "sma" in data["tools"]


def test_call_tool_success(monkeypatch):
    monkeypatch.setattr(indicators.registry, "get_indicator", lambda name: FakeIndicator(), raising=False)

    app = create_http_api_app()
    client = TestClient(app)

    payload = {"close": [1, 2, 3, 4, 5], "timeperiod": 3}
    r = client.post("/api/tools/sma", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["success"] is True
    assert isinstance(data.get("values"), list)


def test_call_tool_returns_dict_values(monkeypatch):
    """If indicator returns dict values (named series), API should return the dict intact."""
    class DictIndicator:
        async def calculate(self, market_data, params):
            class Result:
                def __init__(self):
                    self.success = True
                    self.values = {"sma": [10, 20, 30]}
                    self.metadata = {"timeperiod": params.get("timeperiod")}

            return Result()

    monkeypatch.setattr(indicators.registry, "get_indicator", lambda name: DictIndicator(), raising=False)

    app = create_http_api_app()
    client = TestClient(app)

    payload = {"close": [1, 2, 3, 4, 5], "timeperiod": 3}
    r = client.post("/api/tools/sma", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["success"] is True
    assert isinstance(data.get("values"), dict)
    assert data["values"].get("sma") == [10, 20, 30]


def test_call_tool_missing_close(monkeypatch):
    monkeypatch.setattr(indicators.registry, "get_indicator", lambda name: FakeIndicator(), raising=False)

    app = create_http_api_app()
    client = TestClient(app)

    r = client.post("/api/tools/sma", json={"timeperiod": 3})
    # missing required field 'close' -> Pydantic/FastAPI returns 422
    assert r.status_code == 422


def test_call_tool_not_found(monkeypatch):
    monkeypatch.setattr(indicators.registry, "get_indicator", lambda name: None, raising=False)

    app = create_http_api_app()
    client = TestClient(app)

    payload = {"close": [1, 2, 3], "timeperiod": 3}
    r = client.post("/api/tools/unknown_tool", json=payload)
    # API returns HTTP 404 for unknown tools
    assert r.status_code == 404
    data = r.json()
    # FastAPI HTTPException returns a JSON body with 'detail'
    assert data.get("detail") == "tool not found"
