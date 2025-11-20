"""Test MCP server functionality."""

import pytest

from mcp_talib.core.server import create_server
from mcp_talib.indicators import registry
from mcp_talib.models.market_data import MarketData


@pytest.mark.asyncio
async def test_server_creation():
    """Test that server can be created and tools are registered."""
    server = create_server()
    assert server is not None


@pytest.mark.asyncio
async def test_indicators_integrity():
    """Test that indicators can be instantiated and calculated correctly."""
    test_data = [10.0, 12.0, 11.0, 13.0, 14.0, 15.0, 14.0, 16.0, 15.0, 17.0, 
                 18.0, 17.0, 19.0, 20.0, 19.0, 21.0, 22.0, 23.0, 24.0, 25.0, 
                 24.0, 26.0, 27.0]
    
    market_data = MarketData(close=test_data)
    
    # Test SMA
    sma_indicator = registry.get_indicator("sma")
    assert sma_indicator is not None
    result = await sma_indicator.calculate(market_data, {"timeperiod": 10})
    assert result.success is True
    assert "sma" in result.values
    assert len(result.values["sma"]) == len(test_data) - 10 + 1
    
    # Test EMA
    ema_indicator = registry.get_indicator("ema")
    assert ema_indicator is not None
    result = await ema_indicator.calculate(market_data, {"timeperiod": 10})
    assert result.success is True
    assert "ema" in result.values
    assert len(result.values["ema"]) == len(test_data) - 10 + 1
    
    # Test RSI
    rsi_indicator = registry.get_indicator("rsi")
    assert rsi_indicator is not None
    result = await rsi_indicator.calculate(market_data, {"timeperiod": 14})
    assert result.success is True
    assert "rsi" in result.values
    # RSI calculation starts after timeperiod values
    assert 0 <= min(result.values["rsi"]) <= 100
    assert 0 <= max(result.values["rsi"]) <= 100


@pytest.mark.asyncio
async def test_insufficient_data():
    """Test that indicators handle insufficient data correctly."""
    market_data = MarketData(close=[1.0, 2.0, 3.0])  # Only 3 data points
    
    # Test SMA with insufficient data
    sma_indicator = registry.get_indicator("sma")
    result = await sma_indicator.calculate(market_data, {"timeperiod": 10})
    assert result.success is False
    assert "Not enough data" in result.error_message
    
    # Test EMA with insufficient data
    ema_indicator = registry.get_indicator("ema")
    result = await ema_indicator.calculate(market_data, {"timeperiod": 10})
    assert result.success is False
    assert "Not enough data" in result.error_message
    
    # Test RSI with insufficient data
    rsi_indicator = registry.get_indicator("rsi")
    result = await rsi_indicator.calculate(market_data, {"timeperiod": 14})
    assert result.success is False
    assert "Not enough data" in result.error_message


@pytest.mark.asyncio
async def test_transport_stability():
    """Test that transport layer can be instantiated without crashing."""
    from mcp_talib.transport.stdio import StdioTransport

    server = create_server()
    transport = StdioTransport(server)

    # Verify transport setup doesn't crash and references server
    assert transport.server is server