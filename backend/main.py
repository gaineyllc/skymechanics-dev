"""
FastAPI application for SkyMechanics Platform.
Provides REST API endpoints for graph database operations.
"""
import structlog
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from db import db_client
from models import (
    GraphQueryRequest,
    MultiTenantCreateRequest,
    MultiTenantQueryRequest,
    EntityCreateRequest,
    RelationshipCreateRequest,
    CustomerCreateRequest,
    JobCreateRequest,
    MechanicCreateRequest,
    SuccessResponse,
    ErrorResponse
)
from settings import settings
from routes import onboarding as onboarding_router
from routes import users as users_router
from routes import jobs as jobs_router
from routes import users as users_router

# Configure structlog
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

app = FastAPI(
    title="SkyMechanics Platform API",
    description="Graph database API for multi-tenant job management",
    version="0.1.0"
)

# Use settings for vLLM URL
VLLM_URL = settings.vllm_url


@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup."""
    try:
        db_client.connect()
        print("✅ Connected to FalkorDB")
    except Exception as e:
        print(f"❌ Failed to connect to FalkorDB: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown."""
    db_client.close()
    print("👋 Closed FalkorDB connection")


# ========== Exception Handlers ==========

@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    """Handle validation errors."""
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            success=False,
            error="Validation Error",
            details=str(exc.errors())
        ).model_dump()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handle unexpected errors."""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            success=False,
            error="Internal Server Error",
            details=str(exc)
        ).model_dump()
    )


# ========== Health Check ==========

@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint."""
    try:
        db_client._client.ping()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": f"disconnected: {str(e)}"}


# ========== Graph Operations ==========

