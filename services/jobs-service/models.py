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

class JobAssignRequest(BaseModel):
    """Request to assign a job to a mechanic."""
    mechanic_id: int


class JobCompleteRequest(BaseModel):
    """Request to complete a job with signatures."""
    mechanic_signature: str  # Base64 encoded image or hash
    owner_signature: Optional[str] = None
    parts_used: List[Dict[str, Any]] = Field(default_factory=list)
    labor_hours: Optional[float] = None
    labor_cost: Optional[float] = None
    total_cost: Optional[float] = None


class JobSummaryResponse(BaseModel):
    """Response for job summary with cost breakdown."""
    job_id: int
    customer_id: int
    aircraft_id: Optional[int]
    aircraft_tail_number: Optional[str]
    title: str
    description: Optional[str]
    status: str
    priority: str
    mechanic_id: Optional[int]
    mechanic_name: Optional[str]
    completed_at: Optional[datetime]
    labor_hours: Optional[float]
    parts_cost: Optional[float]
    labor_cost: Optional[float]
    total_cost: Optional[float]
    parts_used: List[Dict[str, Any]]
    signature_status: str  # "pending", "mechanic_signed", "owner_signed", "completed"
    created_at: datetime
    updated_at: datetime


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


# ========== Aircraft Service Models ==========

class AircraftCreateRequest(BaseModel):
    """Request to create a new aircraft."""
    tail_number: str
    model_id: Optional[int] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    registration_expires: Optional[str] = None
    airworthiness_directives: List[str] = Field(default_factory=list)
    service_bulletins: List[str] = Field(default_factory=list)


class AircraftResponse(BaseModel):
    """Response for aircraft operations."""
    aircraft_id: int
    tail_number: str
    model_id: Optional[int]
    manufacturer: Optional[str]
    model: Optional[str]
    year: Optional[int]
    registration_expires: Optional[str]
    airworthiness_directives: List[str]
    service_bulletins: List[str]
    created_at: datetime


class AircraftUpdateRequest(BaseModel):
    """Request to update an aircraft."""
    tail_number: Optional[str] = None
    model_id: Optional[int] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    registration_expires: Optional[str] = None
    airworthiness_directives: Optional[List[str]] = None
    service_bulletins: Optional[List[str]] = None


# ========== Parts Service Models ==========

class PartCreateRequest(BaseModel):
    """Request to create a new part."""
    part_number: str
    name: str
    description: Optional[str] = None
    quantity: int = 0
    unit_cost: float = 0.0
    supplier: Optional[str] = None
    lead_time_days: Optional[int] = None


class PartResponse(BaseModel):
    """Response for part operations."""
    part_id: int
    part_number: str
    name: str
    description: Optional[str]
    quantity: int
    unit_cost: float
    supplier: Optional[str]
    lead_time_days: Optional[int]
    created_at: datetime


class PartUpdateRequest(BaseModel):
    """Request to update a part."""
    part_number: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    unit_cost: Optional[float] = None
    supplier: Optional[str] = None
    lead_time_days: Optional[int] = None


# ========== Notification Service Models ==========

class NotificationCreateRequest(BaseModel):
    """Request to create a notification."""
    user_id: int
    title: str
    message: str
    type: str = "info"
    read: bool = False
    expires_at: Optional[str] = None


class NotificationResponse(BaseModel):
    """Response for notification operations."""
    notification_id: int
    user_id: int
    title: str
    message: str
    type: str
    read: bool
    created_at: datetime
    expires_at: Optional[str]


class NotificationUpdateRequest(BaseModel):
    """Request to update a notification."""
    title: Optional[str] = None
    message: Optional[str] = None
    type: Optional[str] = None
    read: Optional[bool] = None
    expires_at: Optional[str] = None


# ========== Invoice Service Models ==========

class InvoiceCreateRequest(BaseModel):
    """Request to create a new invoice."""
    job_id: int
    customer_id: int
    parts_total: float = 0.0
    labor_total: float = 0.0
    tax: float = 0.0
    discount: float = 0.0
    status: str = "pending"
    due_date: Optional[str] = None
    notes: Optional[str] = None


class InvoiceResponse(BaseModel):
    """Response for invoice operations."""
    invoice_id: int
    job_id: int
    customer_id: int
    parts_total: float
    labor_total: float
    tax: float
    discount: float
    total: float
    status: str
    created_at: datetime
    due_date: Optional[str]
    paid_at: Optional[str]
    notes: Optional[str]


class InvoiceUpdateRequest(BaseModel):
    """Request to update an invoice."""
    job_id: Optional[int] = None
    customer_id: Optional[int] = None
    parts_total: Optional[float] = None
    labor_total: Optional[float] = None
    tax: Optional[float] = None
    discount: Optional[float] = None
    status: Optional[str] = None
    due_date: Optional[str] = None
    notes: Optional[str] = None


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
