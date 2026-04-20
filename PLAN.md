# SkyMechanics: Infrastructure & Development Plan

## Vision

Scale from MVP to Uber-like platform while staying within free-tier constraints during development.

---

## Phase 0: Foundation (Current) - **Completed**

### Stack
| Component | Tool | Free Tier | Notes |
|-----------|------|-----------|-------|
| API | FastAPI | ✅ | Python web framework |
| DB | FalkorDB | ✅ | Graph database |
| Auth | JWT | ✅ | Custom implementation |
| Frontend | React | ✅ | Vite build |
| Hosting | VPS | ✅ | Self-hosted |

### What's Done
- [x] Multi-tenant architecture (graph-per-tenant)
- [x] Onboarding flow with tenant creation
- [x] Aircraft & Mechanic management
- [x] Basic job workflow

---

## Phase 1: Service Breakout & Caching (2-3 weeks)

### Goal: Decouple services, add Redis caching, prepare for scale

### New Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway (envoy)                      │
│              /api/v1/* → route to services                  │
└─────────────────────────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼───────┐  ┌─────────▼─────────┐  ┌──────▼───────┐
│  Auth Service │  │ Mechanic Service │  │ Jobs Service │
│   (FastAPI)   │  │   (FastAPI)      │  │  (FastAPI)   │
└───────────────┘  └──────────────────┘  └──────────────┘
                             │
                   ┌─────────▼─────────┐
                   │   Redis Cache     │
                   │   (port 6379)     │
                   └───────────────────┘
```

### Implementation Tasks

#### 1. Extract Auth Service
```
backend/auth-service/
├── main.py              # FastAPI app
├── routes/
│   ├── auth.py          # Login, register, token refresh
│   ├── users.py         # User CRUD
│   └── permissions.py   # Role-based access
├── models/
│   ├── user.py
│   └── token.py
├── db.py                # PostgreSQL connection
└── requirements.txt
```

**Database**: PostgreSQL (free tier via Neon.tech or Supabase)
- Users table
- Refresh tokens table
- Audit log table

#### 2. Extract Mechanic Service
```
backend/mechanics-service/
├── main.py
├── routes/
│   ├── mechanics.py
│   ├── profiles.py
│   └── availability.py
├── onboarding.py        # Tenant onboarding helpers
├── models/
│   └── mechanic.py
└── requirements.txt
```

**Database**: FalkorDB (keep existing)

#### 3. Extract Jobs Service
```
backend/jobs-service/
├── main.py
├── routes/
│   ├── jobs.py
│   ├── jobsheets.py
│   └── billing.py
├── models/
│   └── job.py
└── requirements.txt
```

**Database**: FalkorDB + PostgreSQL (for billing records)

#### 4. Add Redis Caching Layer
```
redis/
└── docker-compose.yml   # Redis + RedisInsight
```

**Caching Strategy**:
| Key Pattern | TTL | Content |
|-------------|-----|---------|
| `tenant:{id}` | 1h | Tenant metadata |
| `mechanic:{id}` | 30m | Mechanic profile |
| `job:{id}` | 15m | Active job status |
| `location:{id}` | 5m | Real-time location |
| `cache:stats` | 1m | Cache hit/miss stats |

### Free Tool Alternatives
| Need | Paid Option | Free Option | Recommendation |
|------|-------------|-------------|----------------|
| PostgreSQL | AWS RDS | **Neon.tech** | Serverless PostgreSQL |
| PostgreSQL | Supabase Pro | **Supabase Free** | DB + Auth + Storage |
| Redis | AWS ElastiCache | **Redis Cloud Free** | 30MB, no cluster |
| Monitoring | Datadog | **Prometheus + Grafana** | Self-hosted |
| Logging | Loggly | **Grafana Loki** | Self-hosted |

---

## Phase 2: Real-Time & Event-Driven (3-4 weeks)

### Goal: WebSocket streams, location tracking, job dispatch

### New Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     WebSocket Gateway                        │
│              /ws/* → broadcast to clients                   │
└─────────────────────────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼───────┐  ┌─────────▼─────────┐  ┌──────▼───────┐
│  Auth Service │  │ Mechanic Service │  │ Jobs Service │
│   (FastAPI)   │  │   (FastAPI)      │  │  (FastAPI)   │
└───────────────┘  └──────────────────┘  └──────────────┘
                             │
                   ┌─────────▼─────────┐
                   │   Redis Pub/Sub   │
                   │   Kafka Lite      │
                   └───────────────────┘
```

### Implementation Tasks

#### 1. WebSocket Implementation
**Location**: All services (add `/ws` endpoints)

```python
# Example in mechanics-service
@router.websocket("/ws/mechanics/{mechanic_id}/updates")
async def mechanic_updates(websocket: WebSocket, mechanic_id: int):
    await websocket.accept()
    # Subscribe to Redis channel
    # Broadcast updates to connected clients
```

**Events to stream**:
- `mechanic:location_updated` - GPS coordinate changes
- `job:status_changed` - Job status updates
- `job:assigned` - New job assignment
- `mechanic:availability_changed` - Schedule updates

#### 2. Kafka Lite (Message Queue)
**Tool**: [Redpanda Console](https://redpanda.com/download) (free, lightweight Kafka alternative)

**Topics**:
| Topic | Events |
|-------|--------|
| `mechanic.locations` | GPS pings, geofence events |
| `job.status` | Created, started, completed, cancelled |
| `job.dispatch` | Assignment events |
| `audit.events` | All system events |
| `billing.events` | Invoice events |

#### 3. Location Tracking Service
**Database**: PostgreSQL with PostGIS extension

```sql
-- Spatial index for proximity queries
CREATE INDEX idx_mechanic_location ON mechanics 
USING GIST (ST_SetSRID(ST_MakePoint(longitude, latitude), 4326));

-- Function to find nearby mechanics
CREATE OR REPLACE FUNCTION find_nearby_mechanics(
  lat FLOAT, lng FLOAT, radius_km INT
) RETURNS TABLE AS $$
  SELECT * FROM mechanics
  WHERE ST_DWithin(
    ST_SetSRID(ST_MakePoint(longitude, latitude), 4326),
    ST_SetSRID(ST_Point($1, $2), 4326),
    $3 * 1000
  );
$$ LANGUAGE sql;
```

#### 4. Frontend WebSocket Client
```typescript
// frontend/src/services/websocket.ts
class WebSocketClient {
  private connections = new Map<string, WebSocket>();

  connect(endpoint: string, onMessage: (data: any) => void) {
    const ws = new WebSocket(`ws://${endpoint}`);
    ws.onmessage = (event) => onMessage(JSON.parse(event.data));
    this.connections.set(endpoint, ws);
    return ws;
  }

  subscribe(topic: string, callback: (data: any) => void) {
    // Subscribe to Redis/Kafka topic via backend
  }
}
```

---

## Phase 3: Analytics & Reporting (2-3 weeks)

### Goal: Business intelligence, utilization metrics, revenue tracking

### New Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     Analytics Pipeline                       │
│                                                              │
│  [Services] → [Kafka] → [ClickHouse] → [Superset]          │
│                              ↓                              │
│                         [Dashboard UI]                       │
└─────────────────────────────────────────────────────────────┘
```

### Implementation Tasks

#### 1. ClickHouse (Time-Series Database)
**Why**: Free tier available, excellent for time-series analytics
**Use Cases**:
- Job duration tracking
- Mechanic utilization metrics
- Fleet availability analytics

#### 2. Apache Superset (Dashboard)
**Free**: Self-hosted
**Dashboards**:
- Fleet utilization (% of aircraft in service)
- Mechanic workload (jobs/hour)
- Revenue by tenant
- Customer satisfaction (ratings)

#### 3. Analytics Data Model
```sql
-- Jobs fact table
CREATE TABLE jobs_fact (
  job_id UUID,
  tenant_id VARCHAR,
  mechanic_id INT,
  aircraft_id INT,
  status VARCHAR,
  duration_minutes INT,
  revenue DECIMAL(10,2),
  created_at TIMESTAMP,
  completed_at TIMESTAMP
);

-- Mechanic metrics aggregate table
CREATE TABLE mechanic_metrics (
  mechanic_id INT,
  date DATE,
  jobs_completed INT,
  total_hours DECIMAL(5,2),
  avg_rating DECIMAL(3,2),
  PRIMARY KEY (mechanic_id, date)
);
```

---

## Phase 4: Mobile App (4-6 weeks)

### Goal: iOS/Android apps for mechanics

### Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     Mobile Clients                           │
│                    (React Native)                            │
└─────────────────────────────────────────────────────────────┘
                             │
                   ┌─────────▼─────────┐
                   │  API Gateway       │
                   │  (Rate Limiting)   │
                   └───────────────────┘
```

### Free Tools
| Need | Tool | Notes |
|------|------|-------|
| Cross-platform | **React Native** | Free, large community |
| Auth | **Auth0 Free Tier** | Or Supabase Auth |
| Push Notifications | **Firebase Cloud Messaging** | Free tier |
| App Distribution | **Firebase App Distribution** | Free beta testing |
| Crash Reporting | **Sentry** | Free tier |

---

## Phase 5: Production Scaling (Ongoing)

### Infrastructure Checklist

| Area | Free/Dev Option | Production Option |
|------|-----------------|-------------------|
| Hosting | VPS (DigitalOcean) | Kubernetes (EKS/GKE) |
| Database | Self-hosted FalkorDB | FalkorDB cloud |
| Auth | Custom JWT | Auth0 + custom providers |
| CI/CD | GitHub Actions | GitHub Actions (same) |
| Monitoring | Prometheus + Grafana | Datadog / New Relic |
| Logging | Loki | CloudWatch / Papertrail |
| CDN | None | Cloudflare / Bunny.net |

### Cost Optimization Strategies

1. **Use Supabase for MVP**:
   - Free PostgreSQL
   - Built-in Auth
   - Storage (1GB)
   - Realtime (WebSockets)
   - **Saves**: $100+/month in infrastructure

2. **Self-host监控 tools**:
   - Prometheus + Grafana (free)
   - Loki for logs (free)
   - Alertmanager for alerts (free)

3. **Gradual migration**:
   - Start with free tiers
   - Track usage metrics
   - Upgrade only when needed

---

## Implementation Roadmap (Timeline)

| Week | Phase | Deliverables |
|------|-------|--------------|
| 1-2 | Phase 1 | Auth/Job/Mechanic services, Redis caching |
| 3-5 | Phase 2 | WebSocket streams, Kafka Lite, location tracking |
| 6-7 | Phase 3 | ClickHouse setup, Superset dashboards |
| 8-11 | Phase 4 | React Native MVP, testing |
| 12+ | Phase 5 | Production deployment, monitoring |

**Total estimated**: 12-16 weeks for full platform

---

## Risk Assessment & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| FalkorDB scaling | Medium | Test cluster size, add read replicas |
| Real-time latency | High | Use Redis Pub/Sub, optimize WebSocket |
| Mobile app complexity | High | Use Expo for faster development |
| Cost overruns | Medium | Start with Supabase free tier |

---

## Immediate Next Steps

**Do this week**:
1. [ ] Create service repositories (auth, mechanics, jobs)
2. [ ] Set up Redis cache
3. [ ] Create shared models package
4. [ ] Document API contracts between services
5. [ ] Set up CI/CD pipeline (GitHub Actions)

**Ready to proceed?** I can:
- Generate the service templates
- Create the shared models package
- Set up the GitHub repository structure

Which should I prioritize?
