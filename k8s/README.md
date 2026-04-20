# SkyMechanics Kubernetes Deployment

## Overview
Production Kubernetes manifests for SkyMechanics platform.

## Directory Structure

```
k8s/
├── dev/              # Development environment
├── staging/          # Staging environment
├── prod/             # Production environment
├── services/         # Shared service definitions
├── manifests/        # Kustomize overlays
└── README.md
```

## Prerequisites

- Kubernetes cluster (k3d, EKS, GKE, AKS)
- kubectl configured
- Docker images pushed to GHCR

## Quick Start

```bash
# Create namespace
kubectl apply -f k8s/dev/namespace.yaml

# Deploy all services
kubectl apply -f k8s/dev/

# Check deployment status
kubectl get all -n skymechanics

# View logs
kubectl logs -f deployment/auth-service -n skymechanics

# Scale deployment
kubectl scale deployment auth-service --replicas=3 -n skymechanics
```

## Services

| Service | Port | Replicas | Status |
|---------|------|----------|--------|
| auth-service | 8200 | 2 | Ready |
| mechanics-service | 8201 | 2 | Ready |
| jobs-service | 8202 | 2 | Ready |
| analytics-service | 8203 | 1 | Ready |
| gateway-service | 8204 | 1 | Ready |

## Ingress Configuration

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: skymechanics-ingress
  namespace: skymechanics
spec:
  rules:
  - host: api.skymechanics.com
    http:
      paths:
      - path: /api/v1
        pathType: Prefix
        backend:
          service:
            name: auth-service
            port:
              number: 8200
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| PORT | Service port |
| FALKORDB_HOST | FalkorDB hostname |
| FALKORDB_PORT | FalkorDB port (6379) |
| REDIS_HOST | Redis hostname |
| REDIS_PORT | Redis port (6379) |
| POSTGRES_HOST | PostgreSQL hostname |
| POSTGRES_PORT | PostgreSQL port (5432) |
| CLICKHOUSE_HOST | ClickHouse hostname |
| CLICKHOUSE_PORT | ClickHouse port (9000) |

## Monitoring

### Prometheus Metrics
```bash
kubectl port-forward -n skymechanics svc/prometheus 9090:9090
```

### Grafana Dashboard
```bash
kubectl port-forward -n monitoring svc/grafana 3000:3000
```

## Rollback

```bash
kubectl rollout undo deployment/auth-service -n skymechanics
kubectl rollout history deployment/auth-service -n skymechanics
```

## Scaling

```bash
# Manual scaling
kubectl scale deployment auth-service --replicas=5 -n skymechanics

# Auto-scaling (HPA)
kubectl autoscale deployment auth-service --min=2 --max=10 -n skymechanics
```
