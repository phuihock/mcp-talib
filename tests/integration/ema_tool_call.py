import asyncio
import json
import subprocess
import os

async def run_ema():
    # Start the server in subprocess
    proc = subprocess.Popen(
        ["uv", "run", "python", "-m", "mcp_talib.cli"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Send list tools request
    list_request = json.dumps({
        "type": "ListToolsRequest",
        "id": 1
    })
    
    print("Sending list tools request...")
    stdout, _ = proc.communicate(input=list_request + "\n")
    print("Response:", stdout)
    
    # Now send tool call request
    proc = subprocess.Popen(
        ["uv", "run", "python", "-m", "mcp_talib.cli"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    call_request = json.dumps({
        "type": "CallToolRequest",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "calculate_ema",
            "arguments": {
                "close_prices": [10.0, 12.0, 11.0, 13.0, 14.0, 15.0, 14.0, 16.0, 15.0, 17.0, 
                                 18.0, 17.0, 19.0, 20.0, 19.0, 21.0, 22.0, 23.0, 24.0, 25.0, 
                                 24.0, 26.0, 27.0],
                "timeperiod": 10
            }
        }
    })
    
    print("Sending EMA tool call request...")
    stdout, _ = proc.communicate(input=call_request + "\n")
    
    # Find the response in the output
    for line in stdout.split('\n'):
        if line.strip().startswith('{') and 'success' in line:
            try:
                result = json.loads(line)
                print(f"EMA calculation result:")
                print(json.dumps(result, indent=2))
                break
            except:
                pass

if __name__ == "__main__":
    asyncio.run(run_ema())
