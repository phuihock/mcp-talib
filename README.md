# TA-Lib MCP Server

Technical analysis indicators MCP server and HTTP API for the Model Context Protocol.

## Quick Start

```bash
# Install dependencies
uv sync --dev

# Copy logging configuration
cp logging.conf.example logging.conf

# Run MCP server with STDIO transport (default)
uv run python -m mcp_talib.cli --mode mcp --transport stdio

# Run MCP server with HTTP transport
uv run python -m mcp_talib.cli --mode mcp --transport http --port 8000

# Run HTTP API server only
uv run python -m mcp_talib.cli --mode api --port 8001

# Run CLI tools directly
uv run python -m mcp_talib.cli_tools list
uv run python -m mcp_talib.cli_tools call sma --close '[1,2,3,4,5]' --timeperiod 3
```

## Architecture

This project provides **three independent access methods**:

### 1. MCP Server (`--mode mcp`)
- Pure MCP protocol implementation exposing all TA-Lib indicators as MCP tools
- Supports both STDIO and HTTP transports
- For use with MCP clients (Claude Desktop, MCP Inspector, MCP.js, etc.)
- No REST endpoints

**Run with STDIO** (for Claude Desktop):
```bash
uv run python -m mcp_talib.cli --mode mcp --transport stdio
```

**Run with HTTP** (for MCP Inspector or web clients):
```bash
uv run python -m mcp_talib.cli --mode mcp --transport http --port 8000
# Then connect MCP Inspector to http://localhost:8000/mcp
```

### 2. HTTP API Server (`--mode api`)
- Pure REST API with `/api/tools/*` JSON endpoints
- For programmatic HTTP access to indicators
- No MCP protocol, just clean REST

**Run HTTP API**:
```bash
uv run python -m mcp_talib.cli --mode api --port 8001
```

**Example request**:
```bash
curl -X POST http://localhost:8001/api/tools/sma \
  -H 'Content-Type: application/json' \
  -d '{"close": [1,2,3,4,5], "timeperiod": 3}'
```

### 3. CLI Tools
Direct command-line access to all indicators via Typer:

```bash
uv run python -m mcp_talib.cli_tools list
uv run python -m mcp_talib.cli_tools call sma --close '[1,2,3,4,5]' --timeperiod 3
```

## Features

- **All TA-Lib Overlap Studies**: BBANDS, DEMA, EMA, HT_TRENDLINE, KAMA, MA, MAMA, MAVP, MIDPOINT, MIDPRICE, SAR, SAREXT, SMA, T3, TEMA, TRIMA, WMA
- **Three Access Methods**: MCP, HTTP REST, CLI
- **Dual Transport**: STDIO and HTTP for MCP
- **Cross-platform**: Works on Linux, macOS, Windows
- **Comprehensive Testing**: 26+ unit and integration tests
- **Error Handling**: Detailed error messages and validation

## Logging Configuration

The server requires a `logging.conf` file for configuration. Copy the example:

```bash
cp logging.conf.example logging.conf
```

Customize logging levels, format, and output file in `logging.conf`. The server logs to `console.log` to maintain MCP protocol compliance.

## Client Configuration

### Claude Desktop Integration

1. **Create a configuration file** at `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or appropriate location for your OS.

2. **Add the MCP server configuration**:

```json
{
  "mcpServers": {
    "talib": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "-m",
        "mcp_talib.cli",
        "--mode",
        "mcp",
        "--transport",
        "stdio"
      ],
      "cwd": "/path/to/mcp-talib"
    }
  }
}
```

3. **Restart Claude Desktop** to load the TA-Lib server.

4. **Verify installation** by asking Claude: "What technical analysis tools do you have?"

### MCP Inspector (HTTP)

For HTTP transport, configure MCP Inspector to connect to:

```
http://localhost:8000/mcp
```

Run the MCP server with HTTP:
```bash
uv run python -m mcp_talib.cli --mode mcp --transport http --port 8000
```

**Important**: The HTTP transport includes CORS middleware to support browser-based MCP clients like MCP Inspector. If you're behind a reverse proxy or need to restrict access, update the `allow_origins` setting in `transport/http.py`.

### MCP.js Client Example

```javascript
import { MCPServerClient } from '@modelcontextprotocol/client';

