# Production Deployment Configuration

## Production Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Load Balancer (nginx)                     │
│                         Port 80 → 8080                          │
└─────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
┌───────▼───────┐         ┌────────▼────────┐        ┌──────────▼──────────┐
│  Frontend     │         │   Backend API   │        │   Redis Cluster     │
│  React App    │         │   FastAPI       │        │   (Caching/Pub/Sub) │
│  Port 3003    │         │   Port 8080     │        │   Ports 6380, 8001  │
└───────────────┘         └─────────────────┘        └─────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
            ┌───────▼───────┐ ┌─────▼───────┐ ┌────▼────────────────┐
            │   FalkorDB    │ │   Redis    │ │   vLLM AI Server   │
            │   Graph DB    │ │   Backup   │ │   (Qwen3-Coder)    │
            │   Port 6379   │ │   Sync     │ │   Port 8000        │
            └───────────────┘ └────────────┘ └────────────────────┘
```

## Docker Compose Configuration

See `docker-compose.yml` for:
- FalkorDB with multi-tenancy enabled
- Redis Stack for caching and Pub/Sub
- Backend API with production environment
- Frontend with optimized builds

## Environment Variables

```bash
# Production (backend)
host=falkordb
port=6379
REDIS_HOST=redis
REDIS_PORT=6379
FALKORDB_PASSWORD=your_password
vllm_url=http://100.69.118.20:8000
ENV=production
```

## Deployment Commands

### Build and Start
```bash
docker compose up -d --build
```

### View Logs
```bash
docker compose logs -f api
```

### Stop Services
```bash
docker compose down
```

### Stop and Remove Volumes
```bash
docker compose down -v
```

## Monitoring

### RedisInsight (Admin UI)
- URL: `http://localhost:8001`
- Default credentials: `admin` / `admin`

### Health Check
```bash
curl http://localhost:8080/api/v1/health
```

### Ready Check
```bash
curl http://localhost:8080/api/v1/ready
```

## Backup Strategy

### FalkorDB
```bash
docker compose exec falkordb redis-cli BGSAVE
docker compose exec falkordb redis-cli SAVE
```

### Redis
```bash
docker compose exec redis redis-cli BGSAVE
docker compose exec redis redis-cli SAVE
```

### Manual Backup
```bash
# Backup FalkorDB data
docker compose exec falkordb cp -r /data /backups/falkordb-$(date +%Y%m%d)

# Backup Redis data  
docker compose exec redis cp -r /data /backups/redis-$(date +%Y%m%d)
```

## Performance Tuning

### FalkorDB Configuration
```yaml
environment:
  - FALKORDB_MAX_GRAPHS=100
```

### Redis Configuration
```yaml
environment:
  - REDIS_ARGS=--maxmemory 2gb --maxmemory-policy allkeys-lru
```

### Backend Connection Pool
- FalkorDB: 100 connections
- Redis: 150 total connections (separated pools)
- vLLM: 25 concurrent requests

## Security

### TLS/SSL (Production)
```bash
# Use nginx with Let's Encrypt
# See: https://nginx.org/en/docs/http/configuring_https_servers.html
```

### Authentication
- JWT tokens for API authentication
- Redis for token storage (production)
- Tenant isolation in FalkorDB graphs

### Network Security
- Internal docker network for microservices
- Host-only ports for external access
- Firewall rules recommended for production

## Scaling

### Horizontal Scaling
```bash
# Multiple backend instances
docker compose up -d --scale api=3
```

### Vertical Scaling
```yaml
# Increase resource limits in docker-compose.yml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

## CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Server
        run: |
          ssh user@production "cd /path/to/skymechanics-dev && docker compose pull && docker compose up -d"
```

## Rollback

### Rollback to Previous Version
```bash
# Restore from backup
docker compose exec falkordb redis-cli --rdb /backups/falkordb-20240101.rdb
docker compose exec redis redis-cli --rdb /backups/redis-20240101.rdb

# Restart services
docker compose restart
```

## Troubleshooting

### Services Not Starting
```bash
# Check logs
docker compose logs

# Check health
docker compose ps
```

### Database Connection Issues
```bash
# Test FalkorDB
docker compose exec falkordb redis-cli ping

# Test Redis
docker compose exec redis redis-cli ping
```

### Backend Not Responding
```bash
# Check backend logs
docker compose logs api

# Restart backend
docker compose restart api
```

## Production Checklist

- [ ] TLS/SSL certificates configured
- [ ] Environment variables set for production
- [ ] Backup automation configured
- [ ] Monitoring dashboard set up
- [ ] Security audit completed
- [ ] Load testing performed
- [ ] Documentation complete
- [ ] Rollback plan tested
