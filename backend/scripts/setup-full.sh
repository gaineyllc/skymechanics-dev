#!/bin/bash
# Complete SkyMechanics setup script
# This script initializes PostgreSQL and seeds FalkorDB

set -e

echo "=============================================="
echo "  SkyMechanics Full Setup"
echo "  Postgres + FalkorDB Initialization"
echo "=============================================="
echo ""

# Configuration
PGHOST="${PGHOST:-localhost}"
PGPORT="${PGPORT:-5432}"
PGUSER="${PGUSER:-postgres}"
PGDATABASE="${PGDATABASE:-postgres}"
PGPASSWORD="${PGPASSWORD:-postgres}"

FALKORDB_HOST="${FALKORDB_HOST:-localhost}"
FALKORDB_PORT="${FALKORDB_PORT:-6379}"
TENANT_ID="${TENANT_ID:-default}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Initialize PostgreSQL
echo -e "${YELLOW}[Step 1/3] Initializing PostgreSQL...${NC}"
echo "Host: $PGHOST:$PGPORT"
echo "Database: $PGDATABASE"

# Wait for PostgreSQL
echo "Waiting for PostgreSQL to be ready..."
until psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -c "SELECT 1" > /dev/null 2>&1; do
    sleep 1
done

echo -e "${GREEN}PostgreSQL is ready!${NC}"

# Run schema initialization
echo "Applying database schema..."
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f /app/scripts/init-db.sql

echo -e "${GREEN}PostgreSQL schema initialized!${NC}"

# Step 2: Verify PostgreSQL data
echo ""
echo -e "${YELLOW}[Step 2/3] Verifying PostgreSQL test accounts...${NC}"

echo "Created accounts:"
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -c "SELECT user_id, email, role, phone FROM users ORDER BY user_id;"

echo -e "${GREEN}PostgreSQL test accounts verified!${NC}"

# Step 3: Seed FalkorDB
echo ""
echo -e "${YELLOW}[Step 3/3] Seeding FalkorDB...${NC}"
echo "Host: $FALKORDB_HOST:$FALKORDB_PORT"
echo "Tenant: $TENANT_ID"

# Run FalkorDB seeding
python3 /app/scripts/seed-falkordb.py

echo ""
echo "=============================================="
echo -e "${GREEN}  Full Setup Complete!${NC}"
echo "=============================================="
echo ""
echo "Test Accounts:"
echo "  Admin:     admin@skymechanics.dev (password: admin123)"
echo "  Mechanic:  mechanic@skymechanics.dev (password: mechanic123)"
echo "  Customer:  customer@skymechanics.dev (password: customer123)"
echo ""
echo "Test Data:"
echo "  - 3 Customers (UHNW individuals/corporations)"
echo "  - 5 Mechanics (specialized in AW609, S-76D, ACH160, H145, 525)"
echo "  - 6 Aircraft (various luxury helicopters)"
echo "  - 10 Jobs (service requests)"
echo ""
echo "Next Steps:"
echo "  1. Access the frontend at http://localhost:3000"
echo "  2. Login with admin@skymechanics.dev"
echo "  3. Explore the dashboard and verify all features"
