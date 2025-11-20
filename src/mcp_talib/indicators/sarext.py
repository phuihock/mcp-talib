"""Parabolic SAR - Extended (SAREXT) adapter using TA-Lib."""

from typing import Dict, Any
import numpy as np
import talib as ta

from .base import BaseIndicator
from ..models.market_data import MarketData
from ..models.indicator_result import IndicatorResult


class SAREXTIndicator(BaseIndicator):
    def __init__(self):
        super().__init__(name="sarext", description="Parabolic SAR - Extended")

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "high_prices": {"type": "array", "items": {"type": "number"}},
                "low_prices": {"type": "array", "items": {"type": "number"}},
                "startvalue": {"type": ["number", "null"]},
                "offsetonreverse": {"type": "number", "default": 0.0},
                "acceleration_initlong": {"type": "number", "default": 0.02},
                "acceleration_long": {"type": "number", "default": 0.02},
                "acceleration_maxlong": {"type": "number", "default": 0.2},
                "acceleration_initshort": {"type": "number", "default": 0.02},
                "acceleration_short": {"type": "number", "default": 0.02},
                "acceleration_maxshort": {"type": "number", "default": 0.2},
            },
            "required": ["high_prices", "low_prices"],
        }

    async def calculate(self, market_data: MarketData, options: Dict[str, Any] = None) -> IndicatorResult:
        if options is None:
            options = {}
        high = np.asarray(market_data.high or [], dtype=float)
        low = np.asarray(market_data.low or [], dtype=float)

        # Map our input option keys (snake_case) to TA-Lib SAREXT parameter names
        key_map = {
            "startvalue": "startvalue",
            "offsetonreverse": "offsetonreverse",
            "acceleration_initlong": "accelerationinitlong",
            "acceleration_long": "accelerationlong",
            "acceleration_maxlong": "accelerationmaxlong",
            "acceleration_initshort": "accelerationinitshort",
            "acceleration_short": "accelerationshort",
            "acceleration_maxshort": "accelerationmaxshort",
        }

        params = {}
        for src_key, ta_key in key_map.items():
            if src_key in options and options.get(src_key) is not None:
                params[ta_key] = options.get(src_key)

        try:
            out = ta.SAREXT(high, low, **params)
            return IndicatorResult(indicator_name=self.name, success=True, values={"sarext": out.tolist()}, metadata={"input_points": len(high), "output_points": len(out)})
        except Exception as e:
            return IndicatorResult(indicator_name=self.name, success=False, values={}, error_message=str(e))
