"""
WebSocket event streaming module for Phase 1.

Provides real-time updates via Redis Pub/Sub.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Optional
from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends
from pydantic import BaseModel

from db import get_redis_client
from db import db_settings

logger = logging.getLogger(__name__)
router = APIRouter()

# Active WebSocket connections by event type
active_connections: Dict[str, list] = {
    "mechanic": [],
    "job": [],
    "notification": [],
}


class ConnectionManager:
    """Manages WebSocket connections for event distribution."""
    
    def __init__(self):
        self.active_connections: Dict[str, list] = {}
    
    async def connect(self, websocket: WebSocket, event_type: str):
        await websocket.accept()
        if event_type not in self.active_connections:
            self.active_connections[event_type] = []
        self.active_connections[event_type].append(websocket)
        logger.info(f"Client connected to {event_type} events")
    
    def disconnect(self, websocket: WebSocket, event_type: str):
        if event_type in self.active_connections:
            self.active_connections[event_type].remove(websocket)
        logger.info(f"Client disconnected from {event_type} events")
    
    async def broadcast(self, event_type: str, message: Dict[str, Any]):
        """Broadcast message to all connections of an event type."""
        if event_type not in self.active_connections:
            return
        
        disconnected = []
        for connection in self.active_connections[event_type]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error sending to {event_type} connection: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for client in disconnected:
            self.disconnect(client, event_type)


connection_manager = ConnectionManager()


@router.websocket("/ws/mechanics/{mechanic_id}/updates")
async def mechanic_updates(
    websocket: WebSocket,
    mechanic_id: int,
    redis = Depends(get_redis_client)
):
    """Stream mechanic updates including location, status, availability."""
    await connection_manager.connect(websocket, f"mechanic:{mechanic_id}")
    
    try:
        # Subscribe to Redis channel for this mechanic
        pubsub = redis.pubsub()
        channel = f"mechanic:{mechanic_id}:updates"
        await pubsub.subscribe(channel)
        
        # Send connection confirmation
        await websocket.send_json({
            "type": "connected",
            "event_type": "mechanic",
            "mechanic_id": mechanic_id,
            "timestamp": asyncio.get_event_loop().time()
        })
        
        # Process incoming messages
        while True:
            # Check for incoming commands
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=30.0
                )
                message = json.loads(data)
                
                if message.get("type") == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": asyncio.get_event_loop().time()
                    })
                elif message.get("type") == "subscribe":
                    # Handle client-side subscription requests
                    pass
                    
            except asyncio.TimeoutError:
                # Send keepalive
                await websocket.send_json({
                    "type": "heartbeat",
                    "timestamp": asyncio.get_event_loop().time()
                })
            
            # Check for Redis messages
            try:
                message = await asyncio.wait_for(
                    pubsub.get_message(ignore_subscribe_messages=True),
                    timeout=5.0
                )
                
                if message and message["type"] == "message":
                    data = json.loads(message["data"])
                    await websocket.send_json({
                        "type": "event",
                        "event_type": data.get("event_type"),
                        "payload": data.get("payload"),
                        "timestamp": asyncio.get_event_loop().time()
                    })
                    
            except asyncio.TimeoutError:
                continue
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for mechanic {mechanic_id}")
    except Exception as e:
        logger.error(f"Error in mechanic websocket: {e}")
    finally:
        await pubsub.unsubscribe(channel)
        await pubsub.close()
        connection_manager.disconnect(websocket, f"mechanic:{mechanic_id}")


@router.websocket("/ws/jobs/{job_id}/updates")
async def job_updates(
    websocket: WebSocket,
    job_id: int,
    redis = Depends(get_redis_client)
):
    """Stream job status updates."""
    await connection_manager.connect(websocket, f"job:{job_id}")
    
    try:
        pubsub = redis.pubsub()
        channel = f"job:{job_id}:updates"
        await pubsub.subscribe(channel)
        
        await websocket.send_json({
            "type": "connected",
            "event_type": "job",
            "job_id": job_id,
            "timestamp": asyncio.get_event_loop().time()
        })
        
        while True:
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=30.0
                )
                message = json.loads(data)
                
                if message.get("type") == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": asyncio.get_event_loop().time()
                    })
                    
            except asyncio.TimeoutError:
                await websocket.send_json({
                    "type": "heartbeat",
                    "timestamp": asyncio.get_event_loop().time()
                })
            
            try:
                message = await asyncio.wait_for(
                    pubsub.get_message(ignore_subscribe_messages=True),
                    timeout=5.0
                )
                
                if message and message["type"] == "message":
                    data = json.loads(message["data"])
                    await websocket.send_json({
                        "type": "event",
                        "event_type": data.get("event_type"),
                        "payload": data.get("payload"),
                        "timestamp": asyncio.get_event_loop().time()
                    })
                    
            except asyncio.TimeoutError:
                continue
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for job {job_id}")
    except Exception as e:
        logger.error(f"Error in job websocket: {e}")
    finally:
        await pubsub.unsubscribe(channel)
        await pubsub.close()
        connection_manager.disconnect(websocket, f"job:{job_id}")


@router.websocket("/ws/notifications")
async def notifications(websocket: WebSocket):
    """Global notifications stream."""
    await connection_manager.connect(websocket, "notification")
    
    try:
        await websocket.send_json({
            "type": "connected",
            "event_type": "notification",
            "timestamp": asyncio.get_event_loop().time()
        })
        
        while True:
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=60.0
                )
                message = json.loads(data)
                
                if message.get("type") == "ping":
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": asyncio.get_event_loop().time()
                    })
                    
            except asyncio.TimeoutError:
                await websocket.send_json({
                    "type": "heartbeat",
                    "timestamp": asyncio.get_event_loop().time()
                })
                
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected for notifications")
    except Exception as e:
        logger.error(f"Error in notification websocket: {e}")
    finally:
        connection_manager.disconnect(websocket, "notification")


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
def get_router() -> APIRouter:
    """Get the events router."""
    return router
