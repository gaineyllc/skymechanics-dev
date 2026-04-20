#!/bin/bash
# Push Docker images to GHCR

set -e

REPO="ghcr.io/gaineyllc"

# Authenticate using GITHUB_TOKEN (set in CI environment)
if [ -n "$GITHUB_TOKEN" ]; then
    echo "$GITHUB_TOKEN" | docker login ghcr.io -u "$GITHUB_ACTOR" --password-stdin
else
    echo "Warning: GITHUB_TOKEN not set. Run this from GitHub Actions or set GITHUB_TOKEN manually."
    exit 1
fi

# Build and push images with size reporting
echo "=== Building and Pushing Images ==="

# Auth Service
echo "Building auth-service..."
docker build -t "$REPO/auth-service:latest" -f services/auth-service/Dockerfile .
AUTH_SIZE=$(docker images "$REPO/auth-service:latest" --format "{{.Size}}")
echo "auth-service size: $AUTH_SIZE"
docker push "$REPO/auth-service:latest"

# Mechanics Service
echo "Building mechanics-service..."
docker build -t "$REPO/mechanics-service:latest" -f services/mechanics-service/Dockerfile .
MECHANICS_SIZE=$(docker images "$REPO/mechanics-service:latest" --format "{{.Size}}")
echo "mechanics-service size: $MECHANICS_SIZE"
docker push "$REPO/mechanics-service:latest"

# Jobs Service
echo "Building jobs-service..."
docker build -t "$REPO/jobs-service:latest" -f services/jobs-service/Dockerfile .
JOBS_SIZE=$(docker images "$REPO/jobs-service:latest" --format "{{.Size}}")
echo "jobs-service size: $JOBS_SIZE"
docker push "$REPO/jobs-service:latest"

# Analytics Service
echo "Building analytics-service..."
docker build -t "$REPO/analytics-service:latest" -f services/analytics-service/Dockerfile .
ANALYTICS_SIZE=$(docker images "$REPO/analytics-service:latest" --format "{{.Size}}")
echo "analytics-service size: $ANALYTICS_SIZE"
docker push "$REPO/analytics-service:latest"

# Gateway Service
echo "Building gateway-service..."
docker build -t "$REPO/gateway-service:latest" -f services/gateway-service/Dockerfile .
GATEWAY_SIZE=$(docker images "$REPO/gateway-service:latest" --format "{{.Size}}")
echo "gateway-service size: $GATEWAY_SIZE"
docker push "$REPO/gateway-service:latest"

# Calculate total storage usage
TOTAL_SIZE=$(echo "$AUTH_SIZE + $MECHANICS_SIZE + $JOBS_SIZE + $ANALYTICS_SIZE + $GATEWAY_SIZE" | bc)
echo "=== Total Storage Usage: $TOTAL_SIZE ==="

# Check if we're approaching free tier limits (2GB)
FREE_TIER_LIMIT_GB=2
FREE_TIER_LIMIT_BYTES=$((FREE_TIER_LIMIT_GB * 1073741824))

# Convert total size to bytes (approximate)
TOTAL_BYTES=$(echo "$TOTAL_SIZE" | sed 's/[^0-9.]//g')
case "$TOTAL_SIZE" in
    *GB) TOTAL_BYTES=$(echo "$TOTAL_BYTES * 1073741824" | bc) ;;
    *MB) TOTAL_BYTES=$(echo "$TOTAL_BYTES * 1048576" | bc) ;;
    *KB) TOTAL_BYTES=$(echo "$TOTAL_BYTES * 1024" | bc) ;;
esac

THRESHOLD=$((FREE_TIER_LIMIT_BYTES * 80 / 100))  # 80% threshold

if [ "$TOTAL_BYTES" -gt "$THRESHOLD" ]; then
    echo "⚠️ ALERT: Storage usage is approaching free tier limit (2GB)!"
    echo "Current usage: $TOTAL_SIZE"
else
    echo "✅ Storage usage is within free tier limit."
fi

echo "=== Push Complete ==="
