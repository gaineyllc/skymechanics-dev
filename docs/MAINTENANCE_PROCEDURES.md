# SkyMechanics - Maintenance Procedures Configuration System

## Overview

This document describes the system for configuring, storing, and executing aircraft maintenance procedures with drag-and-drop visual workflow builder integration.

---

## Authoritative FAA Sources

### Primary Documentation

| Source | Description | URL |
|--------|-------------|-----|
| **AC 43.13-1B** | Acceptable Methods, Techniques, and Practices - Aircraft Inspection and Repair | [FAA Link](https://www.faa.gov/documentlibrary/media/advisory_circular/ac_43.13-1b_w-chg1.pdf) |
| **AC 43.13-2A** | Acceptable Methods, Techniques, and Practices - Aircraft Alterations (Cancelled) | [FAA Link](https://www.faa.gov/regulations_policies/advisory_circulars/index.cfm/go/document.information/documentid/74416) |
| **AC 20-106** | Aircraft Inspection for the General Aviation Aircraft Owner | [FAA Link](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-106.pdf) |

### Aircraft-Specific Documentation

| Document Type | Description | Source |
|---------------|-------------|--------|
| **AMM (Aircraft Maintenance Manual)** | Manufacturer's detailed maintenance instructions | Aircraft OEM (Boeing, Airbus, Cessna, etc.) |
| **MPD (Maintenance Planning Document)** | Scheduled maintenance tasks and intervals | Aircraft OEM |
| **MMEL (Master Minimum Equipment List)** | Equipment that can be inoperative while maintaining airworthiness | Aircraft OEM |
| **IPC (Illustrated Parts Catalog)** | Parts identification with exploded diagrams | Aircraft OEM |
| **WDM (Wiring Diagram Manual)** | Electrical system wiring diagrams | Aircraft OEM |
| **SRM (Structural Repair Manual)** | Structural repair procedures | Aircraft OEM |

### Annual Inspection Requirements

**FAR 91.409** - Annual Inspection Requirements:
- Full inspection of aircraft at one time
- Certification as to airworthiness
- Oil cooler shutters检查
- Corrosion inspection (especially coastal/hangared aircraft)

**Recommended Checklists:**
- [FAA AC 20-106 Checklist](https://www.faa.gov/documentLibrary/media/Advisory_Circular/AC_20-106.pdf)
- [Safety Culture Annual/100HR Checklist](https://safetyculture.com/library/transport-and-logistics/aircraft-annual-100hr-inspection-37jrg2ttxducihn6)

### Parts and Tools Standards

**Parts Documentation:**
- **Category Parts List (CPL)** - FAA authorized parts database | [FAA CPL](https://www.faa.gov/aircraft/air_cert/production_approvals/mfg_best_practice/category_parts_list)
- **Standard Parts** - FAA guidance on standard fasteners and components | [AOPA Standard Parts](https://www.aopa.org/news-and-media/all-news/2023/november/09/aircraft-maintenance-understanding-standard-parts)

**Tool Requirements:**
- **Socket Sets**: 1/4" and 3/8" drive, 12-point, shallow/deep sockets
- **Torque Wrenches**: 30-200 in-lb range
- **Pliers**: Duck bill, diagonal cutters, needle nose
- **Wrenches**: Combination open-box end, 12-point
- **Specialty Tools**: Aircraft spark plug socket, brake bleeding tool, dial calipers

**Reference Tool Lists:**
- [LETU Required Tool List](https://www.letu.edu/academics/aviation/files/Required-Tool-List.pdf)
- [Lane CC Minimum Tool List](https://www.lanecc.edu/media/3408)
- [PCC Aviation Tool List](https://www.pcc.edu/programs/aviation-maintenance/wp-content/uploads/sites/88/2019/07/tools.pdf)

---

## Configuration System Architecture

### Data Model

```cypher
// Configuration Source (FAA or OEM)
CREATE (:ConfigSource {
  id: "faa-ac-43-13-1b",
  name: "AC 43.13-1B",
  type: "advisory_circular",
  version: "with Change 1",
  url: "https://www.faa.gov/documentlibrary/media/advisory_circular/ac_43.13-1b_w-chg1.pdf",
  last_updated: date(),
  is_active: true
})

// Aircraft Type Configuration
CREATE (:AircraftType {
  id: "cessna-172-r",
  make: "Cessna",
  model: "172R",
  category: "airplane",
  certification: "FAA",
  amm_ref: "Cessna 172R AMM",
  mpd_ref: "Cessna 172R MPD",
  ipc_ref: "Cessna 172R IPC"
})

// Procedure Template (from FAA/OEM)
CREATE (:ProcedureTemplate {
  id: "annual-inspection-airframe",
  name: "Annual Inspection - Airframe",
  category: "annual",
  authority: "FAA AC 20-106",
  estimated_duration_hours: 8,
  required_specialty: "general"
})

// Task within Procedure
CREATE (:Task {
  id: "annual-inspection-airframe-1",
  name: "Exterior Inspection",
  sequence: 1,
  category: "visual",
  estimated_duration_minutes: 60,
  required_tools: ["inspectionmirror", "flashlight"],
  required_parts: [],
  checklist_items: [
    {"item": "Wings and control surfaces", "checked": false},
    {"item": "Fuselage and doors", "checked": false},
    {"item": "Tail surfaces", "checked": false},
    {"item": "Landing gear", "checked": false}
  ]
})

// Tool Configuration
CREATE (:Tool {
  id: "torque-wrench-30-200",
  name: "Torque Wrench 30-200 in-lb",
  category: "torque",
  calibration_required: true,
  calibration_interval_months: 6
})

// Parts Catalog Reference
CREATE (:Part {
  id: "b-3-17",
  part_number: "B-3-17",
  name: "Cowlings, Upper and Lower",
  aircraft_compatible: ["cessna-172-r"],
  oem_source: "Cessna",
  category: "structural"
})
```

### API Endpoints

```http
GET  /api/config/sources               # List all configuration sources
POST /api/config/sources               # Add new configuration source
GET  /api/config/sources/{id}          # Get configuration source details
DELETE /api/config/sources/{id}        # Remove configuration source

GET  /api/config/procedures            # List all procedure templates
GET  /api/config/procedures/{id}       # Get procedure template with tasks
POST /api/config/procedures            # Create procedure template
PUT  /api/config/procedures/{id}       # Update procedure template
DELETE /api/config/procedures/{id}     # Delete procedure template

GET  /api/config/tasks                 # List all task templates
POST /api/config/tasks                 # Create task template
GET  /api/config/tasks/{id}            # Get task template details

GET  /api/config/tools                 # List all tool configurations
POST /api/config/tools                 # Add tool configuration
GET  /api/config/tools/{id}            # Get tool details

GET  /api/config/parts                 # List all parts catalog
POST /api/config/parts                 # Add parts catalog entry
GET  /api/config/parts/{id}            # Get parts details

GET  /api/config/aircraft-types        # List aircraft type configurations
POST /api/config/aircraft-types        # Add aircraft type
```

### Visual Workflow Builder

**Drag-and-Drop Interface:**

1. **Procedure Builder** - Drag procedures onto canvas
2. **Task Editor** - Drag tasks into procedure flow
3. **Logic Nodes** - Add decision points, dependencies, loops
4. **Tool/Premise Connector** - Link required tools to tasks

**Visual Elements:**

```
┌─────────────────────────────────────────────────────────────┐
│  Procedure: Annual Inspection - Airframe                   │
│  Duration: 8 hours | Authority: FAA AC 20-106              │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │   Start      │───▶│ Visual Insp. │───▶│ Structural   │ │
│  │   (Start)    │    │ (60 min)     │    │ Inspection   │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│           │                   │                   │        │
│           ▼                   ▼                   ▼        │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐ │
│  │ Powerplant   │───▶│ Avionics     │───▶│ Final Checks │ │
│  │ Inspection   │    │ Inspection   │    │ (Sign-off)   │ │
│  └──────────────┘    └──────────────┘    └──────────────┘ │
│                           │                                │
│                           ▼                                │
│                    ┌──────────────┐                        │
│                    │   End        │                        │
│                    │   (Complete) │                        │
│                    └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

**Logic Nodes:**

```json
{
  "type": "conditional",
  "id": "logic-1",
  "label": "Engine Type Check",
  "condition": "aircraft.powerplant_type",
  "operator": "equals",
  "value": "rotary",
  "branches": {
    "true": "rotary-engine-inspection",
    "false": "piston-engine-inspection"
  }
}
```

### User Configuration Flow

**Step 1: Import Configuration Source**
```
POST /api/config/sources
{
  "name": "Cessna 172R AMM",
  "type": "aircraft_manual",
  "version": "Section 05",
  "file_upload": true  // or external_url
}
```

**Step 2: Select Procedure Template**
```
GET /api/config/procedures?source_id=faa-ac-20-106
```

**Step 3: Customize Procedure**
- Drag tasks into desired sequence
- Add conditional logic branches
- Link aircraft-specific requirements
- Assign required tools

**Step 4: Save and Apply**
```
PUT /api/config/procedures/{id}
{
  "name": "Annual Inspection - Cessna 172R",
  "aircraft_types": ["cessna-172-r"],
  "tasks": [...],
  "logic": [...]
}
```

---

## Implementation Priority

### Phase 1: Foundation (P0)
- [ ] Tool configuration API endpoints
- [ ] Parts catalog import (FAA CPL)
- [ ] Basic procedure template storage
- [ ] Simple task list in workflow builder

### Phase 2: Visual Builder (P1)
- [ ] Drag-and-drop task reordering
- [ ] Conditional logic nodes
- [ ] Tool-to-task linking
- [ ] Visual procedure preview

### Phase 3: FAA Sources (P2)
- [ ] AC 43.13-1B integration
- [ ] AC 20-106 annual inspection templates
- [ ] Task import from FAA documents
- [ ] Auto-extraction of checklist items

### Phase 4: Aircraft-Specific (P3)
- [ ] AMM/MPD integration
- [ ] IPC parts lookup
- [ ] Aircraft type configuration
- [ ] Custom procedure building

---

## Storage Schema (FalkorDB)

```cypher
// Indexes for performance
CREATE INDEX procedure_index FOR (p:Procedure) ON (p.id)
CREATE INDEX task_index FOR (t:Task) ON (t.id)
CREATE INDEX tool_index FOR (t:Tool) ON (t.id)
CREATE INDEX part_index FOR (p:Part) ON (p.id)
CREATE INDEX aircraft_index FOR (a:AircraftType) ON (a.id)

// Relationship types
// - (:Procedure)-[:CONTAINS_TASK]->(:Task)
// - (:Task)-[:REQUIRES_TOOL]->(:Tool)
// - (:Task)-[:REQUIRES_PART]->(:Part)
// - (:AircraftType)-[:USES_PROCEDURE]->(:Procedure)
// - (:Procedure)-[:SOURCE_FROM]->(:ConfigSource)
```

---

## Next Steps

1. **Design UI Components** - React components for visual workflow builder
2. **Implement Config API** - Backend endpoints for configuration management
3. **Create Data Import** - Scripts to parse FAA documents
4. **Build Workflow Builder** - Drag-and-drop interface with logic nodes
5. **Test Integration** - End-to-end testing with real aircraft types

---

## References

- FAA Advisory Circulars: https://www.faa.gov/regulations_policies/advisory_circulars/
- Aircraft Maintenance Manual Standards: ATA iSpec 2200
- FAA Parts Database: https://www.faa.gov/aircraft/air_cert/production_approvals/
- Tool Calibration Standards: ASME B89.1.1, ISO 6789
