# SkyMechanics Human Demo Gap Analysis

**Date:** 2026-04-22 09:36 EDT  
**Status:** Full service deployment verified (13 pods running)  
**Target:** End-to-End demo (Owner → Aircraft → Job → Mechanic → Completion)

---

## Executive Summary

**Current State:** 13 services deployed and healthy  
**Target State:** Human-readable end-to-end demo workflow  
**Estimated Effort:** ~40 hours for P0+P1 gaps

### Service Status (2026-04-22 09:36 UTC)
| Service | Port | Status | Notes |
|---------|------|--------|-------|
| auth-service | 8200 | ✅ Running | WebSocket support added |
| aircraft-service | 8201 | ✅ Running | WebSocket support added |
| jobs-service | 8202 | ✅ Running | Full CRUD, status transitions |
| mechanics-service | 8204 | ✅ Running | Base CRUD operations |
| frontend | 3000 | ✅ Running | React app with registration forms |
| gateway | 8080 | ✅ Running | WebSocket routing |
| analytics | 8209 | ✅ Running | - |
| parts | 8205 | ✅ Running | - |
| notification | 8206 | ✅ Running | - |
| invoice | 8207 | ✅ Running | - |
| falkordb | 6379 | ✅ Running | Graph database |
| postgres | 5432 | ✅ Running | User/auth data |
| redis | 6379 | ✅ Running | Caching |

---

## Demo Workflow Requirements

### P0 - Core Demo Flow (Must Have)
1. **Owner Onboarding**
   - Create owner account with organization
   - Owner dashboard with aircraft list
   - Invite mechanic via email

2. **Aircraft Management**
   - Add aircraft with tail number
   - View aircraft status
   - Link to maintenance records

3. **Job Creation & Assignment**
   - Create maintenance request
   - Select aircraft and procedure
   - Assign to mechanic

4. **Mechanic Workflow**
   - View assigned jobs
   - Execute procedure steps
   - Capture digital signature

5. **Job Completion**
   - Mark all steps complete
   - Owner review and approval
   - PDF report generation

---

## Detailed Gap Analysis

### 1. Owner Onboarding Flow (P0 - 12 hours)

#### Frontend Components Needed
| Component | File | Status | Estimate |
|-----------|------|--------|----------|
| Owner Registration Form | `pages/Register/OwnerRegister.tsx` | ✅ Created | - |
| Owner Dashboard | `pages/Dashboard.tsx` | ⚠️ Basic | +8 hrs |
| Aircraft List View | `pages/Aircraft.tsx` | ⚠️ Basic | +4 hrs |

#### Backend Endpoints Needed
| Endpoint | Method | Description | Status |
|----------|--------|-------------|--------|
| `/api/v1/owner/dashboard` | GET | Owner fleet summary | Missing |
| `/api/v1/owner/invites` | POST | Invite mechanic | Missing |
| `/api/v1/owner/profile` | GET | Owner profile details | Missing |

#### Database Schema
| Node | Property | Status |
|------|----------|--------|
| `Owner` node | `org_id`, `preferences` | Missing |
| `Invitation` node | `token`, `expires`, `status` | Missing |

---

### 2. Aircraft Management (P0 - 8 hours)

#### Current Status
- ✅ `POST /api/v1/aircraft` - Create aircraft
- ✅ `GET /api/v1/aircraft` - List aircraft
- ✅ `GET /api/v1/aircraft/{id}` - Get aircraft
- ✅ `PUT /api/v1/aircraft/{id}` - Update aircraft
- ✅ `DELETE /api/v1/aircraft/{id}` - Delete aircraft

#### Missing Features
| Feature | Endpoint | Status |
|---------|----------|--------|
| Fleet summary | `GET /api/v1/aircraft/dashboard` | Missing |
| Airworthiness status | `GET /api/v1/aircraft/{id}/airworthiness` | Missing |
| Registration expiry alerts | `GET /api/v1/aircraft/deadlines` | Missing |

#### Frontend Components
| Component | File | Status |
|-----------|------|--------|
| Aircraft Dashboard | `pages/Aircraft.tsx` | ⚠️ Basic |
| Deadline Calendar | `components/DeadlineCalendar.tsx` | Missing |

---

### 3. Job Creation & Assignment (P0 - 10 hours)

#### Current Status
- ✅ `POST /api/v1/jobs` - Create job
- ✅ `GET /api/v1/jobs` - List jobs
- ✅ `GET /api/v1/jobs/{id}` - Get job
- ✅ `PUT /api/v1/jobs/{id}/status` - Update status

#### Missing Features
| Feature | Endpoint | Status |
|---------|----------|--------|
| Assign mechanic | `PUT /api/v1/jobs/{id}/assign` | Missing |
| Complete job | `POST /api/v1/jobs/{id}/complete` | Missing |
| Procedure execution | `POST /api/v1/jobs/{id}/procedure/start` | Missing |
| Job summary (cost breakdown) | `GET /api/v1/jobs/{id}/summary` | Missing |
| PDF export | `GET /api/v1/jobs/{id}/pdf` | Missing |

#### Database Schema
| Node | Relationship | Status |
|------|--------------|--------|
| `Job` → `Mechanic` (ASSIGNED_TO) | Missing |
| `Job` → `Procedure` (USES_PROCEDURE) | Missing |
| `Job` → `Parts` (USES_PART) | Missing |

