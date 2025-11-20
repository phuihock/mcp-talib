"""CLI entry point for TA-Lib MCP Server."""

import argparse
import asyncio
import logging
import logging.config
import os
import sys
from pathlib import Path

from .core.server import create_server
from .transport.stdio import StdioTransport
from .transport.http import HttpTransport

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
        # Read config file
        with open(config_file_path, 'r') as f:
            config_content = f.read()
        
        logger = logging.getLogger(__name__)
        logger.info(f"Loaded logging configuration from {config_file_path}")
        return False
    except Exception as e:
        raise RuntimeError(f"Failed to load logging config from {config_file_path}: {e}")


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="TA-Lib MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport type (default: stdio)"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host for HTTP transport (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for HTTP transport (default: 8000)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    return parser.parse_args()


async def main():
    """Main CLI entry point."""
    args = parse_args()
    
    # Set up logging before creating server
    setup_logging(debug=args.debug, args=args)
    
    server = create_server()

    if args.transport == "stdio":
        logger.debug("Starting MCP server with STDIO transport...")
        transport = StdioTransport(server, debug=args.debug)
        await transport.run()
    elif args.transport == "http":
        logger.debug(f"Starting MCP server with HTTP transport on {args.host}:{args.port}...")
        transport = HttpTransport(server, host=args.host, port=args.port, debug=args.debug)
        await transport.run()
    else:
        logger.error(f"Unknown transport: {args.transport}")
        sys.exit(1)


def cli_main():
    """Entry point for package scripts."""
    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())