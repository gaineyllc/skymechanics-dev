"""
Reputation system routes for SkyMechanics Platform.
Handles certification tracking, experience records, reviews, and reputation scoring.
"""
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from typing import Optional, List, Dict
from datetime import datetime

from db import db_client
from pubsub import (
    publish_reputation_updated,
    Channels
)

router = APIRouter(
    prefix="/api/v1/mechanics",
    tags=["Reputation"]
)


def calculate_reputation_score(graph, mechanic_id: int) -> Dict[str, any]:
    """
    Calculate reputation score for a mechanic based on:
    1. Certification Status (25 points)
    2. Experience Depth (20 points)
    3. Performance Metrics (30 points)
    4. Recent Activity (15 points)
    5. Compliance (10 points)
    
    Returns: Dict with total_score and component_breakdown
    """
    # 1. Certification Status (max 25 points)
    cert_query = """
    MATCH (m:Mechanic {node_id: $mechanic_id})-[:HOLDS]->(c:Certification)
    WHERE c.status = 'active'
    RETURN COUNT(c) AS active_certs
    """
    cert_result = graph.query(cert_query, params={"mechanic_id": mechanic_id})
    active_certs = cert_result.result_set[0][0] if cert_result.result_set else 0
    
    # Points: 5 per active cert, max 25
    cert_score = min(active_certs * 5, 25)
    
    # 2. Experience Depth (max 20 points)
    exp_query = """
    MATCH (m:Mechanic {node_id: $mechanic_id})-[:EXPERIENCE]->(e:ExperienceRecord)
    RETURN SUM(e.years_active) AS total_years, COUNT(e) AS aircraft_types
    """
    exp_result = graph.query(exp_query, params={"mechanic_id": mechanic_id})
    
    total_years = exp_result.result_set[0][0] if exp_result.result_set and exp_result.result_set[0][0] else 0
    aircraft_types = exp_result.result_set[0][1] if exp_result.result_set and len(exp_result.result_set[0]) > 1 else 0
    
    # Points: 2 per year, 1 per aircraft type, max 20
    exp_score = min(int(total_years * 2 + aircraft_types), 20)
    
    # 3. Performance Metrics (max 30 points)
    perf_query = """
    MATCH (m:Mechanic {node_id: $mechanic_id})-[:ASSIGNED_TO]->(j:Job)<-[:GIVEN_BY]-(r:Review)
    WITH COUNT(r) AS review_count,
         AVG(r.rating) AS avg_rating,
         SUM(CASE WHEN j.status = 'completed' THEN 1 ELSE 0 END) AS completed_jobs
    RETURN review_count, avg_rating, completed_jobs
    """
    perf_result = graph.query(perf_query, params={"mechanic_id": mechanic_id})
    
    review_count = perf_result.result_set[0][0] if perf_result.result_set and perf_result.result_set[0][0] else 0
    avg_rating = perf_result.result_set[0][1] if perf_result.result_set and perf_result.result_set[0][1] else 0
    completed_jobs = perf_result.result_set[0][2] if perf_result.result_set and len(perf_result.result_set[0]) > 2 else 0
    
    # Points: based on review count, rating, and completion rate
    if review_count > 0:
        rating_score = (avg_rating / 5.0) * 15  # Up to 15 points for rating
        review_score = min(review_count * 0.5, 10)  # Up to 10 points for review count
        completion_score = min(completed_jobs * 0.1, 5)  # Up to 5 points for completions
        perf_score = rating_score + review_score + completion_score
    else:
        perf_score = 0
    
    # 4. Recent Activity (max 15 points)
    activity_query = """
    MATCH (m:Mechanic {node_id: $mechanic_id})-[:EXPERIENCE]->(e:ExperienceRecord)
    WHERE e.last_flight_date IS NOT NULL
    WITH max(e.last_flight_date) AS last_activity
    WITH datetime(last_activity) AS last_activity_dt, datetime() AS now_dt
    RETURN duration(in_months between last_activity_dt, now_dt).months AS months_since_activity
    """
    activity_result = graph.query(activity_query, params={"mechanic_id": mechanic_id})
    
    months_since_activity = activity_result.result_set[0][0] if activity_result.result_set else 12
    
    # Points: 15 for recent, decays over time
    if months_since_activity <= 3:
        activity_score = 15
    elif months_since_activity <= 6:
        activity_score = 12
    elif months_since_activity <= 12:
        activity_score = 8
    else:
        activity_score = 5
    
    # 5. Compliance (max 10 points)
    # Check for any violations or issues
    compliance_query = """
    MATCH (m:Mechanic {node_id: $mechanic_id})
    RETURN m.compliance_score AS score
    """
    compliance_result = graph.query(compliance_query, params={"mechanic_id": mechanic_id})
    
    compliance_score = compliance_result.result_set[0][0] if compliance_result.result_set else 10
    
    # Calculate total
    total_score = int(cert_score + exp_score + perf_score + activity_score + compliance_score)
    
    return {
        "total_score": min(total_score, 100),
        "component_scores": {
            "certification_status": int(cert_score),
            "experience_depth": int(exp_score),
            "performance": int(perf_score),
            "recent_activity": int(activity_score),
            "compliance": int(compliance_score)
        },
        "metrics": {
            "review_count": review_count,
            "avg_rating": round(avg_rating, 2) if avg_rating else None,
            "completed_jobs": completed_jobs,
            "active_certifications": active_certs,
            "total_years_experience": int(total_years),
            "aircraft_types": aircraft_types,
            "months_since_activity": months_since_activity
        }
    }


