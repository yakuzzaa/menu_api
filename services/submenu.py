import uuid

from fastapi import HTTPException
from pydantic import UUID4

from cache.redis_cache import Cache
from database.models import Submenu
from repository.menu import MenuRepository
from repository.submenu import SubmenuRepository


class SubmenuServices:
    @classmethod
    async def find_all(cls, menu_id: UUID4) -> list[Submenu]:
        key = f'submenu_list_{menu_id}'
        cache_submenus = await Cache.get(key)
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
        await Cache.create(key, submenu_list)
        return submenu_list

    @classmethod
    async def find_by_id(cls, menu_id: UUID4, target_id: UUID4) -> Submenu:
        key = f'submenu_{menu_id}_{target_id}'
        cache_submenu = await Cache.get(key)
        if cache_submenu:
            return cache_submenu

        submenu: Submenu = await SubmenuRepository.read_by_id(menu_id, target_id)
        if not submenu:
            raise HTTPException(status_code=404, detail='submenu not found')
        result_submenu: Submenu = submenu[0]
        result_submenu.dishes_count = submenu[1]
        await Cache.create(key, result_submenu)
        return result_submenu

    @classmethod
    async def add(cls, menu_id, submenu) -> dict:
        key = [f'menu_{menu_id}', 'menu_list', f'submenu_list_{menu_id}']
        if not await MenuRepository.check_object_exists(target_id=menu_id):
            raise HTTPException(404, 'Menu not found')
        submenu_dump = submenu.model_dump()
        submenu_dump['menu_id'] = menu_id
        submenu_dump['id'] = uuid.uuid4()
        await SubmenuRepository.create(**submenu_dump)
        submenu_dump['dishes_count'] = 0
        await Cache.delete(key)
        return submenu_dump

    @classmethod
    async def update_by_id(cls, menu_id: UUID4, target_id: UUID4, **changes) -> dict:
        key = [
            f'submenu_list_{menu_id}',
            f'submenu_{menu_id}_{target_id}',
        ]
        if not await SubmenuRepository.check_object_exists(target_menu_id=menu_id,
                                                           target_submenu_id=target_id):
            raise HTTPException(status_code=404, detail='Item not found')
        changes['id'] = target_id
        await SubmenuRepository.update_by_id(target_id, **changes)
        changes['dishes_count'] = 0
        changes['menu_id'] = menu_id
        await Cache.delete(key)
        return changes

    @classmethod
    async def delete_by_id(cls, menu_id: UUID4, target_id: UUID4) -> str:
        key = [
            f'menu_{menu_id}',
            'menu_list',
            f'submenu_list_{menu_id}',
            f'submenu_{menu_id}_{target_id}',
            f'dish_{menu_id}_{target_id}',
        ]
        if not await SubmenuRepository.check_object_exists(target_menu_id=menu_id,
                                                           target_submenu_id=target_id):
            raise HTTPException(status_code=404, detail='Item not found')
        await SubmenuRepository.delete_by_id(target_id)
        await Cache.delete(key)
        return f'Запись с id {target_id} удалена.'
