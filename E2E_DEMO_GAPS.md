# SkyMechanics End-to-End Demo Process Gaps

**Date:** 2026-04-21  
**Focus:** Complete workflow from user onboarding → maintenance completion → owner handoff

---

## Current State Summary

### What's Working (as of 2026-04-21 23:30 UTC)
- ✅ 9 microservices running in k3d cluster
- ✅ Aircraft service base template with CRUD endpoints
- ✅ FalkorDB multi-tenant graph database connected
- ✅ Docker images building and deploying
- ✅ Kubernetes service manifests in place

### What's Missing for End-to-End Demo

---

## 1. USER ONBOARDING FLOW

### Personas Involved
- **Owner** (Sarah/David) - Registers, adds aircraft, sees dashboard
- **Mechanic** (Maria/Raj) - Hired/assigned, completes jobs
- **Inspector** (Admin) - Reviews work, signs off

### Gaps per Persona

#### A. Owner Onboarding (US-1.1-1.10, US-2.1-2.10)
| Step | Description | Status | Priority |
|------|-------------|--------|----------|
| 1 | Create owner account | ❌ Missing | P0 |
| 2 | Organization setup | ❌ Missing | P0 |
| 3 | Add aircraft | ✅ Partial | P0 |
| 4 | Invite mechanics | ❌ Missing | P0 |
| 5 | Set maintenance preferences | ❌ Missing | P1 |
| 6 | Configure reminders | ❌ Missing | P1 |

**Missing Components:**
- Owner registration form (frontend)
- Organization creation API
- Multi-tenant onboarding workflow (MT-001)
- Owner dashboard with aircraft list
- Preference/settings UI

**Backend Gaps:**
- `POST /api/v1/tenants/onboard` endpoint (API-016)
- `POST /api/v1/users/owner/register`
- Tenant provisioning workflow

#### B. Mechanic Onboarding (US-4.1-4.5, US-5.1-5.5)
| Step | Description | Status | Priority |
|------|-------------|--------|----------|
| 1 | Create mechanic profile | ❌ Missing | P0 |
| 2 | Assign specialties | ❌ Missing | P0 |
| 3 | Link to aircraft | ❌ Missing | P0 |
| 4 | View assigned jobs | ❌ Missing | P0 |
| 5 | Digital signature capture | ❌ Missing | P0 |

**Missing Components:**
- Mechanic profile creation form
- Specialty assignment UI
- Aircraft-mechanic linking (DB-006)
- Mechanic job dashboard

**Backend Gaps:**
- `POST /api/v1/mechanics/register`
- `PUT /api/v1/mechanics/{id}/specialties`
- `POST /api/v1/aircraft/{id}/mechanics`
- `GET /api/v1/mechanics/{id}/jobs`

#### C. Inspector/Admin Setup
| Step | Description | Status | Priority |
|------|-------------|--------|----------|
| 1 | Admin role assignment | ❌ Missing | P0 |
| 2 | Permission configuration | ❌ Missing | P0 |
| 3 | Audit log access | ❌ Missing | P1 |

**Missing Components:**
- Role-based access control (RBAC)
- User role management UI
- Audit log viewer

---

## 2. MAINTENANCE WORKFLOW FLOW

### A. Job Creation (US-1.2, US-4.1-4.2)
| Step | Description | Status | Priority |
|------|-------------|--------|----------|
| 1 | Select aircraft | ⚠️ Partial | P0 |
| 2 | Create maintenance request | ❌ Missing | P0 |
| 3 | Assign to mechanic | ❌ Missing | P0 |
| 4 | Select procedure template | ❌ Missing | P0 |
| 5 | Add notes | ❌ Missing | P1 |

**Backend Gaps:**
- `POST /api/v1/jobs` with aircraft ID
- `PUT /api/v1/jobs/{id}/assign` (US-6.2)
- Procedure template selection
- Job note attachment

**Database Gaps:**
- `Job` node with procedure reference
- `ASSIGNED_TO` relationship
- `CREATED_FOR` relationship to aircraft

#### B. Procedure Execution (US-10.1-10.10)
| Step | Description | Status | Priority |
|------|-------------|--------|----------|
| 1 | View procedure steps | ❌ Missing | P0 |
| 2 | Check off checklist items | ❌ Missing | P0 |
| 3 | See required tools | ❌ Missing | P0 |
| 4 | Record parts used | ❌ Missing | P0 |
| 5 | Upload photos | ❌ Missing | P1 |
| 6 | Flag issues | ❌ Missing | P1 |
| 7 | Track time per step | ❌ Missing | P2 |
| 8 | Save incomplete | ❌ Missing | P2 |

