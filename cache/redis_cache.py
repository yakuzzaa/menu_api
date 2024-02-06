import json
from typing import Any, Optional, Union

from fastapi.encoders import jsonable_encoder

from database.redis import redis_client

CacheReturnType = Optional[Union[dict[str, Any]]]


class Cache:
    @classmethod
    async def get(cls, key: str) -> CacheReturnType:
        data: Any = await redis_client.get(name=key)
        if not data:
            return None
        return json.loads(data)

    @classmethod
    async def create(cls, key: str, value: Any) -> None:
        data: str = json.dumps(jsonable_encoder(value))
        await redis_client.set(name=key, value=data)

    @classmethod
    async def delete(cls, key: list[str] | str) -> None:
        keys: list = await redis_client.keys(f'{key}*')
        if keys:
            await redis_client.delete(*keys)
