"""
Redis Pub/Sub module for real-time updates.
"""
from typing import Callable, Optional
import asyncio
import json

from db import get_redis_pubsub


class PubSubManager:
    """Redis Pub/Sub manager for real-time updates."""
    
    def __init__(self):
        self._client = None
        self._pubsub = None
        self._handlers = {}
        self._running = False
    
    async def connect(self):
        """Connect to Redis Pub/Sub."""
        self._client = get_redis_pubsub()
        self._pubsub = self._client.pubsub()
        return self
    
    async def subscribe(self, channel: str, handler: Callable):
        """Subscribe to a channel with a handler function."""
        self._handlers[channel] = handler
        await self._pubsub.subscribe(channel)
    
    async def unsubscribe(self, channel: str):
        """Unsubscribe from a channel."""
        if channel in self._handlers:
            del self._handlers[channel]
        await self._pubsub.unsubscribe(channel)
    
    async def publish(self, channel: str, message: dict):
        """Publish a message to a channel."""
        await self._client.publish(channel, json.dumps(message))
    
    async def run(self):
        """Run the Pub/Sub listener."""
        self._running = True
        try:
            async for message in self._pubsub.listen():
                if message["type"] == "message":
                    channel = message["channel"]
                    data = json.loads(message["data"])
                    
                    if channel in self._handlers:
                        await self._handlers[channel](data)
        except asyncio.CancelledError:
            pass
        finally:
            self._running = False
    
    async def close(self):
        """Close the Pub/Sub connection."""
        self._running = False
        if self._pubsub:
            await self._pubsub.close()
        if self._client:
            await self._client.close()


# Global Pub/Sub manager instance
pubsub_manager = PubSubManager()


# Pub/Sub channel definitions
class Channels:
    """Redis Pub/Sub channel names."""
    
    # Tenant channels
    TENANT_CREATE = "tenant:create"
    TENANT_DELETE = "tenant:delete"
    
    # Mechanic channels
    MECHANIC_CREATE = "mechanic:create"
    MECHANIC_UPDATE = "mechanic:update"
    MECHANIC_DELETE = "mechanic:delete"
    
    # Job channels
    JOB_CREATE = "job:create"
    JOB_UPDATE = "job:update"
    JOB_COMPLETE = "job:complete"
    JOB_ASSIGN = "job:assign"
    
    # Customer channels
    CUSTOMER_CREATE = "customer:create"
    CUSTOMER_UPDATE = "customer:update"
    
    # Reputation channels
    REPUTATION_UPDATE = "reputation:update"
    
    # Procedure channels
    PROCEDURE_CREATE = "procedure:create"
    PROCEDURE_UPDATE = "procedure:update"
    
    # All channels for a tenant
    TENANT_ALL = "tenant:{tenant_id}:all"


# Helper functions for publishing events
async def publish_tenant_created(tenant_id: str, tenant_name: str):
    """Publish tenant created event."""
    await pubsub_manager.publish(
        Channels.TENANT_CREATE,
        {"tenant_id": tenant_id, "tenant_name": tenant_name}
    )
    await pubsub_manager.publish(
        f"{Channels.TENANT_ALL.format(tenant_id=tenant_id)}",
        {"event": "tenant_created", "tenant_id": tenant_id}
    )


async def publish_mechanic_updated(mechanic_id: int, tenant_id: str):
    """Publish mechanic updated event."""
    await pubsub_manager.publish(
        Channels.MECHANIC_UPDATE,
        {"mechanic_id": mechanic_id, "tenant_id": tenant_id}
    )
    await pubsub_manager.publish(
        f"{Channels.TENANT_ALL.format(tenant_id=tenant_id)}",
        {"event": "mechanic_updated", "mechanic_id": mechanic_id}
    )


async def publish_job_status_changed(job_id: int, tenant_id: str, status: str):
    """Publish job status changed event."""
    await pubsub_manager.publish(
        Channels.JOB_UPDATE,
        {"job_id": job_id, "tenant_id": tenant_id, "status": status}
    )
    await pubsub_manager.publish(
        f"{Channels.TENANT_ALL.format(tenant_id=tenant_id)}",
        {"event": "job_status_changed", "job_id": job_id, "status": status}
    )


async def publish_reputation_updated(mechanic_id: int, tenant_id: str):
    """Publish reputation updated event."""
    await pubsub_manager.publish(
        Channels.REPUTATION_UPDATE,
        {"mechanic_id": mechanic_id, "tenant_id": tenant_id}
    )
