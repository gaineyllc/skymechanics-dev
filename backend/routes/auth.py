"""
Authentication API routes.
Handles JWT-based authentication and session management.
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
import hashlib
import secrets

router = APIRouter()

# In-memory token store (replace with Redis in production)
token_store = {}
refresh_tokens = {}


class TokenData(BaseModel):
    """Token payload data."""
    user_id: str
    tenant_id: str
    role: str
    expires: datetime


class LoginRequest(BaseModel):
    """Login request."""
    email: str
    password: str
    tenant_id: str = "default"


class LoginResponse(BaseModel):
    """Login response with tokens."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # seconds


class RegisterRequest(BaseModel):
    """Registration request."""
    email: str
    password: str
    first_name: str
    last_name: str
    tenant_id: str = "default"
    role: str = "user"


class RegisterResponse(BaseModel):
    """Registration response."""
    user_id: str
    email: str
    message: str


class RefreshRequest(BaseModel):
    """Token refresh request."""
    refresh_token: str


@router.post("/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Authenticate a user and return JWT tokens.
    
    In production, replace with proper password hashing and database lookup.
    """
    # TODO: Implement proper password verification
    # For now, this is a placeholder that accepts any credentials
    
    if not request.email or not request.password:
        raise HTTPException(status_code=400, detail="Email and password required")
    
    # Generate user ID from email (placeholder)
    user_id = hashlib.sha256(request.email.encode()).hexdigest()[:16]
    
    # Create access token
    access_token = create_access_token(user_id, request.tenant_id, "user")
    
    # Create refresh token
    refresh_token = secrets.token_urlsafe(32)
    refresh_tokens[refresh_token] = {
        "user_id": user_id,
        "tenant_id": request.tenant_id,
        "created_at": datetime.now()
    }
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=3600  # 1 hour
    )


@router.post("/auth/register", response_model=RegisterResponse)
async def register(request: RegisterRequest):
    """
    Register a new user.
    
    Creates a new user account and returns success message.
    """
    # TODO: Implement proper user creation with password hashing
    # Validate email format
    if "@" not in request.email:
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Validate password strength
    if len(request.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    
    # Generate user ID
    user_id = hashlib.sha256(request.email.encode()).hexdigest()[:16]
    
    # Store user (placeholder - would use database in production)
    user_store[user_id] = {
        "email": request.email,
        "first_name": request.first_name,
        "last_name": request.last_name,
        "tenant_id": request.tenant_id,
        "role": request.role,
        "created_at": datetime.now()
    }
    
    return RegisterResponse(
        user_id=user_id,
        email=request.email,
        message="User registered successfully"
    )


@router.post("/auth/refresh")
async def refresh_token(request: RefreshRequest):
    """
    Refresh access token using refresh token.
    
    Returns new access token if refresh token is valid.
    """
    if request.refresh_token not in refresh_tokens:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    token_data = refresh_tokens[request.refresh_token]
    
    # Check if refresh token expired (7 days)
    if datetime.now() - token_data["created_at"] > timedelta(days=7):
        del refresh_tokens[request.refresh_token]
        raise HTTPException(status_code=401, detail="Refresh token expired")
    
    # Create new access token
    access_token = create_access_token(
        token_data["user_id"],
        token_data["tenant_id"],
        "user"
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 3600
    }


@router.post("/auth/logout")
async def logout(request: Request):
    """
    Logout user and invalidate tokens.
    
    Removes access token from store (in production, add to blacklist).
    """
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header[7:]
        if token in token_store:
            del token_store[token]
    
    return {"message": "Logged out successfully"}


@router.get("/auth/profile")
async def get_profile(request: Request):
    """
    Get current user profile from token.
    
    Extracts user info from JWT token.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No authorization header")
    
    token = auth_header[7:]
    
    if token not in token_store:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    token_data = token_store[token]
    
    return {
        "user_id": token_data["user_id"],
        "tenant_id": token_data["tenant_id"],
        "role": token_data["role"],
        "email": "user@example.com",  # Would come from database
        "first_name": "User",  # Would come from database
        "last_name": "User"  # Would come from database
    }


def create_access_token(user_id: str, tenant_id: str, role: str) -> str:
    """Create a JWT access token."""
    # Generate token
    token = secrets.token_urlsafe(32)
    
    # Store in memory (replace with Redis in production)
    token_store[token] = TokenData(
        user_id=user_id,
        tenant_id=tenant_id,
        role=role,
        expires=datetime.now() + timedelta(hours=1)
    )
    
    return token


# In-memory user store (replace with database in production)
user_store = {}

# Add auth router to main app
# app.include_router(router, prefix="/api/v1", tags=["auth"])
