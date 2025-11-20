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

    @api.post("/api/tools/{tool_name}", response_model=ToolResult, openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "examples": {
                        "sma": {
                            "summary": "sma",
                            "value": {"close": [1,2,3,4,5], "timeperiod": 3}
                        },
                        "ema": {
                            "summary": "ema",
                            "value": {"close": [1,2,3,4,5], "timeperiod": 3}
                        },
                        "rsi": {
                            "summary": "rsi",
                            "value": {"close": [1,2,3,4,5], "timeperiod": 14}
                        },
                        "bbands": {
                            "summary": "bbands",
                            "value": {"close": [1,2,3,4,5], "timeperiod": 20, "nbdevup": 2.0, "nbdevdn": 2.0, "matype": 0}
                        },
                        "dema": {
                            "summary": "dema",
                            "value": {"close": [1,2,3,4,5], "timeperiod": 30}
                        },
                        "ht_trendline": {
                            "summary": "ht_trendline",
                            "value": {"close": [1,2,3,4,5]}
                        },
                        "kama": {
                            "summary": "kama",
                            "value": {"close": [1,2,3,4,5], "timeperiod": 10}
                        },
                        "ma": {
                            "summary": "ma",
                            "value": {"close": [1,2,3,4,5], "timeperiod": 30, "matype": 0}
                        },
                        "mama": {
                            "summary": "mama",
                            "value": {"close": [1,2,3,4,5], "fastlimit": 0.5, "slowlimit": 0.05}
                        },
                        "mavp": {
                            "summary": "mavp",
                            "value": {"close": [1,2,3,4,5], "periods": [3,4,5], "minperiod": 2, "maxperiod": 30}
                        },
                        "midpoint": {
                            "summary": "midpoint",
                            "value": {"close": [1,2,3,4,5], "timeperiod": 14}
                        },
                        "midprice": {
                            "summary": "midprice",
                            "value": {"high": [2,3,4,5,6], "low": [1,2,3,4,5], "timeperiod": 14}
                        },
                        "sar": {
                            "summary": "sar",
                            "value": {"high": [2,3,4,5,6], "low": [1,2,3,4,5], "acceleration": 0.02, "maximum": 0.2}
                        },
                        "sarext": {
                            "summary": "sarext",
                            "value": {"high": [2,3,4,5,6], "low": [1,2,3,4,5], "startvalue": None, "offsetonreverse": 0.0, "acceleration_initlong": 0.02, "acceleration_long": 0.02, "acceleration_maxlong": 0.2, "acceleration_initshort": 0.02, "acceleration_short": 0.02, "acceleration_maxshort": 0.2}
                        },
                        "t3": {
                            "summary": "t3",
                            "value": {"close": [1,2,3,4,5], "timeperiod": 5, "vfactor": 0.7}
                        },
                        "tema": {
                            "summary": "tema",
                            "value": {"close": [1,2,3,4,5], "timeperiod": 30}
                        },
                        "trima": {
                            "summary": "trima",
                            "value": {"close": [1,2,3,4,5], "timeperiod": 30}
                        },
                        "wma": {
                            "summary": "wma",
                            "value": {"close": [1,2,3,4,5], "timeperiod": 30}
                        },
                    }
                }
            }
        }
    })
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
