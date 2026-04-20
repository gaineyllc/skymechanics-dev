#!/bin/bash
# Push Docker images to GHCR (simple version)

set -e

REPO="ghcr.io/gaineyllc"
GITHUB_ACTOR="gaineyllc"

echo "=== GHCR Push Script ==="
echo "Repository: $REPO"
echo ""

# Check for GITHUB_TOKEN
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ GITHUB_TOKEN not set"
    echo ""
    echo "Please set your GitHub Personal Access Token:"
    echo "1. Go to https://github.com/settings/tokens"
    echo "2. Click 'Generate new token' → 'Fine-grained token'"
    echo "3. Repository access: 'Only select repositories' → 'gaineyllc/skymechanics-dev'"
    echo "4. Permissions → Package:
       - Read: Allow
       - Write: Allow"
    echo "5. Copy the token and run:"
    echo "   export GITHUB_TOKEN=\"your-token-here\""
    echo ""
    exit 1
fi

# Authenticate
echo "Authenticating to GHCR..."
echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_ACTOR" --password-stdin
echo "✅ Authenticated!"
echo ""

# Build and push images
echo "=== Building and Pushing Images ==="
echo ""

# Auth Service
echo "1/5: auth-service..."
docker build -t "$REPO/auth-service:latest" -f services/auth-service/Dockerfile . 2>&1 | tail -5
docker push "$REPO/auth-service:latest"
AUTH_SIZE=$(docker images "$REPO/auth-service:latest" --format "{{.Size}}")
echo "   Size: $AUTH_SIZE"
echo ""

# Mechanics Service
echo "2/5: mechanics-service..."
docker build -t "$REPO/mechanics-service:latest" -f services/mechanics-service/Dockerfile . 2>&1 | tail -5
docker push "$REPO/mechanics-service:latest"
MECHANICS_SIZE=$(docker images "$REPO/mechanics-service:latest" --format "{{.Size}}")
echo "   Size: $MECHANICS_SIZE"
echo ""

# Jobs Service
echo "3/5: jobs-service..."
docker build -t "$REPO/jobs-service:latest" -f services/jobs-service/Dockerfile . 2>&1 | tail -5
docker push "$REPO/jobs-service:latest"
JOBS_SIZE=$(docker images "$REPO/jobs-service:latest" --format "{{.Size}}")
echo "   Size: $JOBS_SIZE"
echo ""

# Analytics Service
echo "4/5: analytics-service..."
docker build -t "$REPO/analytics-service:latest" -f services/analytics-service/Dockerfile . 2>&1 | tail -5
docker push "$REPO/analytics-service:latest"
ANALYTICS_SIZE=$(docker images "$REPO/analytics-service:latest" --format "{{.Size}}")
echo "   Size: $ANALYTICS_SIZE"
echo ""

# Gateway Service
echo "5/5: gateway-service..."
docker build -t "$REPO/gateway-service:latest" -f services/gateway-service/Dockerfile . 2>&1 | tail -5
docker push "$REPO/gateway-service:latest"
GATEWAY_SIZE=$(docker images "$REPO/gateway-service:latest" --format "{{.Size}}")
echo "   Size: $GATEWAY_SIZE"
echo ""

# Calculate total
echo "=== Storage Summary ==="
echo "auth-service:       $AUTH_SIZE"
echo "mechanics-service:  $MECHANICS_SIZE"
echo "jobs-service:       $JOBS_SIZE"
echo "analytics-service:  $ANALYTICS_SIZE"
echo "gateway-service:    $GATEWAY_SIZE"
echo "---------------------------"
echo "Total:              $(echo "$AUTH_SIZE + $MECHANICS_SIZE + $JOBS_SIZE + $ANALYTICS_SIZE + $GATEWAY_SIZE" | sed 's/MB//g' | awk '{printf "%.2f MB", $1+$2+$3+$4+$5}')"
echo ""

# Alert at 80% threshold (1.6GB free tier)
FREE_TIER_MB=2048
THRESHOLD_MB=$(echo "$FREE_TIER_MB * 0.8" | bc | cut -d. -f1)

TOTAL_MB=$(echo "$AUTH_SIZE + $MECHANICS_SIZE + $JOBS_SIZE + $ANALYTICS_SIZE + $GATEWAY_SIZE" | sed 's/MB//g' | awk '{printf "%.0f", $1+$2+$3+$4+$5}')

if [ "$TOTAL_MB" -gt "$THRESHOLD_MB" ]; then
    echo "⚠️  WARNING: Storage usage approaching free tier limit!"
    echo "Current usage: ${TOTAL_MB}MB / ${FREE_TIER_MB}MB"
else
    echo "✅ Storage usage is within free tier limit."
    echo "Usage: ${TOTAL_MB}MB / ${FREE_TIER_MB}MB (80% threshold)"
fi

echo ""
echo "=== Push Complete ==="
