import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "mcp-talib"],
    )

    async with stdio_client(server_params) as (reader, writer):
        async with ClientSession(reader, writer) as session:
            await session.initialize()

            # Call SMA tool
            result = await session.call_tool(
                "calculate_sma",
                arguments={
                    "close_prices": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                    "timeperiod": 10
                }
            )
            print("SMA calculation result:")
            print(result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())
