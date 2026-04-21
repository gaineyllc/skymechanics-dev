# FAA Certification & Repairman System - Implementation Plan

## Overview

Build a robust reputation system for vetting and optimal job matching. The system will track:
- FAA certifications (A&P, IA, Repairman)
- Experience with aircraft types
- Performance metrics
- Customer reviews
- Compliance history

## Phase 1: Database Schema (30 min)

### 1.1 Extend Existing Models

**backend/models.py** - Add new models:

```python
from datetime import date
from enum import Enum
from typing import List, Optional

class CertificationType(str, Enum):
    A&P_MECHANIC = "A&P Mechanic"
    INSPECTION_AUTHORIZATION = "IA"
    REPAIRMAN_GENERAL = "Repairman (General)"
    REPAIRMAN_EXPERIMENTAL = "Repairman (Experimental)"
    REPAIRMAN_LIGHT_SPORT = "Repairman (Light-Sport)"

class RepairmanCertType(str, Enum):
    INSPECTION = "Inspection"
    MAINTENANCE = "Maintenance"

class RepairmanCategory(str, Enum):
    AIRPLANE = "Airplane"
    ROTORCRAFT = "Rotorcraft"
    GLIDER = "Glider"
    LIGHTER_THAN_AIR = "Lighter-than-air"
    POWERED_LIFT = "Powered-lift"
    POWERED_PARACHUTE = "Powered-parachute"
    WEIGHT_SHIFT_CONTROL = "Weight-shift-control"

class MechanicCertification(Base):
    __tablename__ = "mechanic_certifications"
    
    id = Column(Integer, primary_key=True)
    mechanic_id = Column(Integer, ForeignKey("mechanics.id"))
    certification_type = Column(Enum(CertificationType))
    license_number = Column(String)
    issue_date = Column(Date)
    expiry_date = Column(Date)
    status = Column(String, default="active")  # active, expired, suspended
    notes = Column(Text, nullable=True)
    
    # Relationships
    mechanic = relationship("Mechanic", back_populates="certifications")

class RepairmanCertificate(Base):
    __tablename__ = "repairman_certificates"
    
    id = Column(Integer, primary_key=True)
    mechanic_id = Column(Integer, ForeignKey("mechanics.id"))
    cert_type = Column(Enum(RepairmanCertType))
    rating = Column(String)
    category = Column(Enum(RepairmanCategory))
    aircraft_id = Column(Integer, ForeignKey("aircraft.id"), nullable=True)
    issue_date = Column(Date)
    expiry_date = Column(Date)
    training_provider = Column(String, nullable=True)
    course_number = Column(String, nullable=True)
    
    mechanic = relationship("Mechanic", back_populates="repairman_certs")
    aircraft = relationship("Aircraft", back_populates="repairman_certs")

class ExperienceRecord(Base):
    __tablename__ = "experience_records"
    
    id = Column(Integer, primary_key=True)
    mechanic_id = Column(Integer, ForeignKey("mechanics.id"))
    aircraft_id = Column(Integer, ForeignKey("aircraft.id"), nullable=True)
    aircraft_type_id = Column(Integer, ForeignKey("aircraft_types.id"), nullable=True)
    start_date = Column(Date)
    end_date = Column(Date, nullable=True)
    hours_flown = Column(Integer)
    description = Column(Text, nullable=True)
    proficiency_level = Column(String)  # novice, basic, intermediate, advanced, expert
    is_current = Column(Boolean, default=False)
    
    mechanic = relationship("Mechanic", back_populates="experience")
    aircraft = relationship("Aircraft", back_populates="experience")
    aircraft_type = relationship("AircraftType", back_populates="experience")
```

### 1.2 Add Endpoints

**backend/routes/mechanics.py** - Add:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas

router = APIRouter(prefix="/api/v1/mechanics", tags=["mechanics"])

@router.post("/{mechanic_id}/certifications", response_model=schemas.MechanicCertification)
def add_mechanic_certification(
    mechanic_id: int,
    cert: schemas.MechanicCertificationCreate,
    db: Session = Depends(get_db)
):
    # Add certification

@router.get("/{mechanic_id}/certifications", response_model=List[schemas.MechanicCertification])
def get_mechanic_certifications(mechanic_id: int, db: Session = Depends(get_db)):
    # Get certifications

@router.post("/{mechanic_id}/repairman-certs", response_model=schemas.RepairmanCertificate)
def add_repairman_certificate(
    mechanic_id: int,
    cert: schemas.RepairmanCertificateCreate,
    db: Session = Depends(get_db)
):
    # Add repairman cert

@router.get("/{mechanic_id}/repairman-certs", response_model=List[schemas.RepairmanCertificate])
def get_repairman_certificates(mechanic_id: int, db: Session = Depends(get_db)):
    # Get repairman certs

@router.post("/{mechanic_id}/experience", response_model=schemas.ExperienceRecord)
def add_experience_record(
    mechanic_id: int,
    exp: schemas.ExperienceRecordCreate,
    db: Session = Depends(get_db)
):
    # Add experience record

