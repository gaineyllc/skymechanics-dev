# SkyMechanics: Kubernetes-Native Architecture Plan

## Vision

Build SkyMechanics as a **cloud-native microservices platform** from Day 1, designed to scale to Uber-level traffic with Kubernetes as the foundation.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Kubernetes Cluster                              │
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │
│  │  Ingress    │  │  API Gateway│  │  Auth SVC   │  │  Redis    │  │
│  │  (Traefik)  │  │ (Envoy)     │  │ (FastAPI)   │  │  Cluster  │  │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └─────┬─────┘  │
│         │                 │                 │               │       │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐  ┌─────▼─────┐  │
│  │Mechanics SVC│  │  Jobs SVC   │  │ Tenants SVC │  │Kafka      │  │
│  │ (FastAPI)   │  │ (FastAPI)   │  │ (FastAPI)   │  │  Cluster  │  │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └─────┬─────┘  │
│         │                 │                 │               │       │
│  ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐  ┌─────▼─────┐  │
│  │ FalkorDB    │  │ PostgreSQL  │  │ FalkorDB    │  │ClickHouse │  │
│  │  Cluster    │  │  (Timescale)│  │  Per-Tenant │  │  Cluster  │  │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────┘   │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                   Service Mesh (Istio)                       │  │
│  │              mTLS, tracing, observability                    │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Core Kubernetes Components

### 1. Ingress Controller
| Tool | Free Tier | Notes |
|------|-----------|-------|
| Traefik | ✅ | Easy config, dashboard |
| NGINX Ingress | ✅ | Industry standard |
| Envoy Gateway | ✅ | Modern, API-driven |

**Recommendation**: **Traefik** for simplicity during development

### 2. Service Mesh (Optional for MVP)
| Tool | Free Tier | Notes |
|------|-----------|-------|
| Istio | ✅ | Feature-rich, complex |
| Linkerd | ✅ | Lightweight, easy |
| Kuma | ✅ | Universal, simple |

**Recommendation**: **Start without mesh**, add Linkerd later for observability

### 3. Service Discovery
- Kubernetes DNS (built-in)
- CoreDNS for custom DNS rules

### 4. Config Management
| Tool | Free Tier | Notes |
|------|-----------|-------|
| ConfigMaps | ✅ | Kubernetes native |
| Secrets | ✅ | Kubernetes native |
| External Secrets | ✅ | Sync from vaults |
| Velero | ✅ | Backup/restore |

---

## Phase 0: Kubernetes Migration Preparation (1 week)

### Prerequisites Checklist

| Task | Tool | Notes |
|------|------|-------|
| Local Kubernetes | **Minikube** / **Kind** | Development cluster |
| Cluster Management | **k3d** | Lightweight dev cluster |
| Kubernetes IDE | **Lens** | Visual cluster management |
| YAML Linting | **kubeval** / **kubeconform** | Validation |
| Helm Linting | **helm lint** | Chart validation |

### Docker Image Strategy

**Multi-stage builds for each service**:

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# Stage 2: Runtime
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

**Registry Options**:
- **Docker Hub** (free tier)
- **GitHub Container Registry** (free for public repos)
- **Google Container Registry** (free tier)

---

## Phase 1: Kubernetes-Native Services (3-4 weeks)

### Service Architecture

```
frontend/
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── hpa.yaml
└── Dockerfile

auth-service/
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── hpa.yaml
└── Dockerfile

mechanics-service/
├── k8s/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── pvc.yaml (FalkorDB client config)
│   └── hpa.yaml
└── Dockerfile
```

### Service Definitions

#### 1. Auth Service

**deployment.yaml**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: auth-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: auth-service
  template:
    metadata:
      labels:
        app: auth-service
    spec:
      containers:
      - name: auth-service
        image: ghcr.io/gaineyllc/auth-service:latest
        ports:
        - containerPort: 8000
        env:
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: auth-db-credentials
              key: host
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: auth-secrets
              key: jwt-secret
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: auth-service
spec:
  selector:
    app: auth-service
  ports:
  - port: 8000
    targetPort: 8000
  type: ClusterIP
```

**ConfigMaps & Secrets**:
- `configmap.yaml`: App configuration
- `secret.yaml`: Database credentials, JWT secrets

#### 2. Mechanics Service

**deployment.yaml** (FalkorDB-focused):
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mechanics-service
spec:
  replicas: 2  # FalkorDB is stateful, be conservative
  selector:
    matchLabels:
      app: mechanics-service
  template:
    metadata:
      labels:
        app: mechanics-service
    spec:
      containers:
      - name: mechanics-service
        image: ghcr.io/gaineyllc/mechanics-service:latest
        ports:
        - containerPort: 8001
        env:
        - name: FALKORDB_HOST
          value: "falkordb-cluster"
        - name: FALKORDB_PORT
          value: "6379"
        resources:
          requests:
            memory: "512Mi"
            cpu: "200m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        volumeMounts:
        - name: falkordb-config
          mountPath: /app/falkordb
      volumes:
      - name: falkordb-config
        configMap:
          name: falkordb-client-config
```

