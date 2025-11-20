import asyncio
import json
import numpy as np
import pytest
import talib as ta
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.mark.asyncio
async def test_sar_matches_talib():
    server_params = StdioServerParameters(command="uv", args=["run", "python", "-m", "mcp_talib.cli"]) 
    high = [float(x + 1) for x in range(1, 101)]
    low = [float(x) for x in range(1, 101)]

    expected = ta.SAR(np.asarray(high, dtype=float), np.asarray(low, dtype=float))

    async with stdio_client(server_params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            result = await session.call_tool("calculate_sar", {"high_prices": high, "low_prices": low})
            if hasattr(result, "value"):
                value = result.value
            else:
                text = getattr(result.content[0], "text", None)
                assert text is not None
                value = json.loads(text)

            assert value.get("success") is True
            vals = value["values"]
            np.testing.assert_allclose(np.asarray(vals["sar"], dtype=float), expected, rtol=1e-6, atol=1e-8)


if __name__ == "__main__":
    asyncio.run(test_sar_matches_talib())
