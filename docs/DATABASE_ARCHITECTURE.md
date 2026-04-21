# SkyMechanics Architecture - Database Plan

## Current Architecture

### Stack
- **FalkorDB** - Primary graph database (multi-tenancy enabled)
- **Redis** - Pub/Sub and caching
- **vLLM** - AI inference (existing integration)
- **FastAPI** - REST API backend

### Database Purpose

| Database | Role | Why This Choice |
|----------|------|-----------------|
| **FalkorDB** | Graph database for all relationships | Multi-tenant native, 496x faster than Neo4j, open source, Redis-compatible |
| Neo4j | Not used | FalkorDB is a superior replacement with same Cypher syntax |
| PostgreSQL | Not used | Graph queries are the primary access pattern, not relational |

## Final State Architecture

```
SkyMechanics Platform
├── FalkorDB (Primary)
│   ├── tenant_{id} graphs (multi-tenancy)
│   ├── Mechanic nodes with certifications
│   ├── Aircraft nodes with type relationships
│   ├── Job nodes linked to mechanics
│   └── Review nodes for reputation scoring
├── Redis (Caching)
│   └── Session storage
│   └── Pub/Sub for real-time updates
└── vLLM (AI)
    └── Mechanic recommendations
    └── Job matching
```

## What We're Building

### Phase 1: Certification Tracking
- Add Certification node type
- Add RepairmanCertificate node type
- Add ExperienceRecord node type
- Relationships: `[:HOLDS]`, `[:EXPERIENCE]`

### Phase 2: Reputation Scoring
- Review graph with ratings
- Performance metrics tracking
- Job completion analytics
- Dynamic reputation calculation

### Phase 3: Job Matching
- Graph queries for mechanic suitability
- Aircraft type matching
- Certification validation
- Geographic proximity scoring

## Query Examples

### Find Qualified Mechanics
```cypher
MATCH (m:Mechanic)-[:HOLDS]->(c:Certification)
WHERE c.certification_type IN ['A&P Mechanic', 'IA']
  AND c.status = 'active'
  AND c.expiry_date > date()
RETURN m, c
```

### Find Mechanics for Aircraft Type
```cypher
MATCH (m:Mechanic)-[:EXPERIENCE]->(at:AircraftType {make: 'Cessna', model: '172'})
RETURN m ORDER BY m.reputation_score DESC
```

### Calculate Reputation
```cypher
MATCH (m:Mechanic)-[:WORKS_ON]->(j:Job)<-[:GIVEN_BY]-(r:Review)
WITH m, AVG(r.rating) as avg_rating, COUNT(r) as review_count
SET m.reputation_score = avg_rating, m.review_count = review_count
RETURN m.name, avg_rating, review_count
```

## Why FalkorDB?

1. **Multi-tenancy native** - Each tenant = isolated graph
2. **Performance** - 6,693 QPS at 8 threads (6.7x Neo4j)
3. **Open source** - Free tier for development
4. **Redis compatible** - Same protocol, easy integration
5. **Cypher support** - Same syntax as Neo4j (migration path)

## Migration Options (Future)

| Migration | Effort | Notes |
|-----------|--------|-------|
| FalkorDB → Neo4j | Low | Same Cypher, just change driver |
| PostgreSQL → FalkorDB | High | Requires graph model redesign |
| Mixed PostgreSQL+FalkorDB | Medium | Use PostgreSQL for analytics |

## Status: ✅ CORRECT ARCHITECTURE

**FalkorDB is the optimal choice** for this multi-tenant graph database platform. No changes needed.
