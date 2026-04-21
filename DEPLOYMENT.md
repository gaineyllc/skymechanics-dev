# SkyMechanics Platform - Deployment Status

## Phase 1 Complete ✅
### Port Policy Fixed

All services now use ports **8200+** to avoid conflicts with vLLM (port 8000).

## Phase 2 Complete ✅
### Real-Time & WebSocket Gateway

| Component | Port | Status |
|-----------|------|--------|
| Gateway Service | 8204 | Built |

**Features:**
- Real-time event broadcasting via WebSocket
- Mechanic location updates
- Job status notifications
- Global alerts
- Heartbeat health checks

**Endpoints:**
- `/ws/health` - Basic health check
- `/ws/mechanics/{id}/updates` - Mechanic-specific updates
- `/ws/jobs/{id}/updates` - Job-specific status changes
- `/ws/global/notifications` - System-wide alerts

## Phase 3 Complete ✅
### Analytics & Reporting Infrastructure

- HPA configs (2-10 replicas per service)
- Network policies for tenant isolation
- RBAC with minimal permissions
- Helm chart documentation
- Kubernetes Dashboard ready

## Phase 3 Complete ✅
### Analytics & Reporting Infrastructure

| Component | Port | Status |
|-----------|------|--------|
| Auth Service | 8200 | Built |
| Mechanics Service | 8201 | Built |
| Jobs Service | 8202 | Built |
| Analytics Service | 8203 | Built |
| Gateway Service | 8204 | Built |
| Aircraft Service | 8208 | Built |
| Parts Service | 8205 | Built |
| Notification Service | 8206 | Built |
| Invoice Service | 8207 | Built |
| ClickHouse | 9000/8123 | Ready |

**Docker Images Built:**
- `ghcr.io/gaineyllc/auth-service:latest`
- `ghcr.io/gaineyllc/mechanics-service:latest`
- `ghcr.io/gaineyllc/jobs-service:latest`
- `ghcr.io/gaineyllc/analytics-service:latest`
- `ghcr.io/gaineyllc/gateway-service:latest`
- `ghcr.io/gaineyllc/aircraft-service:latest`
- `ghcr.io/gaineyllc/parts-service:latest`
- `ghcr.io/gaineyllc/notification-service:latest`
- `ghcr.io/gaineyllc/invoice-service:latest`

**To push all images:**
```bash
docker login ghcr.io -u gaineyllc
docker push ghcr.io/gaineyllc/auth-service:latest
docker push ghcr.io/gaineyllc/mechanics-service:latest
docker push ghcr.io/gaineyllc/jobs-service:latest
docker push ghcr.io/gaineyllc/analytics-service:latest
docker push ghcr.io/gaineyllc/gateway-service:latest
docker push ghcr.io/gaineyllc/aircraft-service:latest
docker push ghcr.io/gaineyllc/parts-service:latest
docker push ghcr.io/gaineyllc/notification-service:latest
docker push ghcr.io/gaineyllc/invoice-service:latest
```

## Phase 4 Complete ✅
### Mobile App (React Native)

**Project Location:** `mobile/`

**Features:**
- Login/Registration screens
- Dashboard with metrics
- Job list and details
- Mechanic directory
- Profile management
- Auth context with token persistence

**To Run:**
```bash
cd mobile
npm install
npx pod-install ios
npm run android  # or npm run ios
```

## Services Configuration

| Service | Port | Status |
|---------|------|--------|
| auth-service | 8200 | Built |
| mechanics-service | 8201 | Built |
| jobs-service | 8202 | Built |
| analytics-service | 8203 | Built |
| gateway-service | 8204 | Built |
| aircraft-service | 8208 | Built |
| parts-service | 8205 | Built |
| notification-service | 8206 | Built |
| invoice-service | 8207 | Built |
| skymechanics-falkordb | 6379 | Healthy |
| skymechanics-redis | 6379 | Running |
| clickhouse | 9000/8123 | Ready |

## Mobile App

**Project Location:** `mobile/`

**To Run:**
```bash
cd mobile
npm install
npx pod-install ios
npm run android  # or npm run ios
```

**Features:**
- Login/Registration screens
- Dashboard with metrics
- Job list and details
- Mechanic directory
- Profile management
- Auth context with token persistence

## WebSocket Client (Mobile)

