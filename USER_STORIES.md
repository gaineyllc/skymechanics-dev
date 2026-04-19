# SkyMechanics - User Stories & Requirements

## Aircraft Owner Personas

### 1. Small Flight School Owner (Sarah)
**Background:** Runs a regional flight school with 5 aircraft, 12 instructors, and 50+ students.
**Goals:** Track maintenance across fleet, ensure airworthiness, manage vendor invoices

**User Stories:**
| ID | As a... | I want to... | So that... |
|----|---------|------------|------------|
| US-1.1 | Flight school owner | View all aircraft in one dashboard | See fleet health at a glance |
| US-1.2 | Flight school owner | Log maintenance events per aircraft | MaintainFAA compliance records |
| US-1.3 | Flight school owner | Link mechanics to specific aircraft | Track which techs know each plane |
| US-1.4 | Flight school owner | Set up recurring maintenance reminders | Avoid missed inspections |
| US-1.5 | Flight school owner | Attach inspection reports as PDFs | Keep audit-ready documentation |

**Requirements:**
- R-1.1: Aircraft entity with registration number, make/model, airworthiness status
- R-1.2: Maintenance log entries linked to aircraft
- R-1.3: Many-to-many between mechanics and aircraft (specialties)
- R-1.4: Scheduled maintenance templates (annual, 100-hr, 50-hr)
- R-1.5: Document attachment capability (PDF, images)

### 2. Solo Aircraft Owner (David)
**Background:** Owns a Cessna 172 for personal use, does some maintenance himself.
**Goals:** Simple maintenance tracking, cost tracking, find qualified mechanics

**User Stories:**
| ID | As a... | I want to... | So that... |
|----|---------|------------|------------|
| US-2.1 | Solo owner | Create my single aircraft entry | Start tracking from day one |
| US-2.2 | Solo owner | Log my own maintenance work | Keep personal service records |
| US-2.3 | Solo owner | Find mechanics by specialty (e.g. "G1000") | Hire right expert for avionics |
| US-2.4 | Solo owner | See cost summary by maintenance type | Budget for annuals |
| US-2.5 | Solo owner | Get email reminders 30 days before annual | Don't miss deadlines |

**Requirements:**
- R-2.1: Simplified aircraft creation (minimal fields)
- R-2.2: Self-service maintenance logging with labor cost field
- R-2.3: Mechanic search by specialty with dropdown filters
- R-2.4: Cost aggregation by category (parts, labor, total)
- R-2.5: Notification system with configurable triggers

### 3. Aircraft Management Company (Corporate)
**Background:** Manages 50+ aircraft for clients across multiple locations.
**Goals:** Multi-tenant operations, client billing, fleet analytics

**User Stories:**
| ID | As a... | I want to... | So that... |
|----|---------|------------|------------|
| US-3.1 | Fleet manager | Switch between client organizations | Manage multiple clients securely |
| US-3.2 | Accountant | Generate monthly invoices per aircraft | Bill clients accurately |
| US-3.3 | Director | View fleet-wide maintenance costs | Identify expensive aircraft |
| US-3.4 | Operations lead | Assign jobs to mechanics by location | Balance workload across base |
| US-3.5 | Compliance officer | Export all maintenance records for audit | Pass FAA inspection |

**Requirements:**
- R-3.1: Multi-tenant architecture (client-level isolation)
- R-3.2: Invoice generation with line-item maintenance records
- R-3.3: Dashboard with fleet-wide KPIs (cost, downtime, MTBF)
- R-3.4: Mechanic assignment with location/shift constraints
- R-3.5: Data export (CSV/Excel) for compliance

## Mechanic Personas

### 4. A&P Mechanic (Maria)
**Background:** Certified A&P mechanic, works at FBO, doing 10-15 jobs/week.
**Goals:** Track work completed, manage tool inventory, see job history

**User Stories:**
| ID | As a... | I want to... | So that... |
|----|---------|------------|------------|
| US-4.1 | Mechanic | View my assigned jobs | Know what's due today |
| US-4.2 | Mechanic | Mark job complete with sign-off | Get paid for completed work |
| US-4.3 | Mechanic | View aircraft service history | Understand past issues |
| US-4.4 | Mechanic | Log parts used per job | Return unused parts, track costs |
| US-4.5 | Mechanic | Upload inspection checklists | Pass form to customer |

**Requirements:**
- R-4.1: Job assignment dashboard with status filters
- R-4.2: Job completion workflow with digital signature
- R-4.3: Aircraft service history timeline view
- R-4.4: Parts consumption tracking (inventory integration)
- R-4.5: Checklist template system with attachment

### 5. Avionics Specialist (Raj)
**Background:** Specializes in Garmin G1000, Dynon, and experimental avionics.
**Goals:** Track complex avionics installations, manage calibration records

