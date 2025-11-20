"""Exponential Moving Average (EMA) indicator implementation."""

from typing import List, Dict, Any
from .base import BaseIndicator
from ..models.market_data import MarketData
from ..models.indicator_result import IndicatorResult


class EMAIndicator(BaseIndicator):
    """Exponential Moving Average (EMA) indicator implementation."""
    
    def __init__(self):
        """Initialize EMA indicator."""
        super().__init__(
            name="ema",
            description="Exponential Moving Average (EMA) - gives more weight to recent prices"
        )
    
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
                    "description": "Number of periods for EMA calculation"
                }
            },
            "required": ["close_prices"]
        }
    
    async def calculate(
        self, 
        market_data: MarketData, 
        options: Dict[str, Any] = None
    ) -> IndicatorResult:
        """Calculate EMA indicator."""
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
        
        # Calculate EMA
        # Multiplier: (2 / (timeperiod + 1))
        multiplier = 2.0 / (timeperiod + 1)
        
        # Initialize EMA with SMA of first timeperiod values
        ema_values = []
        initial_sma = sum(close_prices[:timeperiod]) / timeperiod
        ema_values.append(initial_sma)
        
        # Calculate EMA for remaining values
        for i in range(timeperiod, len(close_prices)):
            ema = (close_prices[i] - ema_values[-1]) * multiplier + ema_values[-1]
            ema_values.append(ema)
        
        return IndicatorResult(
            indicator_name=self.name,
            success=True,
            values={"ema": ema_values},
            metadata={
                "timeperiod": timeperiod,
                "multiplier": multiplier,
                "input_points": len(close_prices),
                "output_points": len(ema_values)
            }
        )