"""
Aircraft Service - SkyMechanics
Handles aircraft management, airworthiness tracking, and maintenance records.
"""
from fastapi import FastAPI, HTTPException
from fastapi.websockets import WebSocket, WebSocketDisconnect
from pydantic import BaseModel, ValidationError
from typing import Optional, List, Dict, Any
from datetime import datetime
import os
import sys
import falkordb
import asyncio
import json

# Import shared models
sys.path.insert(0, '/app/shared')
from models import (
    AircraftCreateRequest,
    AircraftResponse,
    AircraftUpdateRequest,
    SuccessResponse,
    ErrorResponse
)

# Configuration
FALKORDB_HOST = os.getenv("FALKORDB_HOST", "falkordb")
FALKORDB_PORT = int(os.getenv("FALKORDB_PORT", 6379))
FALKORDB_PASSWORD = os.getenv("FALKORDB_PASSWORD", "")
GRAPH_NAME = os.getenv("FALKORDB_GRAPH_NAME", "skymechanics")

# FastAPI app
app = FastAPI(
    title="Aircraft Service",
    version="1.0.0",
    description="Aircraft management and airworthiness tracking",
    prefix="/api/v1"
)


# Pydantic models (duplicated for standalone operation - will be removed after integration)
class AircraftCreateRequest(BaseModel):
    tail_number: str
    model_id: Optional[int] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    registration_expires: Optional[str] = None
    airworthiness_directives: List[str] = []
    service_bulletins: List[str] = []


class AircraftResponse(BaseModel):
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
    tail_number: Optional[str] = None
    model_id: Optional[int] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    registration_expires: Optional[str] = None
    airworthiness_directives: Optional[List[str]] = None
    service_bulletins: Optional[List[str]] = None


class AircraftListResponse(BaseModel):
    aircraft: List[AircraftResponse]
    total: int


# Initialize FalkorDB client
def get_falkordb_client():
    """Get FalkorDB client with graph name."""
    client = falkordb.FalkorDB(
        host=FALKORDB_HOST,
        port=FALKORDB_PORT,
        password=FALKORDB_PASSWORD
    )
    return client.select_graph(GRAPH_NAME)


