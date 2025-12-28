import redis
from app.config import settings
import json

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)

def check_idempotency_key(key: str):
    val = redis_client.get(f"idempotency:{key}")
    if val:
        return json.loads(val)
    return None

def store_idempotency_response(key: str, response: dict):
    redis_client.setex(
        f"idempotency:{key}",
        86400, # 24 hours
        json.dumps(response, default=str)
    )
