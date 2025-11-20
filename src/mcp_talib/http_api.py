"""HTTP API factory exposing registered indicators and mounting the MCP app.

This module provides `create_http_app(mcp)` which returns a FastAPI app
that exposes JSON HTTP endpoints for calling registered indicators and
mounts the FastMCP streamable HTTP app at `/mcp` so MCP Inspector and
other MCP clients continue to work.
"""

from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mcp.server.fastmcp import FastMCP

from .indicators import registry
from .models.market_data import MarketData
from .schemas import ToolRequest, ToolResult


def create_http_app(mcp: FastMCP) -> FastAPI:
    """Create a FastAPI app that exposes `/api/tools/*` and mounts `/mcp`.

    - POST `/api/tools/{tool_name}`: JSON body with `close` (list of floats)
      and other parameters passed to the indicator.
    - GET `/api/tools`: list available tools
    """

    api = FastAPI(title="mcp-talib HTTP API", docs_url="/docs", redoc_url=None)

    api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # tighten for production
        allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["mcp-session-id"],
        max_age=3600,
    )

    @api.post("/api/tools/{tool_name}", response_model=ToolResult)
    async def call_tool(tool_name: str, payload: ToolRequest):
        """Generic wrapper to call a registered indicator.

        Expected JSON shape: { "close": [...], ...params }
        """
        indicator = registry.get_indicator(tool_name)
        if not indicator:
            raise HTTPException(status_code=404, detail="tool not found")

        # Use validated close list from the Pydantic model and forward extra
        close = payload.close
        params = {k: v for k, v in payload.model_dump().items() if k != "close"}

        market_data = MarketData(close=close)

        result = await indicator.calculate(market_data, params or {})

        # Normalize result into strict ToolResult JSON
        if getattr(result, "success", False):
            # Keep the full values payload (list or dict) as-is so clients can
            # access both series and named series objects like {"sma": [...]}.
            values = result.values if isinstance(result.values, (list, dict)) else None
            metadata = result.metadata if isinstance(result.metadata, dict) else None
            return ToolResult(success=True, values=values, metadata=metadata)

        err = getattr(result, "error", None) or "calculation error"
        return ToolResult(success=False, error=str(err))

    @api.get("/api/tools")
    async def list_tools() -> Dict[str, List[str]]:
        """Return a best-effort list of available tool names."""
        # Try registry API; fall back to a conservative list if unavailable
        tools: List[str] = []
        if hasattr(registry, "list_indicators"):
            try:
                tools = registry.list_indicators()
            except Exception:
                tools = []

        if not tools:
            # minimal fallback — update as indicators change
            tools = ["sma", "ema", "rsi"]

        return {"tools": tools}

    # Mount the FastMCP starlette app so MCP clients continue to work at /mcp
    starlette_app = mcp.streamable_http_app()
    api.mount("/mcp", starlette_app)

    return api
