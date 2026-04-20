#!/bin/bash
#undeploy-all.sh - Remove SkyMechanics components from Kubernetes

set -e

echo "=== SkyMechanics Kubernetes Undeployment ==="

# Export KUBECONFIG if needed
if [ -z "$KUBECONFIG" ] && [ -f "$HOME/.kube/k3d-skymechanics-dev.config" ]; then
    export KUBECONFIG="$HOME/.kube/k3d-skymechanics-dev.config"
fi

echo "Removing Ingress..."
kubectl delete -f k8s/ingress.yaml 2>/dev/null || true

echo "Removing Services..."
kubectl delete -f k8s/jobs-service.yaml 2>/dev/null || true
kubectl delete -f k8s/mechanics-service.yaml 2>/dev/null || true
kubectl delete -f k8s/auth-service.yaml 2>/dev/null || true

echo "Removing Deployments..."
kubectl delete -f k8s/redis.yaml 2>/dev/null || true
kubectl delete -f k8s/postgres.yaml 2>/dev/null || true
kubectl delete -f k8s/falkordb.yaml 2>/dev/null || true

echo "Removing Metrics Server..."
kubectl delete -f k8s/metrics-server.yaml 2>/dev/null || true

echo "Removing Namespace (WARNING: This will delete all data)..."
kubectl delete namespace skymechanics

echo ""
echo "=== Undeployment Complete ==="
