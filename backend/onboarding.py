"""
Onboarding module for SkyMechanics Platform.
Handles account creation, tenant graph setup, and initial data population.
"""
import secrets
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, validator
from db import db_client


# ============== Pydantic Models ==============

class OnboardRequest(BaseModel):
    """Request model for account onboarding."""
    email: EmailStr
    password: str
    account_type: str
    org_name: str
    first_name: str
    last_name: str

    @validator('account_type')
    def validate_account_type(cls, v):
        allowed = {'flight_school', 'solo_owner', 'fbo_shop'}
        if v not in allowed:
            raise ValueError(f'account_type must be one of: {allowed}')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class BulkImportRequest(BaseModel):
    """Request model for bulk import during onboarding."""
    aircraft: Optional[List[dict]] = None
    mechanics: Optional[List[dict]] = None

    class Config:
        extra = 'forbid'


class OnboardResponse(BaseModel):
    """Response model for successful onboarding."""
    success: bool
    tenant_id: str
    graph_name: str
    token: str
    user_id: str


class OnboardStatusResponse(BaseModel):
    """Response model for onboarding status check."""
    setup_complete: bool
    tenant_id: Optional[str] = None
    has_aircraft: bool = False
    has_mechanics: bool = False
    has_admin: bool = False


# ============== Core Functions ==============

def generate_tenant_id() -> str:
    """Generate a unique tenant ID."""
    return f"t_{secrets.token_hex(8)}"


def generate_graph_name(tenant_id: str) -> str:
    """Generate the FalkorDB graph name for a tenant."""
    return f"skymechanics_tenant_{tenant_id}"


def create_tenant_graph(graph_name: str) -> bool:
    """
    Create a new FalkorDB graph for a tenant.
    Returns True if successful, False otherwise.
    """
    try:
        # Switch to the new graph
        db_client.set_graph(graph_name)
        
        # Create the graph (CREATE in FalkorDB)
        db_client.get_graph().query("CREATE ()")
        
        # Create indexes for common queries
        indexes = [
            "CREATE INDEX ON :Customer(name)",
            "CREATE INDEX ON :Aircraft(tail_number)",
            "CREATE INDEX ON :Mechanic(name)",
            "CREATE INDEX ON :Job(status)",
        ]
        
        graph = db_client.get_graph()
        for index_query in indexes:
            try:
                graph.query(index_query)
            except Exception as e:
                # Index may already exist, skip
                print(f"Index creation skipped or failed: {e}")
        
        return True
    except Exception as e:
        print(f"Error creating tenant graph: {e}")
        return False


def initialize_graph_schema(graph_name: str) -> bool:
    """
    Initialize the graph schema with required indexes.
    Returns True if successful, False otherwise.
    """
    try:
        db_client.set_graph(graph_name)
        graph = db_client.get_graph()
        
        # Create indexes
        indexes = [
            "CREATE INDEX ON :Customer(name)",
            "CREATE INDEX ON :Aircraft(tail_number)",
            "CREATE INDEX ON :Mechanic(name)",
            "CREATE INDEX ON :Job(status)",
        ]
        
        for index_query in indexes:
            try:
                graph.query(index_query)
                print(f"Created index: {index_query}")
            except Exception as e:
                print(f"Index creation skipped or failed: {e}")
        
        return True
    except Exception as e:
        print(f"Error initializing graph schema: {e}")
        return False


def create_admin_user(graph_name: str, email: str, first_name: str, 
                      last_name: str, role: str = "admin") -> Optional[str]:
    """
    Create the initial admin user in the tenant graph.
    Returns the user node ID if successful, None otherwise.
    """
    try:
        db_client.set_graph(graph_name)
        graph = db_client.get_graph()
        
        # Check if user already exists
        check_query = "MATCH (u:User {email: $email}) RETURN u"
        check_result = graph.query(check_query, params={"email": email})
        
        if check_result.result_set:
            print(f"User with email {email} already exists")
            return str(check_result.result_set[0][0].id)
        
        # Create admin user node
        create_query = (
            "CREATE (u:User {"
            "email: $email, "
            "first_name: $first_name, "
            "last_name: $last_name, "
            "role: $role, "
            "created_at: $created_at"
            "}) RETURN u"
        )
        
        result = graph.query(create_query, params={
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "role": role,
            "created_at": datetime.utcnow().isoformat()
        })
        
        if result.result_set:
            user_id = str(result.result_set[0][0].id)
            print(f"Created admin user with ID: {user_id}")
            return user_id
        
        return None
    except Exception as e:
        print(f"Error creating admin user: {e}")
        return None


