# Mechanic Onboarding UX - Complete

## Overview

This document describes the complete mechanic onboarding experience for the SkyMechanics Platform.

## Features Implemented

### Backend (`/backend/routes/mechanics.py`)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/mechanics` | GET | List all mechanics |
| `/api/v1/mechanics` | POST | Create a new mechanic with basic info |
| `/api/v1/mechanics/{id}` | GET | Get mechanic with full profile |
| `/api/v1/mechanics/{id}/profile` | POST | Update/create mechanic profile |

### Frontend Components

| Component | Location | Description |
|-----------|----------|-------------|
| `Mechanics.tsx` | `frontend/src/pages/` | Main mechanics listing page |
| `CreateMechanicModal.tsx` | `frontend/src/components/` | Multi-step modal for creating mechanics |
| `MechanicsDetailModal.tsx` | `frontend/src/components/` | Modal for viewing mechanic details |

## User Flow

### 1. Create Mechanic (Two-Step Process)

**Step 1: Basic Information**
- Name
- Email (required)
- Phone (optional)

**Step 2: Profile Details** (optional)
- License Number
- Certifications / Specialties (comma-separated)
- Availability (JSON format)
- Current Location (GPS coordinates)

### 2. View Mechanic Details

Click "View Details" on any mechanic card to see:
- Basic information
- Certifications (shown as badges)
- Full profile details (license, availability, location)
- System information (node ID, label)

## Data Models

### Mechanic Interface

```typescript
interface Mechanic {
  node_id: number
  label: string
  properties: {
    name: string
    email: string
    phone: string
    specialties: string[]
  }
  profile?: {
    license_number: string
    certifications: string[]
    availability: Record<string, any>
    current_location: { lat: number; lng: number }
    created_at: string
    updated_at: string
  }
}
```

## API Request Examples

### Create Mechanic

```bash
curl -X POST http://localhost:8080/api/v1/mechanics \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "555-1234",
    "specialties": ["IA", "A&P"]
  }'
```

### Update Mechanic Profile

```bash
curl -X POST http://localhost:8080/api/v1/mechanics/123/profile \
  -H "Content-Type: application/json" \
  -d '{
    "license_number": "FAA-2345678",
    "certifications": ["IA", "A&P", "Powerplant"],
    "availability": {
      "monday": "08:00-17:00",
      "tuesday": "08:00-17:00"
    },
    "current_location": {
      "lat": 40.7128,
      "lng": -74.0060
    }
  }'
```

## Graph Database Schema

### Nodes

- `:Mechanic` - Main mechanic entity
- `:User` - Authentication user
- `:MechanicProfile` - Extended profile information

### Relationships

- `(User)-[:HAS_PROFILE]->(MechanicProfile)` - Links user to profile

## Next Steps (Optional)

- [ ] Add edit functionality for existing mechanics
- [ ] Implement bulk import
- [ ] Add image upload for mechanic profiles
- [ ] Integrate with workflow builder
- [ ] Add mobile app support
