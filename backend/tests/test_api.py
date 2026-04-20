"""
Integration tests for SkyMechanics Platform API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

# Import the app
import sys
sys.path.insert(0, '/home/gaineyllc/.openclaw/workspace/skymechanics-dev/backend')
from main import app
from db import FalkorDBClient


client = TestClient(app)


class TestHealthEndpoint:
    """Tests for /health endpoint."""

    def test_health_check_success(self):
        """Test health check returns healthy status."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "database" in data


class TestCustomersEndpoint:
    """Tests for /customers endpoint."""
    
    @pytest.mark.skip(reason="Requires FalkorDB connection")
    def test_create_customer_success(self):
        """Test successful customer creation."""
        customer_data = {
            "name": "Test Owner",
            "email": "test@example.com",
            "phone": "+1234567890",
            "address": {"street": "123 Test St"}
        }
        response = client.post("/customers", json=customer_data)
        assert response.status_code == 200
        data = response.json()
        assert data["label"] == "Customer"
        assert data["properties"]["name"] == "Test Owner"

    @pytest.mark.skip(reason="Requires FalkorDB connection")
    def test_create_customer_duplicate_email(self):
        """Test creating customer with duplicate email."""
        customer_data = {
            "name": "Test Owner",
            "email": "duplicate@example.com",
            "phone": "+1234567890",
            "address": {"street": "123 Test St"}
        }
        # Create first customer
        client.post("/customers", json=customer_data)
        # Try to create duplicate
        response = client.post("/customers", json=customer_data)
        assert response.status_code == 409


class TestJobsEndpoint:
    """Tests for /jobs endpoint."""
    
    @pytest.mark.skip(reason="Requires FalkorDB connection")
    def test_create_job_success(self):
        """Test successful job creation."""
        job_data = {
            "customer_id": 1,
            "title": "Test Engine Repair",
            "description": "Engine inspection and repair",
            "status": "pending",
            "priority": 2
        }
        response = client.post("/jobs", json=job_data)
        assert response.status_code == 200
        data = response.json()
        assert data["label"] == "Job"
        assert data["properties"]["title"] == "Test Engine Repair"

    @pytest.mark.skip(reason="Requires FalkorDB connection")
    def test_create_job_invalid_customer(self):
        """Test creating job with non-existent customer."""
        job_data = {
            "customer_id": 9999,
            "title": "Test Job",
            "description": "Test",
            "status": "pending",
            "priority": 1
        }
        response = client.post("/jobs", json=job_data)
        assert response.status_code == 404


class TestMechanicsEndpoint:
    """Tests for /mechanics endpoint."""
    
    @pytest.mark.skip(reason="Requires FalkorDB connection")
    def test_create_mechanic_success(self):
        """Test successful mechanic creation."""
        mechanic_data = {
            "name": "Test Mechanic",
            "email": "mechanic@test.com",
            "phone": "+1987654321",
            "specialties": ["Engine", "Avionics"]
        }
        response = client.post("/mechanics", json=mechanic_data)
        assert response.status_code == 200
        data = response.json()
        assert data["label"] == "Mechanic"
        assert data["properties"]["name"] == "Test Mechanic"


class TestJobDetailEndpoint:
    """Tests for /jobs/{job_id} endpoint."""
    
    @pytest.mark.skip(reason="Requires FalkorDB connection")
    def test_get_job_not_found(self):
        """Test getting a non-existent job."""
        response = client.get("/jobs/9999")
        assert response.status_code == 404

    @pytest.mark.skip(reason="Requires FalkorDB connection")
    def test_update_job_success(self):
        """Test updating a job."""
        job_data = {
            "customer_id": 1,
            "title": "Job to Update",
            "description": "Original description",
            "status": "pending",
            "priority": 2
        }
        # Create job first
        create_response = client.post("/jobs", json=job_data)
        job_id = create_response.json()["node_id"]
        
        # Update job
        update_data = {"status": "open", "priority": 3}
        response = client.put(f"/jobs/{job_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["properties"]["status"] == "open"

    @pytest.mark.skip(reason="Requires FalkorDB connection")
    def test_delete_job_success(self):
        """Test deleting a job."""
        job_data = {
            "customer_id": 1,
            "title": "Job to Delete",
            "description": "To be deleted",
            "status": "pending",
            "priority": 1
        }
        # Create job first
        create_response = client.post("/jobs", json=job_data)
        job_id = create_response.json()["node_id"]
        
        # Delete job
        response = client.delete(f"/jobs/{job_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True

    @pytest.mark.skip(reason="Requires FalkorDB connection")
    def test_delete_job_not_found(self):
        """Test deleting a non-existent job."""
        response = client.delete("/jobs/9999")
        assert response.status_code == 404
