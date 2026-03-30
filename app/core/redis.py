import redis.asyncio as aioredis
from app.core.config import settings

# Create an asynchronous Redis connection pool
# decode_responses=True ensures we get Python strings back instead of raw bytes
redis_client = aioredis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",
    decode_responses=True
)