"""
Multi-tenancy API routes.
Creates and manages tenant-specific graphs in FalkorDB.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter()


class TenantCreateRequest(BaseModel):
    """Request to create a new tenant graph."""
    tenant_id: str
    graph_name: Optional[str] = None
    tenant_name: Optional[str] = None
    is_active: bool = True


class TenantResponse(BaseModel):
    """Response for tenant operations."""
    tenant_id: str
    graph_name: str
    tenant_name: Optional[str]
    is_active: bool
    created_at: datetime
    database_status: str


class TenantListResponse(BaseModel):
    """Response for tenant listing."""
    tenants: List[TenantResponse]
    total: int


class TenantQueryRequest(BaseModel):
    """Request to query a specific tenant's graph."""
    tenant_id: str
    query: str
    params: Optional[dict] = None


@router.post("/tenants", response_model=TenantResponse)
async def create_tenant(request: TenantCreateRequest):
    """
    Create a new tenant graph in FalkorDB.
    
    Each tenant gets their own isolated graph database.
    The graph is created with initial schema nodes.
    """
    from db import db_client
    from models import ErrorResponse
    
    try:
        # Connect to database
        db_client.connect()
        
        # Generate graph name
        graph_name = request.graph_name or f"tenant_{request.tenant_id}"
        
        # Create new graph for this tenant
        graph = db_client.get_graph(graph_name)
        
        # Create initial tenant schema
        create_tenant_schema(graph)
        
        return TenantResponse(
            tenant_id=request.tenant_id,
            graph_name=graph_name,
            tenant_name=request.tenant_name,
            is_active=request.is_active,
            created_at=datetime.now(),
            database_status="active"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tenants", response_model=TenantListResponse)
async def list_tenants():
    """List all tenant graphs in the database."""
    from db import db_client
    
    try:
        db_client.connect()
        
        # Get all graph names
        graphs = db_client._client.list_graphs()
        
        # Filter to only tenant graphs
        tenant_graphs = [g for g in graphs if g.startswith("tenant_")]
        
        # Build response
        tenants = []
        for graph_name in tenant_graphs:
            tenant_id = graph_name.replace("tenant_", "")
            tenants.append(TenantResponse(
                tenant_id=tenant_id,
                graph_name=graph_name,
                tenant_name=None,  # Could be stored in a metadata graph
                is_active=True,
                created_at=datetime.now(),
                database_status="active"
            ))
        
        return TenantListResponse(tenants=tenants, total=len(tenants))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tenants/{tenant_id}", response_model=TenantResponse)
async def get_tenant(tenant_id: str):
    """Get details for a specific tenant."""
    from db import db_client
    
    try:
        db_client.connect()
        graph_name = f"tenant_{tenant_id}"
        graph = db_client.get_graph(graph_name)
        
        # Check if graph exists by querying
        result = graph.query("RETURN 1 AS test")
        
        return TenantResponse(
            tenant_id=tenant_id,
            graph_name=graph_name,
            tenant_name=None,
            is_active=True,
            created_at=datetime.now(),
            database_status="active"
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Tenant not found: {str(e)}")


@router.post("/tenants/{tenant_id}/query")
async def query_tenant(tenant_id: str, request: TenantQueryRequest):
    """
    Execute a Cypher query against a specific tenant's graph.
    
    The query is automatically scoped to the tenant's graph.
    """
    from db import db_client
    
    try:
        db_client.connect()
        graph_name = f"tenant_{tenant_id}"
        db_client.set_graph(graph_name)
        graph = db_client.get_graph()
        
        # Execute query
        result = graph.query(request.query, params=request.params or {})
        
        return {
            "headers": result.headers,
            "results": result.result_set,
            "stats": result.stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/tenants/{tenant_id}")
async def delete_tenant(tenant_id: str):
    """
    Delete a tenant and their graph.
    
    WARNING: This permanently deletes all tenant data.
    """
    from db import db_client
    
    try:
        db_client.connect()
        graph_name = f"tenant_{tenant_id}"
        db_client.set_graph(graph_name)
        
        # Drop the entire graph
        graph = db_client.get_graph()
        graph.delete_graph()
        
        return {"message": f"Tenant {tenant_id} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def create_tenant_schema(graph):
    """Create initial schema nodes for a new tenant."""
    # Create schema definition nodes
    schema_nodes = [
        ("TenantSchema", {"name": "sky_mechanics_schema", "version": "1.0"}),
        ("SchemaVersion", {"version": "1.0", "created_at": datetime.now().isoformat()}),
    ]
    
    for label, props in schema_nodes:
        query = f"""
        CREATE (n:{label} $props)
        """
        graph.query(query, params={"props": props})


# Add multi-tenancy router to main app
# app.include_router(router, prefix="/api/v1", tags=["tenants"])
