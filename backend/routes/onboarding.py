# Routes package
from onboarding import (
    full_onboarding,
    complete_onboarding,
    check_onboarding_status,
    OnboardRequest,
    BulkImportRequest,
    OnboardResponse,
    OnboardStatusResponse
)

from fastapi import APIRouter, HTTPException, Depends
from pydantic import ValidationError
from typing import Optional

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
        result = full_onboarding(
            email=request.email,
            password=request.password,
            company_name=request.company_name,
            full_name=request.full_name
        )
        return OnboardResponse(**result)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Onboarding failed: {str(e)}")


@router.post("/complete", response_model=OnboardResponse)
async def complete(request: OnboardRequest):
    """
    Complete onboarding for an existing user.
    
    This endpoint:
    1. Creates a new FalkorDB graph for the tenant
    2. Sets up the graph schema (indexes)
    3. Returns authentication token and tenant info
    """
    try:
        result = complete_onboarding(
            email=request.email,
            company_name=request.company_name,
            full_name=request.full_name
        )
        return OnboardResponse(**result)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Completing onboarding failed: {str(e)}")


@router.post("/bulk", response_model=OnboardResponse)
async def bulk_import(request: BulkImportRequest):
    """
    Bulk import onboarding data for a tenant.
    
    This endpoint:
    1. Creates a new FalkorDB graph for the tenant
    2. Sets up the graph schema (indexes)
    3. Bulk imports customers, mechanics, and jobs
    4. Returns authentication token and tenant info
    """
    try:
        result = bulk_import_onboard_data(
            email=request.email,
            password=request.password,
            company_name=request.company_name,
            full_name=request.full_name,
            customers=request.customers,
            mechanics=request.mechanics,
            jobs=request.jobs
        )
        return OnboardResponse(**result)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk onboarding failed: {str(e)}")


@router.get("/status", response_model=OnboardStatusResponse)
async def status(tenant_id: str):
    """
    Check onboarding status for a tenant.
    """
    try:
        result = check_onboarding_status(tenant_id)
        return OnboardStatusResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Checking onboarding status failed: {str(e)}")
