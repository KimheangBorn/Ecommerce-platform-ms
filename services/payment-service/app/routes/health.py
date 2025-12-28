from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine
from app.config import settings
import redis

router = APIRouter()

@router.get("/live")
async def liveness():
    return {"status": "UP"}

@router.get("/ready")
async def readiness():
    # Check DB
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        return {"status": "DOWN", "error": "Database disconnected"}, 503

    # Check Redis
    try:
        r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        r.ping()
        redis_status = "connected"
    except Exception:
        return {"status": "DOWN", "error": "Redis disconnected"}, 503

    return {
        "status": "UP",
        "database": db_status,
        "redis": redis_status
    }
