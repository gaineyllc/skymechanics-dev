# SkyMechanics ClickHouse Service

## Overview
Time-series database for analytics, reporting, and metrics.

## Ports
- **9000**: ClickHouse native protocol
- **8123**: HTTP API

## Docker Compose

```bash
cd services/clickhouse
docker-compose up -d
```

## Data Models

### Jobs Fact Table
```sql
CREATE TABLE jobs_fact (
  job_id String,
  tenant_id String,
  mechanic_id UInt32,
  aircraft_id UInt32,
  status LowCardinality(String),
  duration_minutes UInt32,
  revenue Decimal(10,2),
  created_at DateTime,
  completed_at DateTime
) ENGINE = MergeTree()
ORDER BY (tenant_id, created_at);
```

### Mechanic Metrics Aggregate
```sql
CREATE TABLE mechanic_metrics (
  mechanic_id UInt32,
  date Date,
  jobs_completed UInt32,
  total_hours Decimal(5,2),
  avg_rating Decimal(3,2)
) ENGINE = AggregatingMergeTree()
ORDER BY (mechanic_id, date);
```

## Schema Setup

Run after ClickHouse starts:

```bash
docker exec -it skymechanics-clickhouse clickhouse-client \
  --query "CREATE DATABASE IF NOT EXISTS skymechanics"
```

Then execute schema files from `backend/analytics/schema/`.
