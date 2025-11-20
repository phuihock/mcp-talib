"""HTTP API server exposing /api/tools endpoints.

This module provides create_http_api_app() which returns a FastAPI app
with only HTTP endpoints for calling indicators. It contains no MCP-specific
routes or mounting logic—use this for pure REST/HTTP access.
"""

from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .indicators import registry
from .models.market_data import MarketData
from .schemas import ToolRequest, ToolResult


def create_http_api_app() -> FastAPI:
    """Create a FastAPI app that exposes only `/api/tools/*` endpoints.

    - POST `/api/tools/{tool_name}`: JSON body with `close` (list of floats)
      and other parameters passed to the indicator.
    - GET `/api/tools`: list available tools
    - GET `/api/health`: health check
    """

    api = FastAPI(
        title="mcp-talib HTTP API",
        description="Pure HTTP API for TA-Lib indicators (no MCP)",
        docs_url="/docs",
        redoc_url=None
    )

    api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["mcp-session-id"],
        max_age=3600,
    )

    @api.get("/api/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "ok"}

    @api.post("/api/tools/{tool_name}", response_model=ToolResult)
    async def call_tool(tool_name: str, payload: ToolRequest):
        """Generic wrapper to call a registered indicator.

        Expected JSON shape: { "close": [...], ...params }
        """
        indicator = registry.get_indicator(tool_name)
        if not indicator:
            raise HTTPException(status_code=404, detail="tool not found")

        close = payload.close
        params = {k: v for k, v in payload.model_dump().items() if k != "close"}

        market_data = MarketData(close=close)
        result = await indicator.calculate(market_data, params or {})

        if getattr(result, "success", False):
            values = result.values if isinstance(result.values, (list, dict)) else None
            metadata = result.metadata if isinstance(result.metadata, dict) else None
            return ToolResult(success=True, values=values, metadata=metadata)

        err = getattr(result, "error", None) or "calculation error"
        return ToolResult(success=False, error=str(err))

    @api.get("/api/tools")
    async def list_tools() -> Dict[str, List[str]]:
        """Return list of available tool names."""
        tools: List[str] = []
        if hasattr(registry, "list_indicators"):
            try:
                tools = registry.list_indicators()
            except Exception:
                tools = []

        if not tools:
            tools = ["sma", "ema", "rsi"]

        return {"tools": tools}

    return api
