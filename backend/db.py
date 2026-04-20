"""
Database connection module for FalkorDB.
Handles connection pooling and multi-tenant graph management.
"""
import falkordb
import redis
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database settings from environment variables."""
    model_config = SettingsConfigDict(
        env_prefix="",
        env_file=".env",
        extra="ignore"
    )
    
    host: str = "localhost"
    port: int = 6379
    password: Optional[str] = None
    db_name: str = "skymechanics"


db_settings = DatabaseSettings()


def get_db_settings() -> DatabaseSettings:
    """Get database settings, prioritizing environment variables."""
    return DatabaseSettings()


def get_redis_client() -> redis.asyncio.Redis:
    """Get Redis client for Pub/Sub operations."""
    return redis.asyncio.Redis(
        host=db_settings.host,
        port=db_settings.port,
        password=db_settings.password,
        decode_responses=True
    )


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
        self._client = falkordb.FalkorDB(
            host=self.host,
            port=self.port,
            password=self.password
        )
        return self
    
    def get_graph(self, graph_name: str = None):
        """Get graph instance."""
        if self._graph is None:
            graph_name = graph_name or self.db_name
            self._graph = self._client.select_graph(graph_name)
        return self._graph
    
    def set_graph(self, graph_name: str):
        """Switch to a different graph (multi-tenancy)."""
        self._graph = self._client.select_graph(graph_name)
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


# Global client instance - uses settings from environment variables
db_client = FalkorDBClient()
