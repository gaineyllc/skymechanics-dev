"""
Database connection module for FalkorDB.
Handles connection pooling and multi-tenant graph management.
"""
import redis
from redis.commands.graph import Graph
from typing import Optional
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    """Database settings from environment variables."""
    
    host: str = "localhost"
    port: int = 6379
    password: Optional[str] = None
    db_name: str = "skymechanics"


db_settings = DatabaseSettings()


class FalkorDBClient:
    """Client for FalkorDB graph database."""
    
    def __init__(
        self,
        host: str = None,
        port: int = None,
        password: Optional[str] = None,
        db_name: str = None
    ):
        self.host = host or db_settings.host
        self.port = port or db_settings.port
        self.password = password or db_settings.password
        self.db_name = db_name or db_settings.db_name
        self._client = None
        self._graph = None
    
    def connect(self):
        """Establish connection to FalkorDB."""
        self._client = redis.Redis(
            host=self.host,
            port=self.port,
            password=self.password,
            decode_responses=True
        )
        # Test connection
        self._client.ping()
        return self
    
    def get_graph(self, graph_name: str = None):
        """Get graph instance."""
        if self._graph is None:
            graph_name = graph_name or self.db_name
            self._graph = Graph(self._client, graph_name)
        return self._graph
    
    def set_graph(self, graph_name: str):
        """Switch to a different graph (multi-tenancy)."""
        self._graph = Graph(self._client, graph_name)
        return self._graph
    
    def close(self):
        """Close connection."""
        if self._client:
            self._client.close()
            self._graph = None
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Global client instance
db_client = FalkorDBClient()
