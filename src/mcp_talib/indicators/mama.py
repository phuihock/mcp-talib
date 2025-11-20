"""MESA Adaptive Moving Average (MAMA) adapter using TA-Lib."""

from typing import Dict, Any
import numpy as np
import talib as ta

from .base import BaseIndicator
from ..models.market_data import MarketData
from ..models.indicator_result import IndicatorResult


class MAMAIndicator(BaseIndicator):
    def __init__(self):
        super().__init__(name="mama", description="MESA Adaptive Moving Average (MAMA)")

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "close_prices": {"type": "array", "items": {"type": "number"}},
                "fastlimit": {"type": "number", "default": 0.5},
                "slowlimit": {"type": "number", "default": 0.05},
            },
            "required": ["close_prices"],
        }

    async def calculate(self, market_data: MarketData, options: Dict[str, Any] = None) -> IndicatorResult:
        if options is None:
            options = {}
        fastlimit = options.get("fastlimit", 0.5)
        slowlimit = options.get("slowlimit", 0.05)
        close = np.asarray(market_data.close, dtype=float)

        try:
            mama, fama = ta.MAMA(close, fastlimit=fastlimit, slowlimit=slowlimit)
            return IndicatorResult(
                indicator_name=self.name,
                success=True,
                values={"mama": mama.tolist(), "fama": fama.tolist()},
                metadata={"fastlimit": fastlimit, "slowlimit": slowlimit, "input_points": len(close), "output_points": len(mama)},
            )
        except Exception as e:
            return IndicatorResult(indicator_name=self.name, success=False, values={}, error_message=str(e))
