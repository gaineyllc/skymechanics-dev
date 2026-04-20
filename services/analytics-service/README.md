# SkyMechanics Analytics Service

FastAPI service for business intelligence, reporting, and metrics.

## Ports
- **8203**: Analytics service (follows 8200+ pattern)

## Docker Build
```bash
docker build -t ghcr.io/gaineyllc/analytics-service:latest -f services/analytics-service/Dockerfile .
```

## Docker Run
```bash
docker run -d -p 8203:8203 \
  --env PORT=8203 \
  --env CLICKHOUSE_HOST=clickhouse \
  --env CLICKHOUSE_PORT=9000 \
  ghcr.io/gaineyllc/analytics-service:latest
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/ready` | GET | Readiness probe |
| `/api/v1/metrics/fleet` | GET | Fleet utilization metrics |
| `/api/v1/metrics/mechanics` | GET | Mechanic workload metrics |
| `/api/v1/metrics/revenue` | GET | Revenue tracking metrics |
| `/docs` | GET | Swagger UI |

## Metrics Served

### Fleet Metrics
- Total aircraft count
- In-service vs maintenance breakdown
- Utilization rate

### Mechanic Metrics
- Total/active mechanics
- Jobs completed
- Average jobs per mechanic

### Revenue Metrics
- Daily, monthly, yearly revenue
- Trend comparisons

## Database Integration

ClickHouse for time-series analytics:
- Jobs fact table for duration tracking
- Mechanic metrics aggregates
- Custom reporting queries

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 8203 | Service port |
| `CLICKHOUSE_HOST` | clickhouse | ClickHouse hostname |
| `CLICKHOUSE_PORT` | 9000 | ClickHouse native port |
| `CLICKHOUSE_USER` | default | ClickHouse username |
| `CLICKHOUSE_PASSWORD` | (empty) | ClickHouse password |
