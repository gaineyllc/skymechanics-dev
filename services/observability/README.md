# SkyMechanics Observability Stack

This directory contains Prometheus and Grafana configurations.

## Components

| Component | Port | Purpose |
|-----------|------|---------|
| Prometheus | 9090 | Metrics collection and storage |
| Grafana | 3000 | Metrics visualization and dashboards |
| Loki | 3100 | Log aggregation |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Observability Stack                      │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  Prometheus │  │   Grafana   │  │    Loki     │          │
│  │   (9090)    │  │  (3000)     │  │   (3100)    │          │
│  └──────┬──────┘  └─────────────┘  └──────┬──────┘          │
│         │                                 │                  │
│  ┌──────▼──────┐                   ┌──────▼──────┐          │
│  │  Services   │<──Metrics───┐     │  Services   │          │
│  │   (8000-2)  │             │     │   (8000-2)  │          │
│  └─────────────┘             │     └─────────────┘          │
│                              │                              │
│                        ┌─────▼─────┐                        │
│                        │ Redis Pub │                        │
│                        │ /Sub     │                        │
│                        └───────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

## Prometheus Configuration

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'skymechanics'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
```

## Grafana Dashboards

### Service Health Dashboard
- CPU/Memory usage per service
- Request rate and latency
- Error rates
- Service availability

### Redis Dashboard
- Memory usage
- Key count
- Hit/miss ratio
- Connection count

## Setup

```bash
# Deploy Prometheus
kubectl apply -f k8s/prometheus/

# Deploy Grafana
kubectl apply -f k8s/grafana/

# Access Grafana
kubectl port-forward -n skymechanics svc/grafana 3000:3000
# Username: admin
# Password: admin (change after first login)
```

## Alerting

```yaml
# alerts.yml
groups:
  - name: skymechanics-alerts
    rules:
    - alert: ServiceDown
      expr: up{job="skymechanics"} == 0
      for: 5m
      labels:
        severity: critical
      annotations:
        summary: "Service {{ $labels.instance }} is down"
        description: "{{ $labels.instance }} has been down for more than 5 minutes."

    - alert: HighErrorRate
      expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.01
      for: 5m
      labels:
        severity: warning
      annotations:
        summary: "High error rate detected"
        description: "Error rate is above 1% for 5 minutes."
```
