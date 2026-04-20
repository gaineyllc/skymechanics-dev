# Memory Threshold Alert Script

**WARNING**: This script requires sudo to install as a systemd service.

## Installation

```bash
chmod +x k8s/setup-local.sh
sudo ./k8s/setup-local.sh
```

This installs:
- `/etc/systemd/system/skymemalert.service` - Systemd service
- Memory monitoring via `/home/gaineyllc/.openclaw/workspace/skymechanics-dev/k8s/monitor-resources.sh`
- Automatic startup on boot

## Usage

### One-time Check
```bash
./k8s/monitor-resources.sh check
```

### Continuous Monitoring
```bash
./k8s/monitor-resources.sh monitor
```

### Start as Service
```bash
sudo systemctl start skymemalert
sudo systemctl enable skymemalert
```

### Stop Service
```bash
sudo systemctl stop skymemalert
sudo systemctl disable skymemalert
```

## Alert Actions

When memory exceeds threshold:

1. **Log message** to system log
2. **Send Telegram notification** (if OpenClaw configured)
3. **Continue monitoring** - doesn't kill processes automatically

## Memory Targets

| Memory Usage | Status | Action |
|--------------|--------|--------|
| < 70% | Normal | No action |
| 70-85% | Warning | Log only |
| > 85% | Alert | Telegram + Log |
| > 95% | Critical | Alert + review needed |

## Customization

Edit the script to change thresholds:

```bash
# In k8s/monitor-resources.sh
MEMORY_THRESHOLD=85  # Change this value
```

## Notes

- The script is **non-intrusive** - it doesn't kill processes
- It's designed to **notify you** so you can take action
- For Kubernetes, the memory limits ensure containers can't exceed their allocation
- Your host has 121 GiB RAM - the cluster uses max ~3.5 GiB
- Logs are written to `/var/log/skymechanics-resource-alerts.log`

## Systemd Service

```ini
[Unit]
Description=SkyMechanics Memory Alert Service
After=network.target

[Service]
Type=simple
ExecStart=/home/gaineyllc/.openclaw/workspace/skymechanics-dev/k8s/monitor-resources.sh monitor
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

## Uninstall

```bash
# Stop service
sudo systemctl stop skymemalert
sudo systemctl disable skymemalert

# Remove service file
sudo rm /etc/systemd/system/skymemalert.service
sudo systemctl daemon-reload
```

## Manual Alternative (no sudo)

```bash
# Start monitoring in background
./k8s/monitor-resources.sh monitor &
```

## Manual Alternative Uninstall

To remove manual installation:

```bash
# Kill background process
pkill -f 'monitor-resources.sh monitor'

# Remove custom service
sudo rm /etc/systemd/system/skymemalert.service
sudo systemctl daemon-reload
```
