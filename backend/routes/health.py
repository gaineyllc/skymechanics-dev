from fastapi import APIRouter
from db import db_client

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    status = "healthy"
    try:
        # Try to connect to get db status
        db_client.connect()
        db_status = "connected"
        db_client.close()
    except Exception as e:
        db_status = f"error: {str(e)}"
        status = "degraded"
    
    return {
        "status": status,
        "database": db_status,
        "timestamp": "2026-04-20T15:00:00Z"
    }


@router.get("/api/v1/health")
async def api_health_check():
    """API health check endpoint."""
    return {"status": "healthy", "api": "v1"}


@router.get("/ready")
async def ready_check():
    """Readiness check endpoint."""
    return {"status": "ready"}


@router.get("/api/v1/ready")
async def api_ready_check():
    """API readiness check endpoint."""
    return {"status": "ready", "api": "v1"}
