# SkyMechanics Dev Log

A running log of development progress on the GB10 workstation (promaxgb10-495f).

---

## 2026-04-20

### 22:00 EDT
**End-to-End Job Workflow (complete):**
- Created `/api/v1/jobs` endpoints with full workflow support
- Job workflow states: pending -> open -> in_progress -> completed
- Workflow transitions validated on status updates
- Visual workflow builder component with node graph
- Graph shows objects and relationships in the database

**API Endpoints Added:**
- `GET /api/v1/jobs` - List jobs with filters
- `POST /api/v1/jobs` - Create new job
- `GET /api/v1/jobs/{id}` - Get job by ID
- `PUT /api/v1/jobs/{id}` - Update job properties
- `POST /api/v1/jobs/{id}/status` - Update job status with workflow validation
- `DELETE /api/v1/jobs/{id}` - Soft delete job
- `GET /api/v1/jobs/{id}/workflow` - Get workflow data for visual builder
- `GET /api/v1/jobs/workflow/complete` - Get complete workflow definition

**Frontend Components:**
- `/workflow` - Read-only workflow view
- `/workflow/edit` - Editable workflow builder
- Nodes: job, customer, mechanic, aircraft
- Edges: relationships between nodes
- Legend with workflow states and transitions

**Current State:**
- Backend: FastAPI port **8003** (FalkorDB + Redis + new routes)
- Frontend: React port **3002** (updated with WorkflowBuilder)

### 21:14 EDT
**User Onboarding / Role Profiles (completed):**
- Created `/api/v1/users` endpoints for role-based user profiles
- Implemented three role types:
  - **Owner** - `/api/v1/users/{id}/profile/owner`
  - **Admin** - `/api/v1/users/{id}/profile/admin`
  - **Mechanic** - `/api/v1/users/{id}/profile/mechanic`
- All endpoints tested and working on port 8003

**Current Backend:**
- FastAPI running on port **8003** (FalkorDB + Redis)
- Frontend running on port **3002** (React + Vite + Tailwind)

**API Endpoints Added:**
- `POST /api/v1/users` - Create user with role
- `GET /api/v1/users/{id}` - Get user profile
- `POST /api/v1/users/{id}/profile/owner` - Create owner profile
- `POST /api/v1/users/{id}/profile/admin` - Create admin profile
- `POST /api/v1/users/{id}/profile/mechanic` - Create mechanic profile

### 21:12 EDT
**Current State:**
- Backend: FastAPI on port 8002 (FalkorDB + Redis)
- Frontend: React on port 3002
- Dev log created, committed to repo

**Today's Priority:**
Build complete end-to-end workflow by morning:
1. User onboarding (3 roles: Owner, Admin, Mechanic)
2. Fleet management interface with location tracking
3. Job workflow (Request → Offer → Accept → Monitor → Complete)
4. E2E tests for full workflow

**Breaking down into features:**
- [x] Role-based user profiles (completed)
- [x] End-to-end job workflow with visual builder (completed)
- [ ] Fleet location/visibility dashboard
- [ ] Job request creation
- [ ] Offer system
- [ ] Job acceptance
- [ ] Progress monitoring
- [ ] Sign-off and completion
- [ ] Full E2E test suite

### 21:07 EDT
- Backend running on port **8002** (FastAPI + FalkorDB + Redis)
- Frontend running on port **3002** (React + Vite + Tailwind)
- All Docker configs committed to repo
- Repo pushed to GitHub

### 20:35 EDT
**Phase 0.5 - Service Breakout & Infrastructure (complete):**
- Extracted backend into 3 microservices:
  - `services/auth-service/` - Auth with PostgreSQL (port 8000)
  - `services/mechanics-service/` - Mechanic management with FalkorDB (port 8001)
  - `services/jobs-service/` - Job scheduling with FalkorDB (port 8002)
- Created `shared/models.py` for cross-service consistency
- Set up Redis for caching and Pub/Sub (port 6379)
- Deployed Prometheus for metrics collection (port 9090)
- Deployed Grafana for dashboard visualization (port 3000)
- Configured alerting rules for service health, errors, memory/CPU
- Updated Kubernetes manifests for each service
- Updated `PLAN.md` with Phase 0.5 completion

