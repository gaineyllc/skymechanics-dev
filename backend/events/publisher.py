"""
Redis Pub/Sub event publisher for Phase 1 WebSocket events.
"""

import asyncio
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


async def publish_event(
    redis,
    event_type: str,
    entity_id: int,
    payload: Dict[str, Any]
):
    """Publish an event to Redis Pub/Sub."""
    channel = f"{event_type}:{entity_id}:updates"
    message = json.dumps({
        "event_type": event_type,
        "payload": payload,
        "timestamp": asyncio.get_event_loop().time()
    })
    
    await redis.publish(channel, message)
    logger.info(f"Published event to {channel}: {message}")


# Helper functions for service modules
async def publish_mechanic_location(
    redis,
    mechanic_id: int,
    latitude: float,
    longitude: float
):
    """Publish mechanic location update."""
    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "timestamp": asyncio.get_event_loop().time()
    }
    await publish_event(redis, "mechanic:location_updated", mechanic_id, payload)


async def publish_job_status_change(
    redis,
    job_id: int,
    old_status: str,
    new_status: str
):
    """Publish job status change."""
    payload = {
        "old_status": old_status,
        "new_status": new_status,
        "timestamp": asyncio.get_event_loop().time()
    }
    await publish_event(redis, "job:status_changed", job_id, payload)


async def publish_job_assigned(
    redis,
    job_id: int,
    mechanic_id: int
):
    """Publish job assignment."""
    payload = {
        "mechanic_id": mechanic_id,
        "timestamp": asyncio.get_event_loop().time()
    }
    await publish_event(redis, "job:assigned", job_id, payload)
