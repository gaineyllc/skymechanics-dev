# Maintenance Procedures Feature - Implementation Plan

## Overview
Build a comprehensive maintenance procedures configuration system with drag-and-drop workflow builder integration.

## Phase 1: Backend - Configuration Models & API (30 min)

### Files to Create/Modify

#### 1. Create `backend/models.py` additions
- `ConfigSource` - FAA/OEM documentation sources
- `ProcedureTemplate` - Maintenance procedure templates
- `Task` - Individual tasks within procedures
- `Tool` - Tool configurations
- `Part` - Parts catalog
- `AircraftType` - Aircraft-specific configurations

#### 2. Create `backend/routes/procedures.py`
- `GET /api/v1/config/sources` - List configuration sources
- `POST /api/v1/config/sources` - Add configuration source
- `GET /api/v1/config/procedures` - List procedure templates
- `POST /api/v1/config/procedures` - Create procedure template
- `GET /api/v1/config/procedures/{id}` - Get procedure with tasks
- `GET /api/v1/config/tasks` - List task templates
- `GET /api/v1/config/tools` - List tool configurations
- `GET /api/v1/config/parts` - List parts catalog
- `POST /api/v1/config/aircraft-types` - Create aircraft type config

#### 3. Create `backend/scripts/import-faa-docs.py`
- Import AC 43.13-1B procedures
- Import AC 20-106 annual inspection templates
- Extract checklist items from documents

## Phase 2: Frontend - Configuration UI (45 min)

### Files to Create/Modify

#### 4. Create `frontend/src/components/ProcedureBuilder.tsx`
- Drag-and-drop task builder
- Task list editor
- Checklist item management
- Tool/part assignment

#### 5. Create `frontend/src/components/ToolConfiguration.tsx`
- Tool catalog display
- Tool configuration form
- Calibration tracking

#### 6. Create `frontend/src/components/PartsCatalog.tsx`
- Parts search and filtering
- Aircraft compatibility matrix
- Part details view

#### 7. Update `frontend/src/services/api.ts`
- Add procedure configuration API methods
- Add tool/part API methods

#### 8. Update `frontend/src/components/index.ts`
- Export new components

## Phase 3: Integration (30 min)

#### 9. Update `frontend/src/components/WorkflowBuilder.tsx`
- Extend for procedure workflow (not just job workflow)
- Add task execution view
- Add step-by-step procedure runner

#### 10. Create `frontend/src/pages/Procedures.tsx`
- Procedure list view
- Procedure detail view
- Procedure builder view

## Phase 4: FAA Documentation Import (30 min)

#### 11. Create import scripts for:
- AC 43.13-1B (acceptable methods & techniques)
- AC 20-106 (annual inspection checklist)
- Standard parts list
- Tool requirements

## Phase 5: Testing & Documentation (15 min)

#### 12. Update tests
#### 13. Update documentation

## Total Time Estimate: 2.5 hours
