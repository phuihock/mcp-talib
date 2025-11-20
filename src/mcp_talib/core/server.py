"""Core MCP server implementation."""

from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP

from ..indicators import registry
from ..models.market_data import MarketData


def create_server() -> FastMCP:
    """Create and configure MCP server instance."""
    mcp = FastMCP("mcp-talib")
    
    @mcp.tool()
    async def calculate_sma(
        close_prices: List[float],
        timeperiod: int = 20
    ) -> Dict[str, Any]:
        """Calculate Simple Moving Average (SMA).
        
        Args:
            close_prices: List of closing prices
            timeperiod: Number of periods to average (default: 20)
            
        Returns:
            Dictionary with SMA values and metadata
        """
        try:
            # Get indicator from registry
            indicator = registry.get_indicator("sma")
            if not indicator:
                raise ValueError("SMA indicator not found")
            
            # Create market data
            market_data = MarketData(close=close_prices)
            
            # Calculate indicator
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod})
            
            if result.success:
                return {
                    "success": True,
                    "values": result.values,
                    "metadata": result.metadata,
                }
            else:
                return {
                    "success": False,
                    "error": result.error,
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
    
    @mcp.tool()
    async def calculate_ema(
        close_prices: List[float],
        timeperiod: int = 20
    ) -> Dict[str, Any]:
        """Calculate Exponential Moving Average (EMA).
        
        Args:
            close_prices: List of closing prices
            timeperiod: Number of periods for average (default: 20)
            
        Returns:
            Dictionary with EMA values and metadata
        """
        try:
            # Get indicator from registry
            indicator = registry.get_indicator("ema")
            if not indicator:
                raise ValueError("EMA indicator not found")
            
            # Create market data
            market_data = MarketData(close=close_prices)
            
            # Calculate indicator
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod})
            
            if result.success:
                return {
                    "success": True,
                    "values": result.values,
                    "metadata": result.metadata,
                }
            else:
                return {
                    "success": False,
                    "error": result.error,
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
    
    @mcp.tool()
    async def calculate_rsi(
        close_prices: List[float],
        timeperiod: int = 14
    ) -> Dict[str, Any]:
        """Calculate Relative Strength Index (RSI).
        
        Args:
            close_prices: List of closing prices
            timeperiod: Number of periods for RSI (default: 14)
            
        Returns:
            Dictionary with RSI values and metadata
        """
        try:
            # Get indicator from registry
            indicator = registry.get_indicator("rsi")
            if not indicator:
                raise ValueError("RSI indicator not found")
            
            # Create market data
            market_data = MarketData(close=close_prices)
            
            # Calculate indicator
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod})
            
            if result.success:
                return {
                    "success": True,
                    "values": result.values,
                    "metadata": result.metadata,
                }
            else:
                return {
                    "success": False,
                    "error": result.error,
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }
    
    return mcp