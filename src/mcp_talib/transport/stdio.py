"""STDIO transport implementation for MCP."""

import logging
import os
import sys
from mcp.server.fastmcp import FastMCP
from .base import BaseTransport

# Configure logger
logger = logging.getLogger(__name__)


class StdioTransport(BaseTransport):
    """STDIO transport implementation."""
    
    def __init__(self, server: FastMCP, debug: bool = False):
        super().__init__(server, debug)
    
    async def run(self) -> None:
        """Run MCP server over STDIO."""
        # For MCP protocol compliance, never print to stdout/stderr
        # All logging goes to console.log as configured in setup_logging()
        if self.debug:
            logger.debug("Starting MCP server with STDIO transport")
            
        # FastMCP handles the stdio transport automatically
        # Use run_stdio_async for better control and cleaner output
        await self.server.run_stdio_async()