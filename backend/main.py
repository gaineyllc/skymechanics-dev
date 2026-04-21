"""
Application entry point and FastAPI setup.
Handles lifespan, logging, and API route registration.
"""
import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from typing import AsyncIterator

# Initialize structlog
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.render_to_log_kwargs,
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Import routes before creating app
from routes import (
    health as health_router,
    customers as customers_router,
    jobs as jobs_router,
    mechanics as mechanics_router,
    onboarding as onboarding_router,
    users as users_router,
    events as events_router,
    procedures as procedures_router,
    tenants as tenants_router,
    auth as auth_router,
)

# Import models for Alembic autogenerate support
import models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Application lifespan manager for startup/shutdown events."""
    logger.info("Starting SkyMechanics backend service")
    
    # Startup
    logger.info("Initializing database connection")
    try:
        from db import db_client
        db_client.connect()
        logger.info("Database connection established")
    except Exception as e:
        logger.warning("Database connection failed", error=str(e))
    
    yield
    
    # Shutdown
    logger.info("Shutting down SkyMechanics backend service")


app = FastAPI(
    title="SkyMechanics API",
    description="A repair shop management system with graph database capabilities",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router.router, prefix="/api/v1", tags=["health"])
app.include_router(onboarding_router.router, prefix="/api/v1", tags=["onboarding"])
app.include_router(users_router.router, prefix="/api/v1", tags=["users"])
app.include_router(customers_router.router, prefix="/api/v1", tags=["customers"])
app.include_router(mechanics_router.router, prefix="/api/v1", tags=["mechanics"])
app.include_router(jobs_router.router, prefix="/api/v1", tags=["jobs"])
app.include_router(events_router.router, prefix="/api/v1", tags=["events"])
app.include_router(procedures_router.router, prefix="/api/v1", tags=["procedures"])
app.include_router(tenants_router.router, prefix="/api/v1", tags=["tenants"])
app.include_router(auth_router.router, prefix="/api/v1", tags=["auth"])


if __name__ == "__main__":
    import uvicorn
    import os
    # PORT POLICY: Use 8200+ to avoid vLLM conflict on port 8000
    port = int(os.environ.get("PORT", 8200))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
