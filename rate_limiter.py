# backend/app/rate_limiter.py
import redis
import os
import hashlib
import json
from datetime import timedelta

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
r = redis.from_url(redis_url)

FREE_LIMIT = int(os.getenv("FREE_LIMIT", 5))  # per day

def allow_request(telegram_id: str) -> bool:
    """
    Free tier limiter: allow up to FREE_LIMIT requests per day per user
    """
    key = f"user:{telegram_id}:requests"
    current = r.get(key)
    if current is None:
        r.setex(key, timedelta(days=1), 1)
        return True
    elif int(current) < FREE_LIMIT:
        r.incr(key)
        return True
    else:
        return False

def make_cache_key(title: str) -> str:
    return "cache:" + hashlib.sha256(title.encode()).hexdigest()

def cache_result(title: str, result: dict, ttl: int = 3600):
    key = make_cache_key(title)
    r.setex(key, ttl, json.dumps(result))

def get_cached_result(title: str):
    key = make_cache_key(title)
    data = r.get(key)
    if data:
        return json.loads(data)
    return None
