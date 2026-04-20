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

### Earlier today
- BaseUI v10 migration completed
- Playwright E2E tests added and passing
- Alembic migrations set up
- Structured logging integrated

---
