"""Pure MCP server with all TA-Lib indicator tools.

This module provides create_mcp_server() which returns a FastMCP instance
with all registered indicators exposed as MCP tools. It contains no HTTP API
endpoints—use this for stdio/SSE/streamable-http transports.

Usage:
    from mcp_talib.core.mcp_server import create_mcp_server
    
    # Create MCP server with all indicator tools
    mcp = create_mcp_server()
    
    # Run with different transports:
    # - STDIO: mcp.run()
    # - HTTP: mcp.run(transport="http", host="0.0.0.0", port=8000)
    # - SSE: mcp.run(transport="sse", host="0.0.0.0", port=8000)
"""

from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP

from ..indicators import registry
from ..models.market_data import MarketData


# Tool definitions: indicator name, description, and parameter specifications
TOOL_SPECS = {
    "sma": {
        "description": "Simple Moving Average (SMA)",
        "params": {"close_prices": List[float], "timeperiod": int},
        "defaults": {"timeperiod": 20},
        "market_data_args": {"close": "close_prices"},
    },
    "ema": {
        "description": "Exponential Moving Average (EMA)",
        "params": {"close_prices": List[float], "timeperiod": int},
        "defaults": {"timeperiod": 20},
        "market_data_args": {"close": "close_prices"},
    },
    "rsi": {
        "description": "Relative Strength Index (RSI)",
        "params": {"close_prices": List[float], "timeperiod": int},
        "defaults": {"timeperiod": 14},
        "market_data_args": {"close": "close_prices"},
    },
    "bbands": {
        "description": "Bollinger Bands (BBANDS)",
        "params": {"close_prices": List[float], "timeperiod": int, "nbdevup": float, "nbdevdn": float, "matype": int},
        "defaults": {"timeperiod": 20, "nbdevup": 2.0, "nbdevdn": 2.0, "matype": 0},
        "market_data_args": {"close": "close_prices"},
    },
    "dema": {
        "description": "Double Exponential Moving Average (DEMA)",
        "params": {"close_prices": List[float], "timeperiod": int},
        "defaults": {"timeperiod": 30},
        "market_data_args": {"close": "close_prices"},
    },
    "ht_trendline": {
        "description": "Hilbert Transform Trendline",
        "params": {"close_prices": List[float]},
        "defaults": {},
        "market_data_args": {"close": "close_prices"},
    },
    "kama": {
        "description": "Kaufman Adaptive Moving Average (KAMA)",
        "params": {"close_prices": List[float], "timeperiod": int},
        "defaults": {"timeperiod": 10},
        "market_data_args": {"close": "close_prices"},
    },
    "ma": {
        "description": "Moving Average (MA)",
        "params": {"close_prices": List[float], "timeperiod": int, "matype": int},
        "defaults": {"timeperiod": 30, "matype": 0},
        "market_data_args": {"close": "close_prices"},
    },
    "mama": {
        "description": "MESA Adaptive Moving Average (MAMA)",
        "params": {"close_prices": List[float], "fastlimit": float, "slowlimit": float},
        "defaults": {"fastlimit": 0.5, "slowlimit": 0.05},
        "market_data_args": {"close": "close_prices"},
    },
    "mavp": {
        "description": "Moving Average Variable Period (MAVP)",
        "params": {"close_prices": List[float], "periods": Optional[float], "minperiod": int, "maxperiod": int},
        "defaults": {"periods": None, "minperiod": 2, "maxperiod": 30},
        "market_data_args": {"close": "close_prices"},
    },
    "midpoint": {
        "description": "Midpoint (MIDPOINT)",
        "params": {"close_prices": List[float], "timeperiod": int},
        "defaults": {"timeperiod": 14},
        "market_data_args": {"close": "close_prices"},
    },
    "midprice": {
        "description": "Midpoint Price (MIDPRICE)",
        "params": {"high_prices": List[float], "low_prices": List[float], "timeperiod": int},
        "defaults": {"timeperiod": 14},
        "market_data_args": {"high": "high_prices", "low": "low_prices"},
    },
    "sar": {
        "description": "Parabolic SAR",
        "params": {"high_prices": List[float], "low_prices": List[float], "acceleration": float, "maximum": float},
        "defaults": {"acceleration": 0.02, "maximum": 0.2},
        "market_data_args": {"high": "high_prices", "low": "low_prices"},
    },
    "sarext": {
        "description": "Parabolic SAR Extended (SAREXT)",
        "params": {
            "high_prices": List[float], 
            "low_prices": List[float], 
            "startvalue": Optional[float],
            "offsetonreverse": float,
            "acceleration_initlong": float,
            "acceleration_long": float,
            "acceleration_maxlong": float,
            "acceleration_initshort": float,
            "acceleration_short": float,
            "acceleration_maxshort": float,
        },
        "defaults": {
            "startvalue": None,
            "offsetonreverse": 0.0,
            "acceleration_initlong": 0.02,
            "acceleration_long": 0.02,
            "acceleration_maxlong": 0.2,
            "acceleration_initshort": 0.02,
            "acceleration_short": 0.02,
            "acceleration_maxshort": 0.2,
        },
        "market_data_args": {"high": "high_prices", "low": "low_prices"},
    },
    "t3": {
        "description": "T3 Moving Average",
        "params": {"close_prices": List[float], "timeperiod": int, "vfactor": float},
        "defaults": {"timeperiod": 5, "vfactor": 0.7},
        "market_data_args": {"close": "close_prices"},
    },
    "tema": {
        "description": "Triple Exponential Moving Average (TEMA)",
        "params": {"close_prices": List[float], "timeperiod": int},
        "defaults": {"timeperiod": 30},
        "market_data_args": {"close": "close_prices"},
    },
    "trima": {
        "description": "Triangular Moving Average (TRIMA)",
        "params": {"close_prices": List[float], "timeperiod": int},
        "defaults": {"timeperiod": 30},
        "market_data_args": {"close": "close_prices"},
    },
    "wma": {
        "description": "Weighted Moving Average (WMA)",
        "params": {"close_prices": List[float], "timeperiod": int},
        "defaults": {"timeperiod": 30},
        "market_data_args": {"close": "close_prices"},
    },
}


