"""Triangular Moving Average (TRIMA) adapter using TA-Lib."""

from typing import Dict, Any
import numpy as np
import talib as ta

from .base import BaseIndicator
from ..models.market_data import MarketData
from ..models.indicator_result import IndicatorResult


class TRIMAIndicator(BaseIndicator):
    def __init__(self):
        super().__init__(name="trima", description="Triangular Moving Average (TRIMA)")

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {"type": "object", "properties": {"close_prices": {"type": "array", "items": {"type": "number"}}, "timeperiod": {"type": "integer", "default": 30}}, "required": ["close_prices"]}

    async def calculate(self, market_data: MarketData, options: Dict[str, Any] = None) -> IndicatorResult:
        if options is None:
            options = {}
        timeperiod = options.get("timeperiod", 30)
        close = np.asarray(market_data.close, dtype=float)

        try:
            out = ta.TRIMA(close, timeperiod=timeperiod)
            return IndicatorResult(indicator_name=self.name, success=True, values={"trima": out.tolist()}, metadata={"timeperiod": timeperiod, "input_points": len(close), "output_points": len(out)})
        except Exception as e:
            return IndicatorResult(indicator_name=self.name, success=False, values={}, error_message=str(e))