# Endpoints
@app.get("/")
async def root():
    return {
        "service": "aircraft-service",
        "status": "running",
        "graph": os.getenv("FALKORDB_GRAPH_NAME", "skymechanics")
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/ready")
async def ready():
    try:
        graph = get_falkordb_client()
        result = graph.query("RETURN 1 AS test")
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {str(e)}")


@app.post("/aircraft", response_model=AircraftResponse)
async def create_aircraft(request: AircraftCreateRequest):
    """Create a new aircraft."""
    try:
        graph = get_falkordb_client()
        
        # Generate unique aircraft ID
        query = """
        MATCH (a:Aircraft)
        WITH coalesce(max(a.aircraft_id), 0) + 1 AS new_id
        CREATE (a:Aircraft {
            aircraft_id: new_id,
            tail_number: $tail_number,
            model_id: $model_id,
            manufacturer: $manufacturer,
            model: $model,
            year: $year,
            registration_expires: $registration_expires,
            airworthiness_directives: $airworthiness_directives,
            service_bulletins: $service_bulletins,
            created_at: timestamp()
        })
        RETURN a {
            aircraft_id: a.aircraft_id,
            tail_number: a.tail_number,
            model_id: a.model_id,
            manufacturer: a.manufacturer,
            model: a.model,
            year: a.year,
            registration_expires: a.registration_expires,
            airworthiness_directives: a.airworthiness_directives,
            service_bulletins: a.service_bulletins,
            created_at: toString(timestamp())
        } AS aircraft
        """
        
        result = graph.query(query, {
            "tail_number": request.tail_number,
            "model_id": request.model_id,
            "manufacturer": request.manufacturer,
            "model": request.model,
            "year": request.year,
            "registration_expires": request.registration_expires,
            "airworthiness_directives": request.airworthiness_directives,
            "service_bulletins": request.service_bulletins
        })
        
        aircraft = result.result_set[0][0]
        return AircraftResponse(**aircraft)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create aircraft: {str(e)}")


@app.get("/aircraft", response_model=AircraftListResponse)
async def list_aircraft(tail_number: Optional[str] = None, model: Optional[str] = None):
    """List all aircraft with optional filters."""
    try:
        graph = get_falkordb_client()
        
        where_clauses = []
        params = {}
        
        if tail_number:
            where_clauses.append("a.tail_number = $tail_number")
            params["tail_number"] = tail_number
        if model:
            where_clauses.append("a.model = $model")
            params["model"] = model
        
        where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        query = f"""
        MATCH (a:Aircraft)
        {where_clause}
        RETURN a {{
            aircraft_id: a.aircraft_id,
            tail_number: a.tail_number,
            model_id: a.model_id,
            manufacturer: a.manufacturer,
            model: a.model,
            year: a.year,
            registration_expires: a.registration_expires,
            airworthiness_directives: a.airworthiness_directives,
            service_bulletins: a.service_bulletins,
            created_at: toString(timestamp())
        }} AS aircraft
        ORDER BY a.created_at DESC
        """
        
        result = graph.query(query, params)
        
        aircraft_list = [
            AircraftResponse(**row[0]) for row in result.result_set
        ] if result.result_set else []
        
        return AircraftListResponse(aircraft=aircraft_list, total=len(aircraft_list))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list aircraft: {str(e)}")


@app.get("/aircraft/{aircraft_id}", response_model=AircraftResponse)
async def get_aircraft(aircraft_id: int):
    """Get aircraft by ID."""
    try:
        graph = get_falkordb_client()
        
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        RETURN a {
            aircraft_id: a.aircraft_id,
            tail_number: a.tail_number,
            model_id: a.model_id,
            manufacturer: a.manufacturer,
            model: a.model,
            year: a.year,
            registration_expires: a.registration_expires,
            airworthiness_directives: a.airworthiness_directives,
            service_bulletins: a.service_bulletins,
            created_at: toString(timestamp())
        } AS aircraft
        """
        
        result = graph.query(query, {"aircraft_id": aircraft_id})
        
        if not result.result_set:
            raise HTTPException(status_code=404, detail=f"Aircraft {aircraft_id} not found")
        
        aircraft = result.result_set[0][0]
        return AircraftResponse(**aircraft)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get aircraft: {str(e)}")


@app.put("/aircraft/{aircraft_id}", response_model=AircraftResponse)
async def update_aircraft(aircraft_id: int, request: AircraftUpdateRequest):
    """Update an aircraft."""
    try:
        graph = get_falkordb_client()
        
        # Check if aircraft exists
        check_query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        RETURN a.aircraft_id AS id
        """
        check_result = graph.query(check_query, {"aircraft_id": aircraft_id})
        if not check_result.result_set:
            raise HTTPException(status_code=404, detail=f"Aircraft {aircraft_id} not found")
        
        # Build dynamic update query
        updates = []
        params = {"aircraft_id": aircraft_id}
        
        if request.tail_number:
            updates.append("a.tail_number = $tail_number")
            params["tail_number"] = request.tail_number
        if request.model_id is not None:
            updates.append("a.model_id = $model_id")
            params["model_id"] = request.model_id
        if request.manufacturer:
            updates.append("a.manufacturer = $manufacturer")
            params["manufacturer"] = request.manufacturer
        if request.model:
            updates.append("a.model = $model")
            params["model"] = request.model
        if request.year is not None:
            updates.append("a.year = $year")
            params["year"] = request.year
        if request.registration_expires:
            updates.append("a.registration_expires = $registration_expires")
            params["registration_expires"] = request.registration_expires
        if request.airworthiness_directives is not None:
            updates.append("a.airworthiness_directives = $airworthiness_directives")
            params["airworthiness_directives"] = request.airworthiness_directives
        if request.service_bulletins is not None:
            updates.append("a.service_bulletins = $service_bulletins")
            params["service_bulletins"] = request.service_bulletins
        
        if not updates:
            # No fields to update, return current aircraft
            return await get_aircraft(aircraft_id)
        
        query = f"""
        MATCH (a:Aircraft {{aircraft_id: $aircraft_id}})
        SET {', '.join(updates)}
        SET a.updated_at = timestamp()
        RETURN a {{
            aircraft_id: a.aircraft_id,
            tail_number: a.tail_number,
            model_id: a.model_id,
            manufacturer: a.manufacturer,
            model: a.model,
            year: a.year,
            registration_expires: a.registration_expires,
            airworthiness_directives: a.airworthiness_directives,
            service_bulletins: a.service_bulletins,
            created_at: toString(timestamp())
        }} AS aircraft
        """
        
        result = graph.query(query, params)
        aircraft = result.result_set[0][0]
        return AircraftResponse(**aircraft)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update aircraft: {str(e)}")


@app.delete("/aircraft/{aircraft_id}", response_model=SuccessResponse)
async def delete_aircraft(aircraft_id: int):
    """Delete an aircraft."""
    try:
        graph = get_falkordb_client()
        
        # Check if aircraft exists
        check_query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        RETURN a.aircraft_id AS id
        """
        check_result = graph.query(check_query, {"aircraft_id": aircraft_id})
        if not check_result.result_set:
            raise HTTPException(status_code=404, detail=f"Aircraft {aircraft_id} not found")
        
        # Delete aircraft
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        DETACH DELETE a
        RETURN 'deleted' AS status
        """
        graph.query(query, {"aircraft_id": aircraft_id})
        
        return SuccessResponse(success=True, message=f"Aircraft {aircraft_id} deleted successfully")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete aircraft: {str(e)}")


@app.post("/aircraft/{aircraft_id}/jobs")
async def get_aircraft_jobs(aircraft_id: int):
    """Get all jobs for an aircraft."""
    try:
        graph = get_falkordb_client()
        
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})<-[:HAS_AIRCRAFT]-(j:Job)
        RETURN j {
            job_id: j.job_id,
            title: j.title,
            description: j.description,
            status: j.status,
            priority: j.priority,
            created_at: toString(timestamp())
        } AS job
        ORDER BY j.created_at DESC
        """
        
        result = graph.query(query, {"aircraft_id": aircraft_id})
        
        jobs = [
            {
                "job_id": row[0]["job_id"],
                "title": row[0]["title"],
                "description": row[0]["description"],
                "status": row[0]["status"],
                "priority": row[0]["priority"],
                "created_at": row[0]["created_at"]
            }
            for row in result.result_set
        ]
        
        return {"aircraft_id": aircraft_id, "jobs": jobs, "total": len(jobs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get aircraft jobs: {str(e)}")


@app.post("/aircraft/{aircraft_id}/airworthiness")
async def get_airworthiness_status(aircraft_id: int):
    """Get airworthiness status and compliance for an aircraft."""
    try:
        graph = get_falkordb_client()
        
        query = """
        MATCH (a:Aircraft {aircraft_id: $aircraft_id})
        OPTIONAL MATCH (a)<-[:MAINTAINS]-(r:RepairOrder)
        OPTIONAL MATCH (a)<-[:APPLIES_TO]-(ad:AirworthinessDirective)
        OPTIONAL MATCH (a)<-[:APPLIES_TO]-(sb:ServiceBulletin)
        RETURN a {
            aircraft_id: a.aircraft_id,
            tail_number: a.tail_number,
            registration_expires: a.registration_expires,
            airworthiness_directives: a.airworthiness_directives,
            service_bulletins: a.service_bulletins,
            updated_at: a.updated_at
        } AS aircraft,
        collect(r {
            repair_order_id: r.repair_order_id,
            status: r.status,
            due_date: r.due_date,
            completed_at: r.completed_at
        }) AS repair_orders,
        collect(ad {
            ad_id: ad.ad_id,
            number: ad.number,
            effective_date: ad.effective_date,
            compliance_status: ad.compliance_status
        }) AS directives,
        collect(sb {
            sb_id: sb.sb_id,
            number: sb.number,
            issue_date: sb.issue_date,
            compliance_status: sb.compliance_status
        }) AS bulletins
        """
        
        result = graph.query(query, {"aircraft_id": aircraft_id})
        
        if not result.result_set:
            raise HTTPException(status_code=404, detail=f"Aircraft {aircraft_id} not found")
        
        row = result.result_set[0]
        aircraft = row[0]
        
        # Calculate compliance status
        now = datetime.utcnow().isoformat()
        compliance_issues = []
        
        if aircraft.get("registration_expires") and aircraft["registration_expires"] < now:
            compliance_issues.append("Registration expired")
        
        directives = row[2] or []
        for ad in directives:
            if ad.get("compliance_status") == " overdue":
                compliance_issues.append(f"AD {ad['number']} overdue")
        
        return {
            "aircraft_id": aircraft_id,
            "tail_number": aircraft["tail_number"],
            "airworthiness_status": "valid" if not compliance_issues else "non-compliant",
            "compliance_issues": compliance_issues,
            "repair_orders": row[1] if row[1] else [],
            "directives": row[2] if row[2] else [],
            "bulletins": row[3] if row[3] else [],
            "last_updated": aircraft.get("updated_at")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get airworthiness: {str(e)}")


# WebSocket endpoints for real-time aircraft updates
active_connections: List[WebSocket] = []


@app.websocket("/ws/aircraft")
async def aircraft_websocket(websocket: WebSocket):
    """WebSocket endpoint for real-time aircraft notifications."""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        # Send initial connection confirmation
        await websocket.send_json({
            "type": "connected",
            "message": "WebSocket connection established for aircraft",
            "timestamp": datetime.utcnow().isoformat()
        })
        
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data) if data else {}
            except json.JSONDecodeError:
                message = {"raw": data}
            
            if message.get("type") == "heartbeat":
                await websocket.send_json({
                    "type": "heartbeat",
                    "timestamp": datetime.utcnow().isoformat()
                })
            elif message.get("type") == "subscribe":
                await websocket.send_json({
                    "type": "subscribed",
                    "channel": message.get("channel"),
                    "timestamp": datetime.utcnow().isoformat()
                })
            
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print(f"Aircraft WebSocket disconnected")
    except Exception as e:
        if websocket in active_connections:
            active_connections.remove(websocket)
        print(f"Aircraft WebSocket error: {e}")


@app.post("/ws/aircraft/broadcast")
async def broadcast_aircraft_update(message: str, channel: Optional[str] = None):
    """Broadcast aircraft notification to all connected clients."""
    payload = {
        "type": "aircraft_notification",
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }
    if channel:
        payload["channel"] = channel
    
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_json(payload)
        except Exception:
            disconnected.append(connection)
    
    for conn in disconnected:
        active_connections.remove(conn)
    
    return {
        "message": "Broadcast sent",
        "connections_affected": len(active_connections) - len(disconnected)
    }


# === P0 DEMO ENDPOINTS ===


@app.get("/aircraft/dashboard")
async def get_aircraft_fleet_summary():
    """Get fleet summary with aircraft count, deadlines, and airworthiness status."""
    try:
        graph = falkordb.Graph(FALKORDB_HOST, FALKORDB_PORT, password=FALKORDB_PASSWORD, graph_name=GRAPH_NAME)
        
        # Get total aircraft count
        count_query = "MATCH (a:Aircraft) RETURN count(a) as count"
        count_result = graph.query(count_query)
        total_count = count_result.result_set[0][0] if count_result.result_set else 0
        
        # Get aircraft with expired registration
        deadline_query = """MATCH (a:Aircraft)
        WHERE a.registration_expires < toString(timestamp())
        RETURN a.tail_number as tail_number, a.registration_expires as expires, 'expired' as status
        UNION
        MATCH (a:Aircraft)
        WHERE a.registration_expires >= toString(timestamp())
        AND a.registration_expires <= toString(timestamp() + 2592000)  // 30 days
        RETURN a.tail_number as tail_number, a.registration_expires as expires, 'expiring' as status
        """
        deadline_result = graph.query(deadline_query)
        deadlines = [
            {"tail_number": row[0], "expires": row[1], "status": row[2]}
            for row in deadline_result.result_set
        ]
        
        # Get airworthiness breakdown
        status_query = """MATCH (a:Aircraft)
        WITH
            CASE WHEN a.registration_expires >= toString(timestamp()) THEN 'valid'
            ELSE 'non-compliant'
            END as status
        RETURN status, count(*) as count
        """
        status_result = graph.query(status_query)
        status_breakdown = {
            row[0]: row[1] for row in status_result.result_set
        }
        
        return {
            "total_aircraft": total_count,
            "airworthiness_breakdown": status_breakdown,
            "upcoming_deadlines": deadlines[:10],  # Top 10
            "last_updated": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get fleet summary: {str(e)}")


@app.put("/api/v1/jobs/{job_id}/assign")
async def assign_job_to_mechanic(job_id: int, request: Dict[str, Any]):
    """Assign a mechanic to a job."""
    try:
        graph = falkordb.Graph(FALKORDB_HOST, FALKORDB_PORT, password=FALKORDB_PASSWORD, graph_name=GRAPH_NAME)
        
        mechanic_id = request.get("mechanic_id")
        if not mechanic_id:
            raise HTTPException(status_code=400, detail="mechanic_id is required")
        
        # Assign mechanic to job
        query = """MATCH (j:Job {id: $job_id}), (m:Mechanic {id: $mechanic_id})
        MERGE (j)-[r:ASSIGNED_TO]->(m)
        ON CREATE SET r.assigned_at = toString(timestamp())
        RETURN j, m
        """
        result = graph.query(query, {"job_id": job_id, "mechanic_id": mechanic_id})
        
        if not result.result_set:
            raise HTTPException(status_code=404, detail=f"Job {job_id} or Mechanic {mechanic_id} not found")
        
        return {
            "success": True,
            "message": f"Job {job_id} assigned to mechanic {mechanic_id}",
            "assigned_at": datetime.utcnow().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to assign job: {str(e)}")


@app.post("/api/v1/jobs/{job_id}/complete")
async def complete_job(job_id: int, request: Dict[str, Any]):
    """Complete a job with digital signature."""
    try:
        graph = falkordb.Graph(FALKORDB_HOST, FALKORDB_PORT, password=FALKORDB_PASSWORD, graph_name=GRAPH_NAME)
        
        mechanic_id = request.get("mechanic_id")
        signature = request.get("signature")
        notes = request.get("notes", "")
        
        if not mechanic_id or not signature:
            raise HTTPException(status_code=400, detail="mechanic_id and signature are required")
        
        # Mark job as completed
        query = """MATCH (j:Job {id: $job_id})
        SET j.status = 'completed',
            j.completed_at = toString(timestamp()),
            j.completed_by = $mechanic_id,
            j.signature = $signature,
            j.notes = $notes
        RETURN j
        """
        result = graph.query(query, {
            "job_id": job_id,
            "mechanic_id": mechanic_id,
            "signature": signature,
            "notes": notes
        })
        
        if not result.result_set:
            raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
        
        return {
            "success": True,
            "message": f"Job {job_id} completed",
            "completed_at": datetime.utcnow().isoformat(),
            "completed_by": mechanic_id
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to complete job: {str(e)}")


@app.get("/api/v1/jobs/{job_id}/summary")
async def get_job_summary(job_id: int):
    """Get job summary with cost breakdown and completion details."""
    try:
        graph = falkordb.Graph(FALKORDB_HOST, FALKORDB_PORT, password=FALKORDB_PASSWORD, graph_name=GRAPH_NAME)
        
        # Get job details with associated data
        query = """MATCH (j:Job {id: $job_id})
        OPTIONAL MATCH (j)-[:ASSIGNED_TO]->(m:Mechanic)
        OPTIONAL MATCH (j)-[:CREATED_FOR]->(a:Aircraft)
        OPTIONAL MATCH (j)-[r:USES_PART]->(p:Part)
        WITH j, m, a, r, p,
            CASE WHEN r IS NOT NULL THEN sum(r.cost) ELSE 0 END as parts_cost,
            CASE WHEN j.labor_hours IS NOT NULL THEN j.labor_hours * COALESCE(j.labor_rate, 100) ELSE 0 END as labor_cost
        RETURN {
            job_id: j.id,
            tail_number: a.tail_number,
            status: j.status,
            created_at: j.created_at,
            completed_at: j.completed_at,
            mechanic: {
                id: m.id,
                name: m.name,
                email: m.email
            },
            labor_cost: labor_cost,
            parts_cost: parts_cost,
            total_cost: labor_cost + parts_cost,
            notes: j.notes
        } as data
        """
        result = graph.query(query, {"job_id": job_id})
        
        if not result.result_set or not result.result_set[0][0]:
            raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
        
        return result.result_set[0][0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get job summary: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8208))
    uvicorn.run(app, host="0.0.0.0", port=port, ws_max_size=1048576, ws_ping_interval=30, ws_ping_timeout=20)
