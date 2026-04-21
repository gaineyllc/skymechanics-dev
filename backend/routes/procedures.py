"""
Procedures routes for SkyMechanics Platform.
Handles maintenance procedure templates, tools, parts, and aircraft type configurations.
"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import ValidationError
from typing import Optional, Dict, Any, List
import os

from models import (
    ConfigSourceCreateRequest,
    ConfigSourceResponse,
    ProcedureTemplateCreateRequest,
    ProcedureTemplateResponse,
    TaskCreateRequest,
    TaskResponse,
    ToolCreateRequest,
    ToolResponse,
    PartCreateRequest,
    PartResponse,
    AircraftTypeCreateRequest,
    AircraftTypeResponse,
    SuccessResponse,
    ErrorResponse
)

router = APIRouter(
    prefix="/api/v1",
    tags=["Procedures"]
)

# In-memory storage (will be replaced with FalkorDB in phase 2)
config_sources: Dict[int, Dict[str, Any]] = {}
procedures: Dict[int, Dict[str, Any]] = {}
tasks: Dict[int, Dict[str, Any]] = {}
tools: Dict[int, Dict[str, Any]] = {}
parts: Dict[int, Dict[str, Any]] = {}
aircraft_types: Dict[int, Dict[str, Any]] = {}

# ID counters
config_source_id_counter = 1
procedure_id_counter = 1
task_id_counter = 1
tool_id_counter = 1
part_id_counter = 1
aircraft_type_id_counter = 1


# ============== Configuration Sources ==============

@router.get("/config/sources", response_model=List[ConfigSourceResponse])
async def list_config_sources():
    """List all configuration sources."""
    return [
        {
            "source_id": k,
            **{kk: vv for kk, vv in v.items() if kk != "id"}
        }
        for k, v in config_sources.items()
    ]


@router.post("/config/sources", response_model=ConfigSourceResponse)
async def create_config_source(request: ConfigSourceCreateRequest):
    """Create a new configuration source."""
    global config_source_id_counter
    
    config_source = {
        "id": config_source_id_counter,
        "name": request.name,
        "type": request.type,
        "version": request.version,
        "url": request.url,
        "description": request.description,
        "is_active": request.is_active,
        "created_at": "2026-04-21T00:00:00Z",
        "last_updated": "2026-04-21T00:00:00Z"
    }
    
    config_sources[config_source_id_counter] = config_source
    config_source_id_counter += 1
    
    return config_source


@router.get("/config/sources/{source_id}", response_model=ConfigSourceResponse)
async def get_config_source(source_id: int):
    """Get a configuration source by ID."""
    if source_id not in config_sources:
        raise HTTPException(status_code=404, detail=f"Configuration source {source_id} not found")
    source = config_sources[source_id]
    return {
        "source_id": source_id,
        **{kk: vv for kk, vv in source.items() if kk != "id"}
    }


# ============== Procedure Templates ==============

@router.get("/config/procedures", response_model=List[ProcedureTemplateResponse])
async def list_procedures(category: Optional[str] = None, is_active: Optional[bool] = None):
    """List procedure templates with optional filters."""
    result = []
    for pid, proc in procedures.items():
        if category and proc.get("category") != category:
            continue
        if is_active is not None and proc.get("is_active") != is_active:
            continue
        # Get tasks for this procedure
        proc_tasks = [
            {
                "task_id": tid,
                **{kk: vv for kk, vv in task.items() if kk != "id" and kk != "procedure_id"}
            }
            for tid, task in tasks.items()
            if task.get("procedure_id") == pid
        ]
        result.append({
            "procedure_id": pid,
            **{kk: vv for kk, vv in proc.items() if kk != "id"},
            "tasks": proc_tasks
        })
    return result


@router.post("/config/procedures", response_model=ProcedureTemplateResponse)
async def create_procedure(request: ProcedureTemplateCreateRequest):
    """Create a new procedure template."""
    global procedure_id_counter
    
    procedure = {
        "id": procedure_id_counter,
        "name": request.name,
        "category": request.category,
        "authority": request.authority,
        "estimated_duration_hours": request.estimated_duration_hours,
        "required_specialty": request.required_specialty,
        "source_id": request.source_id,
        "is_active": request.is_active,
        "created_at": "2026-04-21T00:00:00Z",
        "updated_at": "2026-04-21T00:00:00Z"
    }
    
    procedures[procedure_id_counter] = procedure
    procedure_id_counter += 1
    
    return {
        "procedure_id": procedure_id_counter - 1,
        **{kk: vv for kk, vv in procedure.items() if kk != "id"},
        "tasks": []
    }


@router.get("/config/procedures/{procedure_id}", response_model=ProcedureTemplateResponse)
async def get_procedure(procedure_id: int):
    """Get a procedure template by ID with all tasks."""
    if procedure_id not in procedures:
        raise HTTPException(status_code=404, detail=f"Procedure {procedure_id} not found")
    
    proc = procedures[procedure_id]
    proc_tasks = [
        {
            "task_id": tid,
            **{kk: vv for kk, vv in task.items() if kk != "id" and kk != "procedure_id"}
        }
        for tid, task in tasks.items()
        if task.get("procedure_id") == procedure_id
    ]
    
    return {
        "procedure_id": procedure_id,
        **{kk: vv for kk, vv in proc.items() if kk != "id"},
        "tasks": proc_tasks
    }


# ============== Tasks ==============

@router.get("/config/tasks", response_model=List[TaskResponse])
async def list_tasks(procedure_id: Optional[int] = None):
    """List task templates with optional procedure filter."""
    result = []
    for tid, task in tasks.items():
        if procedure_id and task.get("procedure_id") != procedure_id:
            continue
        result.append({
            "task_id": tid,
            **{kk: vv for kk, vv in task.items() if kk != "id" and kk != "procedure_id"}
        })
    return result


@router.post("/config/tasks", response_model=TaskResponse)
async def create_task(request: TaskCreateRequest):
    """Create a new task template."""
    global task_id_counter
    
    task = {
        "id": task_id_counter,
        "procedure_id": request.procedure_id,
        "name": request.name,
        "sequence": request.sequence,
        "category": request.category,
        "estimated_duration_minutes": request.estimated_duration_minutes,
        "required_tools": request.required_tools,
        "required_parts": request.required_parts,
        "checklist_items": request.checklist_items,
        "instructions": request.instructions,
        "created_at": "2026-04-21T00:00:00Z",
        "updated_at": "2026-04-21T00:00:00Z"
    }
    
    tasks[task_id_counter] = task
    task_id_counter += 1
    
    return {
        "task_id": task_id_counter - 1,
        **{kk: vv for kk, vv in task.items() if kk != "id" and kk != "procedure_id"}
    }


@router.get("/config/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int):
    """Get a task template by ID."""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    task = tasks[task_id]
    return {
        "task_id": task_id,
        **{kk: vv for kk, vv in task.items() if kk != "id" and kk != "procedure_id"}
    }


# ============== Tools ==============

@router.get("/config/tools", response_model=List[ToolResponse])
async def list_tools(category: Optional[str] = None):
    """List tool configurations with optional category filter."""
    result = []
    for tid, tool in tools.items():
        if category and tool.get("category") != category:
            continue
        result.append({
            "tool_id": tid,
            **{kk: vv for kk, vv in tool.items() if kk != "id"}
        })
    return result


@router.post("/config/tools", response_model=ToolResponse)
async def create_tool(request: ToolCreateRequest):
    """Create a new tool configuration."""
    global tool_id_counter
    
    tool = {
        "id": tool_id_counter,
        "name": request.name,
        "category": request.category,
        "part_number": request.part_number,
        "calibration_required": request.calibration_required,
        "calibration_interval_months": request.calibration_interval_months,
        "description": request.description,
        "created_at": "2026-04-21T00:00:00Z",
        "updated_at": "2026-04-21T00:00:00Z"
    }
    
    tools[tool_id_counter] = tool
    tool_id_counter += 1
    
    return {
        "tool_id": tool_id_counter - 1,
        **{kk: vv for kk, vv in tool.items() if kk != "id"}
    }


@router.get("/config/tools/{tool_id}", response_model=ToolResponse)
async def get_tool(tool_id: int):
    """Get a tool configuration by ID."""
    if tool_id not in tools:
        raise HTTPException(status_code=404, detail=f"Tool {tool_id} not found")
    
    tool = tools[tool_id]
    return {
        "tool_id": tool_id,
        **{kk: vv for kk, vv in tool.items() if kk != "id"}
    }


# ============== Parts ==============

@router.get("/config/parts", response_model=List[PartResponse])
async def list_parts(category: Optional[str] = None, aircraft_id: Optional[str] = None):
    """List parts catalog with optional filters."""
    result = []
    for pid, part in parts.items():
        if category and part.get("category") != category:
            continue
        if aircraft_id and aircraft_id not in part.get("aircraft_compatible", []):
            continue
        result.append({
            "part_id": pid,
            **{kk: vv for kk, vv in part.items() if kk != "id"}
        })
    return result


@router.post("/config/parts", response_model=PartResponse)
async def create_part(request: PartCreateRequest):
    """Create a new parts catalog entry."""
    global part_id_counter
    
    part = {
        "id": part_id_counter,
        "part_number": request.part_number,
        "name": request.name,
        "category": request.category,
        "aircraft_compatible": request.aircraft_compatible,
        "oem_source": request.oem_source,
        "description": request.description,
        "created_at": "2026-04-21T00:00:00Z",
        "updated_at": "2026-04-21T00:00:00Z"
    }
    
    parts[part_id_counter] = part
    part_id_counter += 1
    
    return {
        "part_id": part_id_counter - 1,
        **{kk: vv for kk, vv in part.items() if kk != "id"}
    }


@router.get("/config/parts/{part_id}", response_model=PartResponse)
async def get_part(part_id: int):
    """Get a parts catalog entry by ID."""
    if part_id not in parts:
        raise HTTPException(status_code=404, detail=f"Part {part_id} not found")
    
    part = parts[part_id]
    return {
        "part_id": part_id,
        **{kk: vv for kk, vv in part.items() if kk != "id"}
    }


# ============== Aircraft Types ==============

@router.get("/config/aircraft-types", response_model=List[AircraftTypeResponse])
async def list_aircraft_types():
    """List all aircraft type configurations."""
    return [
        {
            "aircraft_type_id": k,
            **{kk: vv for kk, vv in v.items() if kk != "id"}
        }
        for k, v in aircraft_types.items()
    ]


@router.post("/config/aircraft-types", response_model=AircraftTypeResponse)
async def create_aircraft_type(request: AircraftTypeCreateRequest):
    """Create an aircraft type configuration."""
    global aircraft_type_id_counter
    
    aircraft_type = {
        "id": aircraft_type_id_counter,
        "make": request.make,
        "model": request.model,
        "category": request.category,
        "certification": request.certification,
        "amm_ref": request.amm_ref,
        "mpd_ref": request.mpd_ref,
        "ipc_ref": request.ipc_ref,
        "created_at": "2026-04-21T00:00:00Z",
        "updated_at": "2026-04-21T00:00:00Z"
    }
    
    aircraft_types[aircraft_type_id_counter] = aircraft_type
    aircraft_type_id_counter += 1
    
    return {
        "aircraft_type_id": aircraft_type_id_counter - 1,
        **{kk: vv for kk, vv in aircraft_type.items() if kk != "id"}
    }


@router.get("/config/aircraft-types/{aircraft_type_id}", response_model=AircraftTypeResponse)
async def get_aircraft_type(aircraft_type_id: int):
    """Get an aircraft type configuration by ID."""
    if aircraft_type_id not in aircraft_types:
        raise HTTPException(status_code=404, detail=f"Aircraft type {aircraft_type_id} not found")
    
    aircraft_type = aircraft_types[aircraft_type_id]
    return {
        "aircraft_type_id": aircraft_type_id,
        **{kk: vv for kk, vv in aircraft_type.items() if kk != "id"}
    }


# ============== FAA Documentation Import ==============

@router.post("/config/import/faa/ac-43-13-1b")
async def import_ac_43_13_1b():
    """
    Import procedures from FAA AC 43.13-1B.
    
    This endpoint parses and imports the AC 43.13-1B acceptable methods
    and techniques into the procedure template system.
    """
    # TODO: Implement actual document parsing
    # For now, return a placeholder import
    return {
        "success": True,
        "message": "AC 43.13-1B import initiated",
        "procedures_imported": 0,
        "tasks_imported": 0,
        "details": "Document parsing not yet implemented"
    }


@router.post("/config/import/faa/ac-20-106")
async def import_ac_20_106():
    """
    Import annual inspection procedures from FAA AC 20-106.
    
    This endpoint parses and imports the annual inspection checklist
    into the procedure template system.
    """
    # TODO: Implement actual document parsing
    return {
        "success": True,
        "message": "AC 20-106 import initiated",
        "procedures_imported": 0,
        "tasks_imported": 0,
        "details": "Document parsing not yet implemented"
    }


@router.get("/config/procedures/{procedure_id}/execute")
async def execute_procedure(procedure_id: int):
    """
    Get the procedure execution view data.
    
    Returns tasks in execution order with all required resources.
    """
    if procedure_id not in procedures:
        raise HTTPException(status_code=404, detail=f"Procedure {procedure_id} not found")
    
    proc = procedures[procedure_id]
    proc_tasks = [
        {
            "task_id": tid,
            **{kk: vv for kk, vv in task.items() if kk != "id" and kk != "procedure_id"}
        }
        for tid, task in sorted(tasks.items(), key=lambda x: x[1].get("sequence", 0))
        if task.get("procedure_id") == procedure_id
    ]
    
    # Get tool and part details for each task
    for task in proc_tasks:
        task["tools_detail"] = [
            tools.get(int(tid), {})
            for tid in task.get("required_tools", [])
        ]
        task["parts_detail"] = [
            parts.get(int(pid), {})
            for pid in task.get("required_parts", [])
        ]
    
    return {
        "procedure_id": procedure_id,
        "name": proc.get("name", ""),
        "category": proc.get("category", ""),
        "estimated_duration_hours": proc.get("estimated_duration_hours", 0),
        "required_specialty": proc.get("required_specialty", ""),
        "tasks": proc_tasks
    }
