# SkyMechanics Kubernetes Setup - Manual Steps Required

## System Prerequisites

You need to install the following tools as root:

### 1. Install k3d (Kubernetes for Docker)
```bash
curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash
```

### 2. Install kubectl
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
rm kubectl
```

### 3. Verify installations
```bash
k3d version
kubectl version --client
helm version
```

## Setup Commands

Once tools are installed, run:

```bash
# Make scripts executable
chmod +x k8s/*.sh

# Setup K3d cluster
cd k8s
./setup-k3d.sh

# Deploy all services
./deploy-all.sh

# Start memory monitoring
./monitor-resources.sh monitor &
```

## Memory Monitoring

### System-wide monitoring
```bash
# One-time check
k8s/monitor-resources.sh check

# Continuous monitoring
k8s/monitor-resources.sh monitor
```

### Automatic monitoring (requires sudo)
```bash
# Install as systemd service
sudo ./k8s/setup-local.sh

# Check status
systemctl status skymemalert

# View logs
journalctl -u skymemalert -f
```

## Manual k3d Setup (Alternative)

If k3d installation fails, use Minikube:

```bash
# Install Minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-arm64
sudo install minikube-linux-arm64 /usr/local/bin/minikube

# Start cluster
minikube start --driver=docker --memory=4096 --cpus=2

# Deploy
kubectl apply -f k8s/
```

## Testing the Setup

```bash
# Check cluster
kubectl cluster-info

# Check pods
kubectl get pods -n skymechanics

# Check resources
kubectl top pods -n skymechanics

# Port forward for local access
kubectl port-forward -n skymechanics svc/falkordb 6379:6379 &
kubectl port-forward -n skymechanics svc/auth-service 8000:8000 &
```

## Troubleshooting

### k3d install fails
```bash
# Check Docker is running
docker ps

# Try Docker Desktop with WSL2 backend
```

### Memory issues
```bash
# Check host memory
free -h

# Check Docker memory usage
docker stats

# Reduce cluster resources in k3d-cluster.yaml
```

## Clean Up

```bash
# Undeploy services
./k8s/undeploy-all.sh

# Remove K3d cluster
k3d cluster delete skymechanics-dev
```

## Next Steps

1. Install required tools (k3d, kubectl)
2. Run setup scripts
3. Monitor memory with `skymem monitor`
4. Port forward to access services locally
5. Update service Docker images with your actual images

---

**Remember**: The memory alert script (`skymem`) monitors host usage and notifies at 85% threshold to protect your system.