**User Stories:**
| ID | As a... | I want to... | So that... |
|----|---------|------------|------------|
| US-5.1 | Avionics specialist | Create detailed job for avionics install | Document every wire connected |
| US-5.2 | Avionics specialist | Link calibration certificates | Keep calibration records |
| US-5.3 | Avionics specialist | Tag jobs as "Avionics Only" | Filter my specialty work |
| US-5.4 | Avionics specialist | View compatibility matrix for upgrades | Recommend correct upgrades |
| US-5.5 | Avionics specialist | Export job reports as PDF | Give clean reports to customers |

**Requirements:**
- R-5.1: Rich text job description with component-level detail
- R-5.2: Document attachment with certificate type tags
- R-5.3: Job categorization by specialty
- R-5.4: Component compatibility database
- R-5.5: Professional report generation

### 6. Shop Foreman (Elena)
**Background:** Manages a 5-person shop, schedules jobs, tracks progress.
**Goals:** Schedule efficiency, resource allocation, quality control

**User Stories:**
| ID | As a... | I want to... | So that... |
|----|---------|------------|------------|
| US-6.1 | Shop foreman | See all jobs in Gantt chart view | Visualize workload and bottlenecks |
| US-6.2 | Shop foreman | Reassign jobs between mechanics | Balance workload dynamically |
| US-6.3 | Shop foreman | Set job priorities (Urgent/Standard/Routine) | Focus on critical work first |
| US-6.4 | Shop foreman | Generate weekly productivity report | Evaluate shop performance |
| US-6.5 | Shop foreman | Create standard job templates | Ensure consistency across jobs |

**Requirements:**
- R-6.1: Visual scheduling interface (Gantt/kanban)
- R-6.2: Job reassignment with notification
- R-6.3: Priority tagging with visual indicators
- R-6.4: Metrics export (jobs completed, hours, revenue)
- R-6.5: Job template system with predefined steps

## Admin/User Persona

### 7. System Administrator (Dev Team)
**Background:** Handles user management, system configuration, backups.
**Goals:** Secure multi-tenant platform, data integrity, uptime

**User Stories:**
| ID | As a... | I want to... | So that... |
|----|---------|------------|------------|
| US-7.1 | Admin | Create new tenant organizations | Onboard new clients |
| US-7.2 | Admin | Assign user roles (owner/mechanic/reader) | Control data access |
| US-7.3 | Admin | View system health and error logs | Proactively fix issues |
| US-7.4 | Admin | Configure email/SMS notifications | Keep users informed |
| US-7.5 | Admin | Export full database dump | Backup and disaster recovery |

**Requirements:**
- R-7.1: Tenant provisioning workflow
- R-7.2: Role-based access control (RBAC)
- R-7.3: System monitoring dashboard
- R-7.4: Notification channel configuration
- R-7.5: Automated backup system

---

## Priority Matrix

| Priority | Stories | Reason |
|----------|---------|--------|
| P0 - Launch | US-1.1, US-1.2, US-2.1, US-2.2, US-4.1, US-4.2 | Core flight school and solo owner workflows |
| P1 - Month 1 | US-1.3, US-1.4, US-2.3, US-2.4, US-4.3, US-4.4, US-6.1, US-6.3 | Fleet tracking and job scheduling |
| P2 - Month 2 | US-1.5, US-2.5, US-3.1, US-3.2, US-5.1, US-5.2, US-6.2, US-6.4 | Document management and multi-tenant |
| P3 - Month 3 | US-3.3, US-3.4, US-5.3, US-5.4, US-6.5, US-7.1, US-7.2 | Analytics and admin features |

---

## Graph Schema MVP

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Customer   │─────▶│   Aircraft    │─────▶│   Job       │
│ (Owner)     │      │ (Tail Number) │      │ (Maintenance)│
└─────────────┘      └─────────────┘      └─────────────┘
                          ▲                        │
                          │                        ▼
                   ┌─────────────┐         ┌─────────────┐
                   │ Mechanic    │◀────────│ Part        │
                   │ (Specialty) │         │ (Inventory) │
                   └─────────────┘         └─────────────┘
```

**Initial Nodes:**
- `Customer`: name, email, phone, address
- `Aircraft`: tail_number, make, model, registration_expires
- `Mechanic`: name, email, phone, specialties[]
- `Job`: title, description, status, priority, due_date

**Initial Relationships:**
- `(Customer)-[:OWNS]->(Aircraft)`
- `(Mechanic)-[:SPECIALIZES_IN]->(Aircraft)`
- `(Aircraft)-[:HAS_JOB]->(Job)`
- `(Job)-[:USES_PART]->(Part)`
- `(Mechanic)-[:PERFORMS]->(Job)`
