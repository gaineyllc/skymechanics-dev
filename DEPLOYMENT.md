# Deployment Guide

## Local Development

### Prerequisites

- Docker and Docker Compose installed
- k3d for local Kubernetes cluster (optional)
- Python 3.12+

### Running Locally

#### Docker Compose

```bash
cd backend
docker-compose up --build
```

Frontend will be available at `http://localhost:3003`

#### Kubernetes (k3d)

```bash
# Create cluster
k3d cluster create skymechanics-dev

# Build and load images
k3d image import skymechanics-backend:dev

# Apply manifests
kubectl apply -f k8s/dev/
```

## CI/CD Pipeline

### GitHub Actions

The CI/CD pipeline is configured in `.github/workflows/cicd.yml`.

#### Required Secrets

- `GHCR_PAT` - GitHub Personal Access Token with `read:packages` and `write:packages` scopes
- `KUBECONFIG` - Kubernetes config file for deployment

### Self-Hosted Runner Setup

#### Prerequisites

- Ubuntu 22.04+ with Docker installed
- Internet access to GitHub

#### Installation

```bash
# Create runner user
sudo useradd -m -s /bin/bash github-runner

# Download and extract runner
cd /home/github-runner
wget https://github.com/actions/runner/releases/download/v2.333.1/actions-runner-linux-arm64-2.333.1.tar.gz
tar -zxvf actions-runner-linux-arm64-2.333.1.tar.gz

# Configure runner
./config.sh --url https://github.com/gaineyllc/skymechanics-dev --token <TOKEN> --name promaxgb10-495f --unattended

# Create systemd service
sudo cp github-runner.service /etc/systemd/system/
sudo systemctl enable github-runner
sudo systemctl start github-runner
```

#### Sudoers Configuration

To allow runner management without password, add to `/etc/sudoers.d/github-runner`:

```
github-runner ALL=(ALL) NOPASSWD: /bin/systemctl * github-runner
```

## Services

| Service | Port | Description |
|---------|------|-------------|
| auth-service | 8200 | Authentication and user management |
| mechanics-service | 8201 | Mechanics and aircraft management |
| jobs-service | 8202 | Job scheduling and tracking |
| analytics-service | 8203 | Analytics and reporting |
| gateway-service | 8204 | WebSocket gateway |
| aircraft-service | 8208 | Aircraft management |
| parts-service | 8201 | Parts inventory |
| notification-service | 8202 | Notifications and alerts |
| invoice-service | 8203 | Invoicing and billing |
| frontend | 3000 | React web application |

## Monitoring

### Resource Alerts

The `skymemalert.service` monitors memory usage:
- Warning: 70% memory usage
- Critical: 85% memory usage

### Logs

```bash
# View runner logs
journalctl -u github-runner -f

# View service logs
kubectl logs -n skymechanics <pod-name> -f
```

## Troubleshooting

### Runner Offline

1. Check runner status: `ps aux | grep github-runner`
2. Check logs: `journalctl -u github-runner -f`
3. Reconfigure: `./config.sh remove && ./config.sh --url <URL> --token <TOKEN> --unattended`

### Docker Build Failures

1. Check Docker daemon: `sudo systemctl status docker`
2. Rebuild images: `docker-compose build --no-cache`

### Kubernetes Issues

1. Check pods: `kubectl get pods -n skymechanics`
2. Check logs: `kubectl logs -n skymechanics <pod-name>`
3. Describe resources: `kubectl describe <resource> <name> -n skymechanics`
