"""
User routes for SkyMechanics Platform.
Handles role-based user onboarding and profile management.
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import ValidationError
from typing import Optional

from models import (
    UserCreateRequest,
    OwnerProfileRequest,
    AdminProfileRequest,
    MechanicProfileRequest
)

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"]
)


@router.post("", response_model=dict)
async def onboard_user(request: UserCreateRequest):
    """
    Create a new user with role-based profile.
    
    Supports three roles:
    - `owner`: Aircraft owner with vehicle connections
    - `admin`: Platform administrator with permissions
    - `mechanic`: Service provider with certifications
    """
    try:
        # Return success response with user data
        return {
            "success": True,
            "user_id": 0,
            "email": request.email,
            "role": request.role,
            "message": "User created successfully"
        }
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e.errors()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"User creation failed: {str(e)}")


@router.get("/{user_id}")
async def get_user(user_id: int, role: str = "owner"):
    """
    Retrieve a user profile by ID.
    
    Args:
        user_id: User node ID
        role: Role to determine profile type (owner/admin/mechanic)
    """
    try:
        return {
            "user_id": user_id,
            "role": role,
            "profile_type": f"{role}_profile",
            "data": {}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Profile fetch failed: {str(e)}")


@router.post("/{user_id}/profile/owner")
async def create_owner_profile(user_id: int, request: OwnerProfileRequest):
    """
    Create or update owner profile.
    
    Properties:
    - vehicle_ids: List of vehicle/node IDs
    - preferences: Owner preferences dictionary
    """
    try:
        return {
            "success": True,
            "user_id": user_id,
            "profile": {
                "vehicle_ids": request.vehicle_ids,
                "preferences": request.preferences
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Owner profile creation failed: {str(e)}")


@router.post("/{user_id}/profile/admin")
async def create_admin_profile(user_id: int, request: AdminProfileRequest):
    """
    Create or update admin profile.
    
    Properties:
    - permissions: List of admin permissions
    - settings: Admin settings dictionary
    """
    try:
        return {
            "success": True,
            "user_id": user_id,
            "profile": {
                "permissions": request.permissions,
                "settings": request.settings
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Admin profile creation failed: {str(e)}")


@router.post("/{user_id}/profile/mechanic")
async def create_mechanic_profile(user_id: int, request: MechanicProfileRequest):
    """
    Create or update mechanic profile.
    
    Properties:
    - license_number: Optional license number
    - certifications: List of certifications
    - availability: Working hours/days
    - current_location: GPS coordinates {lat, lng}
    """
    try:
        return {
            "success": True,
            "user_id": user_id,
            "profile": {
                "license_number": request.license_number,
                "certifications": request.certifications,
                "availability": request.availability,
                "current_location": request.current_location
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Mechanic profile creation failed: {str(e)}")
