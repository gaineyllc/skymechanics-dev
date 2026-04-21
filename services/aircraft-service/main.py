"""
SkyMechanics Aircraft Service
Exposes aircraft CRUD endpoints and airworthiness management.
"""
import structlog
from fastapi import FastAPI
from pydantic_settings import SettingsConfigDict

import sys
sys.path.insert(0, '/app/shared')
from models import AircraftCreateRequest, AircraftResponse, AircraftUpdateRequest
from db import db_settings, FalkorDBClient
from settings import Settings

logger = structlog.get_logger(__name__)

settings = Settings()

app = FastAPI(
    title="SkyMechanics Aircraft Service",
    description="Aircraft and airworthiness management API",
    version="1.0.0",
)

# Health check
@app.get("/")
async def health():
    return {"status": "healthy"}


@app.get("/api/v1/health")
async def api_health():
    return {"status": "healthy", "service": "aircraft"}


# Aircraft CRUD endpoints (to be implemented)
# @app.get("/api/v1/aircraft")
# @app.get("/api/v1/aircraft/{id}")
# @app.post("/api/v1/aircraft")
# @app.put("/api/v1/aircraft/{id}")
# @app.delete("/api/v1/aircraft/{id}")
# @app.get("/api/v1/aircraft/{id}/airworthiness")
# @app.post("/api/v1/aircraft/{id}/airworthiness")
# @app.get("/api/v1/aircraft/{id}/jobs")
