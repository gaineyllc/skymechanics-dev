"""
Redis cache utility module.
Provides caching layer for production performance.
"""
from typing import Optional, Any
from datetime import timedelta
import json
import hashlib

from db import get_redis_cache


class CacheClient:
    """Redis cache client with utility methods."""
    
    def __init__(self):
        self._client = None
    
    async def connect(self):
        """Connect to Redis cache."""
        self._client = await get_redis_cache().connect()
        return self
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if not self._client:
            return None
        try:
            value = await self._client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception:
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL (default 1 hour)."""
        if not self._client:
            return False
        try:
            await self._client.setex(
                key,
                ttl,
                json.dumps(value)
            )
            return True
        except Exception:
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache."""
        if not self._client:
            return False
        try:
            await self._client.delete(key)
            return True
        except Exception:
            return False
    
    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern."""
        if not self._client:
            return 0
        try:
            keys = await self._client.keys(pattern)
            if keys:
                return await self._client.delete(*keys)
            return 0
        except Exception:
            return 0
    
    async def close(self):
        """Close connection."""
        if self._client:
            await self._client.close()
            self._client = None


# Global cache client instance
cache_client = CacheClient()


def generate_cache_key(prefix: str, *args, **kwargs) -> str:
    """Generate a cache key from arguments."""
    key_data = {
        "prefix": prefix,
        "args": args,
        "kwargs": kwargs
    }
    key_string = json.dumps(key_data, sort_keys=True)
    key_hash = hashlib.md5(key_string.encode()).hexdigest()[:16]
    return f"{prefix}:{key_hash}"


def generate_tenant_cache_key(tenant_id: str, operation: str, *args) -> str:
    """Generate a tenant-specific cache key."""
    return generate_cache_key(f"tenant:{tenant_id}", operation, *args)


def generate_mechanic_cache_key(mechanic_id: int, operation: str) -> str:
    """Generate a mechanic-specific cache key."""
    return generate_cache_key("mechanic", mechanic_id, operation)


def generate_job_cache_key(job_id: int, operation: str) -> str:
    """Generate a job-specific cache key."""
    return generate_cache_key("job", job_id, operation)


def generate_customer_cache_key(customer_id: int, operation: str) -> str:
    """Generate a customer-specific cache key."""
    return generate_cache_key("customer", customer_id, operation)


# Cache TTL constants
CACHE_TTL = {
    "short": 60,           # 1 minute
    "medium": 300,         # 5 minutes
    "long": 3600,          # 1 hour
    "day": 86400,          # 24 hours
    "week": 604800,        # 7 days
}

# Cache patterns
PATTERN = {
    "tenant_all": "tenant:*:all",
    "mechanic_all": "mechanic:*:all",
    "job_all": "job:*:all",
    "customer_all": "customer:*:all",
    "reputation": "reputation:*",
    "matching": "matching:*",
}
