"""
Unit tests for SkyMechanics Platform models.
"""
import pytest
from pydantic import ValidationError

from models import (
    CustomerCreateRequest,
    JobCreateRequest,
    MechanicCreateRequest,
    GraphQueryRequest,
    MultiTenantCreateRequest,
    SuccessResponse,
    ErrorResponse
)


class TestCustomerCreateRequest:
    """Tests for CustomerCreateRequest model."""

    def test_valid_customer_request(self):
        """Test valid customer creation request."""
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "address": {"street": "123 Main St", "city": "City", "state": "State", "zip": "12345"}
        }
        request = CustomerCreateRequest(**data)
        assert request.name == "John Doe"
        assert request.email == "john@example.com"

    def test_customer_request_minimal(self):
        """Test customer creation with minimal data (optional fields)."""
        data = {
            "name": "John Doe",
            "email": "john@example.com"
        }
        request = CustomerCreateRequest(**data)
        assert request.name == "John Doe"
        assert request.email == "john@example.com"
        assert request.phone is None
        assert request.address is None

    def test_customer_request_invalid_email(self):
        """Test customer creation with invalid email format."""
        data = {
            "name": "John Doe",
            "email": "not-an-email",
            "phone": "+1234567890",
            "address": {"street": "123 Main St"}
        }
        # Pydantic doesn't validate email format by default without email-validator
        # This test documents current behavior
        request = CustomerCreateRequest(**data)
        assert request.email == "not-an-email"


class TestJobCreateRequest:
    """Tests for JobCreateRequest model."""

    def test_valid_job_request(self):
        """Test valid job creation request."""
        data = {
            "customer_id": 1,
            "title": "Engine Overhaul",
            "description": "Complete engine inspection and repair",
            "status": "pending",
            "priority": 3
        }
        request = JobCreateRequest(**data)
        assert request.customer_id == 1
        assert request.title == "Engine Overhaul"

    def test_job_request_minimal(self):
        """Test job creation with minimal data (optional fields)."""
        data = {
            "customer_id": 1,
            "title": "Test Job"
        }
        request = JobCreateRequest(**data)
        assert request.customer_id == 1
        assert request.title == "Test Job"
        assert request.description is None
        assert request.status == "pending"  # default value
        assert request.priority == 2  # default: medium (0=none,1=low,2=medium,3=high,4=critical)


class TestMechanicCreateRequest:
    """Tests for MechanicCreateRequest model."""

    def test_valid_mechanic_request(self):
        """Test valid mechanic creation request."""
        data = {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "phone": "+1987654321",
            "specialties": ["Engine", "Avionics", "Structural"]
        }
        request = MechanicCreateRequest(**data)
        assert request.name == "Jane Smith"
        assert len(request.specialties) == 3

    def test_mechanic_request_minimal(self):
        """Test mechanic creation with minimal data."""
        data = {
            "name": "Jane Smith",
            "email": "jane@example.com"
        }
        request = MechanicCreateRequest(**data)
        assert request.name == "Jane Smith"
        assert request.email == "jane@example.com"
        assert request.phone is None
        assert request.specialties == []


class TestGraphQueryRequest:
    """Tests for GraphQueryRequest model."""

    def test_valid_graph_query(self):
        """Test valid graph query request."""
        data = {
            "query": "MATCH (n) RETURN n LIMIT 10"
        }
        request = GraphQueryRequest(**data)
        assert request.query == "MATCH (n) RETURN n LIMIT 10"

    def test_graph_query_with_params(self):
        """Test graph query with parameters."""
        data = {
            "query": "MATCH (n {id: $id}) RETURN n",
            "params": {"id": 123}
        }
        request = GraphQueryRequest(**data)
        assert request.query == "MATCH (n {id: $id}) RETURN n"
        assert request.params == {"id": 123}

    def test_graph_query_minimal(self):
        """Test graph query with minimal data."""
        data = {"query": "MATCH (n) RETURN n"}
        request = GraphQueryRequest(**data)
        assert request.query == "MATCH (n) RETURN n"
        assert request.params is None


class TestMultiTenantCreateRequest:
    """Tests for MultiTenantCreateRequest model."""

    def test_valid_tenant_request(self):
        """Test valid tenant creation request."""
        data = {
            "tenant_id": "tenant_001",
            "graph_name": "tenant_graph_001"
        }
        request = MultiTenantCreateRequest(**data)
        assert request.tenant_id == "tenant_001"

    def test_tenant_request_minimal(self):
        """Test tenant creation with minimal data."""
        data = {
            "tenant_id": "tenant_002"
        }
        request = MultiTenantCreateRequest(**data)
        assert request.tenant_id == "tenant_002"
        assert request.graph_name is None


class TestErrorResponse:
    """Tests for ErrorResponse model."""

    def test_error_response(self):
        """Test error response creation."""
        response = ErrorResponse(success=False, error="Test Error", details="Something went wrong")
        assert response.success is False
        assert response.error == "Test Error"
        assert response.details == "Something went wrong"


class TestSuccessResponse:
    """Tests for SuccessResponse model."""

    def test_success_response_default(self):
        """Test success response with defaults."""
        response = SuccessResponse(success=True)
        assert response.success is True
        assert response.message == ""

    def test_success_response_custom(self):
        """Test success response with custom message."""
        response = SuccessResponse(success=True, message="Operation completed")
        assert response.success is True
        assert response.message == "Operation completed"