---

### 4. Mechanic Workflow (P0 - 8 hours)

#### Current Status
- ✅ `GET /api/v1/mechanics` - List mechanics
- ✅ `GET /api/v1/mechanics/{id}` - Get mechanic
- ✅ `POST /api/v1/mechanics/register` - Register mechanic

#### Missing Features
| Feature | Endpoint | Status |
|---------|----------|--------|
| Get assigned jobs | `GET /api/v1/mechanics/{id}/jobs` | Missing |
| Procedure execution | `POST /api/v1/jobs/{id}/procedure/step/{step_id}/complete` | Missing |
| Signature capture | `POST /api/v1/signatures` | Missing |
| Issue flagging | `POST /api/v1/jobs/{id}/issues` | Missing |

#### Frontend Components
| Component | File | Status |
|-----------|------|--------|
| Mechanic Dashboard | `pages/MechanicDashboard.tsx` | Missing |
| Procedure Execution UI | `components/ProcedureExecution.tsx` | Missing |
| Signature Pad | `components/SignaturePad.tsx` | Missing |

---

### 5. Job Completion & Handoff (P0 - 4 hours)

#### Missing Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/jobs/{id}/complete` | POST | Complete with signature |
| `/api/v1/jobs/{id}/summary` | GET | Cost breakdown + completion report |
| `/api/v1/jobs/{id}/pdf` | GET | Download PDF report |
| `/api/v1/notifications/send` | POST | Notify owner of completion |

#### Frontend Components
| Component | File | Status |
|-----------|------|--------|
| Job Completion Screen | `pages/Jobs/Complete.tsx` | Missing |
| PDF Download | `components/PDFViewer.tsx` | Missing |

---

## Implementation Priority Matrix

### Week 1 (P0 - Demo Blockers)
| Day | Task | Hours | Deliverable |
|-----|------|-------|-------------|
| Mon | Owner dashboard + aircraft list | 6 | Owner sees fleet |
| Mon | Aircraft dashboard endpoints | 4 | Fleet summary API |
| Tue | Job assignment flow | 4 | Assign mechanic to job |
| Tue | Job completion workflow | 4 | Complete job with signature |
| Wed | PDF report generation | 4 | Downloadable reports |
| Wed | Owner handoff notification | 2 | Email/SMS alerts |
| Thu | Frontend integration | 6 | All pages wired up |
| Thu | Testing | 2 | End-to-end verification |
| **Total** | | **32** | **Human demo ready** |

---

## Current Demo Readiness Checklist

### Frontend
- [x] Login page (`pages/Login.tsx`)
- [x] Owner registration (`pages/Register/OwnerRegister.tsx`)
- [x] Mechanic registration (`pages/Register/MechanicRegister.tsx`)
- [x] Dashboard (`pages/Dashboard.tsx`) - Basic
- [x] Aircraft (`pages/Aircraft.tsx`) - Basic
- [x] Jobs (`pages/Jobs.tsx`) - Basic
- [x] Mechanics (`pages/Mechanics.tsx`) - Basic
- [ ] Owner dashboard with fleet view
- [ ] Job assignment UI
- [ ] Procedure execution UI
- [ ] Signature capture component
- [ ] PDF export functionality

### Backend
- [x] Auth service with login/registration
- [x] Aircraft CRUD endpoints
- [x] Jobs CRUD endpoints
- [x] Mechanics CRUD endpoints
- [x] WebSocket endpoints (auth, aircraft, jobs)
- [ ] Owner dashboard API
- [ ] Job assignment API
- [ ] Job completion API
- [ ] Signature validation API
- [ ] PDF export API

### Database
- [x] FalkorDB connected
- [x] Basic nodes created (Aircraft, Job, Mechanic)
- [ ] `Owner` node with organization link
- [ ] `Invitation` node for mechanic invites
- [ ] `Procedure` node with steps
- [ ] `Signature` node for job completion

---

## Estimated Remaining Effort

| Priority | Items | Hours |
|----------|-------|-------|
| P0 (Demo) | 12 | 32 |
| P1 (Enhancements) | 8 | 24 |
| P2 (Nice-to-have) | 5 | 16 |
| **Total** | **25** | **72** |

---

## Recommended Next Steps

1. **Owner Dashboard API** - Create fleet summary with aircraft count, upcoming deadlines
2. **Job Assignment UI** - Link mechanics to jobs with dropdown selection
3. **Procedure Execution Flow** - Step-by-step checklist for mechanics
4. **PDF Report Generation** - Automated report with completion status
5. **End-to-End Test** - Full workflow from owner signup to job completion

---

## Quick Win Items (Can Complete Today)

1. **Add fleet summary endpoint** (`GET /api/v1/aircraft/dashboard`) - 2 hrs
2. **Add job assignment endpoint** (`PUT /api/v1/jobs/{id}/assign`) - 2 hrs
3. **Complete job summary endpoint** (`GET /api/v1/jobs/{id}/summary`) - 2 hrs
4. **Add PDF export endpoint** (`GET /api/v1/jobs/{id}/pdf`) - 2 hrs
5. **Create owner dashboard view** - 4 hrs
6. **Wire up frontend components** - 6 hrs

**Total: 18 hours for working demo**
