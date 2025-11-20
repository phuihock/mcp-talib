"""Technical analysis indicators package."""

from .base import BaseIndicator
from .registry import IndicatorRegistry
from .sma import SMAIndicator
from .ema import EMAIndicator
from .rsi import RSIIndicator
from .bbands import BBANDSIndicator
from .dema import DEMAIndicator
from .ht_trendline import HTTrendlineIndicator
from .kama import KAMAIndicator
from .ma import MAIndicator
from .mama import MAMAIndicator
from .mavp import MAVPIndicator
from .midpoint import MIDPOINTIndicator
from .midprice import MIDPRICEIndicator
from .sar import SARIndicator
from .sarext import SAREXTIndicator
from .t3 import T3Indicator
from .tema import TEMAIndicator
from .trima import TRIMAIndicator
from .wma import WMAIndicator

# Register built-in indicators
registry = IndicatorRegistry()
registry.register("sma", SMAIndicator)
registry.register("ema", EMAIndicator)
registry.register("rsi", RSIIndicator)
registry.register("bbands", BBANDSIndicator)
registry.register("dema", DEMAIndicator)
registry.register("ht_trendline", HTTrendlineIndicator)
registry.register("kama", KAMAIndicator)
registry.register("ma", MAIndicator)
registry.register("mama", MAMAIndicator)
registry.register("mavp", MAVPIndicator)
registry.register("midpoint", MIDPOINTIndicator)
registry.register("midprice", MIDPRICEIndicator)
registry.register("sar", SARIndicator)
registry.register("sarext", SAREXTIndicator)
registry.register("t3", T3Indicator)
registry.register("tema", TEMAIndicator)
registry.register("trima", TRIMAIndicator)
registry.register("wma", WMAIndicator)