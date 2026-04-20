"""WebSocket gateway for SkyMechanics - Real-time event streaming"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import asyncio
import json
from typing import Dict, Set

app = FastAPI(
    title="SkyMechanics WebSocket Gateway",
    description="Real-time event streaming for mechanics and jobs",
    version="0.1.0"
)

# Active WebSocket connections by channel
active_connections: Dict[str, Set[WebSocket]] = {}


@app.get("/health", summary="Health Check")
async def health():
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "channels": len(active_connections),
        "connections": sum(len(conns) for conns in active_connections.values()),
        "timestamp": "2026-04-20T16:00:00Z"
    }


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with API documentation link."""
    return """
    <html>
        <head>
            <title>SkyMechanics WebSocket Gateway</title>
        </head>
        <body>
            <h1>SkyMechanics WebSocket Gateway</h1>
            <p>Version: 0.1.0</p>
            <p><a href="/docs">API Documentation</a></p>
            <p>Connect to WebSocket endpoints to receive real-time updates.</p>
        </body>
    </html>
    """


@app.websocket("/ws/health")
async def health_check(websocket: WebSocket):
    """Basic WebSocket health check."""
    await websocket.accept()
    try:
        while True:
            await asyncio.sleep(30)
            await websocket.send_text(json.dumps({"type": "ping", "timestamp": "2026-04-20T16:00:00Z"}))
    except WebSocketDisconnect:
        pass


@app.websocket("/ws/mechanics/{mechanic_id}/updates")
async def mechanic_updates(websocket: WebSocket, mechanic_id: int):
    """Subscribe to mechanic-specific updates."""
    await websocket.accept()
    channel = f"mechanic:{mechanic_id}"
    
    # Add connection to channel
    if channel not in active_connections:
        active_connections[channel] = set()
    active_connections[channel].add(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "subscribe":
                # Already subscribed
                pass
            elif message.get("type") == "heartbeat":
                await websocket.send_text(json.dumps({
                    "type": "heartbeat_ack",
                    "timestamp": "2026-04-20T16:00:00Z"
                }))
    except WebSocketDisconnect:
        # Remove connection from channel
        if channel in active_connections:
            active_connections[channel].discard(websocket)
            if not active_connections[channel]:
                del active_connections[channel]


@app.websocket("/ws/jobs/{job_id}/updates")
async def job_updates(websocket: WebSocket, job_id: str):
    """Subscribe to job-specific status updates."""
    await websocket.accept()
    channel = f"job:{job_id}"
    
    if channel not in active_connections:
        active_connections[channel] = set()
    active_connections[channel].add(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "heartbeat":
                await websocket.send_text(json.dumps({
                    "type": "heartbeat_ack",
                    "timestamp": "2026-04-20T16:00:00Z"
                }))
    except WebSocketDisconnect:
        if channel in active_connections:
            active_connections[channel].discard(websocket)
            if not active_connections[channel]:
                del active_connections[channel]


@app.websocket("/ws/global/notifications")
async def global_notifications(websocket: WebSocket):
    """Subscribe to global notifications."""
    await websocket.accept()
    channel = "global:notifications"
    
    if channel not in active_connections:
        active_connections[channel] = set()
    active_connections[channel].add(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "heartbeat":
                await websocket.send_text(json.dumps({
                    "type": "heartbeat_ack",
                    "timestamp": "2026-04-20T16:00:00Z"
                }))
    except WebSocketDisconnect:
        if channel in active_connections:
            active_connections[channel].discard(websocket)
            if not active_connections[channel]:
                del active_connections[channel]


async def broadcast_to_channel(channel: str, message: dict):
    """Broadcast message to all connections in a channel."""
    if channel in active_connections:
        message_json = json.dumps(message)
        for websocket in list(active_connections[channel]):
            try:
                await websocket.send_text(message_json)
            except Exception:
                # Remove disconnected clients
                active_connections[channel].discard(websocket)


async def broadcast_to_all(message: dict):
    """Broadcast message to all connected clients."""
    message_json = json.dumps(message)
    for channel, connections in active_connections.items():
        for websocket in list(connections):
            try:
                await websocket.send_text(message_json)
            except Exception:
                connections.discard(websocket)
