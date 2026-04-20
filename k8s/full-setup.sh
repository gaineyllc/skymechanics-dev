#!/bin/bash
# full-setup.sh - Complete autonomous setup for SkyMechanics Kubernetes cluster
# Run: sudo ./full-setup.sh

set -e

echo "=== SkyMechanics Full Setup ==="
echo ""

# Configuration
K3D_VERSION="v5.7.0"
KUBECTL_VERSION=$(curl -s https://dl.k8s.io/release/stable.txt)
HELM_VERSION="v3.20.2"
MEMORY_THRESHOLD=85

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 1. Install k3d
install_k3d() {
    log_info "Installing k3d $K3D_VERSION..."
    
    local k3d_dir="/tmp/k3d-install"
    mkdir -p "$k3d_dir"
    cd "$k3d_dir"
    
    curl -LO "https://github.com/k3d-io/k3d/releases/download/$K3D_VERSION/k3d-linux-arm64"
    install -o root -g root -m 0755 k3d-linux-arm64 /usr/local/bin/k3d
    rm -rf "$k3d_dir"
    
    log_info "k3d installed: $(k3d version --short)"
}

# 2. Install kubectl
install_kubectl() {
    log_info "Installing kubectl $KUBECTL_VERSION..."
    
    local kubectl_dir="/tmp/kubectl-install"
    mkdir -p "$kubectl_dir"
    cd "$kubectl_dir"
    
    curl -LO "https://dl.k8s.io/release/$KUBECTL_VERSION/bin/linux/arm64/kubectl"
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    rm -rf "$kubectl_dir"
    
    log_info "kubectl installed: $(kubectl version --client --short)"
}

# 3. Install helm
install_helm() {
    log_info "Installing helm $HELM_VERSION..."
    
    local helm_dir="/tmp/helm-install"
    mkdir -p "$helm_dir"
    cd "$helm_dir"
    
    curl -LO "https://get.helm.sh/helm-$HELM_VERSION-linux-arm64.tar.gz"
    tar -zxvf helm-$HELM_VERSION-linux-arm64.tar.gz
    install -o root -g root -m 0755 linux-arm64/helm /usr/local/bin/helm
    rm -rf "$helm_dir"
    
    log_info "helm installed: $(helm version --short)"
}

# 4. Install Docker Compose (if not present)
install_docker_compose() {
    log_info "Installing Docker Compose..."
    
    if ! command -v docker-compose &> /dev/null; then
        curl -SL "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-linux-arm64" \
            -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
        log_info "Docker Compose installed"
    else
        log_info "Docker Compose already installed: $(docker-compose version --short)"
    fi
}

# 5. Setup K3d cluster
setup_k3d_cluster() {
    log_info "Setting up K3d cluster..."
    
    cd /home/gaineyllc/.openclaw/workspace/skymechanics-dev/k8s
    
    # Delete existing cluster if it exists
    if k3d cluster list | grep -q skymechanics-dev; then
        log_info "Deleting existing cluster..."
        k3d cluster delete skymechanics-dev
    fi
    
    # Create cluster with memory limits
    k3d cluster create skymechanics-dev \
        --config /home/gaineyllc/.openclaw/workspace/skymechanics-dev/k8s/k3d-cluster.yaml \
        --kubeconfig-update-default \
        --wait 120
    
    log_info "K3d cluster created"
}

# 6. Setup memory monitoring
setup_memory_monitor() {
    log_info "Setting up memory monitoring..."
    
    # Create log directory
    sudo mkdir -p /var/log
    sudo touch /var/log/skymechanics-resource-alerts.log
    sudo chown gaineyllc:gaineyllc /var/log/skymechanics-resource-alerts.log
    
    # Copy monitor script
    cp /home/gaineyllc/.openclaw/workspace/skymechanics-dev/k8s/monitor-resources.sh \
        /usr/local/bin/skymem
    chmod +x /usr/local/bin/skymem
    
    # Create systemd service
    sudo tee /etc/systemd/system/skymemalert.service > /dev/null << EOF
[Unit]
Description=SkyMechanics Memory Alert Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/skymem monitor
Restart=on-failure
RestartSec=5
User=gaineyllc
Group=gaineyllc

[Install]
WantedBy=multi-user.target
EOF
    
    # Reload and start
    sudo systemctl daemon-reload
    sudo systemctl enable skymemalert
    sudo systemctl start skymemalert
    
    log_info "Memory monitoring enabled (threshold: ${MEMORY_THRESHOLD}%)"
}

# 7. Deploy Kubernetes services
deploy_k8s() {
    log_info "Deploying Kubernetes services..."
    
    cd /home/gaineyllc/.openclaw/workspace/skymechanics-dev/k8s
    
    # Wait for cluster to be ready
    log_info "Waiting for cluster to be ready..."
    until kubectl cluster-info &> /dev/null; do
        echo -n "."
        sleep 2
    done
    echo "done"
    
    # Create namespace
    kubectl apply -f namespace.yaml
    
    # Deploy storage class (if needed)
    kubectl apply -f storage-class.yaml 2>/dev/null || true
    
    # Deploy databases
    kubectl apply -f falkordb.yaml
    kubectl apply -f postgres.yaml
    kubectl apply -f redis.yaml
    
    # Wait for databases
    log_info "Waiting for databases..."
    kubectl wait --for=condition=Ready pods -l app=falkordb -n skymechanics --timeout=120s
    kubectl wait --for=condition=Ready pods -l app=postgres -n skymechanics --timeout=120s
    kubectl wait --for=condition=Ready pods -l app=redis -n skymechanics --timeout=60s
    
    # Deploy services
    kubectl apply -f auth-service.yaml
    kubectl apply -f mechanics-service.yaml
    kubectl apply -f jobs-service.yaml
    
    # Deploy ingress
    kubectl apply -f ingress.yaml
    
    # Deploy metrics server
    kubectl apply -f metrics-server.yaml
    
    # Wait for services
    log_info "Waiting for services..."
    kubectl wait --for=condition=Ready pods -n skymechanics --timeout=180s --all
    
    log_info "All services deployed"
}

# 8. Setup port forwarding
setup_port_forwarding() {
    log_info "Setting up port forwarding..."
    
    # Create port-forwarding script
    cat > /usr/local/bin/k8s-forward << 'EOF'
#!/bin/bash
# Port forward for K8s services
kubectl port-forward -n skymechanics svc/falkordb 6379:6379 &
kubectl port-forward -n skymechanics svc/auth-service 8000:8000 &
kubectl port-forward -n skymechanics svc/mechanics-service 8001:8000 &
kubectl port-forward -n skymechanics svc/jobs-service 8002:8000 &
kubectl port-forward -n skymechanics svc/redis 6380:6379 &
echo "Port forwarding started. Press Ctrl+C to stop."
EOF
    chmod +x /usr/local/bin/k8s-forward
    
    log_info "Port forwarding script created at /usr/local/bin/k8s-forward"
}

# 9. Setup CLI helpers
setup_cli_helpers() {
    log_info "Setting up CLI helpers..."
    
    # Create k8s-logs command
    cat > /usr/local/bin/k8s-logs << 'EOF'
#!/bin/bash
# Show logs from all skymechanics pods
kubectl logs -n skymechanics -l app=skymechanics --all-containers --tail=50 "$@"
EOF
    chmod +x /usr/local/bin/k8s-logs
    
    # Create k8s-status command
    cat > /usr/local/bin/k8s-status << 'EOF'
#!/bin/bash
# Show status of all skymechanics services
echo "=== K8s Services ==="
kubectl get pods,svc -n skymechanics
echo ""
echo "=== Resource Usage ==="
kubectl top pods -n skymechanics 2>/dev/null || echo "Metrics server not ready"
EOF
    chmod +x /usr/local/bin/k8s-status
    
    log_info "CLI helpers installed"
}

# 10. Test deployment
test_deployment() {
    log_info "Testing deployment..."
    
    # Wait for all pods to be ready
    log_info "Waiting for all pods to be ready..."
    kubectl wait --for=condition=Ready pods -n skymechanics --timeout=300s --all
    
    # Check services
    log_info "Service endpoints:"
    kubectl get svc -n skymechanics
    
    # Check ingress
    log_info "Ingress status:"
    kubectl get ingress -n skymechanics
    
    log_info "Deployment test complete"
}

# Main execution
main() {
    log_info "Starting full setup..."
    
    # Verify Docker is running
    if ! docker info &> /dev/null; then
        log_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    
    log_info "Docker is running"
    
    # Install tools
    install_k3d
    install_kubectl
    install_helm
    install_docker_compose
    
    # Setup cluster
    setup_k3d_cluster
    
    # Setup monitoring
    setup_memory_monitor
    
    # Deploy services
    deploy_k8s
    
    # Setup helpers
    setup_port_forwarding
    setup_cli_helpers
    
    # Test
    test_deployment
    
    log_info "=== Setup Complete ==="
    echo ""
    echo "Available commands:"
    echo "  k8s-forward     - Start port forwarding"
    echo "  k8s-logs        - Show recent logs"
    echo "  k8s-status      - Show service status"
    echo "  skymem check    - Check memory usage"
    echo "  skymem monitor  - Start memory monitoring"
    echo ""
    echo "Access services at:"
    echo "  FalkorDB:   http://localhost:3000"
    echo "  Auth API:   http://localhost:8000"
    echo "  Mechanics:  http://localhost:8001"
    echo "  Jobs API:   http://localhost:8002"
}

main "$@"
