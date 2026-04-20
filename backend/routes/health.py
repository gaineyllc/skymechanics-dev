from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


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
