# SkyMechanics CI/CD Pipeline

## GitHub Actions Workflows

### Build and Deploy

```yaml
name: Build and Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service: [frontend, auth-service, mechanics-service, jobs-service]

    steps:
    - uses: actions/checkout@v3

    - name: Set up QEMU
      uses: docker/setup-qemu-action@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Login to GitHub Container Registry
      uses: docker/login-action@v3
      with:
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}

    - name: Build and push Docker image
      uses: docker/build-push-action@v5
      with:
        context: ./${{ matrix.service }}
        push: true
        tags: ghcr.io/gaineyllc/${{ matrix.service }}:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production

    steps:
    - name: Deploy to Kubernetes
      run: |
        kubectl set image deployment/${{ matrix.service }} \
          ${{ matrix.service }}=ghcr.io/gaineyllc/${{ matrix.service }}:${{ github.sha }}
```

### Memory Check Workflow

```yaml
name: Memory Check

on:
  schedule:
    - cron: '0 */4 * * *'  # Every 4 hours
  workflow_dispatch:

jobs:
  check-memory:
    runs-on: ubuntu-latest
    steps:
    - name: Check Memory
      run: |
        echo "Current memory usage:"
        free -h
        echo ""
        echo "Docker container memory:"
        docker stats --no-stream --format "table {{.Name}}\t{{.MemPerc}}"
```

### Resource Alert Workflow

```yaml
name: Resource Alert

on:
  workflow_run:
    workflows: ["Build and Deploy"]
    types:
      - completed

jobs:
  alert:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    steps:
    - name: Alert on Failure
      run: |
        echo "Build/Deploy failed!"
        echo "Check logs and system resources"
```

## Helm Charts

### Generate Helm Charts

```bash
# Install Helm if not already installed
curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Create Helm charts
helm create skymechanics
```

## Kubernetes Manifests

All manifests are in `k8s/` directory:

- `namespace.yaml` - Namespace and RBAC
- `falkordb.yaml` - FalkorDB StatefulSet
- `postgres.yaml` - PostgreSQL StatefulSet
- `redis.yaml` - Redis Deployment
- `auth-service.yaml` - Auth Service
- `mechanics-service.yaml` - Mechanics Service
- `jobs-service.yaml` - Jobs Service
- `ingress.yaml` - Traefik Ingress
- `metrics-server.yaml` - Resource Monitoring

## Local Testing

```bash
# Deploy locally with k3d
k3d cluster create skymechanics-dev
kubectl apply -f k8s/

# Monitor resources
./k8s/monitor-resources.sh check
```
