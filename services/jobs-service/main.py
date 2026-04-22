"""
Jobs Service - SkyMechanics
Handles job management, scheduling, and dispatch.
"""
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import os
import base64
from hashlib import sha256
import json

# Configuration
FALKORDB_HOST = os.getenv("FALKORDB_HOST", "falkordb")
FALKORDB_PORT = int(os.getenv("FALKORDB_PORT", 6379))
FALKORDB_PASSWORD = os.getenv("FALKORDB_PASSWORD", None)
TENANT_ID = os.getenv("TENANT_ID", "default")

# FastAPI app
app = FastAPI(title="Jobs Service", version="1.0.0")


# Pydantic models
class JobCreateRequest(BaseModel):
    customer_id: int
    aircraft_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    status: str = "pending"
    priority: str = "medium"
    mechanic_id: Optional[int] = None
    procedure_id: Optional[int] = None
    notes: Optional[str] = None


class JobAssignRequest(BaseModel):
    mechanic_id: int


class JobCompleteRequest(BaseModel):
    mechanic_signature: str  # Base64 encoded image or hash
    owner_signature: Optional[str] = None
    parts_used: List[Dict[str, Any]] = Field(default_factory=list)
    labor_hours: Optional[float] = None
    cost_breakdown: Optional[Dict[str, Any]] = None


class JobUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    mechanic_id: Optional[int] = None


class JobResponse(BaseModel):
    job_id: int
    customer_id: int
    aircraft_id: Optional[int] = None
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    mechanic_id: Optional[int] = None
    mechanic_name: Optional[str] = None
    procedure_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime


class JobSummaryResponse(BaseModel):
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


# Import FalkorDB client
import falkordb


class FalkorDBClient:
    """FalkorDB client for jobs service."""
    
    def __init__(self, host: str = FALKORDB_HOST, port: int = FALKORDB_PORT):
        self.host = host
        self.port = port
        self.password = FALKORDB_PASSWORD
        self.graph_name = "tenant_default"
        self._client = None
        self._graph = None
    
    def connect(self):
        """Establish connection to FalkorDB."""
        self._client = falkordb.FalkorDB(
            host=self.host,
            port=self.port,
            password=self.password
        )
        return self
    
    def get_graph(self):
        """Get graph instance."""
        if self._graph is None:
            if self._client is None:
                self.connect()
            self._graph = self._client.select_graph(self.graph_name)
        return self._graph
    
    def execute(self, query: str, params: Optional[Dict] = None):
        """Execute a Cypher query."""
        try:
            if self._client is None:
                self.connect()
            graph = self.get_graph()
            # Replace datetime() with toString(timestamp()) for FalkorDB compatibility
            query = query.replace("datetime()", "toString(timestamp())")
            result = graph.query(query, params or {})
            # Convert result_set (list of lists) to list of dicts using headers
            headers = [h[1] for h in result.header] if result.header else []
            rows = [dict(zip(headers, row)) for row in result.result_set] if result.result_set else []
            return {
                "results": [rows],
                "headers": headers
            }
        except Exception as e:
            # Reset connection and retry
            self._client = None
            self._graph = None
            raise


# Initialize client
db = FalkorDBClient()


