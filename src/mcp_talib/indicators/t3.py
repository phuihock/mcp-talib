"""Triple Exponential Moving Average (T3) adapter using TA-Lib."""

from typing import Dict, Any
import numpy as np
import talib as ta

from .base import BaseIndicator
from ..models.market_data import MarketData
from ..models.indicator_result import IndicatorResult


class T3Indicator(BaseIndicator):
    def __init__(self):
        super().__init__(name="t3", description="Triple Exponential Moving Average (T3)")

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {"type": "object", "properties": {"close_prices": {"type": "array", "items": {"type": "number"}}, "timeperiod": {"type": "integer", "default": 5}, "vfactor": {"type": "number", "default": 0.7}}, "required": ["close_prices"]}

    async def calculate(self, market_data: MarketData, options: Dict[str, Any] = None) -> IndicatorResult:
        if options is None:
            options = {}
        timeperiod = options.get("timeperiod", 5)
        vfactor = options.get("vfactor", 0.7)
        close = np.asarray(market_data.close, dtype=float)

        try:
            out = ta.T3(close, timeperiod=timeperiod, vfactor=vfactor)
            return IndicatorResult(indicator_name=self.name, success=True, values={"t3": out.tolist()}, metadata={"timeperiod": timeperiod, "vfactor": vfactor, "input_points": len(close), "output_points": len(out)})
        except Exception as e:
            return IndicatorResult(indicator_name=self.name, success=False, values={}, error_message=str(e))
