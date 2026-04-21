# SkyMechanics - User Stories & Requirements

## Aircraft Owner Personas

### 1. Small Flight School Owner (Sarah)
**Background:** Runs a regional flight school with 5 aircraft, 12 instructors, and 50+ students.
**Goals:** Track maintenance across fleet, ensure airworthiness, manage vendor invoices

**User Stories:**
| ID | As a... | I want to... | So that... |
|----|---------|------------|------------|
| US-1.1 | Flight school owner | View all aircraft in one dashboard | See fleet health at a glance |
| US-1.2 | Flight school owner | Log maintenance events per aircraft | Maintain FAA compliance records |
| US-1.3 | Flight school owner | Link mechanics to specific aircraft | Track which techs know each plane |
| US-1.4 | Flight school owner | Set up recurring maintenance reminders | Avoid missed inspections |
| US-1.5 | Flight school owner | Attach inspection reports as PDFs | Keep audit-ready documentation |
| US-1.6 | Flight school owner | View upcoming maintenance deadlines | Plan shop capacity in advance |
| US-1.7 | Flight school owner | Compare labor rates per mechanic | Negotiate better vendor contracts |
| US-1.8 | Flight school owner | Generate fleet compliance report | Show students our safety standards |
| US-1.9 | Flight school owner | Block aircraft from flying when overdue | Maintain regulatory compliance |
| US-1.10 | Flight school owner | Get daily summary of overdue jobs | Start each day with priority clarity |

**Requirements:**
- R-1.1: Aircraft entity with registration number, make/model, airworthiness status
- R-1.2: Maintenance log entries linked to aircraft
- R-1.3: Many-to-many between mechanics and aircraft (specialties)
- R-1.4: Scheduled maintenance templates (annual, 100-hr, 50-hr)
- R-1.5: Document attachment capability (PDF, images)
- R-1.6: Maintenance deadline dashboard with calendar view
- R-1.7: Labor cost comparison across mechanics
- R-1.8: Automated compliance report generation
- R-1.9: Airworthiness status enforcement
- R-1.10: Daily summary notifications

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
| US-2.6 | Solo owner | See cost breakdown per job (parts vs labor) | Understand value of my DIY work |
| US-2.7 | Solo owner | Export service history to PDF | Show potential buyers my care record |
| US-2.8 | Solo owner | Set low-time alerts (50-hr, 100-hr) | Schedule work before it becomes urgent |
| US-2.9 | Solo owner | Add notes to my own work logs | Document what I changed |
| US-2.10 | Solo owner | Get notified when parts are due | Stay proactive about maintenance |

**Requirements:**
- R-2.1: Simplified aircraft creation (minimal fields)
- R-2.2: Self-service maintenance logging with labor cost field
- R-2.3: Mechanic search by specialty with dropdown filters
- R-2.4: Cost aggregation by category (parts, labor, total)
- R-2.5: Notification system with configurable triggers
- R-2.6: Job cost breakdown view
- R-2.7: Export service history as PDF
- R-2.8: Low-time threshold alerts
- R-2.9: Work log notes field
- R-2.10: Parts replacement reminders

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
| US-3.6 | Manager | View aircraft utilization metrics | Optimize aircraft allocation |
| US-3.7 | Billing specialist | Apply client-specific pricing tiers | Handle different billing arrangements |
| US-3.8 | Director | Get monthly fleet health dashboard | Track performance across all clients |
| US-3.9 | Manager | Create client-specific dashboards | Show each client their data |
| US-3.10 | Operations lead | Set up automated status reports | Keep clients informed proactively |

**Requirements:**
- R-3.1: Multi-tenant architecture (client-level isolation)
- R-3.2: Invoice generation with line-item maintenance records
- R-3.3: Dashboard with fleet-wide KPIs (cost, downtime, MTBF)
- R-3.4: Mechanic assignment with location/shift constraints
- R-3.5: Data export (CSV/Excel) for compliance
- R-3.6: Aircraft utilization tracking (flight hours, days in service)
- R-3.7: Client pricing configuration system
- R-3.8: Executive-level fleet analytics
- R-3.9: Client-specific dashboard customization
- R-3.10: Automated status report scheduling

