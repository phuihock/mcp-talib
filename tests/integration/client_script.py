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

            # List tools
            result = await session.list_tools()
            print("Available tools:")
            for tool in result.tools:
                print(f"- {tool.name}: {tool.description}")

if __name__ == "__main__":
    asyncio.run(main())
