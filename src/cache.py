import json
import os
import redis

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)


def check_connection():
    try:
        redis_client.ping()
        return True
    except redis.ConnectionError:
        return False


def get_cache_data(key: str):
    try:

        cached_data = redis_client.get(key)

        if cached_data is None:
            return None

        return json.loads(cached_data)

    except redis.RedisError:
        return None


def set_cache_data(key: str, data, ttl: int = 60):
    try:
        redis_client.setex(key, ttl, json.dumps(data))
        
    except redis.RedisError:
        pass