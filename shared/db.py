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
    redis_host: Optional[str] = None
    # Store as string to avoid parsing error, then convert in __post_init__
    redis_port: Optional[str] = None
    
    def __post_init__(self):
        """Parse redis_port from TCP URL format."""
        if self.redis_port and isinstance(self.redis_port, str):
            if self.redis_port.startswith("tcp://"):
                try:
                    self.redis_port = int(self.redis_port.split(":")[-1])
                except (ValueError, IndexError):
                    self.redis_port = 6379
            else:
                try:
                    self.redis_port = int(self.redis_port)
                except ValueError:
                    self.redis_port = 6379
        # Convert to int for type safety
        if isinstance(self.redis_port, int):
            self.__dict__["redis_port"] = self.redis_port


db_settings = DatabaseSettings()


def get_db_settings() -> DatabaseSettings:
    """Get database settings, prioritizing environment variables."""
    return DatabaseSettings()


def get_redis_client() -> redis.asyncio.Redis:
    """Get Redis client for Pub/Sub operations."""
    redis_port = db_settings.redis_port
    if isinstance(redis_port, str):
        if redis_port.startswith("tcp://"):
            try:
                redis_port = int(redis_port.split(":")[-1])
            except (ValueError, IndexError):
                redis_port = 6379
        else:
            try:
                redis_port = int(redis_port)
            except ValueError:
                redis_port = 6379
    return redis.asyncio.Redis(
        host=db_settings.redis_host or db_settings.host,
        port=redis_port or db_settings.port,
        password=db_settings.password,
        decode_responses=True,
        max_connections=100  # Production connection pool
    )


def get_redis_cache() -> redis.asyncio.Redis:
    """Get Redis client for caching operations (separate pool)."""
    redis_port = db_settings.redis_port
    if isinstance(redis_port, str):
        if redis_port.startswith("tcp://"):
            try:
                redis_port = int(redis_port.split(":")[-1])
            except (ValueError, IndexError):
                redis_port = 6379
        else:
            try:
                redis_port = int(redis_port)
            except ValueError:
                redis_port = 6379
    return redis.asyncio.Redis(
        host=db_settings.redis_host or db_settings.host,
        port=redis_port or db_settings.port,
        password=db_settings.password,
        decode_responses=True,
        db=1,  # Separate DB for cache
        max_connections=50
    )


def get_redis_pubsub() -> redis.asyncio.Redis:
    """Get Redis client for Pub/Sub operations (separate pool)."""
    redis_port = db_settings.redis_port
    if isinstance(redis_port, str):
        if redis_port.startswith("tcp://"):
            try:
                redis_port = int(redis_port.split(":")[-1])
            except (ValueError, IndexError):
                redis_port = 6379
        else:
            try:
                redis_port = int(redis_port)
            except ValueError:
                redis_port = 6379
    return redis.asyncio.Redis(
        host=db_settings.redis_host or db_settings.host,
        port=redis_port or db_settings.port,
        password=db_settings.password,
        decode_responses=True,
        db=2,  # Separate DB for pubsub
        max_connections=25
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
