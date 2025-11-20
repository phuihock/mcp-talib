"""Tests for HTTP API tools list endpoint."""

import pytest
from fastapi.testclient import TestClient

from src.mcp_talib.core.server import create_server
from src.mcp_talib.http_api import create_http_app


@pytest.fixture
def client():
    """Create a test client for the HTTP API."""
    mcp = create_server()
    app = create_http_app(mcp)
    return TestClient(app)


def test_list_tools_returns_all_indicators(client):
    """Test that /api/tools returns all registered indicators."""
    response = client.get("/api/tools")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify the response has the expected structure
    assert "tools" in data
    assert isinstance(data["tools"], list)
    assert len(data["tools"]) > 0
    
    # Verify all expected indicators are present
    expected_tools = {
        "sma", "ema", "rsi", "bbands", "dema", "ht_trendline",
        "kama", "ma", "mama", "mavp", "midpoint", "midprice",
        "sar", "sarext", "t3", "tema", "trima", "wma"
    }
    
    tools_set = set(data["tools"])
    assert tools_set == expected_tools, (
        f"Missing tools: {expected_tools - tools_set}, "
        f"Extra tools: {tools_set - expected_tools}"
    )


def test_list_tools_are_sorted(client):
    """Test that tools list is sorted alphabetically."""
    response = client.get("/api/tools")
    tools = response.json()["tools"]
    
    assert tools == sorted(tools), "Tools should be sorted alphabetically"


def test_tools_are_callable(client):
    """Test that each listed tool can actually be called."""
    response = client.get("/api/tools")
    tools = response.json()["tools"]
    
    # Sample data for testing
    sample_close_prices = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    
    for tool_name in tools:
        # Try to call each tool with minimal valid input
        payload = {"close": sample_close_prices, "timeperiod": 3}
        
        response = client.post(f"/api/tools/{tool_name}", json=payload)
        
        # Should not return 404 (tool exists)
        assert response.status_code != 404, f"Tool {tool_name} returned 404"
        
        # Should return valid JSON response
        result = response.json()
        assert "success" in result, f"Tool {tool_name} response missing 'success' field"


def test_list_tools_endpoint_content_type(client):
    """Test that /api/tools returns proper JSON content type."""
    response = client.get("/api/tools")
    
    assert response.headers.get("content-type") == "application/json"
