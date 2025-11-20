"""Simple Moving Average (SMA) indicator implementation."""

from typing import List, Dict, Any
from .base import BaseIndicator
from ..models.market_data import MarketData
from ..models.indicator_result import IndicatorResult


class SMAIndicator(BaseIndicator):
    """Simple Moving Average (SMA) indicator implementation."""
    
    def __init__(self):
        """Initialize SMA indicator."""
        super().__init__(
            name="sma",
            description="Simple Moving Average (SMA) - calculates the arithmetic mean of prices over a specified time period"
        )
    
    @property
    def name(self) -> str:
        return "sma"
    
    @property
    def description(self) -> str:
        return "Simple Moving Average (SMA) - calculates the average price over a specified period"
    
    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "close_prices": {
                    "type": "array",
                    "items": {"type": "number"},
                    "description": "List of closing prices"
                },
                "timeperiod": {
                    "type": "integer",
                    "default": 20,
                    "description": "Number of periods to average"
                }
            },
            "required": ["close_prices"]
        }
    
    async def calculate(
        self, 
        market_data: MarketData, 
        options: Dict[str, Any] = None
    ) -> IndicatorResult:
        """Calculate SMA indicator."""
        if options is None:
            options = {}
        
        timeperiod = options.get("timeperiod", 20)
        close_prices = market_data.close
        
        if len(close_prices) < timeperiod:
            return IndicatorResult(
                indicator_name=self.name,
                success=False,
                values={},
                error_message=f"Not enough data points. Need at least {timeperiod}, got {len(close_prices)}"
            )
        
        # Calculate SMA
        sma_values = []
        for i in range(timeperiod - 1, len(close_prices)):
            avg = sum(close_prices[i - timeperiod + 1:i + 1]) / timeperiod
            sma_values.append(avg)
        
        return IndicatorResult(
            indicator_name=self.name,
            success=True,
            values={"sma": sma_values},
            metadata={
                "timeperiod": timeperiod,
                "input_points": len(close_prices),
                "output_points": len(sma_values)
            }
        )