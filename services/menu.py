import uuid
from typing import Any

from fastapi import BackgroundTasks, HTTPException
from pydantic import UUID4

from cache.background_tasks import create_background_task, delete_background_task
from cache.redis_cache import Cache, CacheReturnType
from database.models import Menu
from repository.menu import MenuRepository


class MenuServices:
    def __init__(self, background_tasks: BackgroundTasks = None):
        self.background_tasks = background_tasks

    async def full_menu_info(self) -> list[dict] | dict[str, Any] | list[Menu]:
        key: str = 'full_menu_info'
        cache_menus: CacheReturnType = await Cache.get(key)
        if cache_menus:
            return cache_menus
        menus: list[Menu] = await MenuRepository.read_all()
        menus_list = []
        if not menus:
            return menus

        for menu in menus:
            menu_data: dict[str, Any] = {
                'id': menu[0].id,
                'title': menu[0].title,
                'description': menu[0].description,
                'submenus': [
                    {
                        'id': submenu.id,
                        'title': submenu.title,
                        'description': submenu.description,
                        'dishes': [
                            {
                                'id': dish.id,
                                'title': dish.title,
                                'description': dish.description,
                                'price': str(dish.price)
                            } for dish in submenu.dishes
                        ]
                    } for submenu in menu[0].submenus
                ]
            }
            menus_list.append(menu_data)
        await create_background_task(key=key, value=menus_list, background_tasks=self.background_tasks)
        return menus_list

    async def find_all(self) -> list[Menu] | list[dict[str, Any]] | dict[str, Any]:
        key: str = 'menu_list'
        cache_menus: CacheReturnType = await Cache.get(key)
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
        await create_background_task(key=key, value=menu_list, background_tasks=self.background_tasks)
        return menu_list

    async def find_by_id(self, target_id: UUID4) -> Menu | dict[str, Any]:
        key: str = f'menu_{target_id}'
        cache_menu: CacheReturnType = await Cache.get(key)
        if cache_menu:
            return cache_menu

        menu: Menu = await MenuRepository.read_by_id(target_id)
        if not menu:
            raise HTTPException(status_code=404, detail='menu not found')

        result_menu: Menu = menu[0]
        result_menu.submenus_count = menu[1]
        result_menu.dishes_count = menu[2]
        await create_background_task(key=key, value=result_menu, background_tasks=self.background_tasks)
        return result_menu

    async def add(self, **data) -> dict[str, Any]:
        key: list[str] = ['full_menu_info', 'menu_list']
        data['id'] = uuid.uuid4()
        await MenuRepository.create(**data)
        data['submenus_count'] = 0
        data['dishes_count'] = 0
        await delete_background_task(key=key, background_tasks=self.background_tasks)
        return data

    async def update_by_id(self, target_id: UUID4, **changes) -> dict[str, Any]:
        key: list[str] = [f'menu_{target_id}', 'menu_list', 'full_menu_info']

        if not await MenuRepository.check_object_exists(target_id=target_id):
            raise HTTPException(status_code=404, detail='Item not found')
        changes['id'] = target_id
        await MenuRepository.update_by_id(target_id, **changes)
        changes['submenus_count'] = 0
        changes['dishes_count'] = 0
        await delete_background_task(key=key, background_tasks=self.background_tasks)
        return changes

    async def delete_by_id(self, target_id: UUID4) -> str:
        key: list[str] = [
            f'menu_{target_id}',
            'menu_list',
            f'submenu_list_{target_id}',
            f'dish_{target_id}',
            'full_menu_info'
        ]
        if not await MenuRepository.check_object_exists(target_id=target_id):
            raise HTTPException(status_code=404, detail='Item not found')
        await MenuRepository.delete_by_id(target_id)
        await delete_background_task(key=key, background_tasks=self.background_tasks)
        return f'Запись с id {target_id} удалена.'
