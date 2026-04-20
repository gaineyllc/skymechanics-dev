# SkyMechanics K8s Documentation

## Quick Start

```bash
# Setup local environment with memory monitoring
chmod +x k8s/*.sh
./k8s/setup-local.sh

# Setup K3d cluster
cd k8s
./setup-k3d.sh

# Deploy all services
./deploy-all.sh

# Monitor resources
./monitor-resources.sh check
./monitor-resources.sh monitor
```

**Note**: Requires sudo for k3d/kubectl/helm installation. See `k8s/MANUAL-SETUP.md` for details.

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                   Kubernetes Cluster                         │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐ │
│  │  Ingress │  │ Auth SVC │  │Mech SVC  │  │ Jobs SVC   │ │
│  │ Traefik  │  │  :8000   │  │  :8001   │  │  :8002     │ │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘  └─────┬──────┘ │
│        │             │             │             │          │
│  ┌─────▼─────────────▼─────────────▼─────────────▼──────┐  │
│  │              FalkorDB (Graph DB) :6379                 │  │
│  │              PostgreSQL (TimescaleDB) :5432            │  │
│  │              Redis (Cache) :6379                       │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              Metrics Server (resource monitoring)      │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## Resource Limits

All services have memory and CPU limits configured to protect your host:

| Service | Requests | Limits | Memory-Safe |
|---------|----------|--------|-------------|
| FalkorDB | 256Mi | 512Mi | ✅ |
| PostgreSQL | 512Mi | 1Gi | ✅ |
| Redis | 128Mi | 256Mi | ✅ |
| Auth Service | 256Mi | 512Mi | ✅ |
| Mechanics Service | 256Mi | 512Mi | ✅ |
| Jobs Service | 256Mi | 512Mi | ✅ |
| **Total** | ~1.75Gi | ~3.5Gi | ✅ |

## Memory Monitoring

### Continuous Monitoring
```bash
./k8s/monitor-resources.sh monitor
```

### One-time Check
```bash
./k8s/monitor-resources.sh check
```

### System-wide Alert
```bash
./k8s/monitor-resources.sh alert-script
```

The alert script monitors host memory and sends Telegram notifications when usage exceeds 85%.

## Service Endpoints

| Service | Port | URL |
|---------|------|-----|
| Auth | 8000 | http://localhost:8000 |
| Mechanics | 8001 | http://localhost:8001 |
| Jobs | 8002 | http://localhost:8002 |
| FalkorDB Browser | 3000 | http://localhost:3000 |
| PostgreSQL | 5432 | localhost:5432 |
| Redis | 6379 | localhost:6379 |

## Local Port Forwarding

To access services from your host machine:

```bash
# FalkorDB
kubectl port-forward -n skymechanics svc/falkordb 6379:6379 &

# PostgreSQL
kubectl port-forward -n skymechanics svc/postgres 5432:5432 &

# Auth Service
kubectl port-forward -n skymechanics svc/auth-service 8000:8000 &

# Mechanics Service
kubectl port-forward -n skymechanics svc/mechanics-service 8001:8001 &

# Jobs Service
kubectl port-forward -n skymechanics svc/jobs-service 8002:8002 &
```

## Clean Up

```bash
# Stop all services
./k8s/undeploy-all.sh

# Remove K3d cluster
k3d cluster delete skymechanics-dev
```

## Troubleshooting

### High Memory Usage
```bash
# Check current memory
./k8s/monitor-resources.sh check

# View pod resource usage
kubectl top pods -n skymechanics

# Check container stats
docker stats
```

### Service Not Responding
```bash
# Check pod status
kubectl get pods -n skymechanics

# Check logs
kubectl logs -n skymechanics <pod-name>

# Restart pod
kubectl rollout restart deployment -n skymechanics <deployment-name>
```

### Database Connection Issues
```bash
# Check FalkorDB
kubectl exec -n skymechanics <falkordb-pod> -- redis-cli -a <password> ping

# Check PostgreSQL
kubectl exec -n skymechanics <postgres-pod> -- pg_isready -U postgres
```

## Next Steps

1. **Monitor resources** - Keep `skymem monitor` running
2. **Check memory pressure** - System alerts at 85% usage
3. **Review service logs** - `kubectl logs -n skymechanics <pod>`
4. **Scale up as needed** - Increase replicas if load increases

---

**Safety First**: Your system has 121 GiB RAM. The K8s cluster uses ~3.5 GiB max. Memory alerts trigger at 85% host usage to protect your host system.
