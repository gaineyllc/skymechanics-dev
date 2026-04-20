# Memory Threshold Alert Script

This script monitors system memory and protects your host from being overwhelmed by the Kubernetes cluster.

## Configuration

```bash
THRESHOLD=85    # Alert when memory usage exceeds 85%
CHECK_INTERVAL=10  # Check every 10 seconds
```

## How It Works

1. **Monitors `/proc/meminfo`** for available memory
2. **Calculates usage percentage**:
   ```
   mem_used = mem_total - mem_available
   mem_percent = (mem_used * 100) / mem_total
   ```
3. **Triggers alert** if `mem_percent > THRESHOLD`
4. **Sends Telegram notification** to your channel
5. **Logs to system log** for auditing

## Installation

```bash
sudo ./k8s/setup-local.sh
```

This installs:
- `/usr/local/bin/skymem` - Main monitoring script
- `/etc/systemd/system/skymemalert.service` - Systemd service
- Automatic startup on boot

## Usage

### One-time Check
```bash
./k8s/monitor-resources.sh check
# or
skymem check
```

### Continuous Monitoring
```bash
./k8s/monitor-resources.sh monitor
# or
skymem monitor
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

1. **Log message** to system log:
   ```
   Apr 20 10:30:00 promaxgb10 skymemalert: Memory pressure at 87%
   ```

2. **Send Telegram notification**:
   ```
   ⚠️ MEMORY PRESSURE ALERT: 87% on promaxgb10
   ```

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

## Systemd Service

```ini
[Unit]
Description=SkyMechanics Memory Alert Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/skymem monitor
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```