**Backend Gaps:**
- `GET /api/v1/procedures/{id}/steps` (API-007)
- `POST /api/v1/jobs/{id}/procedure/start`
- `POST /api/v1/jobs/{id}/procedure/step/{step_id}/complete`
- `POST /api/v1/jobs/{id}/issues`

**Frontend Gaps:**
- Procedure execution UI (FE-005)
- Checklist display
- Photo upload component
- Issue flagging modal

#### C. Job Completion (US-4.2)
| Step | Description | Status | Priority |
|------|-------------|--------|----------|
| 1 | Mark all steps complete | ❌ Missing | P0 |
| 2 | Digital signature capture | ❌ Missing | P0 |
| 3 | Owner notification | ❌ Missing | P1 |
| 4 | PDF report generation | ❌ Missing | P1 |
| 5 | Final approval | ❌ Missing | P0 |

**Backend Gaps:**
- `POST /api/v1/jobs/{id}/complete` with signature (API-004)
- Signature validation endpoint
- PDF export endpoint (API-009)
- Owner notification trigger

**Frontend Gaps:**
- Signature pad component
- PDF export button (FE-004)
- Notification UI

#### D. Owner Handoff (US-1.7-1.10, US-2.6-2.10)
| Step | Description | Status | Priority |
|------|-------------|--------|----------|
| 1 | View completed job summary | ❌ Missing | P0 |
| 2 | Review cost breakdown | ❌ Missing | P1 |
| 3 | View photo evidence | ❌ Missing | P1 |
| 4 | Download PDF report | ❌ Missing | P1 |
| 5 | Rate service | ❌ Missing | P2 |

**Backend Gaps:**
- `GET /api/v1/jobs/{id}/summary` (job details + cost)
- `GET /api/v1/jobs/{id}/pdf`
- `POST /api/v1/jobs/{id}/rating`

**Frontend Gaps:**
- Job summary view
- Cost breakdown display (FE-003)
- Photo gallery
- PDF download button

---

## 3. AIRCRAFT MAINTENANCE TRACKING (US-1.1-1.9)

### A. Aircraft Dashboard (US-1.1, US-1.6)
| Step | Description | Status | Priority |
|------|-------------|--------|----------|
| 1 | Fleet overview | ⚠️ Partial | P0 |
| 2 | Maintenance deadlines | ❌ Missing | P0 |
| 3 | Airworthiness status | ❌ Missing | P0 |
| 4 | Overdue jobs alert | ❌ Missing | P0 |

**Backend Gaps:**
- `GET /api/v1/aircraft/dashboard` (endpoint for fleet summary)
- `GET /api/v1/aircraft/{id}/deadlines`
- `PUT /api/v1/aircraft/{id}/airworthiness/status` (API-003)

**Frontend Gaps:**
- Aircraft dashboard view (FE-001)
- Deadline calendar (FE-002)

#### B. Airworthiness Enforcement (US-1.9)
| Step | Description | Status | Priority |
|------|-------------|--------|----------|
| 1 | Check registration expiry | ❌ Missing | P0 |
| 2 | Block flying status | ❌ Missing | P0 |
| 3 | Airworthiness directive tracking | ❌ Missing | P0 |

**Database Gaps:**
- `Aircraft.airworthiness_status` property (DB-002)
- `Aircraft.registration_expires` (DB-003)
- `AirworthinessDirective` node (DB-011)

---

## 4. INVENTORY & PARTS (US-4.8, US-10.4)

### Gaps
| Step | Description | Status | Priority |
|------|-------------|--------|----------|
| 1 | View parts inventory | ❌ Missing | P1 |
| 2 | Log parts per job | ❌ Missing | P1 |
| 3 | Stock level alerts | ❌ Missing | P2 |
| 4 | Reorder automation | ❌ Missing | P3 |

**Backend Gaps:**
- `GET /api/v1/parts` (API-005)
- `GET /api/v1/parts/{id}/inventory` (API-006)
- `POST /api/v1/jobs/{id}/parts/add`

**Frontend Gaps:**
- Parts inventory view (FE-010)

---

## 5. BILLING & INVOICING (US-3.2, US-4.5)

### Gaps
| Step | Description | Status | Priority |
|------|-------------|--------|----------|
| 1 | Generate invoice | ❌ Missing | P2 |
| 2 | Invoice line items | ❌ Missing | P2 |
| 3 | Client billing | ❌ Missing | P2 |
| 4 | Export invoices | ❌ Missing | P2 |

**Backend Gaps:**
- `POST /api/v1/invoices/generate` (API-012)
- `GET /api/v1/invoices/export` (API-013)