# Endpoints
@app.get("/")
async def root():
    return {
        "service": "jobs-service", 
        "status": "running",
        "falkordb": f"{FALKORDB_HOST}:{FALKORDB_PORT}"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/ready")
async def ready():
    try:
        db.execute("RETURN 1 AS test")
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {str(e)}")


@app.post("/jobs", response_model=JobResponse)
async def create_job(job: JobCreateRequest):
    """Create a new job."""
    try:
        query = """
        MATCH (c:Customer {id: $customer_id})
        CREATE (j:Job {
            title: $title,
            description: $description,
            status: $status,
            priority: $priority,
            created_at: toString(timestamp())
        })-[:ASSIGNED_TO]->(c)
        RETURN id(j) AS job_id, j.title AS title, j.description AS description, j.status AS status, j.priority AS priority, j.created_at AS created_at
        """
        params = {
            "customer_id": job.customer_id,
            "title": job.title,
            "description": job.description,
            "status": job.status,
            "priority": job.priority
        }
        
        result = db.execute(query, params)
        if not result.get("results") or not result["results"][0]:
            raise HTTPException(status_code=500, detail="Failed to create job")
        
        row = result["results"][0][0]
        created_at_str = str(row.get("created_at", ""))
        
        return JobResponse(
            job_id=row["job_id"],
            customer_id=job.customer_id,
            title=job.title,
            description=job.description,
            status=job.status,
            priority=job.priority,
            mechanic_id=None,
            procedure_id=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job creation failed: {str(e)}")


@app.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: int):
    """Get job by ID."""
    try:
        query = """
        MATCH (j:Job)
        WHERE id(j) = $job_id
        OPTIONAL MATCH (j)-[:ASSIGNED_TO]->(c:Customer)
        OPTIONAL MATCH (j)-[:ASSIGNED_TO]->(m:Mechanic)
        RETURN id(j) AS job_id, c.id AS customer_id, m.id AS mechanic_id, m.name AS mechanic_name, j.title AS title, j.description AS description, j.status AS status, j.priority AS priority, j.created_at AS created_at
        """
        result = db.execute(query, {"job_id": job_id})
        
        if not result["results"] or not result["results"][0]:
            raise HTTPException(status_code=404, detail="Job not found")
        
        row = result["results"][0][0]
        
        return JobResponse(
            job_id=row["job_id"],
            customer_id=row.get("customer_id", 0),
            title=row["title"],
            description=row.get("description"),
            status=row["status"],
            priority=row["priority"],
            mechanic_id=row.get("mechanic_id"),
            mechanic_name=row.get("mechanic_name"),
            procedure_id=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get job: {str(e)}")


@app.put("/jobs/{job_id}", response_model=JobResponse)
async def update_job(job_id: int, job: JobUpdateRequest):
    """Update a job."""
    try:
        updates = []
        params = {"job_id": job_id}
        
        if job.title:
            updates.append("j.title = $title")
            params["title"] = job.title
        if job.description is not None:
            updates.append("j.description = $description")
            params["description"] = job.description
        if job.status:
            updates.append("j.status = $status")
            params["status"] = job.status
        if job.priority:
            updates.append("j.priority = $priority")
            params["priority"] = job.priority
        
        if not updates:
            return await get_job(job_id)
        
        query = f"""
        MATCH (j:Job)
        WHERE id(j) = $job_id
        SET {', '.join(updates)}
        SET j.updated_at = toString(timestamp())
        RETURN id(j) AS job_id, j.title AS title, j.description AS description, j.status AS status, j.priority AS priority, j.created_at AS created_at
        """
        
        result = db.execute(query, params)
        if not result["results"] or not result["results"][0]:
            raise HTTPException(status_code=404, detail="Job not found")
        
        row = result["results"][0][0]
        
        return JobResponse(
            job_id=row["job_id"],
            customer_id=0,
            title=row["title"],
            description=row.get("description"),
            status=row["status"],
            priority=row["priority"],
            mechanic_id=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job update failed: {str(e)}")


@app.get("/jobs", response_model=List[JobResponse])
async def list_jobs(status: Optional[str] = None, priority: Optional[str] = None):
    """List all jobs with optional filters."""
    try:
        where_clauses = []
        params = {}
        
        if status:
            where_clauses.append("j.status = $status")
            params["status"] = status
        if priority:
            where_clauses.append("j.priority = $priority")
            params["priority"] = priority
        
        where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        query = f"""
        MATCH (j:Job)
        {where_clause}
        OPTIONAL MATCH (j)-[:ASSIGNED_TO]->(m:Mechanic)
        RETURN id(j) AS job_id, m.id AS mechanic_id, m.name AS mechanic_name, j.title AS title, j.description AS description, j.status AS status, j.priority AS priority, j.created_at AS created_at
        """
        
        result = db.execute(query, params)
        
        if not result.get("results") or not result["results"][0]:
            return []
        
        return [
            JobResponse(
                job_id=j["job_id"],
                customer_id=0,
                aircraft_id=None,
                title=j["title"],
                description=j.get("description"),
                status=j["status"],
                priority=j["priority"],
                mechanic_id=j.get("mechanic_id"),
                mechanic_name=j.get("mechanic_name"),
                procedure_id=None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            for j in result["results"][0]
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list jobs: {str(e)}")


@app.post("/jobs/{job_id}/assign")
async def assign_job(job_id: int, request: JobAssignRequest):
    """Assign a job to a mechanic."""
    try:
        query = """
        MATCH (j:Job)
        WHERE id(j) = $job_id
        MATCH (m:Mechanic {id: $mechanic_id})
        CREATE (j)-[:ASSIGNED_TO]->(m)
        RETURN id(j) AS job_id
        """
        result = db.execute(query, {
            "job_id": job_id,
            "mechanic_id": request.mechanic_id
        })
        
        if not result["results"] or not result["results"][0]:
            raise HTTPException(status_code=404, detail="Job not found")
        
        return {"message": f"Job {job_id} assigned to mechanic {request.mechanic_id}"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to assign job: {str(e)}")


@app.post("/jobs/{job_id}/complete")
async def complete_job(job_id: int, request: JobCompleteRequest, x_mechanic_id: Optional[int] = Header(None)):
    """Complete a job with signatures."""
    try:
        if not request.mechanic_signature:
            raise HTTPException(status_code=400, detail="Mechanic signature required")
        
        signature_hash = sha256(base64.b64decode(request.mechanic_signature)).hexdigest()
        
        query = """
        MATCH (j:Job)
        WHERE id(j) = $job_id
        SET j.status = $status,
            j.completed_at = toString(timestamp()),
            j.signature_hash = $signature_hash,
            j.mechanic_signature = $mechanic_signature,
            j.parts_used = $parts_used,
            j.labor_hours = $labor_hours
        RETURN id(j) AS job_id, j.status AS status, j.completed_at AS completed_at
        """
        
        result = db.execute(query, {
            "job_id": job_id,
            "status": "completed",
            "signature_hash": signature_hash,
            "mechanic_signature": request.mechanic_signature,
            "parts_used": json.dumps(request.parts_used),
            "labor_hours": request.labor_hours
        })
        
        if not result["results"] or not result["results"][0]:
            raise HTTPException(status_code=404, detail="Job not found")
        
        row = result["results"][0][0]
        completed_at_str = str(row.get("completed_at", ""))
        
        return {
            "message": "Job completed successfully",
            "job_id": job_id,
            "completed_at": completed_at_str,
            "signature_hash": signature_hash
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to complete job: {str(e)}")


@app.get("/jobs/{job_id}/summary")
async def get_job_summary(job_id: int):
    """Get complete job summary with cost breakdown."""
    try:
        query = """
        MATCH (j:Job)
        WHERE id(j) = $job_id
        OPTIONAL MATCH (j)-[:ASSIGNED_TO]->(m:Mechanic)
        OPTIONAL MATCH (j)-[:CREATED_FOR]->(a:Aircraft)
        RETURN id(j) AS job_id, a.tail_number AS tail_number, j.title AS title, j.description AS description, j.status AS status, j.priority AS priority, j.completed_at AS completed_at, j.labor_hours AS labor_hours, j.parts_used AS parts_used, j.signature_hash AS signature_hash, m.name AS mechanic_name, j.created_at AS created_at
        """
        result = db.execute(query, {"job_id": job_id})
        
        if not result["results"] or not result["results"][0]:
            raise HTTPException(status_code=404, detail="Job not found")
        
        row = result["results"][0][0]
        
        parts_used = json.loads(row.get("parts_used", "[]")) if row.get("parts_used") else []
        parts_cost = sum(p.get("cost", 0) for p in parts_used)
        labor_cost = float(row.get("labor_hours", 0) or 0) * 75  # $75/hr labor rate
        total_cost = parts_cost + labor_cost
        
        return JobSummaryResponse(
            job_id=row["job_id"],
            customer_id=0,
            aircraft_id=None,
            aircraft_tail_number=row.get("tail_number"),
            title=row["title"],
            description=row.get("description"),
            status=row["status"],
            priority=row["priority"],
            mechanic_id=None,
            mechanic_name=row.get("mechanic_name"),
            completed_at=datetime.utcnow() if row.get("completed_at") else None,
            labor_hours=row.get("labor_hours"),
            parts_cost=parts_cost,
            labor_cost=labor_cost,
            total_cost=total_cost,
            parts_used=parts_used,
            signature_status="mechanic_signed" if row.get("signature_hash") else "pending",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get job summary: {str(e)}")


@app.post("/jobs/{job_id}/pdf")
async def export_job_pdf(job_id: int):
    """Export job as PDF report."""
    try:
        summary = await get_job_summary(job_id)
        
        parts_list = "\n".join(
            f"  - {p['name']}: ${p.get('cost', 0):.2f}"
            for p in summary.parts_used
        ) or "  No parts used"
        
        pdf_content = f"""JOB REPORT - {job_id}
====================

Customer ID: {summary.customer_id}
Aircraft: {summary.aircraft_tail_number or 'N/A'}
Title: {summary.title}
Status: {summary.status}
Mechanic: {summary.mechanic_name or 'Unassigned'}
Completed: {summary.completed_at or 'Not completed'}

COST BREAKDOWN
--------------
Parts Cost: ${summary.parts_cost or 0:.2f}
Labor Cost: ${summary.labor_cost or 0:.2f}
Total Cost: ${summary.total_cost or 0:.2f}

SIGNATURE STATUS: {summary.signature_status}

PARTS USED:
{parts_list}
"""
        
        return {
            "job_id": job_id,
            "filename": f"job_{job_id}_report.pdf",
            "content_type": "application/pdf",
            "pdf_content_base64": base64.b64encode(pdf_content.encode()).decode(),
            "generated_at": datetime.utcnow().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to export PDF: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
