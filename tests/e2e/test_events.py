"""
Phase 1 End-to-End Tests: WebSocket Events & Redis Pub/Sub

Tests the following:
1. WebSocket connections for mechanics and jobs
2. Event publishing to Redis Pub/Sub
3. Real-time updates via WebSocket
4. Multiple concurrent connections
"""
import pytest
import asyncio
import json
import websockets
from redis.asyncio import Redis


@pytest.mark.asyncio
async def test_websocket_mechanic_connection():
    """Test WebSocket connection for mechanic updates."""
    async with websockets.connect("ws://localhost:8000/api/v1/events/ws/mechanics/1/updates") as ws:
        # Receive connection confirmation
        response = await asyncio.wait_for(ws.recv(), timeout=5.0)
        message = json.loads(response)
        
        assert message["type"] == "connected"
        assert message["event_type"] == "mechanic"
        assert message["mechanic_id"] == 1


@pytest.mark.asyncio
async def test_websocket_job_connection():
    """Test WebSocket connection for job updates."""
    async with websockets.connect("ws://localhost:8000/api/v1/events/ws/jobs/1/updates") as ws:
        # Receive connection confirmation
        response = await asyncio.wait_for(ws.recv(), timeout=5.0)
        message = json.loads(response)
        
        assert message["type"] == "connected"
        assert message["event_type"] == "job"
        assert message["job_id"] == 1


@pytest.mark.asyncio
async def test_websocket_notification_connection():
    """Test WebSocket connection for global notifications."""
    async with websockets.connect("ws://localhost:8000/api/v1/events/ws/notifications") as ws:
        # Receive connection confirmation
        response = await asyncio.wait_for(ws.recv(), timeout=5.0)
        message = json.loads(response)
        
        assert message["type"] == "connected"
        assert message["event_type"] == "notification"


@pytest.mark.asyncio
async def test_redis_pubsub_publish():
    """Test publishing events to Redis Pub/Sub."""
    redis = Redis(host="localhost", port=6379, decode_responses=True)
    
    # Subscribe to a test channel
    pubsub = redis.pubsub()
    await pubsub.subscribe("test:channel")
    
    # Publish a message
    await redis.publish("test:channel", json.dumps({"test": "message"}))
    
    # Receive the message
    message = await asyncio.wait_for(pubsub.get_message(), timeout=5.0)
    
    assert message["type"] == "message"
    assert message["channel"] == "test:channel"
    data = json.loads(message["data"])
    assert data["test"] == "message"
    
    await pubsub.unsubscribe("test:channel")
    await redis.close()


@pytest.mark.asyncio
async def test_mechanic_location_event():
    """Test publishing mechanic location events."""
    redis = Redis(host="localhost", port=6379, decode_responses=True)
    
    # Subscribe to mechanic location updates
    pubsub = redis.pubsub()
    await pubsub.subscribe("mechanic:location_updated:1:updates")
    
    # Import the publisher
    from events.publisher import publish_mechanic_location
    
    # Publish a location event
    await publish_mechanic_location(
        redis=redis,
        mechanic_id=1,
        latitude=37.7749,
        longitude=-122.4194
    )
    
    # Receive the message
    message = await asyncio.wait_for(pubsub.get_message(), timeout=5.0)
    
    assert message["type"] == "message"
    data = json.loads(message["data"])
    assert data["event_type"] == "mechanic:location_updated"
    assert data["payload"]["latitude"] == 37.7749
    assert data["payload"]["longitude"] == -122.4194
    
    await pubsub.unsubscribe("mechanic:location_updated:1:updates")
    await redis.close()


@pytest.mark.asyncio
async def test_multiple_concurrent_connections():
    """Test multiple WebSocket connections for the same mechanic."""
    connections = []
    
    try:
        # Create 3 concurrent connections
        for i in range(3):
            ws = await websockets.connect(
                "ws://localhost:8000/api/v1/events/ws/mechanics/1/updates"
            )
            connections.append(ws)
        
        # Verify all connections received confirmation
        for i, ws in enumerate(connections):
            response = await asyncio.wait_for(ws.recv(), timeout=5.0)
            message = json.loads(response)
            assert message["type"] == "connected"
    finally:
        # Clean up connections
        for ws in connections:
            await ws.close()


@pytest.mark.asyncio
async def test_heartbeat_mechanism():
    """Test WebSocket heartbeat mechanism."""
    async with websockets.connect("ws://localhost:8000/api/v1/events/ws/mechanics/1/updates") as ws:
        # Send a ping
        await ws.send(json.dumps({"type": "ping"}))
        
        # Expect pong response
        response = await asyncio.wait_for(ws.recv(), timeout=5.0)
        message = json.loads(response)
        
        assert message["type"] == "pong"


@pytest.mark.asyncio
async def test_job_status_change_event():
    """Test publishing job status change events."""
    redis = Redis(host="localhost", port=6379, decode_responses=True)
    
    # Subscribe to job status updates
    pubsub = redis.pubsub()
    await pubsub.subscribe("job:status_changed:1:updates")
    
    # Import the publisher
    from events.publisher import publish_job_status_change
    
    # Publish a status change event
    await publish_job_status_change(
        redis=redis,
        job_id=1,
        old_status="pending",
        new_status="open"
    )
    
    # Receive the message
    message = await asyncio.wait_for(pubsub.get_message(), timeout=5.0)
    
    assert message["type"] == "message"
    data = json.loads(message["data"])
    assert data["event_type"] == "job:status_changed"
    assert data["payload"]["old_status"] == "pending"
    assert data["payload"]["new_status"] == "open"
    
    await pubsub.unsubscribe("job:status_changed:1:updates")
    await redis.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"])
