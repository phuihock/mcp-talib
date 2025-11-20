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
                    "error": result.error_message,
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
                    "error": result.error_message,
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
                    "error": result.error_message,
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
            }

    @mcp.tool()
    async def calculate_bbands(
        close_prices: List[float],
        timeperiod: int = 20,
        nbdevup: float = 2.0,
        nbdevdn: float = 2.0,
        matype: int = 0,
    ) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("bbands")
            if not indicator:
                raise ValueError("BBANDS indicator not found")
            market_data = MarketData(close=close_prices)
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod, "nbdevup": nbdevup, "nbdevdn": nbdevdn, "matype": matype})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_dema(close_prices: List[float], timeperiod: int = 30) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("dema")
            if not indicator:
                raise ValueError("DEMA indicator not found")
            market_data = MarketData(close=close_prices)
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_ht_trendline(close_prices: List[float]) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("ht_trendline")
            if not indicator:
                raise ValueError("HT_TRENDLINE indicator not found")
            market_data = MarketData(close=close_prices)
            result = await indicator.calculate(market_data, {})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_kama(close_prices: List[float], timeperiod: int = 10) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("kama")
            if not indicator:
                raise ValueError("KAMA indicator not found")
            market_data = MarketData(close=close_prices)
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_ma(close_prices: List[float], timeperiod: int = 30, matype: int = 0) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("ma")
            if not indicator:
                raise ValueError("MA indicator not found")
            market_data = MarketData(close=close_prices)
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod, "matype": matype})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_mama(close_prices: List[float], fastlimit: float = 0.5, slowlimit: float = 0.05) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("mama")
            if not indicator:
                raise ValueError("MAMA indicator not found")
            market_data = MarketData(close=close_prices)
            result = await indicator.calculate(market_data, {"fastlimit": fastlimit, "slowlimit": slowlimit})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_mavp(close_prices: List[float], periods: float = None, minperiod: int = 2, maxperiod: int = 30) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("mavp")
            if not indicator:
                raise ValueError("MAVP indicator not found")
            market_data = MarketData(close=close_prices)
            opts = {"periods": periods, "minperiod": minperiod, "maxperiod": maxperiod}
            result = await indicator.calculate(market_data, opts)
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_midpoint(close_prices: List[float], timeperiod: int = 14) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("midpoint")
            if not indicator:
                raise ValueError("MIDPOINT indicator not found")
            market_data = MarketData(close=close_prices)
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_midprice(high_prices: List[float], low_prices: List[float], timeperiod: int = 14) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("midprice")
            if not indicator:
                raise ValueError("MIDPRICE indicator not found")
            market_data = MarketData(close=[0], high=high_prices, low=low_prices)
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_sar(high_prices: List[float], low_prices: List[float], acceleration: float = 0.02, maximum: float = 0.2) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("sar")
            if not indicator:
                raise ValueError("SAR indicator not found")
            market_data = MarketData(close=[0], high=high_prices, low=low_prices)
            result = await indicator.calculate(market_data, {"acceleration": acceleration, "maximum": maximum})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_sarext(high_prices: List[float], low_prices: List[float], startvalue: float = None, offsetonreverse: float = 0.0, acceleration_initlong: float = 0.02, acceleration_long: float = 0.02, acceleration_maxlong: float = 0.2, acceleration_initshort: float = 0.02, acceleration_short: float = 0.02, acceleration_maxshort: float = 0.2) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("sarext")
            if not indicator:
                raise ValueError("SAREXT indicator not found")
            market_data = MarketData(close=[0], high=high_prices, low=low_prices)
            opts = {"startvalue": startvalue, "offsetonreverse": offsetonreverse, "acceleration_initlong": acceleration_initlong, "acceleration_long": acceleration_long, "acceleration_maxlong": acceleration_maxlong, "acceleration_initshort": acceleration_initshort, "acceleration_short": acceleration_short, "acceleration_maxshort": acceleration_maxshort}
            result = await indicator.calculate(market_data, opts)
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_t3(close_prices: List[float], timeperiod: int = 5, vfactor: float = 0.7) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("t3")
            if not indicator:
                raise ValueError("T3 indicator not found")
            market_data = MarketData(close=close_prices)
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod, "vfactor": vfactor})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_tema(close_prices: List[float], timeperiod: int = 30) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("tema")
            if not indicator:
                raise ValueError("TEMA indicator not found")
            market_data = MarketData(close=close_prices)
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_trima(close_prices: List[float], timeperiod: int = 30) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("trima")
            if not indicator:
                raise ValueError("TRIMA indicator not found")
            market_data = MarketData(close=close_prices)
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_wma(close_prices: List[float], timeperiod: int = 30) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("wma")
            if not indicator:
                raise ValueError("WMA indicator not found")
            market_data = MarketData(close=close_prices)
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    return mcp