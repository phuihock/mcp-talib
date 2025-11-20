"""Pytest configuration and fixtures."""

import asyncio
import pytest
import pytest_asyncio
from typing import AsyncGenerator

from src.mcp_talib.core.server import create_server
from src.mcp_talib.transport.stdio import StdioTransport


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def server():
    """Create a test MCP server instance."""
    return create_server()


@pytest_asyncio.fixture
async def stdio_transport(server):
    """Create a test STDIO transport instance."""
    transport = StdioTransport(server, debug=True)
    yield transport


@pytest.fixture
def sample_market_data():
    """Sample market data for testing."""
    return {
        "open": [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9],
        "high": [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
        "low": [0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8],
        "close": [1.05, 1.15, 1.25, 1.35, 1.45, 1.55, 1.65, 1.75, 1.85, 1.95],
    }


@pytest.fixture
def sample_sma_params():
    """Sample SMA parameters for testing."""
    return {
        "indicator": "SMA",
        "market_data": {
            "open": [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9],
            "high": [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0],
            "low": [0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8],
            "close": [1.05, 1.15, 1.25, 1.35, 1.45, 1.55, 1.65, 1.75, 1.85, 1.95],
        },
        "timeperiod": 5,
    }