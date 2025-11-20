import asyncio
import json
import numpy as np
import pytest
import talib as ta
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.mark.asyncio
async def test_ht_trendline_matches_talib():
    server_params = StdioServerParameters(command="uv", args=["run", "python", "-m", "mcp_talib.cli"]) 
    close = [float(x) for x in range(1, 101)]

    expected = ta.HT_TRENDLINE(np.asarray(close, dtype=float))

    async with stdio_client(server_params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            result = await session.call_tool("calculate_ht_trendline", {"close_prices": close})
            if hasattr(result, "value"):
                value = result.value
            else:
                text = getattr(result.content[0], "text", None)
                assert text is not None
                value = json.loads(text)

            assert value.get("success") is True
            np.testing.assert_allclose(np.asarray(value["values"]["ht_trendline"], dtype=float), expected, rtol=1e-6, atol=1e-8)


if __name__ == "__main__":
    asyncio.run(test_ht_trendline_matches_talib())
