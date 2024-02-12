from typing import Any

from fastapi import BackgroundTasks

from cache.redis_cache import Cache


async def create_background_task(key: str, value: Any, background_tasks: BackgroundTasks) -> None:
    background_tasks.add_task(Cache.create, key, value)


async def delete_background_task(key: str | list, background_tasks: BackgroundTasks) -> None:
    background_tasks.add_task(Cache.delete, key)
