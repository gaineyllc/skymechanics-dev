"""Analytics data models for SkyMechanics Platform."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class FleetMetrics(BaseModel):
    """Fleet utilization metrics."""
    total_aircraft: int
    in_service: int
    under_maintenance: int
    utilization_rate: float
    timestamp: datetime


class MechanicMetrics(BaseModel):
    """Mechanic workload metrics."""
    total_mechanics: int
    active_today: int
    jobs_completed_today: int
    avg_jobs_per_mechanic: float
    timestamp: datetime


class RevenueMetrics(BaseModel):
    """Revenue tracking metrics."""
    today_revenue: float
    yesterday_revenue: float
    month_to_date: float
    year_to_date: float
    timestamp: datetime


class JobFact(BaseModel):
    """Jobs fact table record."""
    job_id: str
    tenant_id: str
    mechanic_id: int
    aircraft_id: int
    status: str
    duration_minutes: int
    revenue: float
    created_at: datetime
    completed_at: datetime


class MechanicAggregate(BaseModel):
    """Mechanic metrics aggregate record."""
    mechanic_id: int
    date: str
    jobs_completed: int
    total_hours: float
    avg_rating: float
