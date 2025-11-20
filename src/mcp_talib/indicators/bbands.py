"""Bollinger Bands (BBANDS) adapter using TA-Lib."""

from typing import Dict, Any
import numpy as np
import talib as ta

from .base import BaseIndicator
from ..models.market_data import MarketData
from ..models.indicator_result import IndicatorResult


class BBANDSIndicator(BaseIndicator):
    def __init__(self):
        super().__init__(name="bbands", description="Bollinger Bands (BBANDS)")

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "close_prices": {"type": "array", "items": {"type": "number"}},
                "timeperiod": {"type": "integer", "default": 20},
                "nbdevup": {"type": "number", "default": 2.0},
                "nbdevdn": {"type": "number", "default": 2.0},
                "matype": {"type": "integer", "default": 0},
            },
            "required": ["close_prices"],
        }

    async def calculate(self, market_data: MarketData, options: Dict[str, Any] = None) -> IndicatorResult:
        if options is None:
            options = {}

        timeperiod = options.get("timeperiod", 20)
        nbdevup = options.get("nbdevup", 2.0)
        nbdevdn = options.get("nbdevdn", 2.0)
        matype = options.get("matype", 0)

        close = np.asarray(market_data.close, dtype=float)
        try:
            upper, middle, lower = ta.BBANDS(close, timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn, matype=matype)

            return IndicatorResult(
                indicator_name=self.name,
                success=True,
                values={
                    "upperband": upper.tolist(),
                    "middleband": middle.tolist(),
                    "lowerband": lower.tolist(),
                },
                metadata={
                    "timeperiod": timeperiod,
                    "nbdevup": nbdevup,
                    "nbdevdn": nbdevdn,
                    "matype": matype,
                    "input_points": len(close),
                    "output_points": len(middle),
                },
            )

        except Exception as e:
            return IndicatorResult(indicator_name=self.name, success=False, values={}, error_message=str(e))
