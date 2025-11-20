# TA-Lib MCP Server

Technical analysis indicators MCP server for Model Context Protocol.

## Quick Start

```bash
# Install dependencies
uv sync --dev

# Copy logging configuration
cp logging.conf.example logging.conf

# Run server with STDIO transport
uv run python -m mcp_talib.cli --transport stdio

# Run server with HTTP transport
uv run python -m mcp_talib.cli --transport http --host 0.0.0.0 --port 8000
```

## Logging Configuration

The server requires a `logging.conf` file for configuration. Copy the example configuration:

```bash
cp logging.conf.example logging.conf
```

You can customize the logging levels, format, and output file in `logging.conf`. The server logs to `console.log` to maintain MCP protocol compliance.

- **Core Indicators**: SMA, RSI, MACD
- **Advanced Indicators**: Bollinger Bands, Stochastic, ADX
- **Dual Transport**: Both STDIO and HTTP support
- **Performance**: Optimized for high-volume calculations
- **Error Handling**: Comprehensive error handling with detailed messages
- **Monitoring**: Metrics and health endpoints

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

### HTTP Client Configuration

For HTTP transport, configure your client to connect to:

```
http://localhost:8000/mcp
```

The server supports Server-Sent Events (SSE) for real-time updates.

### MCP.js Client Example

```javascript
import { MCPServerClient } from '@modelcontextprotocol/client';

const client = new MCPServerClient({
  name: 'talib',
  command: 'uv',
  args: ['run', 'python', '-m', 'mcp_talib.cli', '--transport', 'stdio'],
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

## Available Tools

The server provides the following MCP tools:

- `calculate_sma` - Simple Moving Average
- `calculate_ema` - Exponential Moving Average
- `calculate_rsi` - Relative Strength Index

## Documentation

See `specs/001-ta-lib-mcp-server/quickstart.md` for detailed usage instructions.

## Development

```bash
# Run tests
uv run pytest

# Format code
uv run black src/ tests/
uv run isort src/ tests/

# Lint code
uv run ruff check src/ tests/
```

## License

MIT

## HTTP API & CLI

This project now exposes the same MCP tools as both HTTP JSON endpoints and a Typed CLI (Typer).

- HTTP endpoint: `POST /api/tools/{tool_name}`
  - Request JSON: `{ "close": [..], ...params }` (e.g. `timeperiod`)
  - Response JSON: `{ "success": true, "values": [...], "metadata": {...} }`
  - Example curl:

```bash
curl -s -X POST http://localhost:8000/api/tools/sma \
  -H 'Content-Type: application/json' \
  -d '{"close": [1,2,3,4,5], "timeperiod": 3}'
```

- MCP endpoint remains at `/mcp` for MCP clients (MCP Inspector, MCP.js, etc.). The HTTP API mounts the MCP app so both APIs coexist.

- CLI (Typer): `src/mcp_talib/cli_tools.py`
  - List tools:

```bash
python -m mcp_talib.cli_tools list
```

  - Call a tool from the CLI:

```bash
python -m mcp_talib.cli_tools call sma --close '[1,2,3,4]' --timeperiod 3
```

Notes:
- Requests are validated using Pydantic (`ToolRequest` / `ToolResult`).
- The underlying indicator implementations remain the single source of truth (registered in the MCP `registry`) — the HTTP API and CLI call the same code so results match.
- For browser clients, CORS is enabled and `mcp-session-id` is exposed in responses.
