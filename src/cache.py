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