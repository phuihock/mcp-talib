"""CLI entry point for TA-Lib MCP Server and HTTP API."""

import argparse
import asyncio
import logging
import logging.config
import os
import sys
from pathlib import Path

from .core.mcp_server import create_mcp_server
from .transport.stdio import StdioTransport
from .transport.http import HttpTransport
from .transport.http_api import HttpApiTransport

# Configure logger
logger = logging.getLogger(__name__)


def setup_logging(debug=False, args=None):
    """Configure logging to ensure MCP protocol compliance using required config file."""
    
    # Require external config file
    config_file_path = Path('logging.conf')
    
    if not config_file_path.exists():
        raise FileNotFoundError(
            f"logging.conf is required but not found. "
            f"Please copy logging.conf.example to logging.conf and customize as needed."
        )
    
    try:
        # Apply file-based logging configuration. Use fileConfig so handlers
        # and formatters defined in `logging.conf` are respected.
        logging.config.fileConfig(str(config_file_path), disable_existing_loggers=False)
    except Exception:
        # Fallback: basicConfig if configuration file is invalid or causes errors.
        level = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(level=level)
        logging.getLogger(__name__).exception("Failed to apply logging.conf; falling back to basicConfig")
    else:
        logging.getLogger(__name__).info(f"Loaded logging configuration from {config_file_path}")

    # If debug flag is set, override root logger level to DEBUG to ensure
    # verbose output when requested.
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)

    return True


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="TA-Lib MCP Server and HTTP API")
    parser.add_argument(
        "--mode",
        choices=["mcp", "api"],
        default="mcp",
        help="Mode: 'mcp' runs MCP server, 'api' runs HTTP API server"
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport for MCP server: stdio or http (ignored if mode='api')"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host for servers (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for server (default: 8000)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    return parser.parse_args()


async def run_mcp_server(transport: str, host: str, port: int, debug: bool):
    """Run the MCP server with the specified transport."""
    server = create_mcp_server()

    if transport == "stdio":
        logger.debug("Starting MCP server with STDIO transport...")
        transport_obj = StdioTransport(server, debug=debug)
        await transport_obj.run()
    elif transport == "http":
        logger.debug(f"Starting MCP server with HTTP transport on {host}:{port}...")
        transport_obj = HttpTransport(server, host=host, port=port, debug=debug)
        await transport_obj.run()
    else:
        logger.error(f"Unknown transport: {transport}")
        sys.exit(1)


async def run_api_server(host: str, port: int, debug: bool):
    """Run the HTTP API server."""
    logger.debug(f"Starting HTTP API server on {host}:{port}...")
    transport = HttpApiTransport(host=host, port=port, debug=debug)
    await transport.run()


async def main():
    """Main CLI entry point."""
    args = parse_args()
    
    # Set up logging before creating server
    setup_logging(debug=args.debug, args=args)
    
    if args.mode == "mcp":
        await run_mcp_server(args.transport, args.host, args.port, args.debug)
    elif args.mode == "api":
        await run_api_server(args.host, args.port, args.debug)
    else:
        logger.error(f"Unknown mode: {args.mode}")
        sys.exit(1)


def cli_main():
    """Entry point for package scripts."""
    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())