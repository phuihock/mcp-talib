"""Parabolic SAR (SAR) adapter using TA-Lib."""

from typing import Dict, Any
import numpy as np
import talib as ta

from .base import BaseIndicator
from ..models.market_data import MarketData
from ..models.indicator_result import IndicatorResult


class SARIndicator(BaseIndicator):
    def __init__(self):
        super().__init__(name="sar", description="Parabolic SAR")

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "high_prices": {"type": "array", "items": {"type": "number"}},
                "low_prices": {"type": "array", "items": {"type": "number"}},
                "acceleration": {"type": "number", "default": 0.02},
                "maximum": {"type": "number", "default": 0.2},
            },
            "required": ["high_prices", "low_prices"],
        }

    async def calculate(self, market_data: MarketData, options: Dict[str, Any] = None) -> IndicatorResult:
        if options is None:
            options = {}
        acceleration = options.get("acceleration", 0.02)
        maximum = options.get("maximum", 0.2)

        high = np.asarray(market_data.high or [], dtype=float)
        low = np.asarray(market_data.low or [], dtype=float)

        try:
            out = ta.SAR(high, low, acceleration=acceleration, maximum=maximum)
            return IndicatorResult(indicator_name=self.name, success=True, values={"sar": out.tolist()}, metadata={"acceleration": acceleration, "maximum": maximum, "input_points": len(high), "output_points": len(out)})
        except Exception as e:
            return IndicatorResult(indicator_name=self.name, success=False, values={}, error_message=str(e))
