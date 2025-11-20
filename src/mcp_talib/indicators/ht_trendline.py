"""Hilbert Transform - Instantaneous Trendline (HT_TRENDLINE) adapter using TA-Lib."""

from typing import Dict, Any
import numpy as np
import talib as ta

from .base import BaseIndicator
from ..models.market_data import MarketData
from ..models.indicator_result import IndicatorResult


class HTTrendlineIndicator(BaseIndicator):
    def __init__(self):
        super().__init__(name="ht_trendline", description="Hilbert Transform - Instantaneous Trendline")

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {"type": "object", "properties": {"close_prices": {"type": "array", "items": {"type": "number"}}}, "required": ["close_prices"]}

    async def calculate(self, market_data: MarketData, options: Dict[str, Any] = None) -> IndicatorResult:
        close = np.asarray(market_data.close, dtype=float)
        try:
            out = ta.HT_TRENDLINE(close)
            return IndicatorResult(
                indicator_name=self.name,
                success=True,
                values={"ht_trendline": out.tolist()},
                metadata={"input_points": len(close), "output_points": len(out)},
            )
        except Exception as e:
            return IndicatorResult(indicator_name=self.name, success=False, values={}, error_message=str(e))
