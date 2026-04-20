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


class JobCreateRequest(BaseModel):
    """Request to create a new job."""
    customer_id: int
    title: str
    description: Optional[str] = None
    status: str = "pending"
    priority: str = "medium"


class JobUpdateRequest(BaseModel):
    """Request to update job properties."""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
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


# ========== Response Wrappers ==========

class SuccessResponse(BaseModel):
    """Standard success response."""
    success: bool = True
    message: str = ""


class ErrorResponse(BaseModel):
    """Standard error response."""
    success: bool = False
    error: str
    details: Optional[str] = None