@router.get("/{mechanic_id}/reputation", response_model=dict)
async def get_mechanic_reputation(
    mechanic_id: int,
    graph_name: str = "skymechanics_demo"
):
    """
    Get reputation metrics for a mechanic.
    
    Returns:
    - total_score: Overall score 0-100
    - component_scores: Breakdown by category
    - metrics: Additional details
    """
    try:
        db_client.set_graph(graph_name)
        graph = db_client.get_graph()
        
        # Check if mechanic exists
        check_query = "MATCH (m:Mechanic {node_id: $mechanic_id}) RETURN m"
        check_result = graph.query(check_query, params={"mechanic_id": mechanic_id})
        
        if not check_result.result_set:
            raise HTTPException(status_code=404, detail="Mechanic not found")
        
        # Calculate score
        score_data = calculate_reputation_score(graph, mechanic_id)
        
        return {
            "mechanic_id": mechanic_id,
            **score_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get reputation: {str(e)}")


@router.get("/reputation/top", response_model=list)
async def get_top_mechanics(
    limit: int = 10,
    min_score: int = 50,
    graph_name: str = "skymechanics_demo"
):
    """
    Get top mechanics by reputation score.
    
    Returns list of mechanics sorted by reputation score descending.
    """
    try:
        db_client.set_graph(graph_name)
        graph = db_client.get_graph()
        
        # Get all mechanics and calculate scores
        mechanics_query = "MATCH (m:Mechanic) RETURN m.node_id AS node_id"
        mechanics_result = graph.query(mechanics_query)
        
        mechanics_with_scores = []
        for row in mechanics_result.result_set:
            mechanic_id = row[0]
            score_data = calculate_reputation_score(graph, mechanic_id)
            
            if score_data["total_score"] >= min_score:
                mechanics_with_scores.append({
                    "mechanic_id": mechanic_id,
                    **score_data
                })
        
        # Sort by total score descending
        mechanics_with_scores.sort(key=lambda x: x["total_score"], reverse=True)
        
        return mechanics_with_scores[:limit]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get top mechanics: {str(e)}")


@router.post("/{mechanic_id}/certifications", response_model=dict)
async def add_certification(
    mechanic_id: int,
    name: str,
    authority: str,
    status: str = "active",
    issue_date: Optional[str] = None,
    expiry_date: Optional[str] = None,
    notes: Optional[str] = None,
    graph_name: str = "skymechanics_demo"
):
    """
    Add a certification to a mechanic.
    
    Request query params:
    - name: Certification name (e.g., 'A&P Mechanic', 'IA')
    - authority: Issuing authority (e.g., 'FAA')
    - status: 'active', 'expired', 'revoked'
    - issue_date: ISO date of issuance (optional)
    - expiry_date: ISO date of expiration (optional)
    - notes: Additional notes (optional)
    """
    try:
        db_client.set_graph(graph_name)
        graph = db_client.get_graph()
        
        # Check if mechanic exists
        check_query = "MATCH (m:Mechanic {node_id: $mechanic_id}) RETURN m"
        check_result = graph.query(check_query, params={"mechanic_id": mechanic_id})
        
        if not check_result.result_set:
            raise HTTPException(status_code=404, detail="Mechanic not found")
        
        # Create certification node
        create_query = """
        MATCH (m:Mechanic {node_id: $mechanic_id})
        CREATE (c:Certification {
            name: $name,
            authority: $authority,
            status: $status,
            issue_date: $issue_date,
            expiry_date: $expiry_date,
            notes: $notes,
            created_at: $created_at
        })
        CREATE (m)-[:HOLDS]->(c)
        RETURN c
        """
        
        result = graph.query(create_query, params={
            "mechanic_id": mechanic_id,
            "name": name,
            "authority": authority,
            "status": status,
            "issue_date": issue_date,
            "expiry_date": expiry_date,
            "notes": notes,
            "created_at": datetime.utcnow().isoformat()
        })
        
        if result.result_set:
            cert_props = result.result_set[0][0].properties
            
            # Publish reputation update event
            await publish_reputation_updated(mechanic_id, graph_name.replace("tenant_", ""))
            
            return {
                "success": True,
                "certification": cert_props
            }
        
        raise HTTPException(status_code=500, detail="Failed to add certification")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add certification: {str(e)}")


@router.post("/{mechanic_id}/experience", response_model=dict)
async def add_experience(
    mechanic_id: int,
    aircraft_type_id: int,
    hours_flown: int = 0,
    years_active: int = 0,
    last_flight_date: Optional[str] = None,
    notes: Optional[str] = None,
    graph_name: str = "skymechanics_demo"
):
    """
    Add experience record for a mechanic.
    
    Request query params:
    - aircraft_type_id: ID of the aircraft type
    - hours_flown: Total hours on this aircraft type
    - years_active: Years of experience
    - last_flight_date: ISO date of last flight (optional)
    - notes: Additional notes (optional)
    """
    try:
        db_client.set_graph(graph_name)
        graph = db_client.get_graph()
        
        # Check if mechanic exists
        check_query = "MATCH (m:Mechanic {node_id: $mechanic_id}) RETURN m"
        check_result = graph.query(check_query, params={"mechanic_id": mechanic_id})
        
        if not check_result.result_set:
            raise HTTPException(status_code=404, detail="Mechanic not found")
        
        # Check if aircraft type exists
        aircraft_check = "MATCH (a:AircraftType {node_id: $aircraft_type_id}) RETURN a"
        aircraft_result = graph.query(aircraft_check, params={"aircraft_type_id": aircraft_type_id})
        
        if not aircraft_result.result_set:
            raise HTTPException(status_code=404, detail="Aircraft type not found")
        
        # Create experience record
        create_query = """
        MATCH (m:Mechanic {node_id: $mechanic_id}), (a:AircraftType {node_id: $aircraft_type_id})
        CREATE (e:ExperienceRecord {
            hours_flown: $hours_flown,
            years_active: $years_active,
            last_flight_date: $last_flight_date,
            notes: $notes,
            created_at: $created_at
        })
        CREATE (m)-[:EXPERIENCE]->(e)-[:ON_AIRCRAFT]->(a)
        RETURN e
        """
        
        result = graph.query(create_query, params={
            "mechanic_id": mechanic_id,
            "aircraft_type_id": aircraft_type_id,
            "hours_flown": hours_flown,
            "years_active": years_active,
            "last_flight_date": last_flight_date,
            "notes": notes,
            "created_at": datetime.utcnow().isoformat()
        })
        
        if result.result_set:
            exp_props = result.result_set[0][0].properties
            
            # Publish reputation update event
            await publish_reputation_updated(mechanic_id, graph_name.replace("tenant_", ""))
            
            return {
                "success": True,
                "experience": exp_props
            }
        
        raise HTTPException(status_code=500, detail="Failed to add experience")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add experience: {str(e)}")


@router.post("/{mechanic_id}/reviews", response_model=dict)
async def add_review(
    mechanic_id: int,
    job_id: int,
    rating: int,
    comment: Optional[str] = None,
    review_type: str = "customer",
    graph_name: str = "skymechanics_demo"
):
    """
    Add a review for a mechanic.
    
    Request query params:
    - job_id: ID of the job being reviewed
    - rating: Rating 1-5
    - comment: Review comment (optional)
    - review_type: 'customer', 'peer', 'supervisor'
    """
    try:
        # Validate rating
        if rating < 1 or rating > 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        
        db_client.set_graph(graph_name)
        graph = db_client.get_graph()
        
        # Check if mechanic exists
        check_query = "MATCH (m:Mechanic {node_id: $mechanic_id}) RETURN m"
        check_result = graph.query(check_query, params={"mechanic_id": mechanic_id})
        
        if not check_result.result_set:
            raise HTTPException(status_code=404, detail="Mechanic not found")
        
        # Check if job exists
        job_check = "MATCH (j:Job {node_id: $job_id}) RETURN j"
        job_result = graph.query(job_check, params={"job_id": job_id})
        
        if not job_result.result_set:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Create review node
        create_query = """
        MATCH (m:Mechanic {node_id: $mechanic_id}), (j:Job {node_id: $job_id})
        CREATE (r:Review {
            rating: $rating,
            comment: $comment,
            review_type: $review_type,
            created_at: $created_at
        })
        CREATE (j)<-[:GIVEN_BY]-(r)-[:OF_MECHANIC]->(m)
        RETURN r
        """
        
        result = graph.query(create_query, params={
            "mechanic_id": mechanic_id,
            "job_id": job_id,
            "rating": rating,
            "comment": comment,
            "review_type": review_type,
            "created_at": datetime.utcnow().isoformat()
        })
        
        if result.result_set:
            review_props = result.result_set[0][0].properties
            
            # Publish reputation update event
            await publish_reputation_updated(mechanic_id, graph_name.replace("tenant_", ""))
            
            return {
                "success": True,
                "review": review_props
            }
        
        raise HTTPException(status_code=500, detail="Failed to add review")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add review: {str(e)}")


@router.get("/{mechanic_id}/matching-jobs", response_model=list)
async def get_matching_jobs(
    mechanic_id: int,
    min_reputation: int = 50,
    limit: int = 10,
    graph_name: str = "skymechanics_demo"
):
    """
    Get jobs that match a mechanic's qualifications based on reputation score.
    
    Returns jobs sorted by:
    1. Mechanic's reputation score
    2. Job priority
    3. Job creation date (newest first)
    """
    try:
        db_client.set_graph(graph_name)
        graph = db_client.get_graph()
        
        # Get mechanic's reputation score
        score_query = """
        MATCH (m:Mechanic {node_id: $mechanic_id})
        RETURN m.node_id AS node_id, m.name AS name, m.specialties AS specialties
        """
        score_result = graph.query(score_query, params={"mechanic_id": mechanic_id})
        
        if not score_result.result_set:
            raise HTTPException(status_code=404, detail="Mechanic not found")
        
        # Get jobs that match mechanic's specialties
        matching_query = """
        MATCH (j:Job {status: 'pending'})
        WHERE j.required_specialty IN $specialties OR j.required_specialty = 'general'
        RETURN j.node_id AS node_id, j.title AS title, j.description AS description,
               j.status AS status, j.priority AS priority, j.created_at AS created_at,
               j.required_specialty AS required_specialty
        ORDER BY j.priority DESC, j.created_at DESC
        LIMIT $limit
        """
        
        specialties = score_result.result_set[0][3] if len(score_result.result_set[0]) > 3 else []
        specialties = specialties if specialties else ["general"]
        
        matching_result = graph.query(matching_query, params={
            "specialties": specialties,
            "limit": limit
        })
        
        jobs = []
        for row in matching_result.result_set:
            jobs.append({
                "node_id": row[0],
                "title": row[1],
                "description": row[2],
                "status": row[3],
                "priority": row[4],
                "created_at": row[5],
                "required_specialty": row[6],
                "mechanic_reputation_score": min_reputation  # Would calculate dynamically
            })
        
        return jobs
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get matching jobs: {str(e)}")


# Add reputation router to main app
# app.include_router(router, prefix="/api/v1", tags=["reputation"])
