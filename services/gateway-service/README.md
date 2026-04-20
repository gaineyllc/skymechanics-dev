# SkyMechanics Gateway Service

WebSocket gateway for real-time event streaming.

## Ports
- **8204**: Gateway service (WebSocket)

## Docker Build
```bash
docker build -t ghcr.io/gaineyllc/gateway-service:latest -f services/gateway-service/Dockerfile .
```

## Docker Run
```bash
docker run -d -p 8204:8204 \
  --env PORT=8204 \
  ghcr.io/gaineyllc/gateway-service:latest
```

## WebSocket Endpoints

| Endpoint | Purpose | Events |
|----------|---------|--------|
| `/ws/health` | Health check | ping |
| `/ws/mechanics/{id}/updates` | Mechanic updates | location, status, availability |
| `/ws/jobs/{id}/updates` | Job updates | status, assignment, completion |
| `/ws/global/notifications` | Global alerts | system-wide notifications |

## Event Types

### Mechanic Events
```json
{
  "type": "location_updated",
  "mechanic_id": 123,
  "latitude": 40.7128,
  "longitude": -74.0060,
  "timestamp": "2026-04-20T16:00:00Z"
}
```

### Job Events
```json
{
  "type": "status_changed",
  "job_id": "job-123",
  "status": "in_progress",
  "assigned_mechanic": 123,
  "timestamp": "2026-04-20T16:00:00Z"
}
```

### Heartbeat
```json
{
  "type": "heartbeat_ack",
  "timestamp": "2026-04-20T16:00:00Z"
}
```

## Client Example (React Native)

```typescript
class WebSocketClient {
  private connections = new Map<string, WebSocket>();

  connect(endpoint: string, onMessage: (data: any) => void) {
    const ws = new WebSocket(`ws://${endpoint}`);
    ws.onmessage = (event) => onMessage(JSON.parse(event.data));
    this.connections.set(endpoint, ws);
    return ws;
  }

  subscribeToMechanic(mechanicId: number, callback: (data: any) => void) {
    return this.connect(`localhost:8204/ws/mechanics/${mechanicId}/updates`, callback);
  }

  subscribeToJob(jobId: string, callback: (data: any) => void) {
    return this.connect(`localhost:8204/ws/jobs/${jobId}/updates`, callback);
  }

  subscribeToNotifications(callback: (data: any) => void) {
    return this.connect(`localhost:8204/ws/global/notifications`, callback);
  }

  sendHeartbeat(ws: WebSocket) {
    ws.send(JSON.stringify({ type: 'heartbeat' }));
  }
}
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8204 | Gateway port |
| `REDIS_HOST` | redis | Redis hostname for Pub/Sub |
| `REDIS_PORT` | 6379 | Redis port |

## Integration with Redis

The gateway can forward events to Redis Pub/Sub for distributed systems:

```python
# Publish to Redis channel
await redis.publish("mechanic:123", json.dumps(event))
```
