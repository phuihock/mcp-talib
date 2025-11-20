"""HTTP REST API transport implementation."""

import logging
import uvicorn
from .base import BaseTransport
from ..http_api_server import create_http_api_app

# Configure logger
logger = logging.getLogger(__name__)


class HttpApiTransport(BaseTransport):
    """HTTP REST API transport for indicator endpoints only (no MCP).
    
    This transport runs a pure FastAPI server exposing /api/tools endpoints
    for calling indicators via HTTP. It does not expose MCP protocol endpoints.
    """
    
    def __init__(self, host: str = "0.0.0.0", port: int = 8001, debug: bool = False):
        # Note: No server argument since this doesn't use FastMCP
        super().__init__(None, debug)
        self.host = host
        self.port = port
    
    async def run(self) -> None:
        """Run the HTTP API server on the specified host and port."""
        if self.debug:
            logger.debug(f"Starting HTTP API server on {self.host}:{self.port}")
        
        # Create the FastAPI app with only /api/tools endpoints
        app = create_http_api_app()
        
        # Run using uvicorn
        config = uvicorn.Config(
            app,
            host=self.host,
            port=self.port,
            log_level="info" if self.debug else "warning",
            access_log=self.debug,
        )
        server = uvicorn.Server(config)
        await server.serve()
