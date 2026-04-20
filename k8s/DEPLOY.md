# Helm Chart for SkyMechanics

## Installation

```bash
# Apply required resources first
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/rbac.yaml
kubectl apply -f k8s/falkordb.yaml
kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/prometheus.yaml
kubectl apply -f k8s/grafana/grafana.yaml

# Apply network policies
kubectl apply -f k8s/network-policy.yaml

# Apply services
kubectl apply -f k8s/auth-service.yaml
kubectl apply -f k8s/mechanics-service.yaml
kubectl apply -f k8s/jobs-service.yaml

# Apply HPA
kubectl apply -f k8s/hpa/services-hpa.yaml

# Apply ingress
kubectl apply -f k8s/ingress.yaml
```

## Verification

```bash
# Check all pods
kubectl get pods -n skymechanics

# Check services
kubectl get svc -n skymechanics

# Check HPA status
kubectl get hpa -n skymechanics

# Check ingress
kubectl get ingress -n skymechanics
```

## Accessing Services

### Port-forward for development

```bash
# Auth service
kubectl port-forward -n skymechanics svc/auth-service 8200:8200

# Mechanics service
kubectl port-forward -n skymechanics svc/mechanics-service 8201:8201

# Jobs service
kubectl port-forward -n skymechanics svc/jobs-service 8202:8202

# Prometheus
kubectl port-forward -n skymechanics svc/prometheus 9090:9090

# Grafana
kubectl port-forward -n skymechanics svc/grafana 3000:3000

# Redis Insight
kubectl port-forward -n skymechanics svc/redis-insight 5540:5540
```

### Kubernetes Dashboard

```bash
# Deploy dashboard
kubectl apply -f k8s/dashboard.yaml
kubectl apply -f k8s/dashboard-rbac.yaml

# Get token
kubectl -n kubernetes-dashboard create token admin-user

# Port-forward
kubectl port-forward -n kubernetes-dashboard svc/kubernetes-dashboard 8443:443

# Access
https://localhost:8443
```

## Testing Endpoints

```bash
# Health check
curl http://localhost:8200/api/v1/health
curl http://localhost:8201/api/v1/health
curl http://localhost:8202/api/v1/health

# Ready check
curl http://localhost:8200/api/v1/ready
curl http://localhost:8201/api/v1/ready
curl http://localhost:8202/api/v1/ready

# WebSocket test (Python)
python3 << 'EOF'
import websockets
import asyncio

async def test():
    async with websockets.connect("ws://localhost:8200/api/v1/events/ws/mechanics/1/updates") as ws:
        print(f"Connected to mechanics service")
        response = await ws.recv()
        print(f"Response: {response}")

asyncio.run(test())
EOF
```

## Troubleshooting

### Pod not starting

```bash
# Check pod logs
kubectl logs <pod-name> -n skymechanics

# Check events
kubectl events -n skymechanics

# Describe pod
kubectl describe pod <pod-name> -n skymechanics
```

### Service not responding

```bash
# Check service endpoints
kubectl get endpoints <service-name> -n skymechanics

# Test connectivity
kubectl exec -it <pod-name> -n skymechanics -- curl http://localhost:8200/api/v1/health
```

### Network policy blocking

```bash
# Check network policy
kubectl get networkpolicy -n skymechanics

# Test without network policy
kubectl patch networkpolicy skymechanics-tenant-isolation -n skymechanics -p '{"spec":{"podSelector":{}}}'
```

## Scaling Services

```bash
# Manual scaling
kubectl scale deployment auth-service -n skymechanics --replicas=5

# HPA will automatically scale based on CPU/memory
kubectl get hpa -n skymechanics
```

## Updating Services

```bash
# Update image
kubectl set image deployment/auth-service auth-service=ghcr.io/gaineyllc/auth-service:v1.0.1 -n skymechanics

# Watch rollout status
kubectl rollout status deployment/auth-service -n skymechanics

# Rollback if needed
kubectl rollout undo deployment/auth-service -n skymechanics
```
