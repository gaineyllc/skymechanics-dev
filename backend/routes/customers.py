"""
Customers routes for SkyMechanics Platform.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import ValidationError
from typing import Optional, Dict

from models import (
    CustomerCreateRequest,
    CustomerResponse,
    CustomerUpdateRequest,
    CustomersResponse,
    SuccessResponse
)

from db import get_db_settings, FalkorDBClient

router = APIRouter(
    prefix="/api/v1/customers",
    tags=["Customers"]
)


@router.get("", response_model=CustomersResponse)
async def list_customers():
    """List all customers."""
    try:
        db_settings = get_db_settings()
        client = FalkorDBClient(host=db_settings.host, port=db_settings.port, password=db_settings.password)
        graph = client.get_graph("skymechanics")
        
        query = """
        MATCH (c:Customer)
        RETURN c {
            .customer_id,
            .name,
            .email,
            .phone,
            .address,
            .created_at
        } as customer
        ORDER BY c.created_at DESC
        """
        result = graph.query(query)
        
        customers = []
        for record in result.result_set:
            customers.append(record[0])
        
        return CustomersResponse(customers=customers, total=len(customers))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list customers: {str(e)}")


@router.post("", response_model=CustomerResponse)
async def create_customer(request: CustomerCreateRequest):
    """Create a new customer."""
    try:
        db_settings = get_db_settings()
        client = FalkorDBClient(host=db_settings.host, port=db_settings.port, password=db_settings.password)
        graph = client.get_graph("skymechanics")
        
        query = """
        CREATE (c:Customer {
            customer_id: $customer_id,
            name: $name,
            email: $email,
            phone: $phone,
            address: $address,
            created_at: timestamp()
        })
        RETURN c {
            .customer_id,
            .name,
            .email,
            .phone,
            .address,
            .created_at
        } as customer
        """
        result = graph.query(query, {
            "customer_id": request.customer_id,
            "name": request.name,
            "email": request.email,
            "phone": request.phone,
            "address": request.address
        })
        
        customer = result.result_set[0][0]
        return CustomerResponse(**customer)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create customer: {str(e)}")


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: str):
    """Get a specific customer by ID."""
    try:
        db_settings = get_db_settings()
        client = FalkorDBClient(host=db_settings.host, port=db_settings.port, password=db_settings.password)
        graph = client.get_graph("skymechanics")
        
        query = """
        MATCH (c:Customer {customer_id: $customer_id})
        RETURN c {
            .customer_id,
            .name,
            .email,
            .phone,
            .address,
            .created_at
        } as customer
        """
        result = graph.query(query, {"customer_id": customer_id})
        
        if not result.result_set:
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
        
        customer = result.result_set[0][0]
        return CustomerResponse(**customer)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get customer: {str(e)}")


@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(customer_id: str, request: CustomerUpdateRequest):
    """Update an existing customer."""
    try:
        db_settings = get_db_settings()
        client = FalkorDBClient(host=db_settings.host, port=db_settings.port, password=db_settings.password)
        graph = client.get_graph("skymechanics")
        
        # Build dynamic update query
        updates = []
        params = {"customer_id": customer_id}
        
        if request.name:
            updates.append("c.name = $name")
            params["name"] = request.name
        if request.email:
            updates.append("c.email = $email")
            params["email"] = request.email
        if request.phone:
            updates.append("c.phone = $phone")
            params["phone"] = request.phone
        if request.address is not None:
            updates.append("c.address = $address")
            params["address"] = request.address
        
        if not updates:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        query = f"""
        MATCH (c:Customer {customer_id: $customer_id})
        SET {', '.join(updates)}
        RETURN c {{
            .customer_id,
            .name,
            .email,
            .phone,
            .address,
            .created_at
        }} as customer
        """
        result = graph.query(query, params)
        
        if not result.result_set:
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
        
        customer = result.result_set[0][0]
        return CustomerResponse(**customer)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update customer: {str(e)}")


@router.delete("/{customer_id}", response_model=SuccessResponse)
async def delete_customer(customer_id: str):
    """Delete a customer."""
    try:
        db_settings = get_db_settings()
        client = FalkorDBClient(host=db_settings.host, port=db_settings.port, password=db_settings.password)
        graph = client.get_graph("skymechanics")
        
        # Check if customer exists and has jobs
        check_query = """
        MATCH (c:Customer {customer_id: $customer_id})
        OPTIONAL MATCH (c)-[:HAS_JOB]->(j:Job)
        RETURN c, count(j) as job_count
        """
        result = graph.query(check_query, {"customer_id": customer_id})
        
        if not result.result_set:
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")
        
        if result.result_set[0][1] > 0:
            raise HTTPException(status_code=400, detail="Cannot delete customer with existing jobs")
        
        # Delete customer
        query = """
        MATCH (c:Customer {customer_id: $customer_id})
        DETACH DELETE c
        RETURN 'deleted' as status
        """
        graph.query(query, {"customer_id": customer_id})
        
        return SuccessResponse(success=True, message=f"Customer {customer_id} deleted successfully")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete customer: {str(e)}")
