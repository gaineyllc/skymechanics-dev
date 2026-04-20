"""
Shared Pydantic models for SkyMechanics microservices.
This package contains models used across multiple services.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ========== Auth Service Models ==========

class UserCreateRequest(BaseModel):
    """Request to create a new user."""
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    password: str


class UserResponse(BaseModel):
    """Response for user operations."""
    user_id: int
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    role: str
    created_at: datetime


class TokenResponse(BaseModel):
    """Authentication token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    """Login request."""
    email: str
    password: str


# ========== Mechanic Service Models ==========

class MechanicCreateRequest(BaseModel):
    """Request to create a new mechanic."""
    name: str
    email: str
    phone: Optional[str] = None
    specialties: List[str] = Field(default_factory=list)


class MechanicResponse(BaseModel):
    """Response for mechanic operations."""
    mechanic_id: int
    name: str
    email: str
    phone: Optional[str] = None
    specialties: List[str]
    license_number: Optional[str] = None
    certifications: List[str] = Field(default_factory=list)
    availability: Dict[str, Any] = Field(default_factory=dict)
    current_location: Optional[Dict[str, float]] = None
    created_at: datetime


class MechanicUpdateRequest(BaseModel):
    """Request to update a mechanic."""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    specialties: Optional[List[str]] = None
    license_number: Optional[str] = None
    certifications: Optional[List[str]] = None
    availability: Optional[Dict[str, Any]] = None
    current_location: Optional[Dict[str, float]] = None


# ========== Jobs Service Models ==========

class JobCreateRequest(BaseModel):
    """Request to create a new job."""
    customer_id: int
    title: str
    description: Optional[str] = None
    status: str = "pending"
    priority: str = "medium"
    mechanic_id: Optional[int] = None


class JobUpdateRequest(BaseModel):
    """Request to update job properties."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    mechanic_id: Optional[int] = None


class JobResponse(BaseModel):
    """Response for job operations."""
    job_id: int
    customer_id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    mechanic_id: Optional[int]
    created_at: datetime
    updated_at: datetime


class JobStatusRequest(BaseModel):
    """Request to update job status."""
    status: str = Field(..., description="Current job status")
    new_status: str = Field(..., description="New job status")
    comment: Optional[str] = None


# ========== Customer Service Models ==========

class CustomerCreateRequest(BaseModel):
    """Request to create a new customer."""
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[Dict[str, str]] = None


class CustomerResponse(BaseModel):
    """Response for customer operations."""
    customer_id: int
    name: str
    email: str
    phone: Optional[str] = None
    address: Optional[Dict[str, str]] = None
    created_at: datetime


class CustomerUpdateRequest(BaseModel):
    """Request to update a customer."""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[Dict[str, str]] = None


# ========== Common Response Models ==========

class SuccessResponse(BaseModel):
    """Standard success response."""
    success: bool = True
    message: str = ""


class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    error: str
    details: Optional[str] = None


class PaginatedResponse(BaseModel):
    """Pagination response wrapper."""
    items: List[Any]
    total: int
    page: int
    page_size: int
    total_pages: int
