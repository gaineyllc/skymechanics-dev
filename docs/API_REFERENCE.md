# Backend API Reference

## Endpoints

### Health
- `GET /api/v1/health` - Health check
- `GET /api/v1/ready` - Readiness check

### Onboarding
- `POST /api/v1/onboarding/tenant` - Create tenant
- `POST /api/v1/onboarding/seed` - Seed graph with initial data

### Users
- `POST /api/v1/users` - Create user
- `GET /api/v1/users/{user_id}` - Get user

### Customers
- `GET /api/v1/customers` - List customers
- `POST /api/v1/customers` - Create customer
- `GET /api/v1/customers/{customer_id}` - Get customer
- `PUT /api/v1/customers/{customer_id}` - Update customer
- `DELETE /api/v1/customers/{customer_id}` - Delete customer

### Mechanics
- `GET /api/v1/mechanics` - List mechanics
- `POST /api/v1/mechanics` - Create mechanic
- `GET /api/v1/mechanics/{mechanic_id}` - Get mechanic
- `POST /api/v1/mechanics/{mechanic_id}/profile` - Update mechanic profile

### Reputation (NEW)
- `GET /api/v1/mechanics/{mechanic_id}/reputation` - Get reputation score
- `GET /api/v1/mechanics/reputation/top` - Get top mechanics
- `POST /api/v1/mechanics/{mechanic_id}/certifications` - Add certification
- `POST /api/v1/mechanics/{mechanic_id}/experience` - Add experience
- `POST /api/v1/mechanics/{mechanic_id}/reviews` - Add review
- `GET /api/v1/mechanics/{mechanic_id}/matching-jobs` - Get matching jobs

### Jobs
- `GET /api/v1/jobs` - List jobs
- `POST /api/v1/jobs` - Create job
- `GET /api/v1/jobs/{job_id}` - Get job
- `PUT /api/v1/jobs/{job_id}` - Update job
- `POST /api/v1/jobs/{job_id}/status` - Update job status
- `GET /api/v1/jobs/{job_id}/workflow` - Get job workflow
- `GET /api/v1/jobs/workflow/complete` - Get complete workflow

### Procedures
- `GET /api/v1/config/procedures` - List procedures
- `POST /api/v1/config/procedures` - Create procedure
- `GET /api/v1/config/procedures/{procedure_id}` - Get procedure
- `PUT /api/v1/config/procedures/{procedure_id}` - Update procedure
- `DELETE /api/v1/config/procedures/{procedure_id}` - Delete procedure

### Events (WebSocket)
- `GET /ws/events` - WebSocket events

### Tenants
- `POST /api/v1/tenants` - Create tenant
- `GET /api/v1/tenants` - List tenants

### Auth
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/logout` - Logout
- `GET /api/v1/auth/me` - Get current user

## Reputation Scoring Algorithm

### Components (Total: 100 points)

1. **Certification Status (25 points)**
   - 5 points per active certification
   - Max: 25 points

2. **Experience Depth (20 points)**
   - 2 points per year of experience
   - 1 point per aircraft type
   - Max: 20 points

3. **Performance (30 points)**
   - Rating score (0-15 points): `(avg_rating / 5.0) * 15`
   - Review count score (0-10 points): `min(review_count * 0.5, 10)`
   - Completion rate score (0-5 points): `min(completed_jobs * 0.1, 5)`
   - Max: 30 points

4. **Recent Activity (15 points)**
   - 3 months or less: 15 points
   - 6 months or less: 12 points
   - 12 months or less: 8 points
   - More than 12 months: 5 points
   - Max: 15 points

5. **Compliance (10 points)**
   - Based on compliance history
   - Max: 10 points

### Score Interpretation

| Score Range | Rating | Color |
|-------------|--------|-------|
| 90-100 | Excellent | Green |
| 70-89 | Good | Blue |
| 50-69 | Average | Orange |
| 0-49 | Needs Improvement | Red |

### API Usage Examples

#### Get Reputation Score
```bash
curl http://localhost:8200/api/v1/mechanics/1/reputation
```

#### Get Top Mechanics
```bash
curl "http://localhost:8200/api/v1/mechanics/reputation/top?limit=5&min_score=70"
```

#### Add Certification
```bash
curl -X POST "http://localhost:8200/api/v1/mechanics/1/certifications?name=A%26P%20Mechanic&authority=FAA&status=active&issue_date=2020-01-01&expiry_date=2025-12-31"
```

#### Add Experience
```bash
curl -X POST "http://localhost:8200/api/v1/mechanics/1/experience?aircraft_type_id=1&hours_flown=500&years_active=3&last_flight_date=2023-12-01"
```

#### Add Review
```bash
curl -X POST "http://localhost:8200/api/v1/mechanics/1/reviews?job_id=1&rating=5&comment=Excellent%20work!"
```

#### Get Matching Jobs
```bash
curl "http://localhost:8200/api/v1/mechanics/1/matching-jobs?min_reputation=70&limit=10"
```

## Response Formats

### Reputation Score Response
```json
{
  "mechanic_id": 1,
  "total_score": 85,
  "component_scores": {
    "certification_status": 20,
    "experience_depth": 16,
    "performance": 22,
    "recent_activity": 15,
    "compliance": 12
  },
  "metrics": {
    "review_count": 12,
    "avg_rating": 4.5,
    "completed_jobs": 45,
    "active_certifications": 4,
    "total_years_experience": 8,
    "aircraft_types": 5,
    "months_since_activity": 2
  }
}
```

### Top Mechanics Response
```json
[
  {
    "mechanic_id": 1,
    "total_score": 85,
    "component_scores": { ... },
    "metrics": { ... }
  },
  {
    "mechanic_id": 2,
    "total_score": 82,
    "component_scores": { ... },
    "metrics": { ... }
  }
]
```

## WebSocket Events

### Reputation Update
```json
{
  "event": "reputation_updated",
  "mechanic_id": 1,
  "tenant_id": "tenant_default",
  "new_score": 85,
  "previous_score": 80
}
```

## Frontend Components

### RepScoreBadge
```tsx
<RepScoreBadge score={85} />
```

### RepBreakdownCard
```tsx
<RepBreakdownCard
  totalScore={85}
  componentScores={{
    certification_status: 20,
    experience_depth: 16,
    performance: 22,
    recent_activity: 15,
    compliance: 12
  }}
/>
```

### MechanicProfileCard
```tsx
<MechanicProfileCard
  mechanic={{
    node_id: 1,
    properties: { name: "John Doe", email: "john@example.com" },
    profile: { license_number: "FAA-12345" },
    reputation: { total_score: 85, ... }
  }}
  onEdit={() => {}}
  onAssign={() => {}}
/>
```
