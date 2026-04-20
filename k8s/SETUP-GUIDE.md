# SkyMechanics Memory Monitoring Setup

## Installation (requires sudo)

```bash
# Make scripts executable
chmod +x k8s/*.sh

# Run setup script (requires sudo for systemd service)
sudo ./k8s/setup-local.sh
```

## After Installation

### Memory Alert Service
- Location: `/etc/systemd/system/skymemalert.service`
- Status: `systemctl status skymemalert`
- Logs: `journalctl -u skymemalert -f`
- Stop: `sudo systemctl stop skymemalert`
- Start: `sudo systemctl start skymemalert`

### Available Commands
```bash
skymem check      # One-time memory check
skymem monitor    # Continuous monitoring (run in background)
skymem help       # Show all options
```

## Manual Alternative (no sudo)

```bash
# Start monitoring in background
./k8s/monitor-resources.sh monitor &

# Or create your own systemd service
sudo tee /etc/systemd/system/skymemalert.service > /dev/null << EOF
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
EOF

sudo systemctl daemon-reload
sudo systemctl enable skymemalert
sudo systemctl start skymemalert
```

## Verify Installation

```bash
# Check memory status
skymem check

# Or run manually
cat /proc/meminfo | grep -E "MemTotal|MemAvailable"
free -h
```

## Telegram Alerts

The alert script requires OpenClaw to be configured with Telegram access:

```bash
openclaw telegram sendMessage \
    --chat-id 5824139677 \
    --text "Memory pressure alert"
```

If OpenClaw is not configured, alerts will be logged to system journal instead.

## Memory Thresholds

| Usage | Action |
|-------|--------|
| < 70% | Normal (no action) |
| 70-85% | Logged to journal |
| > 85% | Telegram + Journal alert |
| > 95% | Critical - review needed |

## Uninstall

```bash
# Stop service
sudo systemctl stop skymemalert
sudo systemctl disable skymemalert

# Remove service file
sudo rm /etc/systemd/system/skymemalert.service
sudo systemctl daemon-reload

# Remove binary
sudo rm /usr/local/bin/skymem
```

## Monitoring Kubernetes Pods

```bash
# View pod resource usage
kubectl top pods -n skymechanics

# View container memory
docker stats --no-stream --format "{{.Name}}\t{{.MemPerc}}"
```
