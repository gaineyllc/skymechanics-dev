# Demo Data Seed Script for SkyMechanics

Pre-populates FalkorDB with realistic demo data for VC demonstrations.

## Usage

```bash
cd /home/gaineyllc/.openclaw/workspace/skymechanics-dev/backend/scripts
python3 seed_demo_data.py
```

## What it Creates

- **30 customers** with varied industries (Private Aviation, Commercial, Charter, etc.)
- **15 mechanics** with different specialties (Powerplant, Airframe, Avionics, etc.)
- **50 aircraft** across various models (Cessna, Piper, Boeing, Airbus, Gulfstream)
- **10 jobs** with mixed statuses (pending, open, in_progress, completed, cancelled)
- **Mechanic assignments** to jobs (5 jobs have mechanics assigned)

## Output

```
=== SkyMechanics Demo Data Seeding ===

[1/5] Seeding customers...
   Created 30 customers

[2/5] Seeding mechanics...
   Created 15 mechanics
   Specialties: Powerplant, Airframe, Avionics, Hydraulics, Electrical Systems, etc.

[3/5] Seeding aircraft...
   Created 50 aircraft
   Sample models: Cessna 172, Piper PA-28, Boeing 737, Gulfstream G650, Bell 206

[4/5] Seeding jobs...
   Created 10 jobs
   Status distribution: pending, open, in_progress, completed, cancelled

[5/5] Assigning mechanics to jobs...
   Assigned mechanics to 5 jobs

=== Demo Data Seeding Complete ===
   Customers: 30
   Mechanics: 15
   Aircraft: 50
   Jobs: 10
```
