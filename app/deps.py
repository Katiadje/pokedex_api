# app/deps.py
import os
import redis

def get_redis():
    url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    client = redis.Redis.from_url(url, decode_responses=True)
    return client
