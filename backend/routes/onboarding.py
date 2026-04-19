"""
Onboarding routes for SkyMechanics Platform.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import ValidationError
from typing import Optional

from onboarding import (
    full_onboarding,
    complete_onboarding,
    check_onboarding_status,
    OnboardRequest,
    BulkImportRequest,
    OnboardResponse,
    OnboardStatusResponse
)

router = APIRouter(
    prefix="/api/v1/onboard",
    tags=["Onboarding"]
)


@router.post("", response_model=OnboardResponse)
async def onboard(request: OnboardRequest):
    """
    Create a new tenant account with initial setup.
    
    This endpoint:
    1. Creates a new FalkorDB graph for the tenant
    2. Sets up the graph schema (indexes)
    3. Creates the initial admin user
    4. Returns authentication token and tenant info
    """
    try:
        result = full_onboarding(request)
        return result
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e.errors()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Onboarding failed: {str(e)}")


@router.post("/bulk")
async def onboard_bulk(
    graph_name: str,
    request: BulkImportRequest,
    token: Optional[str] = None
):
    """
    Import initial aircraft and mechanics data.
    
    This is used during onboarding to quickly set up the tenant
    with demo data.
    """
    try:
        result = complete_onboarding(graph_name, request)
        return {
            "success": True,
            "imported": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Import failed: {str(e)}")


@router.get("/status")
async def onboard_status(graph_name: str) -> OnboardStatusResponse:
    """
    Check the onboarding status for a tenant graph.
    
    Returns whether the tenant has completed setup:
    - Admin user exists
    - At least one aircraft exists
    - At least one mechanic exists
    """
    try:
        result = check_onboarding_status(graph_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")


@router.get("/check-email")
async def check_email(email: str):
    """
    Check if an email is already registered.
    """
    # TODO: Implement email uniqueness check
    return {"email": email, "available": True}
