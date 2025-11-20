import asyncio
import json
import numpy as np
import pytest
import talib as ta
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.mark.asyncio
async def test_bbands_matches_talib():
    server_params = StdioServerParameters(command="uv", args=["run", "python", "-m", "mcp_talib.cli"]) 

    # prepare input
    close = [float(x) for x in range(1, 51)]
    timeperiod = 20
    nbdevup = 2.0
    nbdevdn = 2.0

    # expected via TA-Lib
    expected_upper, expected_middle, expected_lower = ta.BBANDS(np.asarray(close, dtype=float), timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn)

    async with stdio_client(server_params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            result = await session.call_tool(
                "calculate_bbands",
                {"close_prices": close, "timeperiod": timeperiod, "nbdevup": nbdevup, "nbdevdn": nbdevdn},
            )

            if hasattr(result, "value"):
                value = result.value
            else:
                text = getattr(result.content[0], "text", None)
                assert text is not None
                value = json.loads(text)

            assert value.get("success") is True
            values = value["values"]
            # compare lists with numpy
            np.testing.assert_allclose(np.asarray(values["upperband"], dtype=float), expected_upper, rtol=1e-6, atol=1e-8)
            np.testing.assert_allclose(np.asarray(values["middleband"], dtype=float), expected_middle, rtol=1e-6, atol=1e-8)
            np.testing.assert_allclose(np.asarray(values["lowerband"], dtype=float), expected_lower, rtol=1e-6, atol=1e-8)


if __name__ == "__main__":
    asyncio.run(test_bbands_matches_talib())
