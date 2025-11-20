import asyncio
from stdio_client import MCPAsyncStdioClient
import json

async def run_ema():
    client = MCPAsyncStdioClient("stdio", ["uv", "run", "python", "-m", "mcp_talib.cli"])
    
    try:
        await client.connect()
        
        # Test EMA calculation
        result = await client.call_tool(
            "calculate_ema",
            {
                "close_prices": [10.0, 12.0, 11.0, 13.0, 14.0, 15.0, 14.0, 16.0, 15.0, 17.0, 
                                 18.0, 17.0, 19.0, 20.0, 19.0, 21.0, 22.0, 23.0, 24.0, 25.0, 
                                 24.0, 26.0, 27.0],
                "timeperiod": 10
            }
        )
        
        print(f"EMA calculation result:")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(run_ema())
