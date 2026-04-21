"""
Settings for SkyMechanics Aircraft Service.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Service settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # Application settings
    SERVICE_NAME: str = "aircraft"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # FalkorDB settings
    FALKORDB_HOST: str = "localhost"
    FALKORDB_PORT: int = 6379
    FALKORDB_USERNAME: str = "default"
    FALKORDB_PASSWORD: str = ""
    FALKORDB_DATABASE_NAME: str = "falkordb"

    # Multi-tenancy
    MULTI_TENANCY_ENABLED: bool = True
    DEFAULT_TENANT_ID: str = "default"

    # Server settings
    PORT: int = 8208
    HOST: str = "0.0.0.0"

    # Logging
    LOG_LEVEL: str = "INFO"


settings = Settings()
