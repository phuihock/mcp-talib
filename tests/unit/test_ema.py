import asyncio
import json
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.mark.asyncio
async def test_ema():
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "-m", "mcp_talib.cli"],
    )

    async with stdio_client(server_params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()

            # Test EMA calculation
            result = await session.call_tool(
                "calculate_ema",
                {
                    "close_prices": [10.0, 12.0, 11.0, 13.0, 14.0, 15.0, 14.0, 16.0, 15.0, 17.0,
                                     18.0, 17.0, 19.0, 20.0, 19.0, 21.0, 22.0, 23.0, 24.0, 25.0,
                                     24.0, 26.0, 27.0],
                    "timeperiod": 10,
                },
            )

            # Extract the tool response payload. Depending on client version
            # the result may expose `.value` or contain JSON in `content[0].text`.
            if hasattr(result, "value"):
                value = result.value
            else:
                # Fallback: parse JSON from content text
                text = None
                if getattr(result, "content", None):
                    text = getattr(result.content[0], "text", None)
                assert text is not None, "No JSON payload found in CallToolResult"
                value = json.loads(text)
            assert isinstance(value, dict)
            assert value.get("success") is True
            assert "values" in value and "ema" in value["values"]
            ema_values = value["values"]["ema"]
            metadata = value.get("metadata", {})
            assert isinstance(ema_values, list)
            assert metadata.get("output_points") == len(ema_values)
            assert metadata.get("timeperiod") == 10


if __name__ == "__main__":
    asyncio.run(test_ema())
