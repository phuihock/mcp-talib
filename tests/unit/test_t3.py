import asyncio
import json
import numpy as np
import pytest
import talib as ta
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.mark.asyncio
async def test_t3_matches_talib():
    server_params = StdioServerParameters(command="uv", args=["run", "python", "-m", "mcp_talib.cli"]) 
    close = [float(x) for x in range(1, 101)]
    timeperiod = 5
    vfactor = 0.7

    expected = ta.T3(np.asarray(close, dtype=float), timeperiod=timeperiod, vfactor=vfactor)

    async with stdio_client(server_params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            result = await session.call_tool("calculate_t3", {"close_prices": close, "timeperiod": timeperiod, "vfactor": vfactor})
            if hasattr(result, "value"):
                value = result.value
            else:
                text = getattr(result.content[0], "text", None)
                assert text is not None
                value = json.loads(text)

            assert value.get("success") is True
            np.testing.assert_allclose(np.asarray(value["values"]["t3"], dtype=float), expected, rtol=1e-6, atol=1e-8)


if __name__ == "__main__":
    asyncio.run(test_t3_matches_talib())
