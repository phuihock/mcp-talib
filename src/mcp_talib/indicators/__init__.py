"""Technical analysis indicators package."""

from .base import BaseIndicator
from .registry import IndicatorRegistry
from .sma import SMAIndicator
from .ema import EMAIndicator
from .rsi import RSIIndicator

# Register built-in indicators
registry = IndicatorRegistry()
registry.register("sma", SMAIndicator)
registry.register("ema", EMAIndicator)
registry.register("rsi", RSIIndicator)