### 4. Fixed Base Operator (FBO) Manager
**Background:** Runs an FBO with 10+ mechanics, serves private pilots and charter companies.
**Goals:** Maximize shop throughput, track technician efficiency, manage client relationships

**User Stories:**
| ID | As a... | I want to... | So that... |
|----|---------|------------|------------|
| US-4.1 | FBO Manager | View daily shop capacity | Avoid overbooking |
| US-4.2 | FBO Manager | Track turnaround time per job | Improve customer satisfaction |
| US-4.3 | FBO Manager | See which mechanics are idle | Deploy resources efficiently |
| US-4.4 | FBO Manager | Generate customer satisfaction scores | Identify service issues |
| US-4.5 | FBO Manager | Link jobs to client accounts | Track revenue per client |
| US-4.6 | FBO Manager | View completed jobs with photos | Verify quality before sign-off |
| US-4.7 | FBO Manager | Set up customer notification preferences | Send status updates automatically |
| US-4.8 | FBO Manager | Track parts inventory levels | Avoid stockouts |
| US-4.9 | FBO Manager | Create premium service packages | Upsell maintenance bundles |
| US-4.10 | FBO Manager | Generate daily production report | Review shop performance |

**Requirements:**
- R-4.1: Daily capacity dashboard
- R-4.2: Turnaround time tracking
- R-4.3: Technician availability status
- R-4.4: Customer feedback collection
- R-4.5: Client account billing
- R-4.6: Photo evidence per job
- R-4.7: Notification preferences per customer
- R-4.8: Parts inventory management
- R-4.9: Service package definitions
- R-4.10: Daily production metrics

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

## Maintenance Procedures & Configuration Personas

### 8. Maintenance Documentation Manager (Doc Manager)
**Background:** Maintains FAA compliance documentation, configures procedure templates.
**Goals:** Ensure all procedures are FAA-compliant, easy to update when regulations change

**User Stories:**
| ID | As a... | I want to... | So that... |
|----|---------|------------|------------|
| US-8.1 | Doc Manager | Import FAA AC 43.13-1B procedures | Have authoritative maintenance methods |
| US-8.2 | Doc Manager | Import AC 20-106 annual inspection templates | Ensure compliance with annual requirements |
| US-8.3 | Doc Manager | Link procedures to specific aircraft types | Apply correct procedures per aircraft |
| US-8.4 | Doc Manager | Configure recurring maintenance intervals | Automate scheduling for 50-hr, 100-hr, annual |
| US-8.5 | Doc Manager | Update procedure templates when FAA issues changes | Keep platform current with regulations |
| US-8.6 | Doc Manager | Create custom procedure variations | Handle aircraft-specific modifications |
| US-8.7 | Doc Manager | Export procedure configurations for audit | Show compliance during FAA inspection |
| US-8.8 | Doc Manager | Version control for procedure templates | Track changes over time |
| US-8.9 | Doc Manager | Tag procedures by maintenance type | Filter by annual, 100-hr, condition, etc. |
| US-8.10 | Doc Manager | Link parts/tools to procedure tasks | Ensure techs have correct resources |

**Requirements:**
- R-8.1: FAA AC 43.13-1B import capability
- R-8.2: AC 20-106 annual inspection templates
- R-8.3: Aircraft type procedure mapping
- R-8.4: Recurring maintenance configuration
- R-8.5: Procedure template update system
- R-8.6: Custom procedure variation support
- R-8.7: Audit-ready procedure export
- R-8.8: Procedure versioning
- R-8.9: Procedure categorization system
- R-8.10: Parts/tools linking to tasks

### 9. Workflow Builder (Admin)
**Background:** Builds custom maintenance workflows using visual builder.
**Goals:** Create complex maintenance flows with conditional logic

