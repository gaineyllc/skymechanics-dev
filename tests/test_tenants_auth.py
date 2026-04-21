"""
Tests for multi-tenancy endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


class TestTenantsAPI:
    """Test tenant creation and management endpoints."""
    
    def test_create_tenant(self):
        """Test creating a new tenant graph."""
        response = client.post(
            "/api/v1/tenants",
            json={
                "tenant_id": "test_tenant_1",
                "tenant_name": "Test Tenant 1"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["tenant_id"] == "test_tenant_1"
        assert data["graph_name"] == "tenant_test_tenant_1"
        assert data["is_active"] == True
    
    def test_create_tenant_with_custom_graph_name(self):
        """Test creating a tenant with a custom graph name."""
        response = client.post(
            "/api/v1/tenants",
            json={
                "tenant_id": "custom_tenant",
                "graph_name": "custom_graph_name",
                "tenant_name": "Custom Tenant"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["graph_name"] == "custom_graph_name"
    
    def test_list_tenants(self):
        """Test listing all tenants."""
        response = client.get("/api/v1/tenants")
        
        assert response.status_code == 200
        data = response.json()
        assert "tenants" in data
        assert "total" in data
        assert isinstance(data["tenants"], list)
        assert isinstance(data["total"], int)
    
    def test_get_tenant(self):
        """Test getting a specific tenant."""
        # First create a tenant
        create_response = client.post(
            "/api/v1/tenants",
            json={"tenant_id": "get_test_tenant"}
        )
        
        # Then get it
        response = client.get("/api/v1/tenants/get_test_tenant")
        
        assert response.status_code == 200
        data = response.json()
        assert data["tenant_id"] == "get_test_tenant"
    
    def test_get_nonexistent_tenant(self):
        """Test getting a tenant that doesn't exist."""
        response = client.get("/api/v1/tenants/nonexistent_tenant")
        
        assert response.status_code == 404
    
    def test_delete_tenant(self):
        """Test deleting a tenant."""
        # Create tenant
        client.post("/api/v1/tenants", json={"tenant_id": "delete_test_tenant"})
        
        # Delete tenant
        response = client.delete("/api/v1/tenants/delete_test_tenant")
        
        assert response.status_code == 200
        data = response.json()
        assert "deleted successfully" in data["message"]
    
    def test_query_tenant(self):
        """Test querying a tenant's graph."""
        # Create tenant first
        client.post("/api/v1/tenants", json={"tenant_id": "query_test_tenant"})
        
        # Query the tenant
        response = client.post(
            "/api/v1/tenants/query_test_tenant/query",
            json={
                "query": "RETURN 1 AS test"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "headers" in data
        assert "results" in data


class TestAuthAPI:
    """Test authentication endpoints."""
    
    def test_login(self):
        """Test user login."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123",
                "tenant_id": "default"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["expires_in"] == 3600
    
    def test_login_missing_credentials(self):
        """Test login with missing credentials."""
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "test@example.com"}
        )
        
        assert response.status_code == 400
    
    def test_register(self):
        """Test user registration."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "password123",
                "first_name": "New",
                "last_name": "User",
                "tenant_id": "default",
                "role": "user"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert data["email"] == "newuser@example.com"
    
    def test_register_invalid_email(self):
        """Test registration with invalid email."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid-email",
                "password": "password123",
                "first_name": "Test",
                "last_name": "User"
            }
        )
        
        assert response.status_code == 400
    
    def test_register_weak_password(self):
        """Test registration with weak password."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "password": "short",
                "first_name": "Test",
                "last_name": "User"
            }
        )
        
        assert response.status_code == 400
    
    def test_refresh_token(self):
        """Test token refresh."""
        # First login to get tokens
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )
        refresh_token = login_response.json()["refresh_token"]
        
        # Then refresh
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
    
    def test_refresh_invalid_token(self):
        """Test refresh with invalid token."""
        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid_token"}
        )
        
        assert response.status_code == 401
    
    def test_get_profile(self):
        """Test getting user profile."""
        # Login first
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "password123"
            }
        )
        access_token = login_response.json()["access_token"]
        
        # Get profile
        response = client.get(
            "/api/v1/auth/profile",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "role" in data
    
    def test_get_profile_no_auth(self):
        """Test getting profile without authentication."""
        response = client.get("/api/v1/auth/profile")
        
        assert response.status_code == 401
    
    def test_get_profile_invalid_token(self):
        """Test getting profile with invalid token."""
        response = client.get(
            "/api/v1/auth/profile",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == 401
