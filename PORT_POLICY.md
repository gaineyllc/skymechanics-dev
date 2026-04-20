# Port Policy for SkyMechanics

## MANDATORY PORT RULES

**All new services MUST use ports 8200+ to avoid conflicts with vLLM (port 8000).**

### Port Ranges Summary

| Range | Purpose | Status |
|-------|---------|--------|
| 8000 | vLLM (LLM inference) | Reserved - Qwen3-Coder-Next-FP8 |
| 8200-8299 | Backend services | **ACTIVE** |
| 3000-3099 | Frontend services | Active |
| 5432 | PostgreSQL | Active (auth service) |
| 6379 | FalkorDB/Redis | Active |
| 9090-9199 | Monitoring | Active |
| 30000-32767 | Kubernetes NodePort | Not used |

### Backend Service Ports

| Service | Port | Status |
|---------|------|--------|
| Auth Service | 8200 | Production |
| Mechanics Service | 8201 | Production |
| Jobs Service | 8202 | Production |

## Configuration Files Updated

The following files have been updated to use port 8200+:

1. **`backend/main.py`** - Default port changed to 8200
2. **`k8s/auth-service.yaml`** - All ports changed to 8200
3. **`k8s/mechanics-service.yaml`** - All ports changed to 8201
4. **`k8s/jobs-service.yaml`** - All ports changed to 8202
5. **`PLAN.md`** - Updated service endpoints section

## Enforcement

To prevent port 8000 conflicts in the future:

1. **Pre-commit hook**: Check for `port=8000` or `PORT=8000` in new code
2. **Code review**: Verify port assignments before merging
3. **Documentation**: Update this file when adding new services

## Troubleshooting

If you see "address already in use" on port 8000:
- Check for vLLM process: `ps aux | grep vllm`
- Check for uvicorn: `ps aux | grep uvicorn`
- Find process using port: `lsof -i :8000`

## Historical Context

Port 8000 was originally chosen for the backend, but vLLM was later added for local LLM inference. To avoid conflicts, all new services use 8200+ range.
