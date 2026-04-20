# SkyMechanics Redis Configuration

This directory contains Redis setup for caching and Pub/Sub.

## Docker Compose

```yaml
version: '3.8'
services:
  redis:
    image: redis:7-alpine
    container_name: skymechanics-redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes
    restart: unless-stopped

  redis-insight:
    image: redis/redisinsight:latest
    container_name: skymechanics-redis-insight
    ports:
      - "5540:5540"
    volumes:
      - redis-insight:/data
    depends_on:
      - redis
    restart: unless-stopped

volumes:
  redis-data:
  redis-insight:
```

## Usage

### Connect from services

```python
import redis
from functools import wraps

r = redis.Redis(host='redis', port=6379, db=0)

def cache_result(ttl=300):
    """Decorator for caching function results."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{str(args)}:{str(sorted(kwargs.items()))}"
            cached = r.get(cache_key)
            if cached:
                return json.loads(cached)
            result = func(*args, **kwargs)
            r.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator
```

## Cache Key Patterns

| Key Pattern | TTL | Content |
|-------------|-----|---------|
| `tenant:{id}` | 3600s | Tenant metadata |
| `mechanic:{id}` | 1800s | Mechanic profile |
| `job:{id}` | 900s | Active job status |
| `location:{id}` | 300s | Real-time location |
| `cache:stats` | 60s | Cache hit/miss stats |

## Redis Pub/Sub Channels

| Channel | Events |
|---------|--------|
| `mechanic:updates` | Location, availability changes |
| `job:status` | Created, started, completed, cancelled |
| `job:dispatch` | Assignment events |
