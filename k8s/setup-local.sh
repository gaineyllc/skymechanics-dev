#!/bin/bash
# setup-local.sh - Setup local development environment with memory monitoring

set -e

echo "=== SkyMechanics Local Environment Setup ==="
echo ""

# Make scripts executable
chmod +x k8s/setup-k3d.sh
chmod +x k8s/monitor-resources.sh
chmod +x k8s/deploy-all.sh
chmod +x k8s/undeploy-all.sh

# Install memory alert script
echo "Installing memory alert script..."
chmod +x k8s/monitor-resources.sh

# Create systemd service for memory monitoring
echo "Creating systemd service for memory monitoring..."
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

# Start memory monitoring
echo "Starting memory monitoring..."
if command -v systemctl &> /dev/null; then
    sudo systemctl daemon-reload
    sudo systemctl enable skymemalert
    sudo systemctl start skymemalert
    echo "Memory monitoring service started"
else
    echo "systemctl not available. Run: ./k8s/monitor-resources.sh monitor"
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Available commands:"
echo "  ./k8s/monitor-resources.sh check      - One-time memory check"
echo "  ./k8s/monitor-resources.sh monitor    - Continuous monitoring (run in background)"
echo ""
echo "Kubernetes setup:"
echo "  cd k8s && ./setup-k3d.sh"
echo "  ./deploy-all.sh"
echo ""
echo "To stop memory monitoring:"
echo "  sudo systemctl stop skymemalert"
echo "  sudo systemctl disable skymemalert"
