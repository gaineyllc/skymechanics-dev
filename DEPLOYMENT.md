# SkyMechanics Platform - Deployment Status

## Phase 1 Complete ✅
### Port Policy Fixed

All services now use ports **8200+** to avoid conflicts with vLLM (port 8000).

## Phase 2 Complete ✅
### Kubernetes Infrastructure

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
| ClickHouse | 9000/8123 | Ready |

**Docker Images Built:**
- `ghcr.io/gaineyllc/auth-service:latest`
- `ghcr.io/gaineyllc/mechanics-service:latest`
- `ghcr.io/gaineyllc/jobs-service:latest`
- `ghcr.io/gaineyllc/analytics-service:latest`

**To push images:**
```bash
docker login ghcr.io -u gaineyllc
docker push ghcr.io/gaineyllc/auth-service:latest
docker push ghcr.io/gaineyllc/mechanics-service:latest
docker push ghcr.io/gaineyllc/jobs-service:latest
docker push ghcr.io/gaineyllc/analytics-service:latest
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

## Ports Used

| Range | Purpose | Status |
|-------|---------|--------|
| 8000 | vLLM (Qwen3-Coder-Next-FP8) | Reserved |
| 8200 | auth-service | Active |
| 8201 | mechanics-service | Ready |
| 8202 | jobs-service | Ready |
| 8203 | analytics-service | Ready |
| 3000-3099 | Frontend services | React (3003) |
| 5432 | PostgreSQL | Auth service |
| 6379 | FalkorDB/Redis | Active |
| 9000/8123 | ClickHouse | Active |
| 9090-9199 | Monitoring | Prometheus (9090), AlertManager (9093) |
| 30000-32767 | Kubernetes NodePort | Not used |

## Running Locally

### Start all services
```bash
# Terminal 1: Start auth service
cd backend && uvicorn main:app --host 0.0.0.0 --port 8200

# Terminal 2: Start mechanics service
cd services/mechanics-service && uvicorn main:app --host 0.0.0.0 --port 8201

# Terminal 3: Start jobs service
cd services/jobs-service && uvicorn main:app --host 0.0.0.0 --port 8202

# Terminal 4: Start analytics service
cd services/analytics-service && uvicorn main:app --host 0.0.0.0 --port 8203
```

### Start with Docker
```bash
# Redis
docker run -d -p 6379:6379 --name redis redis:7-alpine

# FalkorDB
docker run -d -p 6379:6379 -p 3000:3000 --name falkordb falkordb/falkordb:latest

# Auth service
docker run -d -p 8200:8200 --env PORT=8200 ghcr.io/gaineyllc/auth-service:latest

# Analytics service (requires ClickHouse)
docker run -d -p 8203:8203 \
  --env PORT=8203 \
  --env CLICKHOUSE_HOST=localhost \
  ghcr.io/gaineyllc/analytics-service:latest

# ClickHouse
cd services/clickhouse
docker-compose up -d
```

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
