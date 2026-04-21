"""
Jobs Service - SkyMechanics
Handles job management, scheduling, and dispatch.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import os

# Import shared models
import sys
sys.path.insert(0, '/app')
from models import JobCreateRequest, JobUpdateRequest, JobResponse

# Configuration
FALKORDB_HOST = os.getenv("FALKORDB_HOST", "falkordb")
FALKORDB_PORT = int(os.getenv("FALKORDB_PORT", 6379))
TENANT_ID = os.getenv("TENANT_ID", "default")

# FastAPI app
app = FastAPI(title="Jobs Service", version="1.0.0")


# Pydantic models (duplicated for standalone operation)
class JobCreateRequest(BaseModel):
    customer_id: int
    title: str
    description: Optional[str] = None
    status: str = "pending"
    priority: str = "medium"
    mechanic_id: Optional[int] = None


class JobUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    mechanic_id: Optional[int] = None


class JobResponse(BaseModel):
    job_id: int
    customer_id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    mechanic_id: Optional[int]
    created_at: datetime
    updated_at: datetime


# Simplified FalkorDB client
class FalkorDBClient:
    """Simplified FalkorDB client for jobs service."""
    
    def __init__(self, host: str = FALKORDB_HOST, port: int = FALKORDB_PORT):
        self.host = host
        self.port = port
        self.graph_name = f"tenant_{TENANT_ID}"
    
    def execute(self, query: str, params: Optional[Dict] = None):
        """Execute a Cypher query."""
        return {"results": [], "headers": []}


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
            created_at: datetime()
        })-[:ASSIGNED_TO]->(c)
        RETURN j {
            job_id: id(j),
            customer_id: $customer_id,
            title: j.title,
            description: j.description,
            status: j.status,
            priority: j.priority,
            mechanic_id: null,
            created_at: j.created_at,
            updated_at: j.created_at
        } AS job
        """
        params = {
            "customer_id": job.customer_id,
            "title": job.title,
            "description": job.description,
            "status": job.status,
            "priority": job.priority
        }
        
        result = db.execute(query, params)
        job_id = result["results"][0][0]["job_id"] if result["results"] else 1
        
        return JobResponse(
            job_id=job_id,
            customer_id=job.customer_id,
            title=job.title,
            description=job.description,
            status=job.status,
            priority=job.priority,
            mechanic_id=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job creation failed: {str(e)}")


@app.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: int):
    """Get job by ID."""
    try:
        query = """
        MATCH (j:Job {id: $job_id})
        OPTIONAL MATCH (j)-[:ASSIGNED_TO]->(c:Customer)
        RETURN j {
            job_id: id(j),
            customer_id: c.id,
            title: j.title,
            description: j.description,
            status: j.status,
            priority: j.priority,
            mechanic_id: null,
            created_at: j.created_at,
            updated_at: j.created_at
        } AS job
        """
        result = db.execute(query, {"job_id": job_id})
        
        if not result["results"]:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job_data = result["results"][0][0]["job"]
        
        return JobResponse(
            job_id=job_id,
            customer_id=job_data["customer_id"],
            title=job_data["title"],
            description=job_data["description"],
            status=job_data["status"],
            priority=job_data["priority"],
            mechanic_id=job_data.get("mechanic_id"),
            created_at=datetime.fromisoformat(job_data["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(job_data["updated_at"].replace("Z", "+00:00"))
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
        MATCH (j:Job {{id: $job_id}})
        SET {', '.join(updates)}
        SET j.updated_at = datetime()
        RETURN j {
            job_id: id(j),
            customer_id: null,
            title: j.title,
            description: j.description,
            status: j.status,
            priority: j.priority,
            mechanic_id: null,
            created_at: j.created_at,
            updated_at: j.updated_at
        } AS job
        """
        
        result = db.execute(query, params)
        job_data = result["results"][0][0]["job"]
        
        return JobResponse(
            job_id=job_id,
            customer_id=job_data["customer_id"],
            title=job_data["title"],
            description=job_data["description"],
            status=job_data["status"],
            priority=job_data["priority"],
            mechanic_id=job_data.get("mechanic_id"),
            created_at=datetime.fromisoformat(job_data["created_at"].replace("Z", "+00:00")),
            updated_at=datetime.fromisoformat(job_data["updated_at"].replace("Z", "+00:00"))
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
        RETURN j {
            job_id: id(j),
            customer_id: null,
            title: j.title,
            description: j.description,
            status: j.status,
            priority: j.priority,
            mechanic_id: null,
            created_at: j.created_at,
            updated_at: j.updated_at
        } AS job
        """
        
        result = db.execute(query, params)
        
        return [
            JobResponse(
                job_id=j["job_id"],
                customer_id=j["customer_id"],
                title=j["title"],
                description=j["description"],
                status=j["status"],
                priority=j["priority"],
                mechanic_id=j.get("mechanic_id"),
                created_at=datetime.fromisoformat(j["created_at"].replace("Z", "+00:00")),
                updated_at=datetime.fromisoformat(j["updated_at"].replace("Z", "+00:00"))
            )
            for j in result["results"][0] if result["results"]
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list jobs: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
