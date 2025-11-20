"""Kaufman Adaptive Moving Average (KAMA) adapter using TA-Lib."""

from typing import Dict, Any
import numpy as np
import talib as ta

from .base import BaseIndicator
from ..models.market_data import MarketData
from ..models.indicator_result import IndicatorResult


class KAMAIndicator(BaseIndicator):
    def __init__(self):
        super().__init__(name="kama", description="Kaufman Adaptive Moving Average (KAMA)")

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {"type": "object", "properties": {"close_prices": {"type": "array", "items": {"type": "number"}}, "timeperiod": {"type": "integer", "default": 10}}, "required": ["close_prices"]}

    async def calculate(self, market_data: MarketData, options: Dict[str, Any] = None) -> IndicatorResult:
        if options is None:
            options = {}
        timeperiod = options.get("timeperiod", 10)
        close = np.asarray(market_data.close, dtype=float)

        try:
            out = ta.KAMA(close, timeperiod=timeperiod)
            return IndicatorResult(indicator_name=self.name, success=True, values={"kama": out.tolist()}, metadata={"timeperiod": timeperiod, "input_points": len(close), "output_points": len(out)})
        except Exception as e:
            return IndicatorResult(indicator_name=self.name, success=False, values={}, error_message=str(e))
