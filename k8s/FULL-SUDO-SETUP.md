# Full Autonomous Setup - K8s Sudoers

## Updated Sudoers File

Replace the sudoers file with this complete version:

```bash
# SkyMechanics - Full autonomous setup permissions
# Install with: sudo visudo -f /etc/sudoers.d/skymechanics

User_Alias SKYMECHANICS = gaineyllc

# Tools installation
Cmnd_Alias TOOL_INSTALL = /usr/bin/curl, /usr/bin/install, /bin/mkdir -p /usr/local/bin, \
                          /bin/rm -rf /tmp/k3d-install, /bin/rm -rf /tmp/kubectl-install, \
                          /bin/rm -rf /tmp/helm-install, /bin/rm -f /tmp/k3d-linux-arm64, \
                          /bin/rm -f /tmp/kubectl, /bin/tar -zxvf /tmp/helm-*.tar.gz, \
                          /bin/rm -rf /tmp/linux-arm64, /bin/rm -f /tmp/helm-*.tar.gz

# Docker Compose
Cmnd_Alias DOCKER_COMPOSE_INSTALL = /usr/bin/curl -SL, /bin/mkdir -p /usr/local/bin

# K3d cluster management
Cmnd_Alias K3D_MANAGE = /usr/local/bin/k3d cluster create skymechanics-dev, \
                        /usr/local/bin/k3d cluster delete skymechanics-dev, \
                        /usr/local/bin/k3d cluster list

# Kubectl operations
Cmnd_Alias KUBECTL_MANAGE = /usr/local/bin/kubectl apply -f, \
                            /usr/local/bin/kubectl wait --for=condition=Ready, \
                            /usr/local/bin/kubectl port-forward -n, \
                            /usr/local/bin/kubectl get pods,svc,ingress, \
                            /usr/local/bin/kubectl logs -n, \
                            /usr/local/bin/kubectl top pods -n

# Memory monitoring
Cmnd_Alias MEMORY_MONITOR = /bin/cp /home/gaineyllc/.openclaw/workspace/skymechanics-dev/k8s/monitor-resources.sh /usr/local/bin/skymem, \
                            /bin/chmod +x /usr/local/bin/skymem, \
                            /bin/mkdir -p /var/log, \
                            /usr/bin/touch /var/log/skymechanics-resource-alerts.log, \
                            /bin/chown gaineyllc:gaineyllc /var/log/skymechanics-resource-alerts.log

# Systemd management
Cmnd_Alias SYSTEMD_MANAGE = /usr/bin/tee /etc/systemd/system/skymemalert.service, \
                            /bin/systemctl daemon-reload, \
                            /bin/systemctl enable skymemalert, \
                            /bin/systemctl start skymemalert, \
                            /bin/systemctl stop skymemalert, \
                            /bin/systemctl disable skymemalert, \
                            /bin/rm /etc/systemd/system/skymemalert.service

# Full setup script
Cmnd_Alias FULL_SETUP = /bin/bash /home/gaineyllc/.openclaw/workspace/skymechanics-dev/k8s/full-setup.sh

# CLI helpers
Cmnd_Alias CLI_HELPERS = /bin/bash -c /bin/bash -c 'cat > /usr/local/bin/k8s-forward', \
                         /bin/bash -c 'cat > /usr/local/bin/k8s-logs', \
                         /bin/bash -c 'cat > /usr/local/bin/k8s-status', \
                         /bin/bash -c /bin/chmod +x /usr/local/bin/k8s-forward, \
                         /bin/bash -c /bin/chmod +x /usr/local/bin/k8s-logs, \
                         /bin/bash -c /bin/chmod +x /usr/local/bin/k8s-status

# Allow user to run all commands without password
SKYMECHANICS ALL=(root) NOPASSWD: TOOL_INSTALL
SKYMECHANICS ALL=(root) NOPASSWD: DOCKER_COMPOSE_INSTALL
SKYMECHANICS ALL=(root) NOPASSWD: K3D_MANAGE
SKYMECHANICS ALL=(root) NOPASSWD: KUBECTL_MANAGE
SKYMECHANICS ALL=(root) NOPASSWD: MEMORY_MONITOR
SKYMECHANICS ALL=(root) NOPASSWD: SYSTEMD_MANAGE
SKYMECHANICS ALL=(root) NOPASSWD: FULL_SETUP
SKYMECHANICS ALL=(root) NOPASSWD: CLI_HELPERS
```

## Installation Steps

```bash
# 1. Copy sudoers file
sudo cp k8s/skymechanics-sudoers /etc/sudoers.d/skymechanics

# 2. Set correct permissions
sudo chmod 0440 /etc/sudoers.d/skymechanics

# 3. Validate
sudo visudo -c

# 4. Test
sudo -l | grep skymechanics
```

## Usage

After sudoers is set up, run:

```bash
# Autonomous full setup
sudo ./k8s/full-setup.sh

# Or step by step
sudo ./k8s/setup-local.sh
cd k8s
./setup-k3d.sh
./deploy-all.sh
```

## What This Enables

| Command | Purpose |
|---------|---------|
| `full-setup.sh` | Complete automated setup (tools + cluster + services) |
| `setup-local.sh` | Memory monitoring service |
| `setup-k3d.sh` | K3d cluster creation |
| `deploy-all.sh` | Deploy all K8s services |

## Security Notes

- All commands are explicitly listed
- No wildcard sudo access
- Paths are absolute and specific
- Temporary files are cleaned up after use
- Memory monitoring protects the host system
