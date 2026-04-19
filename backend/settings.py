from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # FalkorDB Configuration
    falkordb_host: str = "localhost"
    falkordb_port: int = 6379
    falkordb_password: Optional[str] = None
    
    # vLLM Configuration
    vllm_url: str = "http://localhost:8000"
    
    # Application Settings
    env: str = "development"
    debug: bool = False
    log_level: str = "INFO"


settings = Settings()