```typescript
// Example: Subscribe to mechanic updates
class WebSocketClient {
  connect(endpoint: string, onMessage: (data: any) => void) {
    const ws = new WebSocket(`ws://${endpoint}`);
    ws.onmessage = (event) => onMessage(JSON.parse(event.data));
    return ws;
  }

  subscribeToMechanic(mechanicId: number, callback: (data: any) => void) {
    return this.connect(`localhost:8204/ws/mechanics/${mechanicId}/updates`, callback);
  }
}
```

## API Endpoints

### Auth Service
- **Health Check**: http://localhost:8200/api/v1/health
- **Swagger UI**: http://localhost:8200/docs
- **WebSocket**: ws://localhost:8200/api/v1/events/ws/mechanics/{id}/updates

### Mechanics Service
- **Health Check**: http://localhost:8201/api/v1/health
- **Swagger UI**: http://localhost:8201/docs

### Jobs Service
- **Health Check**: http://localhost:8202/api/v1/health
- **Swagger UI**: http://localhost:8202/docs

### Analytics Service
- **Health Check**: http://localhost:8203/api/v1/health
- **Swagger UI**: http://localhost:8203/docs
- **Fleet Metrics**: /api/v1/metrics/fleet
- **Mechanic Metrics**: /api/v1/metrics/mechanics
- **Revenue Metrics**: /api/v1/metrics/revenue

### Gateway Service (WebSocket)
- **Health Check**: http://localhost:8204/health
- **WebSocket**: ws://localhost:8204/ws
- **Mechanic Updates**: ws://localhost:8204/ws/mechanics/{id}/updates
- **Job Updates**: ws://localhost:8204/ws/jobs/{id}/updates
- **Global Notifications**: ws://localhost:8204/ws/global/notifications

## Ports Used

| Range | Purpose | Status |
|-------|---------|--------|
| 8000 | vLLM (Qwen3-Coder-Next-FP8) | Reserved |
| 8200 | auth-service | Active |
| 8201 | mechanics-service | Active |
| 8202 | jobs-service | Active |
| 8203 | analytics-service | Active |
| 8204 | gateway-service | Active |
| 8205 | parts-service | Built |
| 8206 | notification-service | Built |
| 8207 | invoice-service | Built |
| 8208 | aircraft-service | Built |
| 3000-3099 | Frontend services | React (3003) |
| 5432 | PostgreSQL | Auth service |
| 6379 | FalkorDB/Redis | Active |
| 6380 | Redis Stack (RedisInsight) | Active |
| 9000/8123 | ClickHouse | Active |
| 9090-9199 | Monitoring | Prometheus (9090), AlertManager (9093) |
| 30000-32767 | Kubernetes NodePort | Not used |

## Running Locally

### Start all services
```bash
# Terminal 1: Start auth service
cd services/auth-service && uvicorn main:app --host 0.0.0.0 --port 8200

# Terminal 2: Start mechanics service
cd services/mechanics-service && uvicorn main:app --host 0.0.0.0 --port 8201

# Terminal 3: Start jobs service
cd services/jobs-service && uvicorn main:app --host 0.0.0.0 --port 8202

# Terminal 4: Start analytics service
cd services/analytics-service && uvicorn main:app --host 0.0.0.0 --port 8203

# Terminal 5: Start gateway service
cd services/gateway-service && uvicorn main:app --host 0.0.0.0 --port 8204

# Terminal 6: Start aircraft service
cd services/aircraft-service && uvicorn main:app --host 0.0.0.0 --port 8208

# Terminal 7: Start parts service
cd services/parts-service && uvicorn main:app --host 0.0.0.0 --port 8205

# Terminal 8: Start notification service
cd services/notification-service && uvicorn main:app --host 0.0.0.0 --port 8206

# Terminal 9: Start invoice service
cd services/invoice-service && uvicorn main:app --host 0.0.0.0 --port 8207
```

### Start with Docker
```bash
# Redis
docker run -d -p 6379:6379 --name redis redis:7-alpine

# FalkorDB
docker run -d -p 6379:6379 -p 3000:3000 --name falkordb falkordb/falkordb:latest

# Using Docker Compose (recommended)
cd /path/to/skymechanics-dev
docker-compose up -d

# Or build and run specific services
docker-compose build auth-service mechanics-service jobs-service analytics-service gateway-service
docker-compose up -d auth-service mechanics-service jobs-service analytics-service gateway-service

## Running All Services with Docker Compose

**Start all services (including new services):**
```bash
cd /path/to/skymechanics-dev
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f
```

**Stop all services:**
```bash
docker-compose down
```

**Stop and remove volumes:**
```bash
docker-compose down -v
```

**Services available:**
| Service | Port | Status |
|---------|------|--------|
| auth-service | 8200 | Built |
| mechanics-service | 8201 | Built |
| jobs-service | 8202 | Built |
| analytics-service | 8203 | Built |
| gateway-service | 8204 | Built |
| aircraft-service | 8208 | Built |
| parts-service | 8205 | Built |
| notification-service | 8206 | Built |
| invoice-service | 8207 | Built |

## Mobile App

**Project Location:** `mobile/`

**To Run:**
```bash
cd mobile
npm install
npx pod-install ios
npm run android  # or npm run ios
```

**Features:**
- Login/Registration screens
- Dashboard with metrics
- Job list and details
- Mechanic directory
- Profile management
- Auth context with token persistence
