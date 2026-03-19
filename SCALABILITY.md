# 📈 Scalability Note

This document outlines the architectural strategies that make this system production-ready and horizontally scalable.

---

## Current Architecture

```
Client → FastAPI (Uvicorn) → MongoDB (Motor async)
```

All components are stateless (JWT auth) so they can be replicated immediately.

---

## Scaling Strategies

### 1. Horizontal Scaling + Load Balancing [IMPLEMENTED]
- FastAPI is **stateless** (JWT tokens, no server-side sessions)
- Use **Gunicorn with Uvicorn workers**: `gunicorn -c gunicorn_conf.py app.main:app`
- This allows the app to use multiple CPU cores by spawning multiple worker processes.


### 2. Database Scaling
- **MongoDB Replica Set**: automatic failover + read replicas for read-heavy workloads
- **MongoDB Atlas** for managed horizontal sharding
- Indexes already created on `email`, `username`, `owner_id`, `created_at` for query performance

### 3. Caching (Redis)
- Cache frequently read, rarely changed data (user profile, task lists)
- Use `redis-py` / `aioredis` with a cache-aside pattern
- Rate limiting via `slowapi` is **IMPLEMENTED** (limits brute-force on auth routes)


```python
# Example: cache user profile for 5 min
@router.get("/me")
async def me(current_user = Depends(get_current_active_user)):
    cache_key = f"user:{current_user['_id']}"
    cached = await redis.get(cache_key)
    if cached:
        return json.loads(cached)
    ...
```

### 4. Microservices Migration Path
The current modular structure makes decomposition straightforward:

| Module | Microservice |
|--------|-------------|
| `auth/` | Auth Service (OAuth2 / Keycloak) |
| `tasks/` | Tasks Service |
| `notifications/` | Notification Service (email, push) |

Each service communicates over **REST** or **message queues** (RabbitMQ / Kafka).

### 5. Async Task Queue
- Use **Celery + Redis** for background jobs (email sending, report generation)
- FastAPI's async nature already supports high concurrency without threading

### 6. Observability
- **Structured logging** with `structlog` or `loguru`
- **Metrics** with Prometheus + Grafana
- **Tracing** with OpenTelemetry

### 7. Docker & Container Orchestration
```yaml
# docker-compose.yml (add later)
services:
  api:
    build: ./backend
    replicas: 3
  mongodb:
    image: mongo:7
  nginx:
    image: nginx:alpine
```

Deploy to **Kubernetes** for auto-scaling based on CPU/request load.

---

## Summary

| Concern | Solution |
|---------|---------|
| API Concurrency | Async FastAPI + Uvicorn workers |
| Stateless Auth | JWT (no server sessions) |
| DB Performance | MongoDB indexes + sharding |
| Caching | Redis (cache-aside) |
| Rate Limiting | slowapi + Redis |
| Horizontal Scaling | Docker + Kubernetes / Cloud LB |
| Observability | Prometheus + OpenTelemetry |
| Decomposition | Modular routes/services → microservices |
