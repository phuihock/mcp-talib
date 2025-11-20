"""HTTP transport implementation for MCP using FastMCP."""

import logging
from typing import Any
from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from .base import BaseTransport

# Configure logger
logger = logging.getLogger(__name__)


class HttpTransport(BaseTransport):
    """HTTP transport implementation using FastMCP streamable-http with CORS support.
    
    This transport runs the MCP server over HTTP using FastMCP's built-in
    streamable-http transport with proper CORS middleware for browser-based clients.
    """
    
    def __init__(self, server: FastMCP[Any], host: str = "0.0.0.0", port: int = 8000, debug: bool = False):
        super().__init__(server, debug)  # type: ignore
        self.host = host
        self.port = port
    
    async def run(self) -> None:
        """Run MCP server over HTTP with CORS middleware for browser clients."""
        if self.debug:
            logger.debug(f"Starting MCP server with HTTP transport on {self.host}:{self.port}")
        
        # Get the Streamable HTTP app from FastMCP
        # This app already has proper lifespan management for the session manager
        app = self.server.streamable_http_app()  # type: ignore
        
        # Add CORS middleware for browser-based MCP clients (e.g., MCP Inspector)
        # add_middleware adds the middleware to the app (not a Mount), so lifespan works
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # In production, specify exact origins like ["http://localhost:6274"]
            allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
            allow_headers=[
                "mcp-protocol-version",
                "mcp-session-id",
                "Authorization",
                "Content-Type",
            ],
            expose_headers=["mcp-session-id"],
            allow_credentials=True,
        )
        
        # Run with uvicorn
        config = uvicorn.Config(
            app,
            host=self.host,
            port=self.port,
            log_level="debug" if self.debug else "info"
        )
        server = uvicorn.Server(config)
        await server.serve()