#### 3. PostgreSQL Service (StatefulSet)

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres-db
spec:
  serviceName: postgres
  replicas: 3
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: timescale/timescaledb:latest-pg14
        ports:
        - containerPort: 5432
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgres-secrets
              key: password
        volumeMounts:
        - name: data
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 10Gi
```

#### 4. FalkorDB Cluster (StatefulSet)

**Key configuration** (load FalkorDB module):

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: falkordb-cluster
spec:
  serviceName: falkordb
  replicas: 3
  selector:
    matchLabels:
      app: falkordb
  template:
    metadata:
      labels:
        app: falkordb
    spec:
      containers:
      - name: falkordb
        image: falkordb/falkordb:latest
        ports:
        - containerPort: 6379
        command: ["redis-server"]
        args:
        - "--loadmodule"
        - "/var/lib/falkordb/bin/falkordb.so"
        - "--requirepass"
        - "$(REDIS_PASSWORD)"
        env:
        - name: REDIS_PASSWORD
          valueFrom:
            secretKeyRef:
              name: falkordb-secrets
              key: password
        volumeMounts:
        - name: data
          mountPath: /data
        - name: module
          mountPath: /var/lib/falkordb/bin
      volumes:
      - name: module
        emptyDir: {}
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 50Gi
```

---

## Phase 2: Redis & Kafka Setup (2 weeks)

### Redis Cluster (Deployment)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-cluster
spec:
  replicas: 3
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
        command: ["redis-server"]
        args:
        - "--cluster-enabled"
        - "yes"
        - "--cluster-config-file"
        - "nodes.conf"
        - "--cluster-node-timeout"
        - "5000"
        volumeMounts:
        - name: config
          mountPath: /usr/local/etc/redis
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
  volumeClaimTemplates:
  - metadata:
      name: config
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 5Gi
```

### Kafka Cluster (KubeRay)

**Alternative**: Use **Redpanda** (lighter, Kafka-compatible)

```yaml
apiVersion: redpanda.vectorized.io/v1alpha1
kind: Cluster
metadata:
  name: redpanda
spec:
  chartRef:
    chartVersion: 5.1.0
  replicas: 3
  resources:
    requests:
      memory: "1Gi"
      cpu: "500m"
    limits:
      memory: "2Gi"
      cpu: "1000m"
```

---

## Phase 3: CI/CD Pipeline (1 week)

### GitHub Actions Workflow

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
        service: [frontend, auth-service, mechanics-service]

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

---

## Phase 4: Observability Stack (2 weeks)

### Prometheus + Grafana

```yaml
# prometheus-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
      - name: prometheus
        image: prom/prometheus:latest
        ports:
        - containerPort: 9090
        volumeMounts:
        - name: config
          mountPath: /etc/prometheus
        - name: data
          mountPath: /prometheus
      volumes:
      - name: config
        configMap:
          name: prometheus-config
      - name: data
        emptyDir: {}
```

### Loki (Logging)

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: loki
spec:
  replicas: 1
  selector:
    matchLabels:
      app: loki
  template:
    metadata:
      labels:
        app: loki
    spec:
      containers:
      - name: loki
        image: grafana/loki:latest
        ports:
        - containerPort: 3100
        volumeMounts:
        - name: data
          mountPath: /loki
      volumes:
      - name: data
        emptyDir: {}
```

---

## Cost Optimization (Free Tier Focus)

| Component | Free Option | Production Option |
|-----------|-------------|-------------------|
| Kubernetes | **K3s** / **k3d** | EKS / GKE |
| Registry | Docker Hub | GHCR / GAR |
| Monitoring | Prometheus + Grafana | Datadog |
| Logging | Loki | CloudWatch |
| CI/CD | GitHub Actions | GitHub Actions (same) |
| Secrets | Kubernetes Secrets | HashiCorp Vault |
| Ingress | Traefik | NGINX Ingress |
| TLS | Let's Encrypt | Cert-Manager + Let's Encrypt |

---

## Implementation Roadmap

| Week | Phase | Deliverables |
|------|-------|--------------|
| 1 | Phase 0 | Local Kubernetes cluster, Helm charts |
| 2-3 | Phase 1 | All services deployed to K8s |
| 4-5 | Phase 2 | Redis cluster, Kafka/Redpanda setup |
| 6 | Phase 3 | CI/CD pipeline working |
| 7-8 | Phase 4 | Observability stack deployed |

---

## Next Steps

1. **Set up local Kubernetes** (k3d or Minikube)
2. **Create Helm charts** for each service
3. **Deploy FalkorDB cluster** to Kubernetes
4. **Migrate existing services** to K8s manifests
5. **Set up CI/CD** with Docker builds

---

## Questions for You

1. **Kubernetes platform preference?**
   - Local: k3d / Minikube / Docker Desktop
   - Cloud: EKS / GKE / AKS (free tier available)
   - Managed: DigitalOcean Kubernetes / Linode Kubernetes

2. **FalkorDB configuration?**
   - Single node (development)
   - 3-node cluster (production-ready)
   - Sentinels vs Cluster mode

3. **Do you want to start with Phase 0 (local cluster setup) or jump to Phase 1 (service manifests)?**

Let me know and I'll generate the actual Kubernetes manifests!
