# SkyMechanics Helm Chart

This directory contains Helm chart configuration for SkyMechanics services.

## Chart Structure

```
helm/
├── skymechanics/
│   ├── Chart.yaml          # Chart metadata
│   ├── values.yaml         # Default configuration
│   ├── values.schema.json  # JSON schema for validation
│   ├── templates/
│   │   ├── _helpers.tpl    # Template helpers
│   │   ├── configmap.yaml  # ConfigMaps
│   │   ├── secrets.yaml    # Secrets (templated)
│   │   ├── deployment.yaml # Service deployments
│   │   ├── hpa.yaml        # HorizontalPodAutoscaler
│   │   ├── service.yaml    # Service definitions
│   │   ├── ingress.yaml    # Ingress rules
│   │   └── network-policy.yaml
│   └── README.md
└── README.md
```

## Installation

```bash
# Add local repo
helm repo add skymechanics ./helm/skymechanics
helm repo update

# Install with default values
helm install skymechanics skymechanics/skymechanics

# Install with custom values
helm install skymechanics skymechanics/skymechanics -f custom-values.yaml

# Upgrade
helm upgrade skymechanics skymechanics/skymechanics

# Rollback
helm rollback skymechanics [REVISION]

# Uninstall
helm uninstall skymechanics
```

## Configuration

### Default Values (`values.yaml`)

```yaml
# Global settings
global:
  namespace: skymechanics
  imagePullPolicy: Always
  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "500m"

# Service configurations
authService:
  enabled: true
  replicas: 2
  port: 8200
  database:
    host: postgres.skymechanics.svc.cluster.local
    port: 5432

mechanicsService:
  enabled: true
  replicas: 2
  port: 8201
  falkordb:
    host: falkordb.skymechanics.svc.cluster.local
    port: 6379

jobsService:
  enabled: true
  replicas: 2
  port: 8202
  falkordb:
    host: falkordb.skymechanics.svc.cluster.local
    port: 6379
  postgresql:
    host: postgres.skymechanics.svc.cluster.local
    port: 5432

# Ingress configuration
ingress:
  enabled: true
  className: nginx
  hosts:
    - host: skymechanics.local
      paths:
        - path: /
          pathType: Prefix

# Monitoring
monitoring:
  prometheus:
    enabled: true
    port: 9090
  grafana:
    enabled: true
    port: 3000
```

### Override Examples

```yaml
# Production values
replicas: 10
resources:
  requests:
    memory: "1Gi"
    cpu: "500m"
  limits:
    memory: "2Gi"
    cpu: "1000m"

# Development values
replicas: 1
resources:
  requests:
    memory: "128Mi"
    cpu: "50m"
  limits:
    memory: "256Mi"
    cpu: "200m"
```

## Template Helpers

### Image Pull Secret

```yaml
{{- define "skymechanics.imagePullSecrets" -}}
imagePullSecrets:
  {{- if .Values.global.imagePullSecrets }}
  {{- toYaml .Values.global.imagePullSecrets | nindent 4 }}
  {{- end }}
{{- end }}
```

### Service Name

```yaml
{{- define "skymechanics.service.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}
```

### Full Resource Name

```yaml
{{- define "skymechanics.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}
```

## Development

### Lint Chart

```bash
helm lint ./helm/skymechanics
```

### Template Rendering

```bash
helm template skymechanics ./helm/skymechanics
helm template skymechanics ./helm/skymechanics --debug
```

### Package Chart

```bash
helm package ./helm/skymechanics
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
name: Helm Chart

on:
  push:
    branches: [main]
    paths:
      - 'helm/**'
      - 'k8s/**'

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Lint Helm chart
        run: helm lint ./helm/skymechanics

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Render Helm templates
        run: helm template skymechanics ./helm/skymechanics --debug

  deploy:
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Kubernetes
        run: |
          helm upgrade skymechanics ./helm/skymechanics \
            --namespace skymechanics \
            --create-namespace \
            --wait
```

## Migration from Manual YAML

1. Verify all manual YAML files are backed up
2. Install Helm chart with existing values
3. Verify all services are running
4. Test API endpoints
5. Delete old YAML files
