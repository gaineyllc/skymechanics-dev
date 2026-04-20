#!/usr/bin/env python3
"""
Seed FalkorDB with test data for SkyMechanics.
Creates:
- 3 customers (UHNW individuals/organizations)
- 5 mechanics (specialized in different helicopter models)
- 6 aircraft (various luxury helicopters)
- 10 jobs (service requests)
- Relationships: Customer->owns->Aircraft, Mechanic->assigned->Job
"""

from falkordb import FalkorDB
import sys
import os

# Configuration
FALKORDB_HOST = os.getenv("FALKORDB_HOST", "falkordb")
FALKORDB_PORT = int(os.getenv("FALKORDB_PORT", 6379))
TENANT_ID = os.getenv("FALKORDB_TENANT", "default")

# Connect to FalkorDB
print(f"Connecting to FalkorDB at {FALKORDB_HOST}:{FALKORDB_PORT}...")
db = FalkorDB(host=FALKORDB_HOST, port=FALKORDB_PORT)

# Graph name per tenant
GRAPH_NAME = f"tenant_{TENANT_ID}"

# Clear existing graph
print(f"Seeding graph '{GRAPH_NAME}' with test data...")
print("Clearing existing data...")
db.delete_graph(GRAPH_NAME)

# Select graph
graph = db.select_graph(GRAPH_NAME)

# ===== CUSTOMERS =====
customers = [
    {"id": 1, "name": "Elena Rossi", "email": "elena.rossi@luxuryflights.com", "phone": "+1-555-1111", "type": "individual"},
    {"id": 2, "name": "Skyward Holdings LLC", "email": "operations@skywardholdings.com", "phone": "+1-555-2222", "type": "corporate"},
    {"id": 3, "name": "Global Aviation Group", "email": "fleet@globalaviation.com", "phone": "+1-555-3333", "type": "corporate"},
]

for c in customers:
    query = "CREATE (c:Customer {id: $id, name: $name, email: $email, phone: $phone, type: $type, created_at: datetime()})"
    graph.query(query, params=c)
print(f"Created {len(customers)} customers")

# ===== MECHANICS =====
mechanics = [
    {"id": 1, "name": "James 'Helo' Hamilton", "email": "james.hamilton@skymechanics.dev", "phone": "+1-555-1001", 
     "specialties": ["AW609", "S-76D"], "license_number": "FAA-MA-12345", "certifications": ["Powerplant", "Airframe"], "availability": {"monday": "08:00-17:00", "tuesday": "08:00-17:00"}},
    {"id": 2, "name": "Sarah Chen", "email": "sarah.chen@skymechanics.dev", "phone": "+1-555-1002", 
     "specialties": ["ACH160", "H145"], "license_number": "FAA-MA-23456", "certifications": ["Powerplant"], "availability": {"tuesday": "09:00-18:00", "wednesday": "09:00-18:00"}},
    {"id": 3, "name": "Michael O'Connor", "email": "mike.oconnor@skymechanics.dev", "phone": "+1-555-1003", 
     "specialties": ["AW609", "525"], "license_number": "FAA-MA-34567", "certifications": ["Powerplant", "Airframe"], "availability": {"wednesday": "08:00-17:00", "thursday": "08:00-17:00"}},
    {"id": 4, "name": "Elena Rodriguez", "email": "elena.rodriguez@skymechanics.dev", "phone": "+1-555-1004", 
     "specialties": ["ACH160", "ACH145"], "license_number": "FAA-MA-45678", "certifications": ["Airframe"], "availability": {"thursday": "09:00-18:00", "friday": "09:00-18:00"}},
    {"id": 5, "name": "David Park", "email": "david.park@skymechanics.dev", "phone": "+1-555-1005", 
     "specialties": ["S-76D", "525", "AW609"], "license_number": "FAA-MA-56789", "certifications": ["Powerplant", "Airframe"], "availability": {"monday": "08:00-17:00", "friday": "08:00-17:00"}},
]

for m in mechanics:
    query = "CREATE (m:Mechanic {id: $id, name: $name, email: $email, phone: $phone, specialties: $specialties, license_number: $license_number, certifications: $certifications, availability: $availability, created_at: datetime()})"
    graph.query(query, params=m)
print(f"Created {len(mechanics)} mechanics")

# ===== AIRCRAFT =====
aircraft = [
    {"id": 1, "tail_number": "N123AW", "model": "AW609", "year": 2024, "status": "available", "location": {"lat": 40.7128, "lon": -74.0060}, "owner_id": 2},
    {"id": 2, "tail_number": "N456AW", "model": "AW609", "year": 2024, "status": "available", "location": {"lat": 34.0522, "lon": -118.2437}, "owner_id": 2},
    {"id": 3, "tail_number": "N789S7", "model": "S-76D", "year": 2022, "status": "available", "location": {"lat": 40.7128, "lon": -74.0060}, "owner_id": 1},
    {"id": 4, "tail_number": "N234A1", "model": "ACH160", "year": 2023, "status": "available", "location": {"lat": 34.0522, "lon": -118.2437}, "owner_id": 3},
    {"id": 5, "tail_number": "N567A1", "model": "ACH145", "year": 2021, "status": "in_maintenance", "location": {"lat": 40.7128, "lon": -74.0060}, "owner_id": 1},
    {"id": 6, "tail_number": "N89052", "model": "525", "year": 2022, "status": "available", "location": {"lat": 41.8781, "lon": -87.6298}, "owner_id": 3},
]

for a in aircraft:
    query = "CREATE (a:Aircraft {id: $id, tail_number: $tail_number, model: $model, year: $year, status: $status, location: $location, owner_id: $owner_id, created_at: datetime()})"
    graph.query(query, params=a)
