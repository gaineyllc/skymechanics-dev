"""
Pydantic models for API requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ========== Request Models ==========

class GraphQueryRequest(BaseModel):
    """Request to execute a Cypher query."""
    query: str = Field(..., description="Cypher query to execute")
    params: Optional[Dict[str, Any]] = Field(None, description="Query parameters")


class MultiTenantCreateRequest(BaseModel):
    """Request to create a new tenant graph."""
    tenant_id: str = Field(..., description="Unique tenant identifier")
    graph_name: str = Field(default=None, description="Name for the tenant's graph")


class MultiTenantQueryRequest(BaseModel):
    """Request to query a specific tenant's graph."""
    tenant_id: str = Field(..., description="Tenant identifier")
    query: str = Field(..., description="Cypher query to execute")
    params: Optional[Dict[str, Any]] = Field(None, description="Query parameters")


class EntityCreateRequest(BaseModel):
    """Request to create a new entity."""
    label: str = Field(..., description="Node label (e.g., 'Customer', 'Job', 'Mechanic')")
    properties: Dict[str, Any] = Field(..., description="Node properties")


class RelationshipCreateRequest(BaseModel):
    """Request to create a relationship."""
    start_node_id: int = Field(..., description="Start node ID")
    end_node_id: int = Field(..., description="End node ID")
    relationship_type: str = Field(..., description="Relationship type (e.g., 'WORKS_ON', 'MANAGES')")
    properties: Optional[Dict[str, Any]] = Field(None, description="Relationship properties")


# ========== Response Models ==========

class QueryResult(BaseModel):
    """Result of a Cypher query."""
    headers: List[str] = Field([], description="Column headers")
    results: List[List[Any]] = Field([], description="Query results")
    stats: Optional[Dict[str, int]] = Field(None, description="Query statistics")


class TenantResponse(BaseModel):
    """Response for tenant operations."""
    tenant_id: str
    graph_name: str
    created_at: datetime


class EntityResponse(BaseModel):
    """Response for entity operations."""
    node_id: int
    label: str
    properties: Dict[str, Any]


class RelationshipResponse(BaseModel):
    """Response for relationship operations."""
    relationship_id: int
    start_node_id: int
    end_node_id: int
    relationship_type: str
    properties: Dict[str, Any]


# ========== Specific Use Case Models ==========

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


class JobCreateRequest(BaseModel):
    """Request to create a new job."""
    customer_id: int
    title: str
    description: Optional[str] = None
    status: str = "pending"
    priority: int = 2  # 0=none, 1=low, 2=medium, 3=high, 4=critical


