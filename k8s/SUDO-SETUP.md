# Full Autonomous Setup - Complete Sudoers Guide

## Updated Sudoers File

The sudoers file at `k8s/skymechanics-sudoers` now includes:

| Command Group | Purpose |
|---------------|---------|
| `TOOL_INSTALL` | k3d, kubectl, helm installation |
| `K3D_MANAGE` | Cluster create/delete/list |
| `KUBECTL_MANAGE` | kubectl apply, wait, port-forward, get, logs, top |
| `MEMORY_MONITOR` | Copy monitor script and create log file |
| `SYSTEMD_MANAGE` | Service enable/start/stop/disable |
| `FULL_SETUP` | Run the full automated script |
| `CLI_WRITE` + `CLI_CHMOD` | Create CLI helper scripts |

## Installation Steps

```bash
# 1. Copy sudoers file (validates automatically)
sudo visudo -f k8s/skymechanics-sudoers

# 2. Verify it works
sudo -l | grep skymechanics
```

Expected output should show all 9 command groups.

## Usage

After sudoers is set up, run:

```bash
# Autonomous full setup (everything)
sudo ./k8s/full-setup.sh

# Or verify individual components
sudo -l | grep FULL_SETUP
sudo -l | grep KUBECTL_MANAGE
```

## What `full-setup.sh` Does

1. Installs k3d, kubectl, helm, docker-compose
2. Creates K3d cluster with memory limits
3. Sets up memory monitoring service
4. Deploys all Kubernetes services
5. Creates CLI helpers (`k8s-forward`, `k8s-logs`, `k8s-status`)

## Testing

```bash
# Test k3d install
sudo /usr/bin/curl --version

# Test kubectl apply
sudo /usr/local/bin/kubectl version --client

# Test full setup
sudo ./k8s/full-setup.sh
```

## Security Notes

- All commands are explicitly listed with full paths
- No wildcard sudo access (`*`)
- Temporary files cleaned up after use
- Memory monitoring protects host from OOM

## Rollback

```bash
# Remove sudoers file
sudo rm /etc/sudoers.d/skymechanics

# Stop memory monitoring
sudo systemctl stop skymemalert
sudo systemctl disable skymemalert
sudo rm /etc/systemd/system/skymemalert.service
```
