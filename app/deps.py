# app/deps.py
import os
import redis
from typing import Optional

def get_redis() -> Optional[redis.Redis]:
    """Retourne un client Redis ou None si Redis n'est pas disponible"""
    try:
        url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        client = redis.Redis.from_url(url, decode_responses=True)
        # Test de connexion
        client.ping()
        return client
    except (redis.ConnectionError, redis.TimeoutError):
        # Redis non disponible, retourner None
        return None