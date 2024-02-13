import uuid
from typing import Any

from fastapi import BackgroundTasks, HTTPException
from pydantic import UUID4

from cache.background_tasks import create_background_task, delete_background_task
from cache.redis_cache import Cache, CacheReturnType
from database.models import Dish
from repository.dish import DishRepository
from repository.submenu import SubmenuRepository
from serializers.dish import AddDishSerializer
from utils.discount_utils import get_price_with_discount


class DishServices:
    def __init__(self, background_tasks: BackgroundTasks = None):
        self.background_tasks = background_tasks

    async def get_dish(self, menu_id: UUID4, submenu_id: UUID4) -> list[Dish] | list[dict[str, Any]] | dict[str, Any]:
        key: str = f'dish_list_{menu_id}_{submenu_id}'
        cache_dishes: CacheReturnType = await Cache.get(key)

        if cache_dishes:
            return cache_dishes

        dishes: list[Dish] = await DishRepository.read(submenu_id)
        dishes_list: list = []
        if not dishes:
            return dishes
        for dish in dishes:
            discount = get_price_with_discount(str(dish.id))
            if discount:
                dish.__dict__['price_with_discount'] = discount
            dish.menu_id = menu_id
            dishes_list.append(dish)
        await create_background_task(key=key, value=dishes, background_tasks=self.background_tasks)
        return dishes_list

    async def get_dish_by_id(self, menu_id: UUID4, submenu_id: UUID4, target_id: UUID4) -> Dish | dict[str, Any]:
        key: str = f'dish_{menu_id}_{submenu_id}_{target_id}'
        cache_dish: CacheReturnType = await Cache.get(key)

        if cache_dish:
            return cache_dish
        dish: Dish = await DishRepository.read_by_id(submenu_id, target_id)
        if not dish:
            raise HTTPException(status_code=404, detail='dish not found')
        discount = get_price_with_discount(str(dish.id))
        if discount:
            dish.__dict__['price_with_discount'] = discount
        dish.menu_id = menu_id
        await create_background_task(key=key, value=dish, background_tasks=self.background_tasks)
        return dish

    async def add(self, menu_id: UUID4, submenu_id: UUID4, dish: AddDishSerializer) -> dict[str, Any]:
        key: list[str] = [
            'menu_list',
            f'menu_{menu_id}',
            f'submenu_list_{menu_id}',
            f'dish_list_{menu_id}_{submenu_id}',
            'full_menu_info'
        ]

        if not await SubmenuRepository.check_object_exists(target_menu_id=menu_id,
                                                           target_submenu_id=submenu_id):
            raise HTTPException(status_code=404, detail='Item not found')

        dish_dump: dict[str, Any] = dish.model_dump()
        dish_dump['submenu_id'] = submenu_id
        dish_dump['id'] = uuid.uuid4()

        await DishRepository.create(**dish_dump)

        dish_dump['menu_id'] = menu_id

        await delete_background_task(key=key, background_tasks=self.background_tasks)

        return dish_dump

    async def update_by_id(self, menu_id: UUID4, submenu_id: UUID4, target_id: UUID4, **changes) -> dict[str, Any]:
        if not (await SubmenuRepository.check_object_exists(target_menu_id=menu_id,
                                                            target_submenu_id=submenu_id) and await DishRepository.check_object_exists(
                submenu_id, target_id)):
            raise HTTPException(status_code=404, detail='Item not found')
        key: list[str] = [
            f'dish_list_{menu_id}_{submenu_id}',
            f'dish_{menu_id}_{submenu_id}_{target_id}',
            'full_menu_info'
        ]
        changes['id'] = target_id
        await DishRepository.update_by_id(target_id, **changes)
        changes['menu_id'] = menu_id
        changes['submenu_id'] = submenu_id
        await delete_background_task(key=key, background_tasks=self.background_tasks)
        return changes

    async def delete_by_id(self, menu_id: UUID4, submenu_id: UUID4, target_id: UUID4) -> str:
        key: list[str] = [
            'menu_list',
            f'menu_{menu_id}',
            f'submenu_list_{menu_id}',
            f'submenu_{menu_id}_{submenu_id}',
            f'dish_list_{menu_id}_{submenu_id}',
            f'dish_{menu_id}_{submenu_id}_{target_id}',
            'full_menu_info'
        ]

        if not (await SubmenuRepository.check_object_exists(target_menu_id=menu_id,
                                                            target_submenu_id=submenu_id) and await DishRepository.check_object_exists(
                submenu_id, target_id)):
            raise HTTPException(status_code=404, detail='Item not found')
        await DishRepository.delete_by_id(target_id)
        await delete_background_task(key=key, background_tasks=self.background_tasks)
        return f'Запись с id {target_id} удалена.'