**Frontend Gaps:**
- Invoice viewer
- Export functionality (FE-004)

---

## 6. NOTIFICATIONS & COMMUNICATION (US-1.4, US-2.5, US-7.4)

### Gaps
| Step | Description | Status | Priority |
|------|-------------|--------|----------|
| 1 | Email notifications | ❌ Missing | P1 |
| 2 | SMS alerts | ❌ Missing | P1 |
| 3 | Preference settings | ❌ Missing | P2 |
| 4 | Notification history | ❌ Missing | P2 |

**Backend Gaps:**
- `POST /api/v1/notifications/send` (API-010)
- `PUT /api/v1/notifications/config` (API-011)

---

## 7. DOCUMENTATION & EXPORT (US-1.5, US-2.7, US-3.5)

### Gaps
| Step | Description | Status | Priority |
|------|-------------|--------|----------|
| 1 | PDF report generation | ❌ Missing | P1 |
| 2 | Compliance export (CSV/Excel) | ❌ Missing | P1 |
| 3 | Document versioning | ❌ Missing | P1 |

**Backend Gaps:**
- `GET /api/v1/reports/{type}/export` (API-009)

**Frontend Gaps:**
- PDF export button (FE-004)
- Export options UI

---

## 8. ANALYTICS & REPORTING (US-3.3, US-3.8, US-1.10)

### Gaps
| Step | Description | Status | Priority |
|------|-------------|--------|----------|
| 1 | Fleet health dashboard | ❌ Missing | P2 |
| 2 | Daily summary | ❌ Missing | P2 |
| 3 | Production reports | ❌ Missing | P2 |

**Backend Gaps:**
- `GET /api/v1/reports/health` (AR-001)
- `GET /api/v1/reports/daily-summary` (AR-007)

**Frontend Gaps:**
- Fleet dashboard (FE-007)
- Daily summary widget (FE-008)

---

## PRIORITY FIX LIST FOR DEMO

### P0 - Must Have for Demo (10 items, ~40 hours)
1. **Owner registration** - Create owner account flow
2. **Mechanic profile creation** - Add mechanic form
3. **Aircraft assignment** - Link mechanics to aircraft
4. **Job creation API** - Start job with aircraft
5. **Procedure execution** - View and complete steps
6. **Digital signature** - Capture and validate
7. **Job completion endpoint** - Finalize with sign-off
8. **Cost breakdown view** - Display parts/labor
9. **PDF report generation** - Downloadable reports
10. **Owner handoff flow** - Complete job summary

### P1 - Should Have for Demo (7 items, ~35 hours)
1. **Owner dashboard** - Aircraft list view
2. **Deadline alerts** - Upcoming maintenance
3. **Notification system** - Email/SMS setup
4. **Parts tracking** - Log parts per job
5. **Photo evidence** - Upload and view
6. **Mechanic job dashboard** - Assigned jobs
7. **PDF export** - Compliance reports

### P2 - Nice to Have (5 items, ~25 hours)
1. **Analytics dashboard** - Fleet health
2. **Daily summary** - Morning notifications
3. **Preference settings** - User config
4. **Gantt chart** - Visual scheduling
5. **Service rating** - Post-job feedback

---

## ESTIMATED TOTAL GAPS

| Category | Count | Hours |
|----------|-------|-------|
| Owner onboarding | 3 | 8 |
| Mechanic onboarding | 4 | 10 |
| Inspection setup | 2 | 5 |
| Maintenance workflow | 6 | 16 |
| Airworthiness tracking | 3 | 6 |
| Inventory/part tracking | 2 | 6 |
| Billing/invoicing | 2 | 6 |
| Notifications | 2 | 5 |
| Documentation/export | 3 | 6 |
| Analytics | 3 | 8 |
| **TOTAL** | **36** | **76** |

---

## RECOMMENDED ACTION PLAN

### Week 1 (P0 - Demo Blockers)
- Day 1-2: Owner registration + organization creation
- Day 3-4: Mechanic profile + aircraft assignment
- Day 5: Job creation + procedure execution

### Week 2 (P0 - Completion)
- Day 1-2: Digital signature + job completion
- Day 3-4: Cost breakdown + PDF export
- Day 5: Owner handoff flow

### Week 3 (P1 - Enhancements)
- Day 1-2: Dashboard views
- Day 3-4: Notifications setup
- Day 5: Photo evidence + parts tracking

**Total Estimated Time:** ~40 hours of focused development

---

*This analysis assumes the existing gaps from GAP_ANALYSIS.md are still valid. The end-to-end demo requires filling these specific workflow gaps to demonstrate a complete from-owner-signup-to-job-completion cycle.*
