import asyncio
import json
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.mark.asyncio
async def test_bbands_tool_call():
    server_params = StdioServerParameters(command="uv", args=["run", "python", "-m", "mcp_talib.cli"]) 

    close = [float(x) for x in range(1, 51)]
    async with stdio_client(server_params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            result = await session.call_tool("calculate_bbands", {"close_prices": close})
            if hasattr(result, "value"):
                value = result.value
            else:
                text = getattr(result.content[0], "text", None)
                assert text is not None
                value = json.loads(text)

            assert value.get("success") is True
            assert "upperband" in value["values"]
            assert "middleband" in value["values"]
            assert "lowerband" in value["values"]


if __name__ == "__main__":
    asyncio.run(test_bbands_tool_call())