print(f"Created {len(aircraft)} aircraft")

# ===== JOBS =====
jobs = [
    {"id": 1, "title": "Routine Inspection - AW609", "description": "Annual inspection and engine check", "status": "completed", "priority": "medium", "scheduled_date": "2026-04-15", "completed_date": "2026-04-16", "aircraft_id": 1, "mechanic_id": 5},
    {"id": 2, "title": "Engine Repair - S-76D", "description": "Replace right engine after bird strike", "status": "completed", "priority": "high", "scheduled_date": "2026-04-10", "completed_date": "2026-04-12", "aircraft_id": 3, "mechanic_id": 5},
    {"id": 3, "title": "AW609 Software Update", "description": "Update flight control software to v2.1", "status": "in_progress", "priority": "medium", "scheduled_date": "2026-04-20", "aircraft_id": 2, "mechanic_id": 5},
    {"id": 4, "title": "ACH160 Interior Refurbishment", "description": "Replace cabin seats and update entertainment system", "status": "pending", "priority": "low", "scheduled_date": "2026-05-01", "aircraft_id": 4, "mechanic_id": 4},
    {"id": 5, "title": "H145 Comprehensive Check", "description": "500-hour inspection including transmission", "status": "pending", "priority": "high", "scheduled_date": "2026-04-25", "aircraft_id": 5, "mechanic_id": 4},
    {"id": 6, "title": "525 Engine Overhaul", "description": "Full engine overhaul for left engine", "status": "pending", "priority": "high", "scheduled_date": "2026-05-10", "aircraft_id": 6, "mechanic_id": 3},
    {"id": 7, "title": "AW609 Pre-Purchase Inspection", "description": "Full inspection for potential buyer", "status": "completed", "priority": "high", "scheduled_date": "2026-04-08", "completed_date": "2026-04-09", "aircraft_id": 1, "mechanic_id": 1},
    {"id": 8, "title": "S-76D Avionics Upgrade", "description": "Install new GPS and navigation system", "status": "pending", "priority": "medium", "scheduled_date": "2026-05-05", "aircraft_id": 3, "mechanic_id": 2},
    {"id": 9, "title": "ACH160 Routine Oil Change", "description": "Regular maintenance", "status": "completed", "priority": "low", "scheduled_date": "2026-04-01", "completed_date": "2026-04-02", "aircraft_id": 4, "mechanic_id": 2},
    {"id": 10, "title": "525 Landing Gear Inspection", "description": "Monthly landing gear check", "status": "completed", "priority": "medium", "scheduled_date": "2026-04-18", "completed_date": "2026-04-19", "aircraft_id": 6, "mechanic_id": 3},
]

for j in jobs:
    query = "CREATE (j:Job {id: $id, title: $title, description: $description, status: $status, priority: $priority, scheduled_date: $scheduled_date, completed_date: $completed_date, created_at: datetime()})"
    graph.query(query, params=j)
print(f"Created {len(jobs)} jobs")

# ===== RELATIONSHIPS =====
print("Creating relationships...")

# Customer owns Aircraft
for a in aircraft:
    query = "MATCH (c:Customer {id: $owner_id}), (a:Aircraft {id: $id}) CREATE (c)-[:OWNS]->(a)"
    graph.query(query, params={"id": a["id"], "owner_id": a["owner_id"]})
print(f"Created OWNS relationships")

# Mechanic assigned to Job
for j in jobs:
    if "mechanic_id" in j:
        query = "MATCH (m:Mechanic {id: $mechanic_id}), (j:Job {id: $id}) CREATE (m)-[:ASSIGNED]->(j)"
        graph.query(query, params={"id": j["id"], "mechanic_id": j["mechanic_id"]})
print(f"Created ASSIGNED relationships")

# ===== CREATE TENANT NODE =====
query = "CREATE (t:Tenant {id: $tenant_id, name: 'SkyMechanics', created_at: datetime()})"
graph.query(query, params={"tenant_id": TENANT_ID})

# Link all entities to tenant
for c in customers:
    query = "MATCH (t:Tenant {id: $tenant_id}), (c:Customer {id: $id}) CREATE (c)-[:BELONGS_TO]->(t)"
    graph.query(query, params={"tenant_id": TENANT_ID, "id": c["id"]})

for m in mechanics:
    query = "MATCH (t:Tenant {id: $tenant_id}), (m:Mechanic {id: $id}) CREATE (m)-[:BELONGS_TO]->(t)"
    graph.query(query, params={"tenant_id": TENANT_ID, "id": m["id"]})

for a in aircraft:
    query = "MATCH (t:Tenant {id: $tenant_id}), (a:Aircraft {id: $id}) CREATE (a)-[:BELONGS_TO]->(t)"
    graph.query(query, params={"tenant_id": TENANT_ID, "id": a["id"]})

for j in jobs:
    query = "MATCH (t:Tenant {id: $tenant_id}), (j:Job {id: $id}) CREATE (j)-[:BELONGS_TO]->(t)"
    graph.query(query, params={"tenant_id": TENANT_ID, "id": j["id"]})

print(f"Linked all entities to tenant '{TENANT_ID}'")

# Print summary
print("\n=== Seed Complete ===")
print(f"Graph: {GRAPH_NAME}")
print(f"Tenants: 1")
print(f"Customers: {len(customers)}")
print(f"Mechanics: {len(mechanics)}")
print(f"Aircraft: {len(aircraft)}")
print(f"Jobs: {len(jobs)}")
print(f"Relationships: Created OWNS, ASSIGNED, and BELONGS_TO edges")

if __name__ == "__main__":
    print("\nFalkorDB seeding completed successfully!")
    sys.exit(0)
