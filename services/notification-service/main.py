"""
SkyMechanics Notification Service
Exposes notification delivery and scheduling endpoints.
"""
import structlog
from fastapi import FastAPI
from pydantic_settings import SettingsConfigDict

import sys
sys.path.insert(0, '/app/shared')
from models import NotificationCreateRequest, NotificationResponse, NotificationUpdateRequest
from db import db_settings, FalkorDBClient
from settings import Settings

logger = structlog.get_logger(__name__)

settings = Settings()

app = FastAPI(
    title="SkyMechanics Notification Service",
    description="Notification delivery and scheduling API",
    version="1.0.0",
)

# Health check
@app.get("/")
async def health():
    return {"status": "healthy"}


@app.get("/api/v1/health")
async def api_health():
    return {"status": "healthy", "service": "notification"}


# Notification endpoints (to be implemented)
# @app.get("/api/v1/notifications")
# @app.post("/api/v1/notifications/send")
# @app.post("/api/v1/notifications/config")
# @app.get("/api/v1/notifications/user/{user_id}")
# @app.delete("/api/v1/notifications/{id}")
