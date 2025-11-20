"""Indicator registry for managing available indicators."""

from typing import Dict, Type, Any

from .base import BaseIndicator


class IndicatorRegistry:
    """Registry for managing indicator instances."""
    
    def __init__(self):
        self._indicators: Dict[str, BaseIndicator] = {}
        self._indicator_classes: Dict[str, Type[BaseIndicator]] = {}
    
    def register(self, name: str, indicator_class: Type[BaseIndicator]) -> None:
        """Register an indicator class."""
        self._indicator_classes[name] = indicator_class
    
    def get_indicators(self) -> Dict[str, BaseIndicator]:
        """Get all registered indicator instances."""
        if not self._indicators:
            # Initialize all registered indicators
            for name, indicator_class in self._indicator_classes.items():
                self._indicators[name] = indicator_class()
        return self._indicators
    
    def get_indicator(self, name: str) -> BaseIndicator:
        """Get a specific indicator instance."""
        indicators = self.get_indicators()
        return indicators.get(name)
    
    def list_indicators(self) -> list[str]:
        """List all registered indicator names."""
        return sorted(list(self._indicator_classes.keys()))