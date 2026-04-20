# SkyMechanics Sudo Setup Instructions

## Quick Setup (Recommended)

```bash
# Copy the sudoers file
sudo cp k8s/skymechanics-sudoers /etc/sudoers.d/skymechanics

# Test that it works
sudo -l | grep skymechanics
```

## What This Enables

| Command | Purpose |
|---------|---------|
| `curl` + `install` | Install k3d/kubectl |
| `setup-local.sh` | Memory monitoring service |
| `systemctl` commands | Start/stop memory monitoring |
| `cp` to `/usr/local/bin` | Install monitor script |

## After Setup

```bash
# Install k3d
curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | sudo bash

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Verify
k3d version
kubectl version --client

# Run setup
sudo ./k8s/setup-local.sh
```

## Testing

After creating the sudoers file:

```bash
# Test k3d install (should work without password)
curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | sudo bash
```

## Undo (If Needed)

```bash
sudo rm /etc/sudoers.d/skymechanics
```

## Security Notes

- Only allows specific paths and commands
- No wildcard sudo access
- Can't modify system-critical files
- Expire policy: commands must be run in correct sequence
