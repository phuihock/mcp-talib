"""Midpoint Price over period (MIDPRICE) adapter using TA-Lib."""

from typing import Dict, Any
import numpy as np
import talib as ta

from .base import BaseIndicator
from ..models.market_data import MarketData
from ..models.indicator_result import IndicatorResult


class MIDPRICEIndicator(BaseIndicator):
    def __init__(self):
        super().__init__(name="midprice", description="Midpoint Price over period")

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "high_prices": {"type": "array", "items": {"type": "number"}},
                "low_prices": {"type": "array", "items": {"type": "number"}},
                "timeperiod": {"type": "integer", "default": 14},
            },
            "required": ["high_prices", "low_prices"],
        }

    async def calculate(self, market_data: MarketData, options: Dict[str, Any] = None) -> IndicatorResult:
        if options is None:
            options = {}
        timeperiod = options.get("timeperiod", 14)

        high = np.asarray(market_data.high or [], dtype=float)
        low = np.asarray(market_data.low or [], dtype=float)

        try:
            out = ta.MIDPRICE(high, low, timeperiod=timeperiod)
            return IndicatorResult(indicator_name=self.name, success=True, values={"midprice": out.tolist()}, metadata={"timeperiod": timeperiod, "input_points": len(high), "output_points": len(out)})
        except Exception as e:
            return IndicatorResult(indicator_name=self.name, success=False, values={}, error_message=str(e))
