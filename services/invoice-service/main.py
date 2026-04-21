"""
SkyMechanics Invoice Service
Exposes billing, invoicing, and export endpoints.
"""
import structlog
from fastapi import FastAPI
from pydantic_settings import SettingsConfigDict

from .settings import Settings

logger = structlog.get_logger(__name__)

settings = Settings()

app = FastAPI(
    title="SkyMechanics Invoice Service",
    description="Billing and invoicing API",
    version="1.0.0",
)

# Health check
@app.get("/")
async def health():
    return {"status": "healthy"}


@app.get("/api/v1/health")
async def api_health():
    return {"status": "healthy", "service": "invoice"}


# Invoice endpoints (to be implemented)
# @app.get("/api/v1/invoices")
# @app.post("/api/v1/invoices/generate")
# @app.get("/api/v1/invoices/{id}")
# @app.delete("/api/v1/invoices/{id}")
# @app.post("/api/v1/invoices/{id}/export/csv")
# @app.post("/api/v1/invoices/{id}/export/pdf")
