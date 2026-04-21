# FAA Certification & Repairman System - Research Summary

## Key FAA Certifications

### 1. A&P Mechanic Certificate (14 CFR Part 65 Subpart D)
- **Requirements:**
  - Age 18+
  - 18-30 months practical experience OR graduation from Part 147 school
  - Pass written, oral, and practical tests
  - Read/write/speak English

- **Ratings:**
  - Airframe (A)
  - Powerplant (P)
  - Combined A&P

- **Privileges:**
  - Maintain, repair, alter aircraft
  - Approve for return to service (after performing work)
  - Perform 100-hour inspections
  - Supervise other mechanics

### 2. Inspection Authorization (IA) (14 CFR Part 65 Subpart F)
- **Requirements:**
  - Hold active A&P for 3+ years
  - 2 years actively engaged in aircraft maintenance
  - Pass written test on major repairs/alterations
  - Fixed base of operations

- **Privileges:**
  - Annual inspections
  - Progressive inspections
  - Major repairs/alterations approval

### 3. Repairman Certificates (14 CFR Part 65 Subparts E, F)

#### a) Repairman (General) - §65.101
- For employees of repair stations, air carriers, commercial operators
- Employer recommendation required
- 18 months experience OR formal training

#### b) Repairman (Experimental Aircraft Builder) - §65.104
- For primary builder of amateur-built aircraft
- Only privilege: perform annual condition inspection on that aircraft
- Only one per aircraft

#### c) Repairman (Light-Sport) - §65.107
- **Two ratings:**
  - Inspection Rating
  - Maintenance Rating

- **Categories:**
  - Airplane, Rotorcraft, Glider, Lighter-than-air, Powered-lift, Powered-parachute, Weight-shift-control

- **Training:**
  - Inspection: 16 hours
  - Maintenance: 80-120 hours

- **Privileges:**
  - Inspection: Condition inspections on owned aircraft only
  - Maintenance: Full maintenance on light-sport category aircraft

## MOSAIC Rule Changes (Effective Oct 22, 2025)

- Light-sport repairman privileges expanded to include Experimental Amateur-Built (EAB) aircraft
- Certificate title simplified to "Repairman Certificate (Light-Sport)"
- Pre-2025 certificates remain valid

## Recommended Graph Schema for Reputation System

### Nodes
```
- Mechanic (label: 'Mechanic')
  - properties: name, email, phone, license_number, certifications[], experience_years, created_at

- Certification (label: 'Certification') 
  - properties: name, issuing_body, expiry_date, license_number
  - relationships: [:HOLDS] -> Mechanic

- RepairmanCertificate (label: 'RepairmanCertificate')
  - properties: type, rating, category, issue_date, expiry_date, aircraft_id
  - relationships: [:HOLDS] -> Mechanic

- AircraftType (label: 'AircraftType')
  - properties: make, model, category, certification, amm_ref, mpd_ref, ipc_ref
  - relationships: [:EXPERIENCE] -> Mechanic

- ExperienceRecord (label: 'ExperienceRecord')
  - properties: start_date, end_date, hours, aircraft_id, aircraft_type, description
  - relationships: [:EXPERIENCE] -> Mechanic

- Job (label: 'Job')
  - properties: title, status, priority, created_at
  - relationships: [:ASSIGNED_TO] -> Mechanic

- Review (label: 'Review')
  - properties: rating (1-5), comment, created_at
  - relationships: [:GIVEN_BY] -> Customer, [:FOR_JOB] -> Job, [:ABOUT_MECHANIC] -> Mechanic

- Skill (label: 'Skill')
  - properties: name, category
  - relationships: [:HAS_SKILL] -> Mechanic
```

### Relationship Properties
```
[:HOLDS]
- issued_date, expiry_date, license_number, status

[:EXPERIENCE]
- hours_flown, aircraft_count, last_flown, proficiency_level

[:ASSIGNED_TO]
- assignment_date, completion_date, priority_level, complexity_score

[:GIVEN_BY]
- review_date, reliability_score

[:HAS_SKILL]
- proficiency_level, years_experience, last_used
```

## Reputation Score Components

### Primary Score (0-100)
1. **Certification Status (25 points)**
   - Valid A&P: 15 points
   - Valid IA: 25 points
   - Valid Repairman certs: 10 points
   - Expired: 0 points

2. **Experience Depth (20 points)**
   - Years active: 0-10 points
   - Aircraft types: 0-5 points
   - Specialized skills: 0-5 points

3. **Performance Metrics (30 points)**
   - Jobs completed: 0-10 points
   - Customer satisfaction: 0-10 points
   - Re-work rate: 0-10 points

4. **Recent Activity (15 points)**
   - Last maintenance date: 0-10 points
   - Continuing education: 0-5 points

5. **Compliance (10 points)**
   - FAA compliance history: 0-5 points
   - Inspection pass rate: 0-5 points

### Secondary Score (0-50)
- Feedback weight (0-20)
- Aircraft compatibility score (0-15)
- Geographic proximity (0-15)

## Implementation Priority

### Phase 1: Core Data Models
1. Extend Mechanic model with certifications array
2. Add RepairmanCertificate model
3. Add ExperienceRecord model

### Phase 2: Graph Integration
1. Create relationships for certifications
2. Create relationships for experience
3. Build query for mechanic reputation

### Phase 3: Scoring System
1. Implement reputation algorithm
2. Add dynamic scoring
3. Build ranking views

### Phase 4: UI Integration
1. Mechanic profile page with reputation
2. Job assignment suggestions
3. Certification tracking dashboard
