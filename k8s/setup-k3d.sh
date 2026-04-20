#!/bin/bash
# setup-k3d.sh - Setup memory-optimized K3d cluster for SkyMechanics

set -e

echo "=== SkyMechanics K3d Cluster Setup ==="

# Check if k3d is installed
if ! command -v k3d &> /dev/null; then
    echo "Installing k3d..."
    curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "Installing kubectl..."
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/arm64/kubectl"
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    rm kubectl
fi

# Create the cluster with memory limits
echo "Creating K3d cluster with memory limits..."
k3d cluster create skymechanics-dev \
    --servers 1 \
    --agents 1 \
    --k3s-server-arg "--kube-apiserver-arg=enable-admission-plugins=NodeRestriction" \
    --k3s-server-arg "--kube-apiserver-arg=admission-control-config-file=/var/lib/rancher/k3s/server/manifests/admission-control.yaml" \
    --wait \
    --timeout 600s

# Configure kubectl
k3d kubeconfig get skymechanics-dev > ~/.kube/k3d-skymechanics-dev.config
export KUBECONFIG=~/.kube/k3d-skymechanics-dev.config:~/.kube/config

# Install Traefik ingress controller (minimal footprint)
echo "Installing Traefik ingress controller..."
kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v3.1/docs/content/reference/dynamic-configuration/kubernetes-crd.yaml

# Wait for Traefik to be ready
sleep 10

# Install Helm
if ! command -v helm &> /dev/null; then
    echo "Installing Helm..."
    curl -fsSL https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
fi

# Enable metrics server for resource monitoring
echo "Installing metrics server..."
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml

# Patch metrics server for ARM64
kubectl patch deployment metrics-server -n kube-system --type='json' -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value": "--kubelet-insecure-tls"}]'

echo "Cluster setup complete!"
echo "Configure your shell:"
echo "  export KUBECONFIG=~/.kube/k3d-skymechanics-dev.config:~/.kube/config"
