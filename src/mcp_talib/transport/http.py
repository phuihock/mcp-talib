"""HTTP transport implementation for MCP using FastMCP."""

import logging
import uvicorn
from typing import cast
from mcp.server.fastmcp import FastMCP
from .base import BaseTransport
from ..http_api import create_http_app

# Configure logger
logger = logging.getLogger(__name__)


class HttpTransport(BaseTransport):
    """HTTP transport implementation using FastMCP."""
    
    def __init__(self, server: FastMCP, host: str = "0.0.0.0", port: int = 8000, debug: bool = False):
        super().__init__(server, debug)
        self.host = host
        self.port = port
    
    async def run(self) -> None:
        """Run MCP server over HTTP with CORS support for browser-based clients like MCP Inspector."""
        if self.debug:
            logger.debug(f"Starting MCP server with HTTP transport on {self.host}:{self.port}")
        
        # Update server settings with host and port
        self.server.settings.host = self.host
        self.server.settings.port = self.port
        
        # Create a FastAPI app that mounts the MCP Starlette app and exposes
        # HTTP endpoints for tools. `create_http_app` applies the necessary
        # CORS middleware and mounts `/mcp` for MCP clients.
        # `self.server` should be a FastMCP instance; cast for static checkers.
        app = create_http_app(cast(FastMCP, self.server))

        # Run the ASGI app using Uvicorn directly so middleware and sub-apps
        # are properly applied.
        config = uvicorn.Config(
            app=app,
            host=self.host,
            port=self.port,
            log_level="info" if self.debug else "warning",
            access_log=self.debug,
        )
        server = uvicorn.Server(config)
        await server.serve()