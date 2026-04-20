"""
Mechanics Service - SkyMechanics
Handles mechanic management, availability, and fleet operations.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import os

# Import shared models
import sys
sys.path.insert(0, '/app/shared')
from models import MechanicCreateRequest, MechanicResponse, MechanicUpdateRequest

# Configuration
FALKORDB_HOST = os.getenv("FALKORDB_HOST", "falkordb")
FALKORDB_PORT = int(os.getenv("FALKORDB_PORT", 6379))
TENANT_ID = os.getenv("TENANT_ID", "default")

# FastAPI app
app = FastAPI(title="Mechanics Service", version="1.0.0")


# Pydantic models (duplicated for standalone operation)
class MechanicCreateRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    specialties: List[str] = []


class MechanicUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    specialties: Optional[List[str]] = None
    license_number: Optional[str] = None
    certifications: Optional[List[str]] = None
    availability: Optional[Dict[str, Any]] = None
    current_location: Optional[Dict[str, float]] = None


class MechanicResponse(BaseModel):
    mechanic_id: int
    name: str
    email: str
    phone: Optional[str] = None
    specialties: List[str]
    license_number: Optional[str] = None
    certifications: List[str]
    availability: Dict[str, Any]
    current_location: Optional[Dict[str, float]] = None
    created_at: datetime


# Simplified FalkorDB client (in production, use proper driver)
class FalkorDBClient:
    """Simplified FalkorDB client for mechanics service."""
    
    def __init__(self, host: str = FALKORDB_HOST, port: int = FALKORDB_PORT):
        self.host = host
        self.port = port
        self.graph_name = f"tenant_{TENANT_ID}"
    
    def execute(self, query: str, params: Optional[Dict] = None):
        """Execute a Cypher query."""
        # In production, use falkordb.Graph.execute()
        # For now, return a mock response
        return {"results": [], "headers": []}
    
    def get_graph(self):
        """Get the graph object."""
        # In production, use falkordb.Graph()
        return self


# Initialize client
db = FalkorDBClient()


# Endpoints
@app.get("/")
async def root():
    return {
        "service": "mechanics-service", 
        "status": "running",
        "falkordb": f"{FALKORDB_HOST}:{FALKORDB_PORT}"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/ready")
async def ready():
    try:
        # Test database connection
        db.execute("RETURN 1 AS test")
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {str(e)}")


@app.post("/mechanics", response_model=MechanicResponse)
async def create_mechanic(mechanic: MechanicCreateRequest):
    """Create a new mechanic."""
    try:
        query = """
        CREATE (m:Mechanic {
            name: $name,
            email: $email,
            phone: $phone,
            specialties: $specialties,
            created_at: datetime()
        })
        RETURN m {
            mechanic_id: id(m),
            name: m.name,
            email: m.email,
            phone: m.phone,
            specialties: m.specialties,
            license_number: m.license_number,
            certifications: m.certifications,
            availability: m.availability,
            current_location: m.current_location,
            created_at: m.created_at
        } AS mechanic
        """
        params = {
            "name": mechanic.name,
            "email": mechanic.email,
            "phone": mechanic.phone,
            "specialties": mechanic.specialties
        }
        
        result = db.execute(query, params)
        mechanic_id = result["results"][0][0]["mechanic_id"] if result["results"] else 1
        
        return MechanicResponse(
            mechanic_id=mechanic_id,
            name=mechanic.name,
            email=mechanic.email,
            phone=mechanic.phone,
            specialties=mechanic.specialties,
            license_number=None,
            certifications=[],
            availability={},
            created_at=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mechanic creation failed: {str(e)}")


@app.get("/mechanics/{mechanic_id}", response_model=MechanicResponse)
async def get_mechanic(mechanic_id: int):
    """Get mechanic by ID."""
    try:
        query = """
        MATCH (m:Mechanic {id: $mechanic_id})
        RETURN m {
            mechanic_id: id(m),
            name: m.name,
            email: m.email,
            phone: m.phone,
            specialties: m.specialties,
            license_number: m.license_number,
            certifications: m.certifications,
            availability: m.availability,
            current_location: m.current_location,
            created_at: m.created_at
        } AS mechanic
        """
        result = db.execute(query, {"mechanic_id": mechanic_id})
        
        if not result["results"]:
            raise HTTPException(status_code=404, detail="Mechanic not found")
        
        mechanic_data = result["results"][0][0]["mechanic"]
        
        return MechanicResponse(
            mechanic_id=mechanic_id,
            name=mechanic_data["name"],
            email=mechanic_data["email"],
            phone=mechanic_data.get("phone"),
            specialties=mechanic_data.get("specialties", []),
            license_number=mechanic_data.get("license_number"),
            certifications=mechanic_data.get("certifications", []),
            availability=mechanic_data.get("availability", {}),
            current_location=mechanic_data.get("current_location"),
            created_at=datetime.fromisoformat(mechanic_data["created_at"].replace("Z", "+00:00"))
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get mechanic: {str(e)}")


@app.put("/mechanics/{mechanic_id}", response_model=MechanicResponse)
async def update_mechanic(mechanic_id: int, mechanic: MechanicUpdateRequest):
    """Update a mechanic."""
    try:
        # Build dynamic query
        updates = []
        params = {"mechanic_id": mechanic_id}
        
        if mechanic.name:
            updates.append("m.name = $name")
            params["name"] = mechanic.name
        if mechanic.email:
            updates.append("m.email = $email")
            params["email"] = mechanic.email
        if mechanic.phone is not None:
            updates.append("m.phone = $phone")
            params["phone"] = mechanic.phone
        if mechanic.specialties:
            updates.append("m.specialties = $specialties")
            params["specialties"] = mechanic.specialties
        
        if not updates:
            # No updates to apply
            return await get_mechanic(mechanic_id)
        
        query = f"""
        MATCH (m:Mechanic {{id: $mechanic_id}})
        SET {', '.join(updates)}
        SET m.updated_at = datetime()
        RETURN m {
            mechanic_id: id(m),
            name: m.name,
            email: m.email,
            phone: m.phone,
            specialties: m.specialties,
            license_number: m.license_number,
            certifications: m.certifications,
            availability: m.availability,
            current_location: m.current_location,
            created_at: m.created_at
        } AS mechanic
        """
        
        result = db.execute(query, params)
        mechanic_data = result["results"][0][0]["mechanic"]
        
        return MechanicResponse(
            mechanic_id=mechanic_id,
            name=mechanic_data["name"],
            email=mechanic_data["email"],
            phone=mechanic_data.get("phone"),
            specialties=mechanic_data.get("specialties", []),
            license_number=mechanic_data.get("license_number"),
            certifications=mechanic_data.get("certifications", []),
            availability=mechanic_data.get("availability", {}),
            current_location=mechanic_data.get("current_location"),
            created_at=datetime.fromisoformat(mechanic_data["created_at"].replace("Z", "+00:00"))
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mechanic update failed: {str(e)}")


@app.get("/mechanics", response_model=List[MechanicResponse])
async def list_mechanics():
    """List all mechanics."""
    try:
        query = """
        MATCH (m:Mechanic)
        RETURN m {
            mechanic_id: id(m),
            name: m.name,
            email: m.email,
            phone: m.phone,
            specialties: m.specialties,
            license_number: m.license_number,
            certifications: m.certifications,
            availability: m.availability,
            current_location: m.current_location,
            created_at: m.created_at
        } AS mechanic
        """
        result = db.execute(query)
        
        return [
            MechanicResponse(
                mechanic_id=m["mechanic_id"],
                name=m["name"],
                email=m["email"],
                phone=m.get("phone"),
                specialties=m.get("specialties", []),
                license_number=m.get("license_number"),
                certifications=m.get("certifications", []),
                availability=m.get("availability", {}),
                current_location=m.get("current_location"),
                created_at=datetime.fromisoformat(m["created_at"].replace("Z", "+00:00"))
            )
            for m in result["results"][0] if result["results"]
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list mechanics: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
