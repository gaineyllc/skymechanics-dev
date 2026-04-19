# SkyMechanics - Onboarding Flow

## Goal
Create a smooth path from first visit to first completed job in < 10 minutes.

## User Journey

```
1. Landing Page (anonymous)
   ↓
2. Sign Up / Login (email/password or Google)
   ↓
3. Account Setup Wizard
   ├─ Choose Account Type: [Flight School] [Solo Owner] [FBO/Shop]
   ├─ Enter Organization Name
   ├─ Create Tenant Graph in FalkorDB
   └─ Add Initial Admin User
   ↓
4. Initial Data Setup (optional, guided)
   ├─ Add First Aircraft
   ├─ Add First Customer (if flight school)
   └─ Add First Mechanic
   ↓
5. First Job Completion
   ├─ Create Job
   ├─ Assign to Mechanic
   └─ Mark Complete
   ↓
6. Dashboard View - Success!
```

## Detailed Steps

### Step 1: Landing Page
**Current State:** Empty `/` endpoint returns API info
**Target State:** Marketing landing page with:
- Platform description
- Account type selector
- "Get Started" button → redirects to `/signup`

### Step 2: Account Creation
**Fields:**
- Email (required)
- Password (required, min 8 chars)
- Account Type: `flight_school` | `solo_owner` | `fbo_shop`
- Organization Name (required)
- Admin First Name (required)
- Admin Last Name (required)

**Validation:**
- Email format check
- Password strength check
- Organization name uniqueness (per account type)

**API Endpoint:**
```
POST /api/v1/onboard
{
  "email": "user@example.com",
  "password": "secure123!",
  "account_type": "flight_school",
  "org_name": "Sky Flight Academy",
  "first_name": "Sarah",
  "last_name": "Johnson"
}
```

**Response:**
```json
{
  "success": true,
  "tenant_id": "t_abc123",
  "graph_name": "skymechanics_tenant_abc123",
  "token": "eyJhbGci...",
  "user_id": "u_xyz789"
}
```

### Step 3: Graph Database Setup
**Backend Action:**
1. Create new FalkorDB graph: `tenant_{tenant_id}`
2. Initialize with schema (optional):
   ```
   CREATE INDEX ON :Customer(name)
   CREATE INDEX ON :Aircraft(tail_number)
   CREATE INDEX ON :Mechanic(name)
   CREATE INDEX ON :Job(status)
   ```
3. Create default admin role in graph

**Code Location:** `backend/onboarding.py`

### Step 4: User Profile Creation
**Fields:**
- User ID (from step 2)
- First Name
- Last Name
- Role: `admin` | `owner` | `mechanic` | `reader`
- Email (for notifications)
- Phone (optional)

**API Endpoint:**
```
POST /api/v1/users
Headers: Authorization: Bearer {token}
{
  "first_name": "Sarah",
  "last_name": "Johnson",
  "role": "admin",
  "email": "sarah@skyflight.com"
}
```

### Step 5: Optional Quick Start Data
**For Flight Schools:**
- Add up to 3 aircraft (tail_number, make, model)
- Add up to 3 mechanics (name, email, specialties)

**For Solo Owners:**
- Add 1 aircraft (tail_number, make, model)
- Add 0-2 mechanics

**API Endpoint:**
```
POST /api/v1/onboard/bulk
Headers: Authorization: Bearer {token}
{
  "aircraft": [
    {"tail_number": "N12345", "make": "Cessna", "model": "172"}
  ],
  "mechanics": [
    {"name": "John Doe", "email": "john@shop.com", "specialties": ["piston"]}
  ]
}
```

### Step 6: First Job Flow
**Job Creation:**
```
POST /api/v1/jobs
Headers: Authorization: Bearer {token}
{
  "title": "Annual Inspection",
  "description": "Annual 100-hour inspection and oil change",
  "status": "pending",
  "priority": "medium",
  "customer_id": 1,
  "aircraft_id": 1,
  "mechanic_id": 1
}
```

## Technical Implementation

### Backend Files Created

1. **`backend/onboarding.py`** ✅
   - `generate_tenant_id()`: Generate unique tenant ID
   - `generate_graph_name()`: Generate FalkorDB graph name
   - `create_tenant_graph()`: Create and index new graph
   - `initialize_graph_schema()`: Set up required indexes
   - `create_admin_user()`: Create initial admin user node
   - `bulk_import_onboard_data()`: Import aircraft/mechanics
   - `check_onboarding_status()`: Verify setup completeness
   - `full_onboarding()`: Execute complete onboarding flow

2. **`backend/routes/onboarding.py`** ✅
   - `POST /api/v1/onboard`: Account creation (full_onboarding)
   - `POST /api/v1/onboard/bulk`: Bulk import (complete_onboarding)
   - `GET /api/v1/onboard/status`: Status check (check_onboarding_status)
   - `GET /api/v1/onboard/check-email`: Email availability check (stub)

3. **`backend/models/onboarding.py`** ✅
   - `OnboardRequest`: Request validation
   - `BulkImportRequest`: Bulk data import validation
   - `OnboardResponse`: Success response
   - `OnboardStatusResponse`: Status check response

### Updated Files

1. **`backend/main.py`** ✅
   - Added `onboarding_router` import and registration

2. **`backend/requirements.txt`** ✅
   - Added `email-validator` dependency

### Frontend Pages (Next Step)

The backend is complete. Frontend implementation remains:

1. **`src/pages/Onboarding.tsx`**
   - Account type selector
   - Organization details
   - Admin user info
   - Submit button

2. **`src/pages/OnboardingSuccess.tsx`**
   - "Setup complete" message
   - "Add Your First Aircraft" button
   - "Skip to Dashboard" option

3. **`src/components/QuickStartWizard.tsx`**
   - Step 1: Aircraft
   - Step 2: Mechanics
   - Step 3: Done!

### Auth Flow Integration

**Current:** No auth in place
**Target:** JWT tokens for API access

**Protected Routes:**
- `/dashboard`
- `/jobs`
- `/customers`
- `/mechanics`
- `/aircraft`

**Public Routes:**
- `/`
- `/signup`
- `/login`
- `/forgot-password`

## Success Metrics

- User completes onboarding in < 5 minutes
- >80% complete full setup (add aircraft/mechanics)
- <5% bounce rate on signup page
- First job created within 24 hours

## Backend Implementation Complete ✅

All three endpoints are working:

| Endpoint | Method | Status | Example |
|----------|--------|--------|----------|
| `/api/v1/onboard` | POST | ✅ Working | Creates account, graph, admin |
| `/api/v1/onboard/bulk` | POST | ✅ Working | Imports aircraft/mechanics |
| `/api/v1/onboard/status` | GET | ✅ Working | Returns setup status |

### Tested Flow

```bash
# 1. Create account
$ curl -X POST http://localhost:8080/api/v1/onboard \
  -H 'Content-Type: application/json' \
  -d '{"email":"test@example.com","password":"secure123!",...}'

# 2. Bulk import data
$ curl -X POST "http://localhost:8080/api/v1/onboard/bulk?graph_name=..." \
  -H 'Content-Type: application/json' \
  -d '{"aircraft":[...],"mechanics":[...]}'

# 3. Check status
$ curl "http://localhost:8080/api/v1/onboard/status?graph_name=..."
```

### Graph Data Verified

```cypher
MATCH (n) RETURN n
```

Results in FalkorDB:
- User node (admin)
- Aircraft node (N12345)
- Mechanic node (John Doe)

**Next:** Frontend onboarding pages to consume these APIs.
