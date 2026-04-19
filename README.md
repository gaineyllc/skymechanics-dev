# SkyMechanics Platform - Local Development Setup

[![Test Suite](https://github.com/gaineyllc/skymechanics-dev/actions/workflows/test.yml/badge.svg)](https://github.com/gaineyllc/skymechanics-dev/actions/workflows/test.yml)

## Overview
This project provides a multi-tenant graph database platform for job management, built with:
- **FastAPI** - REST API backend
- **FalkorDB** - Graph database with multi-tenancy
- **vLLM** - LLM inference (existing integration)

## Quick Start

### Prerequisites
- Docker installed
- 50GB+ free disk space
- GPU recommended for vLLM

### Installation

1. **Navigate to project directory**
```bash
cd /home/gaineyllc/.openclaw/workspace/skymechanics-dev
```

2. **Start the stack**
```bash
docker compose up -d
```

3. **Verify services**
```bash
docker compose ps
```

Expected output:
```
NAME                      STATUS      PORTS
skymechanics-api          running     0.0.0.0:8000->8000/tcp
skymechanics-browser      running     0.0.0.0:3001->3000/tcp
skymechanics-falkordb     running     0.0.0.0:6379->6379/tcp, 0.0.0.0:3000->3000/tcp
```

4. **Seed sample data**
```bash
docker compose exec api python scripts/seed-data.py
```

5. **Access services**
- API: `http://localhost:8000`
- Frontend: `http://localhost:3003` (mapped from container port 3000)
- Browser: `http://localhost:3001`
- Health check: `http://localhost:8000/health`

## Development

### API Documentation
Once the API is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Running Tests
```bash
docker compose exec api pytest
```

### Viewing Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f api
docker compose logs -f falkordb
```

### Stopping the Stack
```bash
docker compose down
```

### Stopping and Removing Data
```bash
docker compose down -v
```

## Project Structure

```
skymechanics-dev/
├── docker-compose.yml          # Local K3s emulation
├── backend/                    # FastAPI application
│   ├── main.py                # API endpoints
│   ├── db.py                  # FalkorDB connections
│   ├── models.py              # Pydantic schemas
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile             # Container definition
├── frontend/                   # React application (Vite)
│   ├── src/                   # Source files
│   │   ├── components/        # Reusable UI components
│   │   │   ├── CreateJobModal.tsx
│   │   │   ├── CreateCustomerModal.tsx
│   │   │   └── CreateMechanicModal.tsx
│   │   ├── pages/             # Page components
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Jobs.tsx
│   │   │   ├── Customers.tsx
│   │   │   ├── Mechanics.tsx
│   │   │   └── Admin.tsx
│   │   ├── services/          # API services
│   │   │   └── api.ts
│   │   ├── App.tsx            # Main app component
│   │   └── main.tsx           # Entry point
│   ├── public/                # Static assets
│   ├── vite.config.ts         # Vite configuration
│   └── Dockerfile             # Container definition
├── scripts/                    # Setup/seed scripts
│   ├── init-db.sh
│   └── seed-data.py
└── k8s/                       # Kubernetes manifests (for later)
    ├── falkordb-helm.yaml
    └── deployment.yaml
```

## API Endpoints

### System
- `GET /health` - Health check

### Graph Operations
- `POST /query` - Execute Cypher query

### Multi-Tenant Operations
- `POST /tenants` - Create new tenant
- `POST /tenants/query` - Query tenant graph

### Entities
- `POST /entities` - Create entity
- `POST /relationships` - Create relationship

### Business Logic
- `GET /customers` - List all customers
- `POST /customers` - Create customer
- `GET /customers/{customer_id}` - Get customer by ID
- `GET /jobs` - List all jobs
- `POST /jobs` - Create job
- `GET /jobs/{job_id}` - Get job by ID
- `GET /mechanics` - List all mechanics
- `POST /mechanics` - Create mechanic
- `GET /mechanics/{mechanic_id}` - Get mechanic by ID

## Multi-Tenancy

Each tenant gets their own graph in FalkorDB:
- Tenant graph name: `tenant_{tenant_id}`
- Isolated data per tenant
- Query: `POST /tenants/query` with `tenant_id`

## Troubleshooting

### Services not starting
```bash
# Check logs
docker compose logs

# Rebuild containers
docker compose up -d --build
```

### Port conflicts
Edit `docker-compose.yml` and change the host ports:
```yaml
ports:
  - "8001:8000"  # Change 8000 to 8001
```

### Database connection issues
```bash
# Restart FalkorDB
docker compose restart falkordb

# Re-run seed data
docker compose exec api python scripts/seed-data.py
```

## Next Steps

1. **Deploy to Kubernetes** - See `k8s/` directory (when ready)
2. **Add authentication** - Implement JWT tokens
3. **Add WebSockets** - Real-time updates
4. **Add caching** - Redis cache layer
5. **Add monitoring** - Prometheus metrics
6. **Test and expand** - Add unit tests, integration tests, e2e tests
7. **Performance optimization** - Query optimization, caching, connection pooling

## License

MIT License - See LICENSE file for details.
