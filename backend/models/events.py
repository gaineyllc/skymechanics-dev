"""
Event models for Phase 1 WebSocket streaming.
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
from pydantic import BaseModel


class EventTypes:
    """Event type constants."""
    MECHANIC_LOCATION = "mechanic:location_updated"
    MECHANIC_STATUS = "mechanic:status_changed"
    MECHANIC_AVAILABILITY = "mechanic:availability_changed"
    JOB_STATUS = "job:status_changed"
    JOB_ASSIGNED = "job:assigned"
    JOB_COMPLETED = "job:completed"
    JOB_CANCELLED = "job:cancelled"
    GEOFENCE_ENTER = "geofence:enter"
    GEOFENCE_EXIT = "geofence:exit"


class EventMessage(BaseModel):
    """Base event message."""
    event_type: str
    payload: Dict[str, Any]
    timestamp: datetime


class LocationUpdate(BaseModel):
    """Location update event payload."""
    mechanic_id: int
    latitude: float
    longitude: float
    accuracy: Optional[float] = None
    timestamp: datetime


class StatusChange(BaseModel):
    """Status change event payload."""
    mechanic_id: Optional[int] = None
    job_id: Optional[int] = None
    old_status: str
    new_status: str
    timestamp: datetime


class AssignmentEvent(BaseModel):
    """Job assignment event payload."""
    job_id: int
    mechanic_id: int
    scheduled_start: Optional[datetime] = None
    scheduled_end: Optional[datetime] = None
    timestamp: datetime


class GeofenceEvent(BaseModel):
    """Geofence event payload."""
    entity_type: str  # "mechanic" or "job"
    entity_id: int
    geofence_name: str
    action: str  # "enter" or "exit"
    timestamp: datetime


class NotificationEvent(BaseModel):
    """Notification event payload."""
    title: str
    message: str
    priority: str = "info"  # info, warning, error
    timestamp: datetime
