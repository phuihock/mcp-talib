"""Moving Average (MA) adapter using TA-Lib."""

from typing import Dict, Any
import numpy as np
import talib as ta

from .base import BaseIndicator
from ..models.market_data import MarketData
from ..models.indicator_result import IndicatorResult


class MAIndicator(BaseIndicator):
    def __init__(self):
        super().__init__(name="ma", description="Moving Average (MA)")

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "close_prices": {"type": "array", "items": {"type": "number"}},
                "timeperiod": {"type": "integer", "default": 30},
                "matype": {"type": "integer", "default": 0},
            },
            "required": ["close_prices"],
        }

    async def calculate(self, market_data: MarketData, options: Dict[str, Any] = None) -> IndicatorResult:
        if options is None:
            options = {}
        timeperiod = options.get("timeperiod", 30)
        matype = options.get("matype", 0)
        close = np.asarray(market_data.close, dtype=float)

        try:
            out = ta.MA(close, timeperiod=timeperiod, matype=matype)
            return IndicatorResult(indicator_name=self.name, success=True, values={"ma": out.tolist()}, metadata={"timeperiod": timeperiod, "matype": matype, "input_points": len(close), "output_points": len(out)})
        except Exception as e:
            return IndicatorResult(indicator_name=self.name, success=False, values={}, error_message=str(e))
