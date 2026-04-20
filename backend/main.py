"""
FastAPI application for SkyMechanics Platform.
Provides REST API endpoints for graph database operations.
"""
import structlog
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from db import db_client
from models import (
    GraphQueryRequest,
    MultiTenantCreateRequest,
    MultiTenantQueryRequest,
    EntityCreateRequest,
    RelationshipCreateRequest,
    CustomerCreateRequest,
    JobCreateRequest,
    JobUpdateRequest,
    JobStatusRequest,
    MechanicCreateRequest,
    SuccessResponse,
    ErrorResponse
)
from settings import settings
from routes import onboarding as onboarding_router
from routes import users as users_router
from routes import jobs as jobs_router
from routes import mechanics as mechanics_router

# Configure structlog
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

app = FastAPI(
    title="SkyMechanics Platform API",
    description="Graph database API for multi-tenant job management",
    version="0.1.0"
)

# Use settings for vLLM URL
VLLM_URL = settings.vllm_url


@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup."""
    try:
        db_client.connect()
        print("✅ Connected to FalkorDB")
    except Exception as e:
        print(f"❌ Failed to connect to FalkorDB: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown."""
    db_client.close()
    print("👋 Closed FalkorDB connection")


# ========== Exception Handlers ==========

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            success=False,
            error="Validation Error",
            details=str(exc.errors())
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handle unexpected errors."""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            success=False,
            error="Internal Server Error",
            details=str(exc)
        ).model_dump()
    )


# ========== Health Check ==========

@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint."""
    try:
        db_client._client.ping()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": f"disconnected: {str(e)}"}


# ========== Root Endpoint ==========

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "SkyMechanics Platform API",
        "version": "0.1.0",
        "description": "Multi-tenant graph database API for job management",
        "endpoints": {
            "health": "/health",
            "jobs": "/api/v1/jobs",
            "users": "/api/v1/users",
            "onboarding": "/api/v1/onboard"
        }
    }


# Include routers
app.include_router(onboarding_router.router)
app.include_router(users_router.router)
app.include_router(jobs_router.router)
app.include_router(mechanics_router.router)
