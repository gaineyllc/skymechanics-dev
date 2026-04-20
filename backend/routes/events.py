"""
Events router for Phase 1 WebSocket streaming.
"""

from fastapi import APIRouter

from events.websocket import router as websocket_router
from events.publisher import publish_event

router = APIRouter(prefix="/events", tags=["events"])

# Include WebSocket endpoints
router.include_router(websocket_router)
