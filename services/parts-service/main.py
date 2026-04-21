"""
SkyMechanics Parts Service
Exposes parts inventory and catalog management endpoints.
"""
import structlog
from fastapi import FastAPI
from pydantic_settings import SettingsConfigDict

import sys
sys.path.insert(0, '/app/shared')
from models import PartCreateRequest, PartResponse, PartUpdateRequest
from db import db_settings, FalkorDBClient
from settings import Settings

logger = structlog.get_logger(__name__)

settings = Settings()

app = FastAPI(
    title="SkyMechanics Parts Service",
    description="Parts inventory and catalog management API",
    version="1.0.0",
)

# Health check
@app.get("/")
async def health():
    return {"status": "healthy"}


@app.get("/api/v1/health")
async def api_health():
    return {"status": "healthy", "service": "parts"}


# Parts CRUD endpoints (to be implemented)
# @app.get("/api/v1/parts")
# @app.get("/api/v1/parts/{id}")
# @app.post("/api/v1/parts")
# @app.put("/api/v1/parts/{id}")
# @app.delete("/api/v1/parts/{id}")
# @app.get("/api/v1/parts/{id}/inventory")
# @app.put("/api/v1/parts/{id}/inventory")
