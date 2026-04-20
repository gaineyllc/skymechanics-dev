#!/bin/bash
# deploy-all.sh - Deploy all SkyMechanics components to Kubernetes

set -e

echo "=== SkyMechanics Kubernetes Deployment ==="

# Export KUBECONFIG if needed
if [ -z "$KUBECONFIG" ] && [ -f "$HOME/.kube/k3d-skymechanics-dev.config" ]; then
    export KUBECONFIG="$HOME/.kube/k3d-skymechanics-dev.config"
fi

# Create namespace
echo "Creating namespace..."
kubectl apply -f k8s/namespace.yaml

# Deploy core infrastructure (DBs)
echo "Deploying FalkorDB..."
kubectl apply -f k8s/falkordb.yaml

echo "Deploying PostgreSQL..."
kubectl apply -f k8s/postgres.yaml

echo "Deploying Redis..."
kubectl apply -f k8s/redis.yaml

# Deploy services
echo "Deploying Auth Service..."
kubectl apply -f k8s/auth-service.yaml

echo "Deploying Mechanics Service..."
kubectl apply -f k8s/mechanics-service.yaml

echo "Deploying Jobs Service..."
kubectl apply -f k8s/jobs-service.yaml

# Deploy ingress
echo "Deploying Ingress..."
kubectl apply -f k8s/ingress.yaml

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 30

# Deploy metrics server
echo "Deploying Metrics Server..."
kubectl apply -f k8s/metrics-server.yaml

# Verify deployment
echo ""
echo "=== Deployment Verification ==="
echo ""

# Check namespace
echo "Namespace Status:"
kubectl get namespace skymechanics

echo ""
echo "Pods Status:"
kubectl get pods -n skymechanics

echo ""
echo "Services Status:"
kubectl get services -n skymechanics

echo ""
echo "FalkorDB Port Forward (for local access):"
echo "  kubectl port-forward -n skymechanics svc/falkordb 6379:6379 &"

echo ""
echo "=== Deployment Complete ==="
echo ""
echo "To access FalkorDB locally, run:"
echo "  kubectl port-forward -n skymechanics svc/falkordb 6379:6379 &"
echo ""
echo "To check pod resources (requires metrics-server):"
echo "  kubectl top pods -n skymechanics"
echo ""
echo "To monitor memory pressure:"
echo "  ./k8s/monitor-resources.sh monitor"
