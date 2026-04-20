"""
Mechanic routes for SkyMechanics Platform.
Handles mechanic creation, listing, and profile management.
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import ValidationError
from typing import Optional
from datetime import datetime

from onboarding import (
    db_client,
    MechanicProfileRequest,
    MechanicProfile,
    create_mechanic_profile,
    get_mechanic_profile,
)

router = APIRouter(
    prefix="/api/v1/mechanics",
    tags=["Mechanics"]
)


@router.get("", response_model=list)
async def list_mechanics(graph_name: str = "skymechanics_demo"):
    """
    List all mechanics in the tenant graph.
    """
    try:
        db_client.set_graph(graph_name)
        graph = db_client.get_graph()
        
        query = """
        MATCH (m:Mechanic)
        RETURN m.node_id AS node_id, m.name AS name, m.email AS email,
               m.phone AS phone, m.specialties AS specialties
        """
        result = graph.query(query)
        
        mechanics = []
        for row in result.result_set:
            mechanics.append({
                "node_id": row[0],
                "label": "Mechanic",
                "properties": {
                    "name": row[1],
                    "email": row[2],
                    "phone": row[3] if row[3] else "",
                    "specialties": row[4] if row[4] else []
                }
            })
        
        return mechanics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list mechanics: {str(e)}")


@router.post("", response_model=dict)
async def create_mechanic(
    request: Request,
    graph_name: str = "skymechanics_demo"
):
    """
    Create a new mechanic in the tenant graph.
    
    Request body:
    - name: Mechanic name
    - email: Email address
    - phone: Phone number (optional)
    - specialties: Array of certifications/specialties
    
    Also creates a MechanicProfile node linked to the User.
    """
    try:
        body = await request.json()
        name = body.get('name')
        email = body.get('email')
        phone = body.get('phone')
        specialties = body.get('specialties', [])
        
        if not name or not email:
            raise HTTPException(status_code=400, detail="Name and email are required")
        
        db_client.set_graph(graph_name)
        graph = db_client.get_graph()
        
        # Create Mechanic node
        create_query = """
        CREATE (m:Mechanic {
            name: $name,
            email: $email,
            phone: $phone,
            specialties: $specialties,
            created_at: $created_at
        })
        RETURN m
        """
        
        result = graph.query(create_query, params={
            "name": name,
            "email": email,
            "phone": phone,
            "specialties": specialties,
            "created_at": datetime.utcnow().isoformat()
        })
        
        if result.result_set:
            mechanic_props = result.result_set[0][0].properties
            
            # Create user node for authentication
            user_query = """
            CREATE (u:User {
                email: $email,
                first_name: $name,
                last_name: '',
                role: 'mechanic',
                created_at: $created_at
            })
            RETURN u
            """
            user_result = graph.query(user_query, params={
                "email": email,
                "name": name.split()[0] if name else email,
                "created_at": datetime.utcnow().isoformat()
            })
            
            if user_result.result_set:
                user_id = str(user_result.result_set[0][0].id)
                
                # Create MechanicProfile
                profile_query = """
                CREATE (p:MechanicProfile {
                    license_number: null,
                    certifications: [],
                    availability: null,
                    current_location: null,
                    created_at: $created_at,
                    updated_at: $created_at
                })
                RETURN p
                """
                profile_result = graph.query(profile_query, params={
                    "created_at": datetime.utcnow().isoformat()
                })
                
                if profile_result.result_set:
                    # Link user to profile
                    link_query = """
                    MATCH (u:User {node_id: $user_id}), (p:MechanicProfile)
                    CREATE (u)-[:HAS_PROFILE]->(p)
                    """
                    graph.query(link_query, params={"user_id": user_id})
                    
                    return {
                        "success": True,
                        "mechanic": {
                            "node_id": mechanic_props.get("node_id"),
                            "label": "Mechanic",
                            "properties": {
                                "name": mechanic_props.get("name"),
                                "email": mechanic_props.get("email"),
                                "phone": mechanic_props.get("phone", ""),
                                "specialties": mechanic_props.get("specialties", [])
                            }
                        },
                        "user_id": user_id,
                        "profile_created": True
                    }
            
            return {
                "success": True,
                "mechanic": {
                    "node_id": mechanic_props.get("node_id"),
                    "label": "Mechanic",
                    "properties": {
                        "name": mechanic_props.get("name"),
                        "email": mechanic_props.get("email"),
                        "phone": mechanic_props.get("phone", ""),
                        "specialties": mechanic_props.get("specialties", [])
                    }
                },
                "user_id": None,
                "profile_created": False
            }
        
        raise HTTPException(status_code=500, detail="Failed to create mechanic")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mechanic creation failed: {str(e)}")


@router.get("/{mechanic_id}", response_model=dict)
async def get_mechanic(
    mechanic_id: int,
    graph_name: str = "skymechanics_demo"
):
    """
    Get a specific mechanic by ID.
    Includes full profile details.
    """
    try:
        db_client.set_graph(graph_name)
        graph = db_client.get_graph()
        
        # Get mechanic node
        mechanic_query = """
        MATCH (m:Mechanic {node_id: $mechanic_id})
        RETURN m
        """
        mechanic_result = graph.query(mechanic_query, params={"mechanic_id": mechanic_id})
        
        if not mechanic_result.result_set:
            raise HTTPException(status_code=404, detail="Mechanic not found")
        
        mechanic_props = mechanic_result.result_set[0][0].properties
        
        # Get profile if exists
        profile_query = """
        MATCH (m:Mechanic {node_id: $mechanic_id})-[:HAS_PROFILE]->(p:MechanicProfile)
        RETURN p
        """
        profile_result = graph.query(profile_query, params={"mechanic_id": mechanic_id})
        
        profile = None
        if profile_result.result_set:
            profile_props = profile_result.result_set[0][0].properties
            profile = {
                "license_number": profile_props.get("license_number"),
                "certifications": profile_props.get("certifications", []),
                "availability": profile_props.get("availability"),
                "current_location": profile_props.get("current_location"),
                "created_at": profile_props.get("created_at"),
                "updated_at": profile_props.get("updated_at")
            }
        
        return {
            "node_id": mechanic_props.get("node_id"),
            "label": "Mechanic",
            "properties": {
                "name": mechanic_props.get("name"),
                "email": mechanic_props.get("email"),
                "phone": mechanic_props.get("phone", ""),
                "specialties": mechanic_props.get("specialties", [])
            },
            "profile": profile
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get mechanic: {str(e)}")


@router.post("/{mechanic_id}/profile", response_model=dict)
async def update_mechanic_profile(
    mechanic_id: int,
    request: Request,
    graph_name: str = "skymechanics_demo"
):
    """
    Update or create a mechanic profile.
    
    Request body:
    - license_number: Optional license number
    - certifications: Array of certifications
    - availability: Schedule dictionary
    - current_location: GPS coordinates {lat, lng}
    """
    try:
        body = await request.json()
        
        db_client.set_graph(graph_name)
        graph = db_client.get_graph()
        
        # Check if mechanic exists
        mechanic_query = "MATCH (m:Mechanic {node_id: $mechanic_id}) RETURN m"
        mechanic_result = graph.query(mechanic_query, params={"mechanic_id": mechanic_id})
        
        if not mechanic_result.result_set:
            raise HTTPException(status_code=404, detail="Mechanic not found")
        
        # Get or create user link
        user_query = """
        MATCH (m:Mechanic {node_id: $mechanic_id})-[:HAS_PROFILE]->(p:MechanicProfile)
        RETURN p
        """
        user_result = graph.query(user_query, params={"mechanic_id": mechanic_id})
        
        if user_result.result_set:
            # Update existing profile
            update_query = """
            MATCH (m:Mechanic {node_id: $mechanic_id})-[:HAS_PROFILE]->(p:MechanicProfile)
            SET p.license_number = $license_number,
                p.certifications = $certifications,
                p.availability = $availability,
                p.current_location = $current_location,
                p.updated_at = $updated_at
            RETURN p
            """
            result = graph.query(update_query, params={
                "mechanic_id": mechanic_id,
                "license_number": body.get("license_number"),
                "certifications": body.get("certifications", []),
                "availability": body.get("availability"),
                "current_location": body.get("current_location"),
                "updated_at": datetime.utcnow().isoformat()
            })
        else:
            # Create new profile and link to mechanic
            create_query = """
            MATCH (m:Mechanic {node_id: $mechanic_id})
            CREATE (p:MechanicProfile {
                license_number: $license_number,
                certifications: $certifications,
                availability: $availability,
                current_location: $current_location,
                created_at: $created_at,
                updated_at: $updated_at
            })
            CREATE (m)-[:HAS_PROFILE]->(p)
            RETURN p
            """
            result = graph.query(create_query, params={
                "mechanic_id": mechanic_id,
                "license_number": body.get("license_number"),
                "certifications": body.get("certifications", []),
                "availability": body.get("availability"),
                "current_location": body.get("current_location"),
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat()
            })
        
        if result.result_set:
            profile_props = result.result_set[0][0].properties
            return {
                "success": True,
                "profile": {
                    "license_number": profile_props.get("license_number"),
                    "certifications": profile_props.get("certifications", []),
                    "availability": profile_props.get("availability"),
                    "current_location": profile_props.get("current_location"),
                    "created_at": profile_props.get("created_at"),
                    "updated_at": profile_props.get("updated_at")
                }
            }
        
        raise HTTPException(status_code=500, detail="Failed to update profile")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile update failed: {str(e)}")
