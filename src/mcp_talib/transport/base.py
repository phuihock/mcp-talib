"""Base transport abstraction layer."""

from abc import ABC, abstractmethod
from typing import Any

from mcp.server import Server


class BaseTransport(ABC):
    """Abstract base class for transport implementations."""
    
    def __init__(self, server: Server, debug: bool = False):
        self.server = server
        self.debug = debug
    
    @abstractmethod
    async def run(self) -> None:
        """Start the transport and server."""
        pass