const client = new MCPServerClient({
  name: 'talib',
  command: 'uv',
  args: ['run', 'python', '-m', 'mcp_talib.cli', '--mode', 'mcp', '--transport', 'stdio'],
  cwd: process.cwd()
});

// List available tools
const tools = await client.listTools();
console.log('Available tools:', tools.map(t => t.name));

// Calculate SMA
const smaResult = await client.callTool('calculate_sma', {
  close_prices: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
  timeperiod: 5
});
console.log('SMA result:', smaResult);
```

### HTTP API Client (Python)

```python
import requests

# List available tools
response = requests.get('http://localhost:8001/api/tools')
tools = response.json()['tools']
print('Available tools:', tools)

# Calculate SMA
payload = {
    'close': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'timeperiod': 5
}
response = requests.post('http://localhost:8001/api/tools/sma', json=payload)
result = response.json()
print('SMA result:', result['values'])
```

## Available Tools

The server provides MCP tools and HTTP endpoints for all TA-Lib overlap studies:

- `calculate_sma` - Simple Moving Average
- `calculate_ema` - Exponential Moving Average
- `calculate_rsi` - Relative Strength Index
- `calculate_bbands` - Bollinger Bands
- `calculate_dema` - Double Exponential Moving Average
- `calculate_ht_trendline` - Hilbert Transform Trendline
- `calculate_kama` - Kaufman Adaptive Moving Average
- `calculate_ma` - Moving Average (with matype)
- `calculate_mama` - MESA Adaptive Moving Average
- `calculate_mavp` - Moving Average Variable Period
- `calculate_midpoint` - Midpoint
- `calculate_midprice` - Midpoint Price
- `calculate_sar` - Parabolic SAR
- `calculate_sarext` - Parabolic SAR Extended
- `calculate_t3` - T3 Moving Average
- `calculate_tema` - Triple Exponential Moving Average
- `calculate_trima` - Triangular Moving Average
- `calculate_wma` - Weighted Moving Average

## Development

```bash
# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/unit/test_sma.py -v

# Run with coverage
uv run pytest --cov=src/mcp_talib

# Format code
uv run black src/ tests/
uv run isort src/ tests/

# Lint code
uv run ruff check src/ tests/
```

## TA-Lib Platform Requirements

This project uses the `ta-lib` Python bindings which require the native TA-Lib C library. On CI or developer machines, you must install the system TA-Lib library before installing Python dependencies.

Links and notes:

- TA-Lib (C library): https://ta-lib.org/ (download and build instructions)
- ta-lib-python (Python bindings): https://github.com/TA-Lib/ta-lib-python

Example (Ubuntu) CI steps:

```bash
# Install build dependencies
sudo apt-get update && sudo apt-get install -y build-essential wget

# Download and build TA-Lib C library
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/usr
make
sudo make install

# Then install Python package
pip install TA-Lib
```

If you prefer not to build the C library, use pre-built wheels where available or run tests in an environment that provides TA-Lib (e.g., manylinux CI images).

## HTTP API & CLI

This project exposes the same MCP tools as both HTTP JSON endpoints and a Typed CLI (Typer).

### HTTP Endpoint

`POST /api/tools/{tool_name}`

**Request JSON**: `{ "close": [..], ...params }` (e.g., `timeperiod`)

**Response JSON**: `{ "success": true, "values": [...], "metadata": {...} }`

**Example**:

```bash
curl -X POST http://localhost:8000/api/tools/sma \
  -H 'Content-Type: application/json' \
  -d '{"close": [1,2,3,4,5], "timeperiod": 3}'
```

### MCP Endpoint

The MCP endpoint remains at `/mcp` for MCP clients (MCP Inspector, MCP.js, etc.). The HTTP API mounts the MCP app so both APIs coexist.

### CLI (Typer)

Access tools from the command line via `src/mcp_talib/cli_tools.py`:

**List available tools**:
```bash
uv run python -m mcp_talib.cli_tools list
```

**Call a tool**:
```bash
uv run python -m mcp_talib.cli_tools call sma --close '[1,2,3,4,5]' --timeperiod 3
```

### Implementation Notes

- Requests are validated using Pydantic
- The underlying indicator implementations are the single source of truth (registered in the MCP registry)
- HTTP API and CLI call the same code so results match exactly
- For browser clients, CORS is enabled and `mcp-session-id` is exposed in responses

## License

MIT
