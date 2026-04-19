# SkyMechanics Platform - Deployment Status

## Running Services

| Service | Status | Port |
|---------|--------|------|
| skymechanics-api | Running | 8080 → 8000 |
| skymechanics-falkordb | Healthy | 3000 (HTTP), 6379 (Redis) |
| skymechanics-browser | Running | 3001 |

## API Endpoints

- **Health Check**: http://localhost:8080/health
- **Swagger UI**: http://localhost:8080/docs
- **OpenAPI**: http://localhost:8080/openapi.json
- **Query API**: POST http://localhost:8080/query

## Sample Data

- 3 customers (John Smith, Jane Doe, Bob Johnson)
- 3 mechanics (Alice Williams, Charlie Brown, Diana Prince)
- 3 jobs (Engine Repair, Brake Replacement, Diagnostic Check)

## Ports Used

- 8000: vLLM (existing)
- 8080: FastAPI API
- 6379: FalkorDB Redis protocol
- 3000: FalkorDB HTTP/Browser
- 3001: FalkorDB Browser (optional)
