"""Pydantic request/response schemas for the HTTP API."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class ToolRequest(BaseModel):
    """Request body for calling a tool.

    Accepts a `close` list and any additional parameters which are included
    as extra fields and forwarded to the indicator.calculate call.
    """

    # Pydantic v2 configuration
    model_config = ConfigDict(extra="allow")

    close: List[float]


class ToolResult(BaseModel):
    model_config = ConfigDict()

    success: bool
    # Allow values to be either a list (series) or a full dict (e.g. {"sma": [...]})
    values: Optional[Any] = None
    metadata: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
