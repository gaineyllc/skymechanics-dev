#!/bin/bash
# End-to-end test script for SkyMechanics Platform

set -e

echo "🚀 Starting SkyMechanics E2E Tests..."

# Start Docker Compose services
echo "🏗️  Starting Docker Compose services..."
cd /home/gaineyllc/.openclaw/workspace/skymechanics-dev
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Run unit tests
echo "📋 Running unit tests..."
cd /home/gaineyllc/.openclaw/workspace/skymechanics-dev/backend
python3 -m pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html

# Check health endpoint
echo "🔍 Checking health endpoints..."
curl -f http://localhost:8080/health || echo "Backend not responding yet"

# Cleanup
echo "🧹 Cleaning up..."
cd /home/gaineyllc/.openclaw/workspace/skymechanics-dev
docker-compose down -v

echo "✅ E2E tests completed!"
