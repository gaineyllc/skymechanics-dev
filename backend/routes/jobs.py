"""
Jobs routes for SkyMechanics Platform.
Handles job CRUD operations and workflow transitions.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import ValidationError
from typing import Optional, Dict, Any, List

from models import (
    JobCreateRequest,
    JobUpdateRequest,
    JobStatusRequest,
    SuccessResponse,
    ErrorResponse
)

router = APIRouter(
    prefix="/api/v1/jobs",
    tags=["Jobs"]
)


# Job workflow states
JOB_WORKFLOW = {
    "pending": ["open", "cancelled"],
    "open": ["in_progress", "completed", "cancelled"],
    "in_progress": ["completed", "pending"],
    "completed": [],
    "cancelled": []
}


@router.get("", response_model=List[Dict[str, Any]])
async def list_jobs(
    status: Optional[str] = None,
    priority: Optional[str] = None,
    customer_id: Optional[int] = None
):
    """
    List jobs with optional filters.
    
    Query params:
    - status: filter by job status
    - priority: filter by priority (low, medium, high)
    - customer_id: filter by customer
    """
    # TODO: Implement actual database query
    return [
        {
            "node_id": 1,
            "label": "Job",
            "properties": {
                "title": "Engine Overhaul",
                "description": "Complete engine inspection and repair",
                "status": "open",
                "priority": "high",
                "customer_id": 101,
                "created_at": "2026-04-19T10:00:00Z",
                "updated_at": "2026-04-19T10:00:00Z"
            }
        }
    ]


@router.get("/{job_id}", response_model=Dict[str, Any])
async def get_job(job_id: int):
    """
    Get a specific job by ID.
    """
    # TODO: Implement actual database query
    return {
        "node_id": job_id,
        "label": "Job",
        "properties": {
            "title": "Engine Overhaul",
            "description": "Complete engine inspection and repair",
            "status": "open",
            "priority": "high",
            "customer_id": 101,
            "mechanic_id": 201,
            "created_at": "2026-04-19T10:00:00Z",
            "updated_at": "2026-04-19T10:00:00Z"
        }
    }


@router.post("", response_model=Dict[str, Any])
async def create_job(request: JobCreateRequest):
    """
    Create a new job.
    
    Creates a job node in the graph with the specified properties.
    """
    try:
        return {
            "success": True,
            "node_id": 1,
            "label": "Job",
            "properties": {
                "title": request.title,
                "description": request.description,
                "status": request.status or "pending",
                "priority": request.priority or "medium",
                "customer_id": request.customer_id,
                "created_at": "2026-04-20T00:00:00Z",
                "updated_at": "2026-04-20T00:00:00Z"
            }
        }
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e.errors()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job creation failed: {str(e)}")


@router.put("/{job_id}", response_model=Dict[str, Any])
async def update_job(job_id: int, request: JobUpdateRequest):
    """
    Update job properties.
    """
    try:
        return {
            "success": True,
            "node_id": job_id,
            "label": "Job",
            "properties": {
                **request.model_dump(),
                "updated_at": "2026-04-20T00:00:00Z"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job update failed: {str(e)}")


@router.post("/{job_id}/status", response_model=Dict[str, Any])
async def update_job_status(job_id: int, request: JobStatusRequest):
    """
    Update job status with workflow validation.
    
    Valid transitions:
    - pending → open, cancelled
    - open → in_progress, completed, cancelled
    - in_progress → completed, pending
    - completed → (no transitions)
    - cancelled → (no transitions)
    """
    # TODO: Implement actual database query with workflow validation
    valid_transitions = JOB_WORKFLOW.get(request.status, [])
    
    if request.new_status not in valid_transitions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition from '{request.status}' to '{request.new_status}'. Valid options: {valid_transitions}"
        )
    
    return {
        "success": True,
        "node_id": job_id,
        "old_status": request.status,
        "new_status": request.new_status,
        "timestamp": "2026-04-20T00:00:00Z"
    }


@router.delete("/{job_id}")
async def delete_job(job_id: int):
    """
    Delete a job (soft delete).
    """
    try:
        return {
            "success": True,
            "node_id": job_id,
            "message": "Job soft deleted"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job deletion failed: {str(e)}")


@router.get("/{job_id}/workflow")
async def get_job_workflow(job_id: int):
    """
    Get the workflow diagram data for a job.
    
    Returns nodes and edges for visual workflow builder.
    """
    return {
        "nodes": [
            {"id": "job_1", "type": "job", "label": "Engine Overhaul", "status": "open", "priority": "high"},
            {"id": "customer_101", "type": "customer", "label": "John Doe", "relationship": "customer_of"},
            {"id": "mechanic_201", "type": "mechanic", "label": "Jane Smith", "relationship": "assigned_to"},
            {"id": "aircraft_501", "type": "aircraft", "label": "N12345", "relationship": "on"},
        ],
        "edges": [
            {"from": "job_1", "to": "customer_101", "label": "for_customer"},
            {"from": "job_1", "to": "mechanic_201", "label": "assigned"},
            {"from": "job_1", "to": "aircraft_501", "label": "on_aircraft"},
        ],
        "workflow": JOB_WORKFLOW
    }


@router.get("/workflow/complete")
async def get_complete_workflow():
    """
    Get the complete job workflow definition for the visual builder.
    
    Returns all nodes, edges, and transitions for full workflow visualization.
    """
    return {
        "workflow": {
            "name": "Job Workflow",
            "description": "Complete job lifecycle workflow",
            "states": [
                {"id": "pending", "label": "Pending", "description": "Job created, awaiting assignment"},
                {"id": "open", "label": "Open", "description": "Job accepted, work准备开始"},
                {"id": "in_progress", "label": "In Progress", "description": "Work in progress"},
                {"id": "completed", "label": "Completed", "description": "Work finished, awaiting sign-off"},
                {"id": "cancelled", "label": "Cancelled", "description": "Job cancelled"}
            ],
            "transitions": [
                {"from": "pending", "to": "open", "label": "Accept Job"},
                {"from": "pending", "to": "cancelled", "label": "Cancel Job"},
                {"from": "open", "to": "in_progress", "label": "Start Work"},
                {"from": "open", "to": "completed", "label": "Complete"},
                {"from": "open", "to": "cancelled", "label": "Cancel"},
                {"from": "in_progress", "to": "completed", "label": "Finish Work"},
                {"from": "in_progress", "to": "pending", "label": "Pause"},
                {"from": "completed", "to": "open", "label": "Request Revisions"},
            ],
            "allowed_relationships": [
                {"from": "Job", "to": "Customer", "label": "for_customer"},
                {"from": "Job", "to": "Mechanic", "label": "assigned_to"},
                {"from": "Job", "to": "Aircraft", "label": "on_aircraft"},
                {"from": "Mechanic", "to": "Customer", "label": "provides_service_to"},
            ]
        }
    }
