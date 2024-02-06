from redis import asyncio as aioredis
from redis.asyncio import Redis

from config import settings

redis_client: Redis = aioredis.from_url(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}', encoding='utf-8',
                                        decode_responses=True)
