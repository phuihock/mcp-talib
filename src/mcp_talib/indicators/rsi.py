"""Relative Strength Index (RSI) indicator implementation."""

from typing import List, Dict, Any
from .base import BaseIndicator
from ..models.market_data import MarketData
from ..models.indicator_result import IndicatorResult


class RSIIndicator(BaseIndicator):
    """Relative Strength Index (RSI) indicator implementation."""
    
    def __init__(self):
        """Initialize RSI indicator."""
        super().__init__(
            name="rsi",
            description="Relative Strength Index (RSI) - momentum oscillator that measures speed and change of price movements"
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
                    "default": 14,
                    "description": "Number of periods for RSI calculation"
                }
            },
            "required": ["close_prices"]
        }
    
    async def calculate(
        self, 
        market_data: MarketData, 
        options: Dict[str, Any] = None
    ) -> IndicatorResult:
        """Calculate RSI indicator."""
        if options is None:
            options = {}
        
        timeperiod = options.get("timeperiod", 14)
        close_prices = market_data.close
        
        if len(close_prices) < timeperiod + 1:
            return IndicatorResult(
                indicator_name=self.name,
                success=False,
                values={},
                error_message=f"Not enough data points. Need at least {timeperiod + 1}, got {len(close_prices)}"
            )
        
        # Calculate price changes
        deltas = [close_prices[i] - close_prices[i-1] for i in range(1, len(close_prices))]
        
        # Separate gains and losses
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        
        # Calculate initial average gain and loss
        avg_gain = sum(gains[:timeperiod]) / timeperiod
        avg_loss = sum(losses[:timeperiod]) / timeperiod
        
        rsi_values = []
        
        # Calculate subsequent values using exponential smoothing
        for i in range(timeperiod, len(gains)):
            avg_gain = (avg_gain * (timeperiod - 1) + gains[i]) / timeperiod
            avg_loss = (avg_loss * (timeperiod - 1) + losses[i]) / timeperiod
            
            # Calculate RS (Relative Strength)
            if avg_loss == 0:
                rs = float('inf')
            else:
                rs = avg_gain / avg_loss
            
            # Calculate RSI: 100 - (100 / (1 + RS))
            rsi = 100 - (100 / (1 + rs))
            rsi_values.append(min(max(rsi, 0), 100))  # Clamp between 0 and 100
        
        return IndicatorResult(
            indicator_name=self.name,
            success=True,
            values={"rsi": rsi_values},
            metadata={
                "timeperiod": timeperiod,
                "input_points": len(close_prices),
                "output_points": len(rsi_values)
            }
        )