@router.get("/{mechanic_id}/experience", response_model=List[schemas.ExperienceRecord])
def get_experience_records(mechanic_id: int, db: Session = Depends(get_db)):
    # Get experience records
```

## Phase 2: Reputation Scoring Engine (45 min)

### 2.1 Scoring Algorithm

**backend/services/reputation.py**:

```python
from datetime import date, timedelta
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session
from .. import models

class ReputationScore:
    def __init__(self):
        self.points = 0
        self.components = {}
    
    def add_component(self, name: str, score: float, max_score: float = 100):
        percentage = (score / max_score) * 100 if max_score > 0 else 0
        self.points += percentage
        self.components[name] = {
            "score": score,
            "max": max_score,
            "percentage": percentage
        }

def calculate_reputation_score(
    db: Session, 
    mechanic_id: int, 
    as_of_date: Optional[date] = None
) -> ReputationScore:
    """
    Calculate comprehensive reputation score for a mechanic.
    Returns 0-100 scale.
    """
    if as_of_date is None:
        as_of_date = date.today()
    
    score = ReputationScore()
    
    # 1. Certification Status (25 points max)
    cert_points = _calculate_certification_score(db, mechanic_id, as_of_date)
    score.add_component("certifications", cert_points, 25)
    
    # 2. Experience Depth (20 points max)
    exp_points = _calculate_experience_score(db, mechanic_id, as_of_date)
    score.add_component("experience", exp_points, 20)
    
    # 3. Performance Metrics (30 points max)
    perf_points = _calculate_performance_score(db, mechanic_id)
    score.add_component("performance", perf_points, 30)
    
    # 4. Recent Activity (15 points max)
    recent_points = _calculate_recent_activity_score(db, mechanic_id, as_of_date)
    score.add_component("recent_activity", recent_points, 15)
    
    # 5. Compliance (10 points max)
    compliance_points = _calculate_compliance_score(db, mechanic_id)
    score.add_component("compliance", compliance_points, 10)
    
    return score

def _calculate_certification_score(
    db: Session, 
    mechanic_id: int, 
    as_of_date: date
) -> float:
    """Calculate points based on active certifications."""
    certs = db.query(models.MechanicCertification).filter(
        models.MechanicCertification.mechanic_id == mechanic_id,
        models.MechanicCertification.status == "active",
        models.MechanicCertification.expiry_date >= as_of_date
    ).all()
    
    points = 0
    for cert in certs:
        if cert.certification_type == "A&P Mechanic":
            points += 10
        elif cert.certification_type == "IA":
            points += 15
        elif cert.certification_type.startswith("Repairman"):
            points += 5
    
    return min(points, 25)

def _calculate_experience_score(
    db: Session, 
    mechanic_id: int, 
    as_of_date: date
) -> float:
    """Calculate points based on years active, aircraft types, specializations."""
    exp_records = db.query(models.ExperienceRecord).filter(
        models.ExperienceRecord.mechanic_id == mechanic_id,
        models.ExperienceRecord.is_current == True
    ).all()
    
    if not exp_records:
        return 0
    
    # Years active (0-10 points)
    years_active = 0
    for exp in exp_records:
        if exp.end_date:
            years = (exp.end_date - exp.start_date).days / 365
            years_active = max(years_active, years)
        else:
            years = (as_of_date - exp.start_date).days / 365
            years_active = max(years_active, years)
    
    years_points = min(years_active, 10)
    
    # Aircraft types (0-5 points)
    unique_aircraft_types = len(set(exp.aircraft_type_id for exp in exp_records if exp.aircraft_type_id))
    types_points = min(unique_aircraft_types, 5)
    
    # Specialized skills (0-5 points)
    advanced_exp = sum(1 for exp in exp_records if exp.proficiency_level == "expert")
    skills_points = min(advanced_exp, 5)
    
    return min(years_points + types_points + skills_points, 20)

def _calculate_performance_score(db: Session, mechanic_id: int) -> float:
    """Calculate points based on job completion, satisfaction, rework."""
    # TODO: Query jobs, reviews, and calculate metrics
    # This is a placeholder - implement with actual data
    return 0

def _calculate_recent_activity_score(
    db: Session, 
    mechanic_id: int, 
    as_of_date: date
) -> float:
    """Calculate points based on recent maintenance activity and training."""
    # TODO: Implement
    return 0

def _calculate_compliance_score(db: Session, mechanic_id: int) -> float:
    """Calculate points based on FAA compliance history."""
    # TODO: Implement
    return 0

def get_top_mechanics_for_job(
    db: Session,
    job_id: int,
    required_certifications: list = None,
    required_aircraft_types: list = None,
    limit: int = 5
) -> list:
    """
    Get top ranked mechanics for a specific job.
    Returns list of (mechanic, score, match_details) tuples.
    """
    # TODO: Implement job matching logic
    pass
```

## Phase 3: API Integration (30 min)

### 3.1 Add Reputation Endpoints

**backend/routes/mechanics.py**:

```python
from ..services.reputation import calculate_reputation_score, get_top_mechanics_for_job

