# Routes package
from .onboarding import router as onboarding_router
from .customers import router as customers_router
from .mechanics import router as mechanics_router
from .jobs import router as jobs_router
from .users import router as users_router
from .health import router as health_router

__all__ = ['onboarding_router', 'customers_router', 'mechanics_router', 'jobs_router', 'users_router', 'health_router']
