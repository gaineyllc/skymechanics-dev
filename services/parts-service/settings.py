"""
Settings for SkyMechanics Parts Service.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    """Service settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # Application settings
    SERVICE_NAME: str = "parts"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # FalkorDB settings
    FALKORDB_HOST: str = "localhost"
    FALKORDB_PORT: int = 6379
    FALKORDB_USERNAME: str = "default"
    FALKORDB_PASSWORD: str = ""
    FALKORDB_DATABASE_NAME: str = "falkordb"

    # Redis settings - store as string, parse in validator
    REDIS_HOST: str = "localhost"
    REDIS_PORT_STR: str | int = "6379"
    REDIS_PASSWORD: str = ""

    @field_validator("REDIS_PORT_STR", mode="before")
    @classmethod
    def parse_redis_port(cls, v: str | int) -> int:
        """Parse REDIS_PORT from URL format (tcp://host:port) to int."""
        if v is None:
            return 6379
        port_str = str(v)
        if port_str.startswith("tcp://"):
            port_str = port_str.split(":")[-1]
        try:
            return int(port_str)
        except ValueError:
            return 6379

    # Multi-tenancy
    MULTI_TENANCY_ENABLED: bool = True
    DEFAULT_TENANT_ID: str = "default"

    # Server settings
    PORT: int = 8205
    HOST: str = "0.0.0.0"

    # Logging
    LOG_LEVEL: str = "INFO"


settings = Settings()
