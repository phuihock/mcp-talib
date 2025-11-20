"""Typer CLI to call registered MCP tools from the command line.

Provides `list` and `call` commands that reuse the same `registry` and
indicator calculate implementation used by MCP tools and the HTTP API.
"""

import json
import asyncio
from typing import Optional, Dict, Any, List

import typer

from .indicators import registry
from .models.market_data import MarketData
from .schemas import ToolResult

app = typer.Typer(help="mcp-talib tools CLI")


def _call_indicator_sync(indicator_name: str, close: List[float], params: Dict[str, Any]):
    """Synchronously call an async indicator.calculate function."""
    indicator = registry.get_indicator(indicator_name)
    if not indicator:
        raise RuntimeError("indicator not found")

    market_data = MarketData(close=close)

    async def run():
        return await indicator.calculate(market_data, params)

    return asyncio.run(run())


@app.command("list")
def list_tools():
    """Print available tool names (JSON)."""
    tools = []
    if hasattr(registry, "list_indicators"):
        try:
            tools = registry.list_indicators()
        except Exception:
            tools = []

    if not tools:
        tools = ["sma", "ema", "rsi"]

    typer.echo(json.dumps({"tools": tools}))


@app.command("call")
def call(
    name: str = typer.Argument(..., help="Tool name"),
    close_json: Optional[str] = typer.Option(None, "--close", "-c", help="JSON array of close prices"),
    json_file: Optional[str] = typer.Option(None, "--file", "-f", help="JSON file with payload"),
    timeperiod: Optional[int] = typer.Option(None, "--timeperiod", "-t"),
):
    """Call a tool. Provide either `--close` JSON array or `--file` with JSON payload.

    Example: `mcp-talib call sma --close '[1,2,3,4]' --timeperiod 3`
    """
    if json_file:
        with open(json_file, "r") as fh:
            payload = json.load(fh)
    elif close_json:
        payload = {"close": json.loads(close_json)}
        if timeperiod:
            payload["timeperiod"] = timeperiod
    else:
        typer.echo("Provide --close or --file", err=True)
        raise typer.Exit(code=2)

    close = payload.get("close")
    if close is None:
        typer.echo("missing 'close' in payload", err=True)
        raise typer.Exit(code=2)

    params = {k: v for k, v in payload.items() if k != "close"}
    res = _call_indicator_sync(name, close, params)

    # Normalize into ToolResult and print strict JSON
    success = getattr(res, "success", False)

    # Preserve full values payload (list or dict)
    raw_values = getattr(res, "values", None)
    values = raw_values if isinstance(raw_values, (list, dict)) else None

    metadata = res.metadata if isinstance(getattr(res, "metadata", None), dict) else None
    error = getattr(res, "error", None)

    out = ToolResult(success=bool(success), values=values, metadata=metadata, error=str(error) if error else None)
    typer.echo(out.model_dump_json())


if __name__ == "__main__":
    app()