def bulk_import_onboard_data(graph_name: str, import_data: BulkImportRequest) -> dict:
    """
    Import aircraft and mechanics during onboarding.
    Returns a summary of imported items.
    """
    results = {
        "aircraft": [],
        "mechanics": [],
        "errors": []
    }
    
    try:
        db_client.set_graph(graph_name)
        graph = db_client.get_graph()
        
        # Import aircraft
        if import_data.aircraft:
            for aircraft in import_data.aircraft:
                try:
                    tail = aircraft.get('tail_number')
                    make = aircraft.get('make', '')
                    model = aircraft.get('model', '')
                    
                    # Check for duplicate
                    check_query = "MATCH (a:Aircraft {tail_number: $tail}) RETURN a"
                    check_result = graph.query(check_query, params={"tail": tail})
                    
                    if not check_result.result_set:
                        create_query = (
                            "CREATE (a:Aircraft {"
                            "tail_number: $tail, "
                            "make: $make, "
                            "model: $model"
                            "}) RETURN a"
                        )
                        result = graph.query(create_query, params={
                            "tail": tail,
                            "make": make,
                            "model": model
                        })
                        
                        if result.result_set:
                            results["aircraft"].append({
                                "tail_number": tail,
                                "node_id": str(result.result_set[0][0].id)
                            })
                except Exception as e:
                    results["errors"].append(f"Aircraft {aircraft.get('tail_number')}: {e}")
        
        # Import mechanics
        if import_data.mechanics:
            for mechanic in import_data.mechanics:
                try:
                    name = mechanic.get('name', '')
                    email = mechanic.get('email', '')
                    specialties = mechanic.get('specialties', [])
                    
                    # Check for duplicate
                    check_query = "MATCH (m:Mechanic {email: $email}) RETURN m"
                    check_result = graph.query(check_query, params={"email": email})
                    
                    if not check_result.result_set:
                        create_query = (
                            "CREATE (m:Mechanic {"
                            "name: $name, "
                            "email: $email, "
                            "specialties: $specialties"
                            "}) RETURN m"
                        )
                        result = graph.query(create_query, params={
                            "name": name,
                            "email": email,
                            "specialties": specialties
                        })
                        
                        if result.result_set:
                            results["mechanics"].append({
                                "name": name,
                                "email": email,
                                "node_id": str(result.result_set[0][0].id)
                            })
                except Exception as e:
                    results["errors"].append(f"Mechanic {mechanic.get('name')}: {e}")
        
        return results
    except Exception as e:
        results["errors"].append(f"Bulk import failed: {e}")
        return results


def check_onboarding_status(graph_name: str) -> OnboardStatusResponse:
    """
    Check the onboarding status for a tenant graph.
    Returns the current state of setup.
    """
    try:
        db_client.set_graph(graph_name)
        graph = db_client.get_graph()
        
        # Check for admin user
        user_check = graph.query("MATCH (u:User {role: 'admin'}) RETURN u")
        has_admin = bool(user_check.result_set)
        
        # Check for aircraft
        aircraft_check = graph.query("MATCH (a:Aircraft) RETURN a LIMIT 1")
        has_aircraft = bool(aircraft_check.result_set)
        
        # Check for mechanics
        mechanic_check = graph.query("MATCH (m:Mechanic) RETURN m LIMIT 1")
        has_mechanics = bool(mechanic_check.result_set)
        
        # Determine if setup is complete
        setup_complete = has_admin and has_aircraft and has_mechanics
        
        return OnboardStatusResponse(
            setup_complete=setup_complete,
            has_aircraft=has_aircraft,
            has_mechanics=has_mechanics,
            has_admin=has_admin
        )
    except Exception as e:
        print(f"Error checking onboarding status: {e}")
        return OnboardStatusResponse(setup_complete=False)


# ============== High-Level Onboarding Function ==============

def full_onboarding(request: OnboardRequest) -> OnboardResponse:
    """
    Execute the full onboarding flow.
    Creates tenant, sets up graph, creates admin user.
    """
    # Generate IDs
    tenant_id = generate_tenant_id()
    graph_name = generate_graph_name(tenant_id)
    
    # Create tenant graph
    if not create_tenant_graph(graph_name):
        raise Exception("Failed to create tenant graph")
    
    # Create admin user
    user_id = create_admin_user(
        graph_name=graph_name,
        email=request.email,
        first_name=request.first_name,
        last_name=request.last_name,
        role="admin"
    )
    
    if not user_id:
        raise Exception("Failed to create admin user")
    
    # Generate a simple token (for MVP, could be JWT in production)
    token = f"token_{secrets.token_hex(16)}"
    
    return OnboardResponse(
        success=True,
        tenant_id=tenant_id,
        graph_name=graph_name,
        token=token,
        user_id=user_id
    )


def complete_onboarding(graph_name: str, import_data: BulkImportRequest) -> dict:
    """
    Complete onboarding by importing initial data.
    """
    return bulk_import_onboard_data(graph_name, import_data)
