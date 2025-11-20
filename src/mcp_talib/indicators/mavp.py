"""Moving Average with Variable Period (MAVP) adapter using TA-Lib."""

from typing import Dict, Any, List
import numpy as np
import talib as ta

from .base import BaseIndicator
from ..models.market_data import MarketData
from ..models.indicator_result import IndicatorResult


class MAVPIndicator(BaseIndicator):
    def __init__(self):
        super().__init__(name="mavp", description="Moving Average with Variable Period (MAVP)")

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "close_prices": {"type": "array", "items": {"type": "number"}},
                "periods": {"type": "number"},
                "minperiod": {"type": "integer", "default": 2},
                "maxperiod": {"type": "integer", "default": 30},
            },
            "required": ["close_prices"],
        }

    async def calculate(self, market_data: MarketData, options: Dict[str, Any] = None) -> IndicatorResult:
        if options is None:
            options = {}
        close = np.asarray(market_data.close, dtype=float)
        periods = options.get("periods", None)
        minperiod = options.get("minperiod", 2)
        maxperiod = options.get("maxperiod", 30)

        try:
            # Enforce a single float `periods` to match the type expectations
            # in the type stubs (`_ta_lib.pyi`). Convert the single float into
            # an ndarray filled to the same length as `close` for TA-Lib.
            if periods is not None:
                periods_arr = np.full(close.shape[0], periods, dtype=float)
                out = ta.MAVP(close, periods_arr)
            else:
                out = ta.MAVP(close, None)

            return IndicatorResult(indicator_name=self.name, success=True, values={"mavp": out.tolist()}, metadata={"periods": periods, "minperiod": minperiod, "maxperiod": maxperiod, "input_points": len(close), "output_points": len(out)})
        except Exception as e:
            return IndicatorResult(indicator_name=self.name, success=False, values={}, error_message=str(e))
