import uuid
from typing import Any

from fastapi import BackgroundTasks, HTTPException
from pydantic import UUID4

from cache.background_tasks import create_background_task, delete_background_task
from cache.redis_cache import Cache, CacheReturnType
from database.models import Submenu
from repository.menu import MenuRepository
from repository.submenu import SubmenuRepository


class SubmenuServices:

    def __init__(self, background_tasks: BackgroundTasks = None):
        self.background_tasks = background_tasks

    async def find_all(self, menu_id: UUID4) -> list[Submenu] | list[dict[str, Any]] | dict[str, Any]:
        key: str = f'submenu_list_{menu_id}'
        cache_submenus: CacheReturnType = await Cache.get(key)
        if cache_submenus:
            return cache_submenus

        submenus: list[Submenu] = await SubmenuRepository.read(menu_id)
        submenu_list: list = []
        if not submenus:
            return submenus
        for submenu in submenus:
            item: Submenu = submenu[0]
            item.dishes_count = submenu[1]
            submenu_list.append(item)
        await create_background_task(key=key, value=submenu_list, background_tasks=self.background_tasks)
        return submenu_list

    async def find_by_id(self, menu_id: UUID4, target_id: UUID4) -> Submenu | dict[str, Any]:
        key: str = f'submenu_{menu_id}_{target_id}'
        cache_submenu: CacheReturnType = await Cache.get(key)
        if cache_submenu:
            return cache_submenu

        submenu: Submenu = await SubmenuRepository.read_by_id(menu_id, target_id)
        if not submenu:
            raise HTTPException(status_code=404, detail='submenu not found')
        result_submenu: Submenu = submenu[0]
        result_submenu.dishes_count = submenu[1]
        await create_background_task(key=key, value=result_submenu, background_tasks=self.background_tasks)
        return result_submenu

    async def add(self, menu_id, submenu) -> dict[str, Any]:
        key: list[str] = [f'menu_{menu_id}', 'menu_list', f'submenu_list_{menu_id}', 'full_menu_info']
        if not await MenuRepository.check_object_exists(target_id=menu_id):
            raise HTTPException(404, 'Menu not found')
        submenu_dump: dict[str, Any] = submenu.model_dump()
        submenu_dump['menu_id'] = menu_id
        submenu_dump['id'] = uuid.uuid4()
        await SubmenuRepository.create(**submenu_dump)
        submenu_dump['dishes_count'] = 0
        await delete_background_task(key=key, background_tasks=self.background_tasks)
        return submenu_dump

    async def update_by_id(self, menu_id: UUID4, target_id: UUID4, **changes) -> dict[str, Any]:
        key: list[str] = [
            f'submenu_list_{menu_id}',
            f'submenu_{menu_id}_{target_id}',
            'full_menu_info'
        ]
        if not await SubmenuRepository.check_object_exists(target_menu_id=menu_id,
                                                           target_submenu_id=target_id):
            raise HTTPException(status_code=404, detail='Item not found')
        changes['id'] = target_id
        await SubmenuRepository.update_by_id(target_id, **changes)
        changes['dishes_count'] = 0
        changes['menu_id'] = menu_id
        await delete_background_task(key=key, background_tasks=self.background_tasks)
        return changes

    async def delete_by_id(self, menu_id: UUID4, target_id: UUID4) -> str:
        key: list[str] = [
            f'menu_{menu_id}',
            'menu_list',
            f'submenu_list_{menu_id}',
            f'submenu_{menu_id}_{target_id}',
            f'dish_{menu_id}_{target_id}',
            'full_menu_info'
        ]
        if not await SubmenuRepository.check_object_exists(target_menu_id=menu_id,
                                                           target_submenu_id=target_id):
            raise HTTPException(status_code=404, detail='Item not found')
        await SubmenuRepository.delete_by_id(target_id)
        await delete_background_task(key=key, background_tasks=self.background_tasks)
        return f'Запись с id {target_id} удалена.'