**Kubernetes Services:**
| Service | Port | Database |
|---------|------|----------|
| auth-service | 8000 | PostgreSQL |
| mechanics-service | 8001 | FalkorDB |
| jobs-service | 8002 | FalkorDB |

**Observability Access:**
| Tool | Port | Access |
|------|------|--------|
| Prometheus | 9090 | `kubectl port-forward -n skymechanics svc/prometheus 9090:9090` |
| Grafana | 3000 | `kubectl port-forward -n skymechanics svc/grafana 3000:3000` |
| Redis Insight | 5540 | `kubectl port-forward -n skymechanics svc/redis-insight 5540:5540` |

**Git Commits:**
- `3de502d` - feat: break backend into microservices (Phase 1)
- `fb9376d` - feat: add Redis and observability stack (Phase 1 continuation)
- `8b6b188` - docs: update PLAN.md with Phase 0.5 completion

### 14:24 EDT
**Backend Microservices (in progress):**
- Split backend into separate services
- Auth service: FastAPI + PostgreSQL
- Mechanics service: FastAPI + FalkorDB
- Jobs service: FastAPI + FalkorDB + PostgreSQL

**New Directory Structure:**
```
skymechanics-dev/
├── k8s/
│   ├── auth-service.yaml
│   ├── mechanics-service.yaml
│   └── jobs-service.yaml
├── services/
│   ├── auth-service/
│   ├── mechanics-service/
│   └── jobs-service/
└── shared/
    └── models.py
```

### 15:14 EDT
**BaseUI v10 Migration (complete):**
- Removed all deprecated baseui components
- Replaced with native React elements and inline styles
- Build now succeeds with stable frontend (port 3002)

### 21:01 EDT
**Backend Health Check (fixed):**
- Fixed health endpoint at root path `/health` and `/ready`
- Updated service YAMLs with correct probe paths
- Services now running: jobs-service, mechanics-service (FalkorDB), auth-service (PostgreSQL)

---

## 2026-04-19

### 15:19 EDT
**Frontend Build (fixed):**
- Resolved BaseUI v10 dependency conflict
- All files migrated from BaseUI v8 to v10
- Build succeeds with native React + inline styles
- End-to-end tests added and passing

### 09:52 EDT
**BaseUI v10 Migration (in progress):**
- Frontend migration from Base UI v8 to v10
- Layout.tsx fully rewritten with inline styles
- CreateJobModal, JobDetail, Customers, Mechanics, Jobs, Admin pages migrated
- Onboarding.tsx, OnboardingSuccess.tsx, QuickStartWizard.tsx created

### 06:44 EDT
**Backend Fully Functional:**
- Fixed duplicate `jobs_router` import
- Installed structlog in container
- Backend runs on port 8080
- Health endpoint confirms FalkorDB connection
- OpenAPI spec shows all endpoints

### 06:38 EDT
**Job Workflow Implementation:**
- Full `/api/v1/jobs` routes implemented
- Status transitions: pending → open → in_progress → completed/cancelled
- Graph-based relationship queries
- Tenant isolation via FalkorDB

---

## 2026-04-18

### 20:08 EDT
**Frontend Scaffolding:**
- React + Vite + Tailwind + Base Web scaffolded
- Core pages: Dashboard, Jobs, JobDetail, Customers, Mechanics, Admin
- AuthContext committed
- **Issue**: BaseUI requires React <19, but 19.2.5 installed

### 19:24 EDT
**Backend Scaffolding:**
- FastAPI backend scaffolded
- FalkorDB integration configured
- Seed data created (3 customers, 3 mechanics, 3 jobs)

### 19:05 EDT
**Architecture Decision:**
- FalkorDB selected over Neo4j, Memgraph, NebulaGraph
- Prioritizing AI/GraphRAG performance, Cypher compatibility, on-prem friendly licensing

### 18:40 EDT
**Project Started:**
- Git repo initialized
- Docker Compose for FalkorDB
- Kubernetes deployment plan defined