@app.post("/query", tags=["Graph"])
async def execute_query(request: GraphQueryRequest):
    """Execute a Cypher query."""
    try:
        graph = db_client.get_graph()
        result = graph.query(request.query, params=request.params or {})
        
        # Convert result to JSON-serializable format
        headers = [result.header] if hasattr(result, 'header') and result.header else []
        results = [list(row) for row in result.result_set] if result.result_set else []
        stats = result.stats if hasattr(result, 'stats') else {}
        
        return {
            "headers": headers,
            "results": results,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== Multi-Tenant Operations ==========

@app.post("/tenants", tags=["Tenants"])
async def create_tenant(request: MultiTenantCreateRequest):
    """Create a new tenant graph."""
    try:
        # Create new graph for tenant
        tenant_graph = db_client.set_graph(request.graph_name or f"tenant_{request.tenant_id}")
        
        # Initialize tenant graph (optional schema setup)
        tenant_graph.query("CREATE ()")
        
        return {
            "success": True,
            "tenant_id": request.tenant_id,
            "graph_name": tenant_graph.name
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tenants/query", tags=["Tenants"])
async def query_tenant(request: MultiTenantQueryRequest):
    """Query a specific tenant's graph."""
    try:
        # Switch to tenant graph
        tenant_graph = db_client.set_graph(f"tenant_{request.tenant_id}")
        
        # Execute query
        result = tenant_graph.query(request.query, params=request.params or {})
        
        # Convert result to JSON-serializable format
        headers = [result.header] if hasattr(result, 'header') and result.header else []
        results = [list(row) for row in result.result_set] if result.result_set else []
        stats = result.stats if hasattr(result, 'stats') else {}
        
        return {
            "headers": headers,
            "results": results,
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== Entity Operations ==========

@app.post("/entities", tags=["Entities"])
async def create_entity(request: EntityCreateRequest):
    """Create a new entity (node)."""
    try:
        graph = db_client.get_graph()
        
        # Build properties string
        props = ", ".join(f"{k}: '{v}'" if isinstance(v, str) else f"{k}: {v}" 
                         for k, v in request.properties.items())
        
        # Create node
        query = f"CREATE (n:{request.label} {{{props}}}) RETURN n"
        result = graph.query(query)
        
        return {
            "node_id": result.result_set[0][0].id,
            "label": request.label,
            "properties": request.properties
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/relationships", tags=["Entities"])
async def create_relationship(request: RelationshipCreateRequest):
    """Create a relationship between two nodes."""
    try:
        graph = db_client.get_graph()
        
        # Build properties string
        props = ""
        if request.properties:
            props = " {" + ", ".join(f"{k}: '{v}'" if isinstance(v, str) else f"{k}: {v}" 
                                   for k, v in request.properties.items()) + "}"
        
        # Create relationship
        query = (
            f"MATCH (a), (b) "
            f"WHERE id(a) = {request.start_node_id} AND id(b) = {request.end_node_id} "
            f"CREATE (a)-[r:{request.relationship_type}{props}]->(b) "
            f"RETURN r"
        )
        result = graph.query(query)
        
        return {
            "relationship_id": result.result_set[0][0].id,
            "start_node_id": request.start_node_id,
            "end_node_id": request.end_node_id,
            "relationship_type": request.relationship_type,
            "properties": request.properties or {}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== Business Logic Endpoints ==========

@app.get("/customers", tags=["Customers"])
async def list_customers():
    """List all customers."""
    try:
        graph = db_client.get_graph()
        
        query = "MATCH (c:Customer) RETURN c ORDER BY c.name"
        result = graph.query(query)
        
        customers = []
        for row in result.result_set:
            node = row[0]
            customers.append({
                "node_id": node.id,
                "label": "Customer",
                "properties": {
                    "name": node.properties.get("name", ""),
                    "email": node.properties.get("email", ""),
                    "phone": node.properties.get("phone", ""),
                    "address": node.properties.get("address", "")
                }
            })
        
        return customers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/jobs", tags=["Jobs"])
async def list_jobs():
    """List all jobs."""
    try:
        graph = db_client.get_graph()
        
        query = "MATCH (j:Job) RETURN j ORDER BY j.priority DESC, j.status"
        result = graph.query(query)
        
        jobs = []
        for row in result.result_set:
            node = row[0]
            jobs.append({
                "node_id": node.id,
                "label": "Job",
                "properties": {
                    "title": node.properties.get("title", ""),
                    "description": node.properties.get("description", ""),
                    "status": node.properties.get("status", "pending"),
                    "priority": node.properties.get("priority", "medium"),
                    "customer_id": node.properties.get("customer_id", 0)
                }
            })
        
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/jobs/{job_id}", tags=["Jobs"])
async def get_job(job_id: int):
    """Create a new customer."""
    try:
        graph = db_client.get_graph()
        
        # Check for duplicate email
        check_query = "MATCH (c:Customer {email: $email}) RETURN c"
        check_result = graph.query(check_query, params={"email": request.email})
        
        if check_result.result_set:
            raise HTTPException(status_code=409, detail="Customer with this email already exists")
        
        # Create customer node
        create_query = (
            "CREATE (c:Customer {"
            "name: $name, email: $email, phone: $phone, address: $address"
            "}) RETURN c"
        )
        result = graph.query(create_query, params={
            "name": request.name,
            "email": request.email,
            "phone": request.phone,
            "address": request.address
        })
        
        return {
            "node_id": result.result_set[0][0].id,
            "label": "Customer",
            "properties": {
                "name": request.name,
                "email": request.email,
                "phone": request.phone,
                "address": request.address
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/jobs", tags=["Jobs"])
async def create_job(request: JobCreateRequest):
    """Create a new job."""
    try:
        graph = db_client.get_graph()
        
        # Verify customer exists
        check_query = "MATCH (c:Customer) WHERE id(c) = $customer_id RETURN c"
        check_result = graph.query(check_query, params={"customer_id": request.customer_id})
        
        if not check_result.result_set:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Create job node
        create_query = (
            "MATCH (c:Customer) WHERE id(c) = $customer_id "
            "CREATE (j:Job {"
            "title: $title, description: $description, status: $status, priority: $priority"
            "}) "
            "CREATE (c)-[:OWNS]->(j) "
            "RETURN j"
        )
        result = graph.query(create_query, params={
            "customer_id": request.customer_id,
            "title": request.title,
            "description": request.description,
            "status": request.status,
            "priority": request.priority
        })
        
        return {
            "node_id": result.result_set[0][0].id,
            "label": "Job",
            "properties": {
                "title": request.title,
                "description": request.description,
                "status": request.status,
                "priority": request.priority,
                "customer_id": request.customer_id
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mechanics", tags=["Mechanics"])
async def list_mechanics():
    """List all mechanics."""
    try:
        graph = db_client.get_graph()
        
        query = "MATCH (m:Mechanic) RETURN m ORDER BY m.name"
        result = graph.query(query)
        
        mechanics = []
        for row in result.result_set:
            node = row[0]
            mechanics.append({
                "node_id": node.id,
                "label": "Mechanic",
                "properties": {
                    "name": node.properties.get("name", ""),
                    "email": node.properties.get("email", ""),
                    "phone": node.properties.get("phone", ""),
                    "specialties": node.properties.get("specialties", [])
                }
            })
        
        return mechanics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mechanics", tags=["Mechanics"])
async def create_mechanic(request: MechanicCreateRequest):
    """Create a new mechanic."""
    try:
        graph = db_client.get_graph()
        
        # Check for duplicate email
        check_query = "MATCH (m:Mechanic {email: $email}) RETURN m"
        check_result = graph.query(check_query, params={"email": request.email})
        
        if check_result.result_set:
            raise HTTPException(status_code=409, detail="Mechanic with this email already exists")
        
        # Create mechanic node
        create_query = (
            "CREATE (m:Mechanic {"
            "name: $name, email: $email, phone: $phone, specialties: $specialties"
            "}) RETURN m"
        )
        result = graph.query(create_query, params={
            "name": request.name,
            "email": request.email,
            "phone": request.phone,
            "specialties": request.specialties
        })
        
        return {
            "node_id": result.result_set[0][0].id,
            "label": "Mechanic",
            "properties": {
                "name": request.name,
                "email": request.email,
                "phone": request.phone,
                "specialties": request.specialties
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== Job Detail Endpoints ==========

@app.get("/jobs/{job_id}", tags=["Jobs"])
async def get_job(job_id: int):
    """Get a specific job by ID."""
    try:
        graph = db_client.get_graph()
        
        query = "MATCH (j:Job) WHERE id(j) = $job_id RETURN j"
        result = graph.query(query, params={"job_id": job_id})
        
        if not result.result_set:
            raise HTTPException(status_code=404, detail="Job not found")
        
        node = result.result_set[0][0]
        
        return {
            "node_id": node.id,
            "label": "Job",
            "properties": {
                "title": node.properties.get("title", ""),
                "description": node.properties.get("description", ""),
                "status": node.properties.get("status", "pending"),
                "priority": node.properties.get("priority", "medium"),
                "customer_id": node.properties.get("customer_id", 0),
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/jobs/{job_id}", tags=["Jobs"])
async def update_job(job_id: int, request: dict):
    """Update a job."""
    try:
        graph = db_client.get_graph()
        
        # Check if job exists
        check_query = "MATCH (j:Job) WHERE id(j) = $job_id RETURN j"
        check_result = graph.query(check_query, params={"job_id": job_id})
        
        if not check_result.result_set:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Update job properties
        props = ", ".join(f"{k}: '{v}'" if isinstance(v, str) else f"{k}: {v}" 
                       for k, v in request.items())
        
        query = f"MATCH (j:Job) WHERE id(j) = $job_id SET j += {{{props}}} RETURN j"
        result = graph.query(query, params={"job_id": job_id})
        
        node = result.result_set[0][0]
        
        return {
            "node_id": node.id,
            "label": "Job",
            "properties": {
                "title": node.properties.get("title", ""),
                "description": node.properties.get("description", ""),
                "status": node.properties.get("status", "pending"),
                "priority": node.properties.get("priority", "medium"),
                "customer_id": node.properties.get("customer_id", 0),
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/jobs/{job_id}", tags=["Jobs"])
async def delete_job(job_id: int):
    """Delete a job."""
    try:
        graph = db_client.get_graph()
        
        # Check if job exists
        check_query = "MATCH (j:Job) WHERE id(j) = $job_id RETURN j"
        check_result = graph.query(check_query, params={"job_id": job_id})
        
        if not check_result.result_set:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Delete job
        query = "MATCH (j:Job) WHERE id(j) = $job_id DETACH DELETE j"
        graph.query(query, params={"job_id": job_id})
        
        return {"success": True, "message": "Job deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ========== Root Endpoint ==========

app.include_router(onboarding_router.router)
app.include_router(users_router.router)
app.include_router(jobs_router.router)

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "SkyMechanics Platform API",
        "version": "0.1.0",
        "description": "Multi-tenant graph database API for job management",
        "endpoints": {
            "health": "/health",
            "query": "/query",
            "tenants": "/tenants",
            "customers": "/customers",
            "jobs": "/jobs",
            "jobs_detail": "/jobs/{job_id}",
            "mechanics": "/mechanics",
            "onboarding": "/api/v1/onboard"
        }
    }
