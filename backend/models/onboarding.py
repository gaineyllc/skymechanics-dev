"""
Pydantic models for onboarding operations.
"""
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime


class OnboardRequest(BaseModel):
    """Request model for account onboarding."""
    email: EmailStr
    password: str
    account_type: str
    org_name: str
    first_name: str
    last_name: str

    @validator('account_type')
    def validate_account_type(cls, v):
        allowed = {'flight_school', 'solo_owner', 'fbo_shop'}
        if v not in allowed:
            raise ValueError(f'account_type must be one of: {allowed}')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class BulkImportRequest(BaseModel):
    """Request model for bulk import during onboarding."""
    aircraft: Optional[List[dict]] = None
    mechanics: Optional[List[dict]] = None


class OnboardResponse(BaseModel):
    """Response model for successful onboarding."""
    success: bool
    tenant_id: str
    graph_name: str
    token: str
    user_id: str


class OnboardStatusResponse(BaseModel):
    """Response model for onboarding status check."""
    setup_complete: bool
    has_aircraft: bool = False
    has_mechanics: bool = False
    has_admin: bool = False
