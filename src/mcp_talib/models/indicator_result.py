"""Indicator result model."""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class IndicatorResult(BaseModel):
    """Result of indicator calculation."""
    
    indicator_name: str = Field(..., description="Name of calculated indicator")
    success: bool = Field(default=True, description="Whether calculation succeeded")
    values: Dict[str, Any] = Field(..., description="Calculated indicator values")
    error_message: Optional[str] = Field(None, description="Error details if calculation failed")
    calculation_time: Optional[float] = Field(None, description="Time taken for calculation in milliseconds")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional calculation metadata")