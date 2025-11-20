"""Base indicator interface."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

from ..models.indicator_result import IndicatorResult
from ..models.market_data import MarketData


class BaseIndicator(ABC):
    """Base class for all technical indicators."""
    
    def __init__(self, name: str, description: str):
        self._name = name
        self._description = description
    
    @property
    def name(self) -> str:
        """Get indicator name."""
        return self._name
    
    @property
    def description(self) -> str:
        """Get indicator description."""
        return self._description
    
    @property
    @abstractmethod
    def input_schema(self) -> Dict[str, Any]:
        """Return the JSON schema for input validation."""
        pass
    
    @abstractmethod
    async def calculate(self, market_data: MarketData, options: Dict[str, Any]) -> IndicatorResult:
        """Calculate indicator values."""
        pass