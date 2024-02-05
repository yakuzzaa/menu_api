import json
from typing import Any

from fastapi.encoders import jsonable_encoder

from database.redis import redis_client


class Cache:
    @classmethod
    async def get(cls, key: str) -> Any | None:
        data = await redis_client.get(name=key)
        if not data:
            return None
        return json.loads(data)

    @classmethod
    async def create(cls, key: str, value: Any) -> None:
        data = json.dumps(jsonable_encoder(value))
        await redis_client.set(name=key, value=data)

    # @classmethod
    # async def delete(cls, keys: list[str] | str) -> None:
    #     await redis_client.delete(*keys)

    @classmethod
    async def delete(cls, key: list[str] | str) -> None:
        keys = await redis_client.keys(f'{key}*')
        if keys:
            await redis_client.delete(*keys)