class JobUpdateRequest(BaseModel):
    """Request to update job properties."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    mechanic_id: Optional[int] = None


class JobStatusRequest(BaseModel):
    """Request to update job status."""
    status: str = Field(..., description="Current job status")
    new_status: str = Field(..., description="New job status")
    comment: Optional[str] = None


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
    phone: Optional[str]
    specialties: List[str]
    created_at: datetime


# ========== Onboarding / User Role Models ==========

class UserCreateRequest(BaseModel):
    """Request to create a new user with role."""
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    role: str = Field(..., description="Role: 'owner', 'admin', 'mechanic'")
    password: str = Field(..., description="User password")


class OwnerProfileRequest(BaseModel):
    """Request to create/update owner profile."""
    vehicle_ids: List[int] = Field(default_factory=list, description="List of vehicle/node IDs")
    preferences: Dict[str, Any] = Field(default_factory=dict, description="Owner preferences")


class AdminProfileRequest(BaseModel):
    """Request to create/update admin profile."""
    permissions: List[str] = Field(default_factory=list, description="Admin permissions")
    settings: Dict[str, Any] = Field(default_factory=dict, description="Admin settings")


class MechanicProfileRequest(BaseModel):
    """Request to create/update mechanic profile."""
    license_number: Optional[str] = None
    certifications: List[str] = Field(default_factory=list)
    availability: Dict[str, Any] = Field(default_factory=dict, description="Working hours, days, etc.")
    current_location: Optional[Dict[str, float]] = Field(None, description="GPS coordinates {lat, lng}")


# ========== Maintenance Procedure Configuration Models ==========

class ConfigSourceCreateRequest(BaseModel):
    """Request to create a new configuration source."""
    name: str = Field(..., description="Name of the configuration source")
    type: str = Field(..., description="Type: 'advisory_circular', 'aircraft_manual', 'oem_document'")
    version: Optional[str] = Field(None, description="Version or edition")
    url: Optional[str] = Field(None, description="External URL to documentation")
    description: Optional[str] = Field(None, description="Description of the source")
    is_active: bool = Field(default=True, description="Is this source currently active?")

class ConfigSourceResponse(BaseModel):
    """Response for configuration source operations."""
    source_id: int
    name: str
    type: str
    version: Optional[str]
    url: Optional[str]
    description: Optional[str]
    is_active: bool
    created_at: datetime
    last_updated: datetime

class TaskCreateRequest(BaseModel):
    """Request to create a new task template."""
    procedure_id: int = Field(..., description="Parent procedure ID")
    name: str = Field(..., description="Task name")
    sequence: int = Field(..., description="Order in procedure")
    category: str = Field(..., description="Category: 'visual', 'disassembly', 'inspection', 'reassembly'")
    estimated_duration_minutes: int = Field(..., description="Estimated duration in minutes")
    required_tools: List[str] = Field(default_factory=list, description="Required tool IDs")
    required_parts: List[str] = Field(default_factory=list, description="Required part IDs")
    checklist_items: List[Dict[str, Any]] = Field(default_factory=list, description="Checklist items")
    instructions: Optional[str] = Field(None, description="Detailed instructions")

class TaskResponse(BaseModel):
    """Response for task operations."""
    task_id: int
    procedure_id: int
    name: str
    sequence: int
    category: str
    estimated_duration_minutes: int
    required_tools: List[str]
    required_parts: List[str]
    checklist_items: List[Dict[str, Any]]
    instructions: Optional[str]
    created_at: datetime
    updated_at: datetime

class ProcedureTemplateCreateRequest(BaseModel):
    """Request to create a new procedure template."""
    name: str = Field(..., description="Procedure name")
    category: str = Field(..., description="Category: 'annual', '100hr', 'condition', 'repair'")
    authority: str = Field(..., description="Authority: 'FAA AC 43.13-1B', 'FAA AC 20-106', etc.")
    estimated_duration_hours: int = Field(..., description="Estimated total duration in hours")
    required_specialty: str = Field(..., description="Required specialty: 'general', 'powerplant', 'avionics'")
    source_id: Optional[int] = Field(None, description="Configuration source ID")
    is_active: bool = Field(default=True, description="Is this procedure active?")

class ProcedureTemplateResponse(BaseModel):
    """Response for procedure template operations."""
    procedure_id: int
    name: str
    category: str
    authority: str
    estimated_duration_hours: int
    required_specialty: str
    source_id: Optional[int]
    is_active: bool
    created_at: datetime
    updated_at: datetime
    tasks: List[Dict[str, Any]] = Field(default_factory=list, description="Tasks in procedure")

class ToolCreateRequest(BaseModel):
    """Request to create a new tool configuration."""
    name: str = Field(..., description="Tool name")
    category: str = Field(..., description="Category: 'torque', 'socket', 'wrench', 'specialty'")
    part_number: Optional[str] = Field(None, description="Manufacturer part number")
    calibration_required: bool = Field(default=False, description="Does this tool require calibration?")
    calibration_interval_months: Optional[int] = Field(None, description="Calibration interval in months")
    description: Optional[str] = Field(None, description="Tool description")

class ToolResponse(BaseModel):
    """Response for tool operations."""
    tool_id: int
    name: str
    category: str
    part_number: Optional[str]
    calibration_required: bool
    calibration_interval_months: Optional[int]
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

class PartCreateRequest(BaseModel):
    """Request to create a new parts catalog entry."""
    part_number: str = Field(..., description="Manufacturer part number")
    name: str = Field(..., description="Part name")
    category: str = Field(..., description="Category: 'structural', 'engine', 'avionics', 'tool'")
    aircraft_compatible: List[str] = Field(default_factory=list, description="Compatible aircraft type IDs")
    oem_source: Optional[str] = Field(None, description="OEM manufacturer")
    description: Optional[str] = Field(None, description="Part description")

class PartResponse(BaseModel):
    """Response for parts operations."""
    part_id: int
    part_number: str
    name: str
    category: str
    aircraft_compatible: List[str]
    oem_source: Optional[str]
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

class AircraftTypeCreateRequest(BaseModel):
    """Request to create an aircraft type configuration."""
    make: str = Field(..., description="Manufacturer (e.g., 'Cessna')")
    model: str = Field(..., description="Model (e.g., '172R')")
    category: str = Field(..., description="Category: 'airplane', 'helicopter', 'gyrocopter'")
    certification: str = Field(default="FAA", description="Certification authority")
    amm_ref: Optional[str] = Field(None, description="AMM reference")
    mpd_ref: Optional[str] = Field(None, description="MPD reference")
    ipc_ref: Optional[str] = Field(None, description="IPC reference")

class AircraftTypeResponse(BaseModel):
    """Response for aircraft type operations."""
    aircraft_type_id: int
    make: str
    model: str
    category: str
    certification: str
    amm_ref: Optional[str]
    mpd_ref: Optional[str]
    ipc_ref: Optional[str]
    created_at: datetime
    updated_at: datetime


# ========== Reputation System Models ==========

class CertificationCreateRequest(BaseModel):
    """Request to create a certification for a mechanic."""
    name: str = Field(..., description="Certification name (e.g., 'A&P Mechanic', 'IA')")
    authority: str = Field(..., description="Issuing authority (e.g., 'FAA')")
    certification_id: Optional[str] = Field(None, description="Certification number")
    issue_date: Optional[str] = Field(None, description="ISO date of issuance")
    expiry_date: Optional[str] = Field(None, description="ISO date of expiration")
    status: str = Field(default="active", description="Status: 'active', 'expired', 'revoked'")
    notes: Optional[str] = Field(None, description="Additional notes")

class CertificationResponse(BaseModel):
    """Response for certification operations."""
    certification_id: int
    name: str
    authority: str
    certification_id_num: Optional[str]
    issue_date: Optional[str]
    expiry_date: Optional[str]
    status: str
    notes: Optional[str]
    created_at: datetime

class RepairmanCertificateCreateRequest(BaseModel):
    """Request to create a repairman certificate."""
    name: str = Field(..., description="Certificate name (e.g., 'Repairman - Experimental')")
    category: str = Field(..., description="Category: 'general', 'experimental_builder', 'light_sport')")
    issue_date: str = Field(..., description="ISO date of issuance")
    expiry_date: Optional[str] = Field(None, description="ISO date of expiration")
    status: str = Field(default="active", description="Status: 'active', 'expired', 'revoked'")

class RepairmanCertificateResponse(BaseModel):
    """Response for repairman certificate operations."""
    certificate_id: int
    name: str
    category: str
    issue_date: str
    expiry_date: Optional[str]
    status: str
    created_at: datetime

class ExperienceRecordCreateRequest(BaseModel):
    """Request to create an experience record."""
    aircraft_type_id: int = Field(..., description="Aircraft type ID")
    hours_flown: int = Field(..., description="Total flight hours on this type")
    years_active: int = Field(default=0, description="Years of experience")
    last_flight_date: Optional[str] = Field(None, description="ISO date of last flight")
    notes: Optional[str] = Field(None, description="Experience notes")

class ExperienceRecordResponse(BaseModel):
    """Response for experience record operations."""
    experience_id: int
    aircraft_type_id: int
    hours_flown: int
    years_active: int
    last_flight_date: Optional[str]
    notes: Optional[str]
    created_at: datetime

class ReviewCreateRequest(BaseModel):
    """Request to create a mechanic review."""
    job_id: int = Field(..., description="Job ID being reviewed")
    rating: int = Field(..., ge=1, le=5, description="Rating 1-5")
    comment: Optional[str] = Field(None, description="Review comment")
    review_type: str = Field(default="customer", description="Type: 'customer', 'peer', 'supervisor'")

class ReviewResponse(BaseModel):
    """Response for review operations."""
    review_id: int
    job_id: int
    rating: int
    comment: Optional[str]
    review_type: str
    created_at: datetime

class SkillCreateRequest(BaseModel):
    """Request to create a mechanic skill."""
    name: str = Field(..., description="Skill name (e.g., 'Engine Overhaul', 'Avionics Installation')")
    level: int = Field(default=1, ge=1, le=10, description="Skill level 1-10")
    verified: bool = Field(default=False, description="Is this skill verified?")

class SkillResponse(BaseModel):
    """Response for skill operations."""
    skill_id: int
    name: str
    level: int
    verified: bool
    created_at: datetime

class ReputationMetrics(BaseModel):
    """Reputation metrics for a mechanic."""
    total_score: int = Field(..., ge=0, le=100, description="Overall reputation score 0-100")
    component_scores: Dict[str, int] = Field(..., description="Breakdown of score components")
    certification_status: int = Field(..., description="Component score (25% weight)")
    experience_depth: int = Field(..., description="Component score (20% weight)")
    performance: int = Field(..., description="Component score (30% weight)")
    recent_activity: int = Field(..., description="Component score (15% weight)")
    compliance: int = Field(..., description="Component score (10% weight)")
    review_count: int = Field(default=0, description="Total number of reviews")
    avg_rating: Optional[float] = Field(None, description="Average rating")
    last_review_date: Optional[str] = Field(None, description="Date of most recent review")


# ========== Response Wrappers ==========

class CustomersResponse(BaseModel):
    """Response for listing customers."""
    customers: List[Dict[str, Any]]
    total: int


class SuccessResponse(BaseModel):
    """Standard success response."""
    success: bool = True
    message: str = ""


class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    error: str
    details: Optional[str] = None
