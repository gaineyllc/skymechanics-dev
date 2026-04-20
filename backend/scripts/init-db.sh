#!/bin/bash
# PostgreSQL initialization and test data seed script

set -e

# Database configuration
PGHOST="${PGHOST:-localhost}"
PGPORT="${PGPORT:-5432}"
PGUSER="${PGUSER:-postgres}"
PGDATABASE="${PGDATABASE:-postgres}"
PGPASSWORD="${PGPASSWORD:-postgres}"

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -c "SELECT 1" > /dev/null 2>&1; do
    sleep 1
done

echo "PostgreSQL is ready!"

# Run schema initialization
echo "Initializing PostgreSQL schema..."
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f /app/scripts/init-db.sql

echo "PostgreSQL setup complete!"

# Display created users
echo ""
echo "=== Test Accounts Created ==="
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -c "SELECT user_id, email, role, phone FROM users;"
