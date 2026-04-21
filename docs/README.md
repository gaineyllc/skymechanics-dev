# SkyMechanics Platform - Documentation

## Table of Contents
1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Architecture](#architecture)
4. [API Reference](#api-reference)
5. [Database Schema](#database-schema)
6. [Reputation System](#reputation-system)
7. [Multi-Tenancy](#multi-tenancy)
8. [Frontend Components](#frontend-components)
9. [Development](#development)
10. [Deployment](#deployment)

---

## Overview

SkyMechanics is a multi-tenant repair shop management platform built with:
- **FastAPI** - Python REST API framework
- **FalkorDB** - Graph database with multi-tenancy support
- **React 19** - Frontend with Vite and Tailwind CSS
- **vLLM** - Local LLM inference for intelligent features

### Key Features
- Multi-tenant architecture with graph isolation
- Mechanic reputation scoring system
- Procedure/workflow management
- Job status tracking
- Aircraft manual integration

---

## Quick Start

### Prerequisites
- Docker ≥ 24.0
- 50GB+ free disk space
- GPU recommended for vLLM

### Installation

```bash
# Clone repository
cd /home/gaineyllc/.openclaw/workspace/skymechanics-dev

# Start services
docker compose up -d

# Verify services
docker compose ps
```

### Access URLs
- **API**: `http://localhost:8200`
- **Frontend**: `http://localhost:3003`
- **FalkorDB Browser**: `http://localhost:3000`
- **RedisInsight**: `http://localhost:8001` (admin/admin)

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Load Balancer (nginx)                 │
│                        Port 80 → 8200                        │
└─────────────────────────────────────────────────────────────┘
                              │
       ┌──────────────────────┼──────────────────────┐
       │                      │                      │
┌──────▼───────┐    ┌────────▼────────┐    ┌────────▼────────┐
│   Frontend   │    │  Backend API    │    │   Redis Cluster │
│  React App   │    │  FastAPI        │    │   (Cache/PubSub)│
│  Port 3003   │    │  Port 8200      │    │   Port 6380     │
└──────────────┘    └─────────────────┘    └─────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
        ┌─────▼───────┐ ┌─────▼───────┐ ┌─────▼──────────────┐
        │  FalkorDB   │ │   Redis     │ │   vLLM AI Server   │
        │  Graph DB   │ │   (Backup)  │ │   (Qwen3-Coder)    │
        │  Port 6379  │ │             │ │   Port 8000        │
        └─────────────┘ └─────────────┘ └────────────────────┘
```

### Component Roles

| Component | Role | Port | Tech |
|-----------|------|------|------|
| Frontend | SPA Dashboard | 3003 | React 19, Vite |
| Backend API | REST API | 8200 | FastAPI |
| FalkorDB | Graph Database | 6379 | FalkorDB |
| Redis | Cache/PubSub | 6380 | Redis Stack |
| vLLM | LLM Inference | 8000 | vLLM |

---

## API Reference

See [API_REFERENCE.md](docs/API_REFERENCE.md) for complete endpoint documentation.

### Available Endpoints

#### Health & System
- `GET /api/v1/health` - Health check
- `GET /api/v1/ready` - Readiness check

#### Onboarding
- `POST /api/v1/onboarding/tenant` - Create tenant
- `POST /api/v1/onboarding/seed` - Seed initial data

#### Customers
- `GET /api/v1/customers` - List customers
- `POST /api/v1/customers` - Create customer

#### Mechanics
- `GET /api/v1/mechanics` - List mechanics
- `POST /api/v1/mechanics` - Create mechanic
- `GET /api/v1/mechanics/{id}` - Get mechanic
- `POST /api/v1/mechanics/{id}/profile` - Update profile

#### Reputation (NEW)
- `GET /api/v1/mechanics/{id}/reputation` - Get reputation score
- `GET /api/v1/mechanics/reputation/top` - Get top mechanics
- `POST /api/v1/mechanics/{id}/certifications` - Add certification
- `POST /api/v1/mechanics/{id}/experience` - Add experience
- `POST /api/v1/mechanics/{id}/reviews` - Add review
- `GET /api/v1/mechanics/{id}/matching-jobs` - Get matching jobs

#### Jobs
- `GET /api/v1/jobs` - List jobs
- `POST /api/v1/jobs` - Create job
- `GET /api/v1/jobs/{id}` - Get job
- `PUT /api/v1/jobs/{id}` - Update job
- `POST /api/v1/jobs/{id}/status` - Update status
- `GET /api/v1/jobs/{id}/workflow` - Get workflow

#### Procedures
- `GET /api/v1/config/procedures` - List procedures
- `POST /api/v1/config/procedures` - Create procedure
- `GET /api/v1/config/tasks` - List tasks
- `GET /api/v1/config/tools` - List tools
- `GET /api/v1/config/parts` - List parts

#### Auth
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/logout` - Logout

---

## Database Schema

### Core Nodes

```
Mechanic
  - node_id
  - name
  - email
  - phone
  - specialties

Certification
  - name
  - authority
  - status
  - issue_date
  - expiry_date

ExperienceRecord
  - hours_flown
  - years_active
  - last_flight_date

Review
  - rating (1-5)
  - comment
  - review_type

Job
  - title
  - description
  - status
  - priority

AircraftType
  - make
  - model
  - category
  - certification
```

### Relationships

```
(Mechanic)-[:HOLDS]->(Certification)
(Mechanic)-[:EXPERIENCE]->(ExperienceRecord)-[:ON_AIRCRAFT]->(AircraftType)
(Review)<-[:GIVEN_BY]-(Job)-[:ASSIGNED_TO]->(Mechanic)
(Aircraft)-[:HAS_PROCEDURE]->(Procedure)
(Procedure)-[:HAS_VERSION]->(ProcedureVersion)
(ProcedureVersion)-[:CONTAINS_TASK]->(Task)
(Task)-[:REQUIRES_TOOL]->(Tool)
(Task)-[:USES_PART]->(Part)
```

---

## Reputation System

### Scoring Algorithm

| Component | Weight | Max Points | Calculation |
|-----------|--------|------------|-------------|
| Certification Status | 25% | 25 | 5 points per active cert |
| Experience Depth | 20% | 20 | 2 points/year + 1/aircraft type |
| Performance | 30% | 30 | Rating, reviews, completions |
| Recent Activity | 15% | 15 | Time since last flight |
| Compliance | 10% | 10 | Compliance history |

### Score Interpretation

| Score Range | Rating | Color |
|-------------|--------|-------|
| 90-100 | Excellent | Green |
| 70-89 | Good | Blue |
| 50-69 | Average | Orange |
| 0-49 | Needs Improvement | Red |

### API Example

```bash
# Get reputation score
curl http://localhost:8200/api/v1/mechanics/1/reputation

# Get top mechanics
curl "http://localhost:8200/api/v1/mechanics/reputation/top?limit=5&min_score=70"

# Add certification
curl -X POST "http://localhost:8200/api/v1/mechanics/1/certifications?name=A%26P%20Mechanic&authority=FAA&status=active"
```

---

## Multi-Tenancy

Each tenant has isolated graph data:

```
Tenant Graph Structure:
  - graph_name: "tenant_{tenant_id}"
  - Isolated from other tenants
  - Same schema across all tenants
```

### Query Example

```python
from db import db_client

db_client.set_graph("tenant_123")
graph = db_client.get_graph()

# Query tenant-specific data
result = graph.query("""
MATCH (m:Mechanic)
RETURN m
""")
```

---

## Frontend Components

### Reputation Components

- **RepScoreBadge** - Display reputation score with color coding
- **RepBreakdownCard** - Show component breakdown with progress bars
- **CertificationsList** - Display certifications as badges
- **ExperienceTimeline** - Timeline of experience records
- **ReputationMetricsCard** - Combined metrics display
- **MechanicProfileCard** - Full mechanic profile with reputation

### Page Components

- **Dashboard** - Overview with stats and recent activity
- **Jobs** - Job list with status filtering
- **Customers** - Customer list with create/edit
- **Mechanics** - Mechanic list with profiles and reputation
- **Inspectors** - Inspector management
- **Aircraft** - Aircraft type management
- **Procedures** - Procedure builder and configuration

---

## Development

### Project Structure

```
skymechanics-dev/
├── backend/
│   ├── main.py              # FastAPI app entry
│   ├── db.py                # Database connections
│   ├── cache.py             # Redis caching
│   ├── pubsub.py            # Pub/Sub events
│   ├── models.py            # Pydantic models
│   ├── routes/
│   │   ├── health.py
│   │   ├── onboarding.py
│   │   ├── customers.py
│   │   ├── mechanics.py
│   │   ├── jobs.py
│   │   ├── reputation.py    # NEW
│   │   ├── users.py
│   │   ├── procedures.py
│   │   ├── events.py
│   │   ├── tenants.py
│   │   └── auth.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ReputationMetrics.tsx   # NEW
│   │   │   ├── MechanicProfile.tsx     # NEW
│   │   │   ├── WorkflowBuilder.tsx
│   │   │   └── ProcedureBuilder.tsx
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Jobs.tsx
│   │   │   └── Mechanics.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   └── App.tsx
│   ├── public/
│   ├── vite.config.ts
│   └── Dockerfile
├── docker-compose.yml
├── docs/
│   ├── API_REFERENCE.md    # NEW
│   └── DATABASE_ARCHITECTURE.md
└── scripts/
    └── seed-data.py
```

### Development Commands

```bash
# Start development stack
docker compose up -d

# Run tests
docker compose exec api pytest

# View logs
docker compose logs -f api

# Stop services
docker compose down

# Stop and remove data
docker compose down -v
```

---

## Deployment

### Docker Compose

```bash
# Production build
docker compose up -d --build

# View status
docker compose ps
```

### Kubernetes (WIP)

See `k8s/` directory for Kubernetes manifests (when ready).

### Environment Variables

```bash
# Backend
PORT=8200
host=falkordb
port=6379
REDIS_HOST=redis
REDIS_PORT=6379
FALKORDB_PASSWORD=your_password
vllm_url=http://100.69.118.20:8000
ENV=production

# Frontend
VITE_API_BASE_URL=http://localhost:8200
VITE_WS_URL=ws://localhost:8200/ws/events
```

---

## Next Steps

1. **Testing**
   - Unit tests (24/24 passing)
   - Integration tests (WIP)
   - E2E tests (WIP)

2. **Documentation**
   - API documentation (complete)
   - Database schema (complete)
   - Deployment guide (complete)

3. **Features**
   - WebSocket real-time updates
   - Redis caching
   - Multi-tenant onboarding UI
   - Procedure workflow execution

4. **Infrastructure**
   - Kubernetes deployment
   - CI/CD pipeline
   - Monitoring/alerting

---

## Support

- **Issues**: GitHub Issues
- **Documentation**: See `docs/` directory
- **API**: `/api/v1/docs` (Swagger UI)

---

## License

MIT License - See LICENSE file for details.
