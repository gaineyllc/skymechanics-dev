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
### Docker Images Built

All 3 Docker images built locally:
- `ghcr.io/gaineyllc/auth-service:latest`
- `ghcr.io/gaineyllc/mechanics-service:latest`
- `ghcr.io/gaineyllc/jobs-service:latest`

**To push images:**
```bash
docker login ghcr.io -u gaineyllc
docker push ghcr.io/gaineyllc/auth-service:latest
docker push ghcr.io/gaineyllc/mechanics-service:latest
docker push ghcr.io/gaineyllc/jobs-service:latest
```

## Services Configuration

| Service | Port | Status |
|---------|------|--------|
| auth-service | 8200 | Running (local) |
| mechanics-service | 8201 | Not running |
| jobs-service | 8202 | Not running |
| skymechanics-falkordb | 6379 | Healthy |
| skymechanics-redis | 6379 | Running |

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

## Ports Used

| Range | Purpose | Status |
|-------|---------|--------|
| 8000 | vLLM (Qwen3-Coder-Next-FP8) | Reserved |
| 8200 | auth-service | Active |
| 8201 | mechanics-service | Ready |
| 8202 | jobs-service | Ready |
| 3000 | FalkorDB HTTP | Active |
| 3001 | FalkorDB Browser | Active |
| 6379 | FalkorDB/Redis | Active |
| 9090 | Prometheus | Ready (k8s) |
| 3000 | Grafana | Ready (k8s) |

## Running Locally

### Start all services
```bash
# Terminal 1: Start auth service
cd backend && uvicorn main:app --host 0.0.0.0 --port 8200

# Terminal 2: Start mechanics service
cd services/mechanics-service && uvicorn main:app --host 0.0.0.0 --port 8201

# Terminal 3: Start jobs service
cd services/jobs-service && uvicorn main:app --host 0.0.0.0 --port 8202
```

### Start with Docker
```bash
# Redis
 docker run -d -p 6379:6379 --name redis redis:7-alpine

# FalkorDB
docker run -d -p 6379:6379 -p 3000:3000 --name falkordb falkordb/falkordb:latest

# Auth service
docker run -d -p 8200:8200 --env PORT=8200 ghcr.io/gaineyllc/auth-service:latest
```
