"""
Auth Service - SkyMechanics
Handles user authentication, registration, and authorization.
"""
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.websockets import WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor
import hashlib
import secrets
import os
import asyncio
import json

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://skymechanics:skymechanics-dev@postgres:5432/skymechanics")
FALKORDB_HOST = os.getenv("FALKORDB_HOST", "falkordb")
FALKORDB_PORT = int(os.getenv("FALKORDB_PORT", 6379))
FALKORDB_PASSWORD = os.getenv("FALKORDB_PASSWORD", None)
JWT_SECRET = secrets.token_hex(32)
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# FastAPI app
app = FastAPI(title="Auth Service", version="1.0.0")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    user_id: int
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    role: str


class UserCreate(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    password: str
    role: str = "member"


class OwnerRegister(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    org_name: str
    org_domain: Optional[str] = None


class MechanicRegister(BaseModel):
    email: str
    first_name: str
    last_name: str
    license: str
    specialties: Optional[List[str]] = None


# Database helper
def get_db_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def get_falkordb_graph():
    import falkordb
    db = falkordb.FalkorDB(host=FALKORDB_HOST, port=FALKORDB_PORT, password=FALKORDB_PASSWORD)
    return db.select_graph("tenant_default")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return secrets.token_hex(32)


# Endpoints
@app.get("/")
async def root():
    return {"service": "auth-service", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/ready")
async def ready():
    try:
        conn = get_db_connection()
        conn.close()
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {str(e)}")


@app.post("/api/v1/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 password flow - login and get access token."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email = %s AND password_hash = %s",
            (form_data.username, hash_password(form_data.password))
        )
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["email"]}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@app.get("/api/v1/users/me", response_model=User)
async def read_users_me(token: str = Depends(oauth2_scheme)):
    """Get current user info."""
    return User(
        user_id=1,
        email="admin@skymechanics.dev",
        first_name="Admin",
        last_name="User",
        role="owner"
    )


@app.post("/api/v1/users", response_model=User)
async def create_user(user: UserCreate):
    """Register a new user."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if user exists
        cur.execute("SELECT user_id FROM users WHERE email = %s", (user.email,))
        if cur.fetchone():
            cur.close()
            conn.close()
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create user
        password_hash = hash_password(user.password)
        cur.execute(
            """INSERT INTO users (email, first_name, last_name, phone, password_hash, role)
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING user_id""",
            (user.email, user.first_name, user.last_name, user.phone, password_hash, user.role)
        )
        user_id = cur.fetchone()["user_id"]
        conn.commit()
        cur.close()
        conn.close()
        
        return User(
            user_id=user_id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            role=user.role
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User creation failed: {str(e)}")


@app.get("/api/v1/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get user by ID."""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return User(
            user_id=user["user_id"],
            email=user["email"],
            first_name=user["first_name"],
            last_name=user["last_name"],
            phone=user["phone"],
            role=user["role"]
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")


@app.post("/onboard/owner")
async def onboard_owner(owner: OwnerRegister):
    """
    Complete owner onboarding flow:
    1. Create owner user account
    2. Create organization in FalkorDB
    3. Create default tenant graph
    4. Set up initial schema
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if user exists
        cur.execute("SELECT user_id FROM users WHERE email = %s", (owner.email,))
        if cur.fetchone():
            cur.close()
            conn.close()
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create user with owner role
        password_hash = hash_password(owner.password)
        cur.execute(
            """INSERT INTO users (email, first_name, last_name, phone, password_hash, role)
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING user_id""",
            (owner.email, owner.first_name, owner.last_name, owner.phone, password_hash, "owner")
        )
        user_id = cur.fetchone()["user_id"]
        conn.commit()
        cur.close()
        conn.close()
        
        # Create organization and tenant in FalkorDB
        g = get_falkordb_graph()
        
        # First, create organization in PostgreSQL
        cur.execute(
            """INSERT INTO organizations (name, domain, is_active)
               VALUES (%s, %s, %s) ON CONFLICT (name) DO NOTHING RETURNING org_id""",
            (owner.org_name, owner.org_domain or owner.email.split("@")[1], True)
        )
        org_result = cur.fetchone()
        org_id = org_result[0] if org_result else None
        
        # Link user to organization
        cur.execute(
            """INSERT INTO user_organizations (user_id, org_id, role, joined_at)
               VALUES (%s, %s, %s, %s) ON CONFLICT (user_id, org_id) DO NOTHING""",
            (user_id, org_id, "admin", datetime.utcnow())
        )
        conn.commit()
        
        # Get or create organization in FalkorDB
        result = g.query("MATCH (o:Organization {name: $name}) RETURN o", {"name": owner.org_name})
        if not result.result_set:
            g.query("""
                CREATE (org:Organization {
                    id: $org_id,
                    name: $org_name,
                    domain: $org_domain,
                    created_at: toString(timestamp())
                })
            """, {
                "org_id": secrets.token_hex(8),
                "org_name": owner.org_name,
                "org_domain": owner.org_domain or owner.email.split("@")[1],
            })
        
        # Create owner profile in graph
        g.query("""
            CREATE (owner:Owner {
                id: $user_id,
                name: $name,
                email: $email,
                phone: $phone,
                role: 'owner',
                created_at: toString(timestamp())
            })
        """, {
            "user_id": user_id,
            "name": f"{owner.first_name} {owner.last_name}",
            "email": owner.email,
            "phone": owner.phone,
        })
        
        # Link owner to organization
        g.query("""
            MATCH (org:Organization {name: $org_name}), (u:Owner {id: $user_id})
            CREATE (u)-[:OWNS]->(org)
        """, {"org_name": owner.org_name, "user_id": user_id})
        
        return {
            "message": "Owner account created",
            "user_id": user_id,
            "org_name": owner.org_name,
            "email": owner.email
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Owner registration failed: {str(e)}")


@app.post("/onboard/mechanic")
async def onboard_mechanic(
    email: str,
    first_name: str,
    last_name: str,
    license: str,
    specialty: Optional[str] = None,
    owner_token: str = Depends(oauth2_scheme)
):
    """
    Mechanic onboarding - owner invites mechanics
    Creates mechanic profile and links to owner's organization
    """
    try:
        g = get_falkordb_graph()
        
        # Check if mechanic exists
        result = g.query("MATCH (m:Mechanic {email: $email}) RETURN id(m) AS id", {"email": email})
        if result.result_set:
            raise HTTPException(status_code=400, detail="Mechanic already exists")
        
        # Create mechanic profile
        g.query("""
            CREATE (m:Mechanic {
                id: $id,
                email: $email,
                name: $name,
                license: $license,
                specialty: $specialty,
                created_at: toString(timestamp())
            })
        """, {
            "id": secrets.token_hex(8),
            "email": email,
            "name": f"{first_name} {last_name}",
            "license": license,
            "specialty": specialty or "general",
        })
        
        return {
            "message": "Mechanic onboarding complete",
            "email": email,
            "name": f"{first_name} {last_name}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mechanic registration failed: {str(e)}")


# Additional P0 endpoints for API routes

@app.post("/api/v1/owner/register")
async def register_owner(owner: OwnerRegister):
    """
    Create owner account via API route.
    This is a P0 endpoint for owner registration.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if user exists
        cur.execute("SELECT user_id FROM users WHERE email = %s", (owner.email,))
        if cur.fetchone():
            cur.close()
            conn.close()
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create user with owner role
        password_hash = hash_password(owner.password)
        cur.execute(
            """INSERT INTO users (email, first_name, last_name, phone, password_hash, role)
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING user_id""",
            (owner.email, owner.first_name, owner.last_name, owner.phone, password_hash, "owner")
        )
        user_id = cur.fetchone()["user_id"]
        conn.commit()
        cur.close()
        conn.close()
        
        # Create organization in FalkorDB
        g = get_falkordb_graph()
        
        # Check if organization exists
        result = g.query("MATCH (o:Organization {name: $name}) RETURN o", {"name": owner.org_name})
        if not result.result_set:
            g.query("""
                CREATE (org:Organization {
                    id: $org_id,
                    name: $org_name,
                    domain: $org_domain,
                    created_at: toString(timestamp())
                })
            """, {
                "org_id": secrets.token_hex(8),
                "org_name": owner.org_name,
                "org_domain": owner.org_domain or owner.email.split("@")[1],
            })
        
        # Create owner profile in graph
        g.query("""
            CREATE (owner_node:Owner {
                id: $user_id,
                name: $name,
                email: $email,
                phone: $phone,
                role: 'owner',
                created_at: toString(timestamp())
            })
        """, {
            "user_id": user_id,
            "name": f"{owner.first_name} {owner.last_name}",
            "email": owner.email,
            "phone": owner.phone,
        })
        
        # Link owner to organization
        g.query("""
            MATCH (org:Organization {name: $org_name}), (u:Owner {id: $user_id})
            CREATE (u)-[:OWNS]->(org)
        """, {"org_name": owner.org_name, "user_id": user_id})
        
        return {
            "message": "Owner account created",
            "user_id": user_id,
            "org_name": owner.org_name,
            "email": owner.email
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Owner registration failed: {str(e)}")


@app.post("/api/v1/mechanic/register")
async def register_mechanic(
    mechanic: MechanicRegister,
    owner_token: str = Depends(oauth2_scheme)
):
    """
    Mechanic registration - owner invites mechanics via API.
    This is a P0 endpoint for mechanic registration.
    """
    try:
        specialties = mechanic.specialties or ["general"]
        g = get_falkordb_graph()
        
        # Check if mechanic exists
        result = g.query("MATCH (m:Mechanic {email: $email}) RETURN id(m) AS id", {"email": mechanic.email})
        if result.result_set:
            raise HTTPException(status_code=400, detail="Mechanic already exists")
        
        # Create mechanic profile
        g.query("""
            CREATE (m:Mechanic {
                id: $id,
                email: $email,
                name: $name,
                license: $license,
                specialties: $specialties,
                created_at: toString(timestamp())
            })
        """, {
            "id": secrets.token_hex(8),
            "email": mechanic.email,
            "name": f"{mechanic.first_name} {mechanic.last_name}",
            "license": mechanic.license,
            "specialties": specialties,
        })
        
        return {
            "message": "Mechanic account created",
            "email": mechanic.email,
            "name": f"{mechanic.first_name} {mechanic.last_name}"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mechanic registration failed: {str(e)}")


# WebSocket endpoints for real-time auth updates
active_connections: List[WebSocket] = []


@app.websocket("/ws/auth")
async def auth_websocket(websocket: WebSocket):
    """WebSocket endpoint for real-time auth notifications."""
    await websocket.accept()
    active_connections.append(websocket)
    
    try:
        # Send initial connection confirmation
        await websocket.send_json({
            "type": "connected",
            "message": "WebSocket connection established for auth",
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
        print(f"Auth WebSocket disconnected")
    except Exception as e:
        if websocket in active_connections:
            active_connections.remove(websocket)
        print(f"Auth WebSocket error: {e}")


@app.post("/ws/auth/broadcast")
async def broadcast_auth_update(message: str, channel: Optional[str] = None):
    """Broadcast auth notification to all connected clients."""
    payload = {
        "type": "auth_notification",
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


# Database initialization script
INIT_DB_SQL = """
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(50),
    password_hash VARCHAR(64) NOT NULL,
    role VARCHAR(50) DEFAULT 'member',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS refresh_tokens (
    token_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    token VARCHAR(512) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, ws_max_size=1048576, ws_ping_interval=30, ws_ping_timeout=20)
