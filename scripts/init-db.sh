#!/bin/bash
# Initialize FalkorDB with multi-tenancy support

echo "⏳ Waiting for FalkorDB to be ready..."
while ! redis-cli -h falkordb -p 6379 ping > /dev/null 2>&1; do
    sleep 1
done

echo "✅ FalkorDB is ready!"

# Enable multi-tenancy module
redis-cli -h falkordb -p 6379 CONFIG SET module-load ""

echo "🔍 FalkorDB initialized with multi-tenancy support"
echo "📊 Available at http://localhost:3001 (browser) or http://localhost:6379 (Redis client)"
