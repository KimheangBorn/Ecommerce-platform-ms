import redis
import json
from app.config import Config

redis_client = redis.Redis(
    host=Config.REDIS_HOST, 
    port=Config.REDIS_PORT, 
    db=Config.REDIS_DB, 
    decode_responses=True
)

def get_cache(key):
    try:
        val = redis_client.get(key)
        if val:
            return json.loads(val)
        return None
    except Exception:
        return None

def set_cache(key, value, ttl=3600):
    try:
        redis_client.setex(key, ttl, json.dumps(value))
    except Exception:
        pass

def delete_cache_pattern(pattern):
    try:
        for key in redis_client.scan_iter(pattern):
            redis_client.delete(key)
    except Exception:
        pass
