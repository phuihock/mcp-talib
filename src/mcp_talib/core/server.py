"""Core MCP server implementation."""

from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP

from ..indicators import registry
from ..models.market_data import MarketData


def create_server() -> FastMCP:
    """Create and configure MCP server instance."""
    mcp = FastMCP("mcp-talib")
    
    @mcp.tool()
    async def calculate_sma(
        close: List[float],
        timeperiod: int = 20
    ) -> Dict[str, Any]:
        """Calculate Simple Moving Average (SMA).
        
        Args:
            close: List of closing prices
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
            market_data = MarketData(close=close)
            
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
        close: List[float],
        timeperiod: int = 20
    ) -> Dict[str, Any]:
        """Calculate Exponential Moving Average (EMA).
        
        Args:
            close: List of closing prices
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
            market_data = MarketData(close=close)
            
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
        close: List[float],
        timeperiod: int = 14
    ) -> Dict[str, Any]:
        """Calculate Relative Strength Index (RSI).
        
        Args:
            close: List of closing prices
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
            market_data = MarketData(close=close)
            
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
        close: List[float],
        timeperiod: int = 20,
        nbdevup: float = 2.0,
        nbdevdn: float = 2.0,
        matype: int = 0,
    ) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("bbands")
            if not indicator:
                raise ValueError("BBANDS indicator not found")
            market_data = MarketData(close=close)
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod, "nbdevup": nbdevup, "nbdevdn": nbdevdn, "matype": matype})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_dema(close: List[float], timeperiod: int = 30) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("dema")
            if not indicator:
                raise ValueError("DEMA indicator not found")
            market_data = MarketData(close=close)
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_ht_trendline(close: List[float]) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("ht_trendline")
            if not indicator:
                raise ValueError("HT_TRENDLINE indicator not found")
            market_data = MarketData(close=close)
            result = await indicator.calculate(market_data, {})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_kama(close: List[float], timeperiod: int = 10) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("kama")
            if not indicator:
                raise ValueError("KAMA indicator not found")
            market_data = MarketData(close=close)
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_ma(close: List[float], timeperiod: int = 30, matype: int = 0) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("ma")
            if not indicator:
                raise ValueError("MA indicator not found")
            market_data = MarketData(close=close)
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod, "matype": matype})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_mama(close: List[float], fastlimit: float = 0.5, slowlimit: float = 0.05) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("mama")
            if not indicator:
                raise ValueError("MAMA indicator not found")
            market_data = MarketData(close=close)
            result = await indicator.calculate(market_data, {"fastlimit": fastlimit, "slowlimit": slowlimit})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_mavp(close: List[float], periods: Optional[float] = None, minperiod: int = 2, maxperiod: int = 30) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("mavp")
            if not indicator:
                raise ValueError("MAVP indicator not found")
            market_data = MarketData(close=close)
            opts = {"periods": periods, "minperiod": minperiod, "maxperiod": maxperiod}
            result = await indicator.calculate(market_data, opts)
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_midpoint(close: List[float], timeperiod: int = 14) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("midpoint")
            if not indicator:
                raise ValueError("MIDPOINT indicator not found")
            market_data = MarketData(close=close)
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_midprice(high: List[float], low: List[float], timeperiod: int = 14) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("midprice")
            if not indicator:
                raise ValueError("MIDPRICE indicator not found")
            market_data = MarketData(close=[0], high=high, low=low)
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_sar(high: List[float], low: List[float], acceleration: float = 0.02, maximum: float = 0.2) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("sar")
            if not indicator:
                raise ValueError("SAR indicator not found")
            market_data = MarketData(close=[0], high=high, low=low)
            result = await indicator.calculate(market_data, {"acceleration": acceleration, "maximum": maximum})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_sarext(high: List[float], low: List[float], startvalue: Optional[float] = None, offsetonreverse: float = 0.0, acceleration_initlong: float = 0.02, acceleration_long: float = 0.02, acceleration_maxlong: float = 0.2, acceleration_initshort: float = 0.02, acceleration_short: float = 0.02, acceleration_maxshort: float = 0.2) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("sarext")
            if not indicator:
                raise ValueError("SAREXT indicator not found")
            market_data = MarketData(close=[0], high=high, low=low)
            opts = {"startvalue": startvalue, "offsetonreverse": offsetonreverse, "acceleration_initlong": acceleration_initlong, "acceleration_long": acceleration_long, "acceleration_maxlong": acceleration_maxlong, "acceleration_initshort": acceleration_initshort, "acceleration_short": acceleration_short, "acceleration_maxshort": acceleration_maxshort}
            result = await indicator.calculate(market_data, opts)
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_t3(close: List[float], timeperiod: int = 5, vfactor: float = 0.7) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("t3")
            if not indicator:
                raise ValueError("T3 indicator not found")
            market_data = MarketData(close=close)
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod, "vfactor": vfactor})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_tema(close: List[float], timeperiod: int = 30) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("tema")
            if not indicator:
                raise ValueError("TEMA indicator not found")
            market_data = MarketData(close=close)
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_trima(close: List[float], timeperiod: int = 30) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("trima")
            if not indicator:
                raise ValueError("TRIMA indicator not found")
            market_data = MarketData(close=close)
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def calculate_wma(close: List[float], timeperiod: int = 30) -> Dict[str, Any]:
        try:
            indicator = registry.get_indicator("wma")
            if not indicator:
                raise ValueError("WMA indicator not found")
            market_data = MarketData(close=close)
            result = await indicator.calculate(market_data, {"timeperiod": timeperiod})
            if result.success:
                return {"success": True, "values": result.values, "metadata": result.metadata}
            return {"success": False, "error": result.error_message}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    return mcp