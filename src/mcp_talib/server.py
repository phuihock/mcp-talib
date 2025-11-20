"""Server entry point for TA-Lib MCP Server."""

import asyncio
import sys

from .cli import main


def start() -> None:
    """Start server with default arguments."""
    asyncio.run(main())


def server_main():
    """Server entry point for package scripts."""
    asyncio.run(main())


if __name__ == "__main__":
    start()