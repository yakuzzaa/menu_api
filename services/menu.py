import uuid

from fastapi import HTTPException
from pydantic import UUID4

from cache.redis_cache import Cache
from database.models import Menu
from repository.menu import MenuRepository


class MenuServices:
    @classmethod
    async def find_all(cls) -> list[Menu]:
        key = 'menu_list'
        cache_menus = await Cache.get(key)
        if cache_menus:
            return cache_menus
        menus: list[Menu] = await MenuRepository.read()
        menu_list: list = []
        if not menus:
            return menus
        for menu in menus:
            item: Menu = menu[0]
            item.submenus_count = menu[1]
            item.dishes_count = menu[2]
            menu_list.append(item)
        await Cache.create(key, menu_list)
        return menu_list

    @classmethod
    async def find_by_id(cls, target_id: UUID4) -> Menu:
        key = f'menu_{target_id}'
        cache_menu = await Cache.get(key)
        if cache_menu:
            return cache_menu

        menu: Menu = await MenuRepository.read_by_id(target_id)
        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')

        result_menu: Menu = menu[0]
        result_menu.submenus_count = menu[1]
        result_menu.dishes_count = menu[2]
        await Cache.create(key, result_menu)
        return result_menu

    @classmethod
    async def add(cls, **data) -> dict:
        data['id'] = uuid.uuid4()
        await MenuRepository.create(**data)
        data['submenus_count'] = 0
        data['dishes_count'] = 0
        await Cache.delete('menu_list')
        return data

    @classmethod
    async def update_by_id(cls, target_id: UUID4, **changes) -> dict:
        key = [f'menu_{target_id}', 'menu_list']

        if not await MenuRepository.check_object_exists(target_id=target_id):
            raise HTTPException(status_code=404, detail='Item not found')
        changes['id'] = target_id
        await MenuRepository.update_by_id(target_id, **changes)
        changes['submenus_count'] = 0
        changes['dishes_count'] = 0
        await Cache.delete(key)
        return changes

    @classmethod
    async def delete_by_id(cls, target_id: UUID4) -> str:
        key = [
            f'menu_{target_id}',
            'menu_list',
            f'submenu_list_{target_id}',
            f'dish_{target_id}',
        ]
        if not await MenuRepository.check_object_exists(target_id=target_id):
            raise HTTPException(status_code=404, detail='Item not found')
        await MenuRepository.delete_by_id(target_id)
        await Cache.delete(key)
        return f'Запись с id {target_id} удалена.'
