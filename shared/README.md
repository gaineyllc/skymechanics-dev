# SkyMechanics Shared Models Package

This package contains Pydantic models used across multiple microservices.

## Usage

```python
from shared.models import UserCreateRequest, MechanicResponse, JobCreateRequest
```

## Models

### Auth Service Models
- `UserCreateRequest` - User registration
- `UserResponse` - User data
- `TokenResponse` - JWT tokens
- `LoginRequest` - Login credentials

### Mechanic Service Models
- `MechanicCreateRequest` - Create mechanic
- `MechanicResponse` - Mechanic data
- `MechanicUpdateRequest` - Update mechanic

### Jobs Service Models
- `JobCreateRequest` - Create job
- `JobUpdateRequest` - Update job
- `JobResponse` - Job data
- `JobStatusRequest` - Status change

### Customer Service Models
- `CustomerCreateRequest` - Create customer
- `CustomerResponse` - Customer data
- `CustomerUpdateRequest` - Update customer

### Common Models
- `SuccessResponse` - Standard success
- `ErrorResponse` - Standard error
- `PaginatedResponse` - Pagination wrapper
