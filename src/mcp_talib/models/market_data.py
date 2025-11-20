"""Market data model."""

from typing import List, Optional
from pydantic import BaseModel, Field, validator, field_validator


class MarketData(BaseModel):
    """OHLCV market data model."""
    
    close: List[float] = Field(..., description="Closing prices array")
    open: Optional[List[float]] = Field(None, description="Opening prices array")
    high: Optional[List[float]] = Field(None, description="Highest prices array")
    low: Optional[List[float]] = Field(None, description="Lowest prices array")
    volume: Optional[List[float]] = Field(None, description="Trading volumes array (optional)")
    timestamp: Optional[List[int]] = Field(None, description="Unix timestamps (optional)")
    
    @field_validator('open', 'high', 'low', 'close')
    @classmethod
    def validate_prices_not_empty(cls, v):
        if not v:
            raise ValueError("Price arrays cannot be empty")
        return v
    
    @field_validator('volume')
    @classmethod
    def validate_volume_length(cls, v, info):
        if v is not None:
            length = len(info.data.get('close', []))
            if len(v) != length:
                raise ValueError("Volume array must match price array length")
        return v
    
    @field_validator('timestamp')
    @classmethod
    def validate_timestamp_length(cls, v, info):
        if v is not None:
            length = len(info.data.get('close', []))
            if len(v) != length:
                raise ValueError("Timestamp array must match price array length")
        return v
    
    @property
    def length(self) -> int:
        """Total number of data points."""
        return len(self.close)