**User Stories:**
| ID | As a... | I want to... | So that... |
|----|---------|------------|------------|
| US-9.1 | Workflow Builder | Drag-and-drop tasks into sequence | Build maintenance procedures visually |
| US-9.2 | Workflow Builder | Add conditional logic branches | Handle different aircraft configurations |
| US-9.3 | Workflow Builder | Link tools to specific tasks | Ensure correct tools are available |
| US-9.4 | Workflow Builder | Set task duration estimates | Improve scheduling accuracy |
| US-9.5 | Workflow Builder | Create procedure dependencies | Enforce proper work order |
| US-9.6 | Workflow Builder | Preview workflow before saving | Catch errors before deployment |
| US-9.7 | Workflow Builder | Duplicate existing procedures | Save time on similar procedures |
| US-9.8 | Workflow Builder | Set task priorities within procedure | Highlight critical steps |
| US-9.9 | Workflow Builder | Add notes/instructions to tasks | Provide context for mechanics |
| US-9.10 | Workflow Builder | Export workflow as PDF/HTML | Share with team or auditors |

**Requirements:**
- R-9.1: Drag-and-drop task builder
- R-9.2: Conditional logic (if/else, aircraft type checks)
- R-9.3: Tool-to-task linking
- R-9.4: Duration estimation per task
- R-9.5: Task dependencies
- R-9.6: Visual workflow preview
- R-9.7: Procedure duplication
- R-9.8: Task priority tags
- R-9.9: Task instructions/notes
- R-9.10: Workflow export capabilities

### 10. Aircraft Technician (Tech)
**Background:** Uses configured procedures to perform maintenance.
**Goals:** Follow step-by-step procedures, track work, report issues

**User Stories:**
| ID | As a... | I want to... | So that... |
|----|---------|------------|------------|
| US-10.1 | Tech | View procedure steps for assigned job | Know exactly what to do |
| US-10.2 | Tech | Check off checklist items as I complete them | Track progress in real time |
| US-10.3 | Tech | See required tools per step | Gather everything before starting |
| US-10.4 | Tech | Record parts used per step | Track consumption accurately |
| US-10.5 | Tech | Upload photos of completed work | Document completion |
| US-10.6 | Tech | Flag issues during procedure | Report problems immediately |
| US-10.7 | Tech | Skip optional steps when not applicable | Handle aircraft variations |
| US-10.8 | Tech | See time spent per step | Improve my efficiency |
| US-10.9 | Tech | Save incomplete procedures | Return later if interrupted |
| US-10.10 | Tech | Get procedure updates mid-job | Receive new instructions if needed |

**Requirements:**
- R-10.1: Step-by-step procedure display
- R-10.2: Checklist item toggling
- R-10.3: Tools visibility per step
- R-10.4: Parts usage recording
- R-10.5: Photo attachment capability
- R-10.6: Issue flagging system
- R-10.7: Step skipping for optional tasks
- R-10.8: Time tracking per step
- R-10.9: Incomplete workflow saving
- R-10.10: Real-time procedure updates

---

## Priority Matrix

| Priority | Stories | Reason |
|----------|---------|--------|
| P0 - Launch | US-1.1, US-1.2, US-2.1, US-2.2, US-4.1, US-4.2, US-8.1, US-9.1 | Core flight school, solo owner, and FAA procedure foundation |
| P1 - Month 1 | US-1.3, US-1.4, US-2.3, US-2.4, US-4.3, US-4.4, US-6.1, US-6.3, US-8.3, US-9.2 | Fleet tracking, job scheduling, and workflow builder logic |
| P2 - Month 2 | US-1.5, US-2.5, US-3.1, US-3.2, US-5.1, US-5.2, US-6.2, US-6.4, US-8.2, US-9.3, US-10.1 | Document management, multi-tenant, and procedure execution |
| P3 - Month 3 | US-3.3, US-3.4, US-5.3, US-5.4, US-6.5, US-7.1, US-7.2, US-8.4, US-8.5, US-9.4-9.10 | Analytics, admin, and advanced workflow features |

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
