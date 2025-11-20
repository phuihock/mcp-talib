import asyncio
import json
import numpy as np
import pytest
import talib as ta
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.mark.asyncio
async def test_mama_matches_talib():
    server_params = StdioServerParameters(command="uv", args=["run", "python", "-m", "mcp_talib.cli"]) 
    close = [float(x) for x in range(1, 101)]
    fastlimit = 0.5
    slowlimit = 0.05

    expected_mama, expected_fama = ta.MAMA(np.asarray(close, dtype=float), fastlimit=fastlimit, slowlimit=slowlimit)

    async with stdio_client(server_params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            result = await session.call_tool("calculate_mama", {"close_prices": close, "fastlimit": fastlimit, "slowlimit": slowlimit})
            if hasattr(result, "value"):
                value = result.value
            else:
                text = getattr(result.content[0], "text", None)
                assert text is not None
                value = json.loads(text)

            assert value.get("success") is True
            vals = value["values"]
            np.testing.assert_allclose(np.asarray(vals["mama"], dtype=float), expected_mama, rtol=1e-6, atol=1e-8)
            np.testing.assert_allclose(np.asarray(vals["fama"], dtype=float), expected_fama, rtol=1e-6, atol=1e-8)


if __name__ == "__main__":
    asyncio.run(test_mama_matches_talib())