@router.get("/{mechanic_id}/reputation")
def get_mechanic_reputation(
    mechanic_id: int,
    db: Session = Depends(get_db),
    as_of_date: Optional[date] = None
):
    """Get detailed reputation score for a mechanic."""
    score = calculate_reputation_score(db, mechanic_id, as_of_date)
    return {
        "total_score": score.points,
        "components": score.components,
        "grade": _calculate_grade(score.points),
        "rank": _calculate_rank(db, mechanic_id)
    }

@router.get("/reputation/top")
def get_top_reputable_mechanics(
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get top 10 mechanics by reputation score."""
    # Query all mechanics and sort by reputation
    pass

@router.get("/{mechanic_id}/matching-jobs")
def get_matching_jobs_for_mechanic(
    mechanic_id: int,
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get jobs matching this mechanic's certifications and experience."""
    # TODO: Implement job matching
    pass

def _calculate_grade(score: float) -> str:
    if score >= 90:
        return "A+"
    elif score >= 85:
        return "A"
    elif score >= 80:
        return "A-"
    elif score >= 75:
        return "B+"
    elif score >= 70:
        return "B"
    elif score >= 65:
        return "B-"
    elif score >= 60:
        return "C+"
    elif score >= 55:
        return "C"
    else:
        return "Below Minimum"
```

## Phase 4: Frontend Components (1 hour)

### 4.1 Mechanic Profile Page

**frontend/src/pages/MechanicProfile.tsx**:

```tsx
export function MechanicProfile({ mechanicId }: { mechanicId: number }) {
    const [mechanic, setMechanic] = useState(null);
    const [reputation, setReputation] = useState(null);
    const [certifications, setCertifications] = useState([]);
    const [experience, setExperience] = useState([]);
    
    useEffect(() => {
        loadMechanicData();
    }, [mechanicId]);
    
    const loadMechanicData = async () => {
        const [mechData, repData, certs, exp] = await Promise.all([
            fetchMechanic(mechanicId),
            fetchMechanicReputation(mechanicId),
            fetchCertifications(mechanicId),
            fetchExperience(mechanicId)
        ]);
        
        setMechanic(mechData);
        setReputation(repData);
        setCertifications(certs);
        setExperience(exp);
    };
    
    return (
        <ProfileContainer>
            <Header>
                <Avatar src={mechanic.avatar_url} />
                <Name>{mechanic.name}</Name>
                <ReputationBadge score={reputation.total_score} />
            </Header>
            
            <Grid>
                <CertificationsSection certifications={certifications} />
                <ExperienceSection experience={experience} />
                <ReputationDetails reputation={reputation} />
            </Grid>
        </ProfileContainer>
    );
}
```

### 4.2 Mechanic List with Reputation

**frontend/src/components/MechanicCard.tsx**:

```tsx
export function MechanicCard({ mechanic, reputation, onClick }: any) {
    return (
        <Card onClick={onClick}>
            <Header>
                <Avatar src={mechanic.avatar_url} />
                <Info>
                    <Name>{mechanic.name}</Name>
                    <ReputationBar score={reputation?.total_score} />
                    <Certifications>
                        {reputation?.components.certifications?.percentage >= 50 && (
                            <Badge>Valid Certs</Badge>
                        )}
                    </Certifications>
                </Info>
            </Header>
            
            <Details>
                <DetailItem icon="briefcase">
                    {mechanic.profile?.experience_years || 0} years
                </DetailItem>
                <DetailItem icon="plane">
                    {calculateAircraftTypes(mechanic.experience)}
                </DetailItem>
                <DetailItem icon="star">
                    {reputation?.components.performance?.percentage || 0}%
                </DetailItem>
            </Details>
        </Card>
    );
}
```

## Phase 5: Integration Testing (30 min)

### 5.1 Backend Tests

```python
# backend/tests/test_reputation.py
import pytest
from datetime import date, timedelta
from ..services.reputation import (
    calculate_reputation_score,
    _calculate_certification_score,
    _calculate_experience_score
)

def test_certification_score_active_ap():
    # Test active A&P certification
    pass

def test_certification_score_expired():
    # Test expired certification
    pass

def test_experience_score_basic():
    # Test basic experience calculation
    pass

def test_reputation_comprehensive():
    # Test full reputation calculation
    pass

def test_job_matching():
    # Test job-matching logic
    pass
```

### 5.2 Frontend Tests

```typescript
// frontend/src/components/__tests__/MechanicCard.test.tsx
describe("MechanicCard", () => {
    it("displays reputation score correctly", () => {
        // Test rendering with different score ranges
    });
    
    it("shows valid certifications badge", () => {
        // Test certification badge display
    });
});
```

## Timeline Summary

| Phase | Task | Time |
|-------|------|------|
| 1 | Database Schema | 30 min |
| 2 | Scoring Engine | 45 min |
| 3 | API Integration | 30 min |
| 4 | Frontend Components | 1 hour |
| 5 | Testing | 30 min |
| **Total** | | **4.5 hours** |

## Next Steps

1. Create database migration for new tables
2. Implement scoring algorithm
3. Build frontend components
4. Integration testing
5. Documentation