async def _calculate_indicator(
    indicator_name: str,
    market_data_kwargs: Dict[str, List[float]],
    indicator_opts: Dict[str, Any],
) -> Dict[str, Any]:
    """Helper function to calculate any indicator.
    
    Args:
        indicator_name: Name of the indicator to calculate
        market_data_kwargs: Keyword arguments for MarketData (close, high, low, etc.)
        indicator_opts: Options/parameters for the indicator
        
    Returns:
        Dictionary with success status, values, and metadata or error message
    """
    try:
        indicator = registry.get_indicator(indicator_name)
        if not indicator:
            raise ValueError(f"{indicator_name.upper()} indicator not found")
        
        market_data = MarketData(**market_data_kwargs)
        result = await indicator.calculate(market_data, indicator_opts)
        
        if result.success:
            return {
                "success": True,
                "values": result.values,
                "metadata": result.metadata,
            }
        return {
            "success": False,
            "error": getattr(result, "error_message", result.error if hasattr(result, "error") else "Unknown error"),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
        }


def _create_tool_function(indicator_name: str, spec: Dict[str, Any]):
    """Factory function to create tool functions dynamically.
    
    Args:
        indicator_name: Name of the indicator
        spec: Tool specification containing description, params, etc.
        
    Returns:
        Async tool function ready to be registered with @mcp.tool()
    """
    async def tool_func(**kwargs) -> Dict[str, Any]:
        # Extract market data arguments
        market_data_kwargs = {}
        indicator_opts = {}
        
        for param, param_arg in spec["market_data_args"].items():
            if param_arg in kwargs:
                market_data_kwargs[param] = kwargs[param_arg]
        
        # Extract indicator options (skip market data args)
        for key, value in kwargs.items():
            if key not in spec["market_data_args"].values():
                indicator_opts[key] = value
        
        return await _calculate_indicator(indicator_name, market_data_kwargs, indicator_opts)
    
    # Set function name and docstring for better introspection
    tool_func.__name__ = f"calculate_{indicator_name}"
    tool_func.__doc__ = f"Calculate {spec['description']}."
    
    return tool_func


def create_mcp_server() -> FastMCP:
    """Create and configure MCP server instance with all indicator tools.
    
    Returns:
        FastMCP instance with all TA-Lib overlap studies registered as tools.
        
    Example:
        >>> mcp = create_mcp_server()
        >>> # Run with STDIO transport (default)
        >>> await mcp.run()
        >>> # Or run with HTTP transport
        >>> await mcp.run(transport="http", host="0.0.0.0", port=8000)
    """
    mcp = FastMCP("mcp-talib")
    
    # Dynamically register all indicator tools
    for indicator_name, spec in TOOL_SPECS.items():
        tool_func = _create_tool_function(indicator_name, spec)
        mcp.add_tool(tool_func)
    
    return mcp
