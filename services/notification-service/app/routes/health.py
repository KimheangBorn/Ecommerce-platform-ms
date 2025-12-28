from fastapi import APIRouter
import redis
from app.config import settings

router = APIRouter()

@router.get("/live")
async def liveness():
    return {"status": "UP"}

@router.get("/ready")
async def readiness():
    try:
        r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        r.ping()
        return {"status": "UP", "redis": "connected"}
    except Exception:
        return {"status": "DOWN", "error": "Redis disconnected"}, 503
