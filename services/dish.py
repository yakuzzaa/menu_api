import uuid

from fastapi import HTTPException
from pydantic import UUID4

from cache.redis_cache import Cache
from database.models import Dish
from repository.dish import DishRepository
from repository.submenu import SubmenuRepository
from serializers.dish import AddDishSerializer


class DishServices:
    @classmethod
    async def get_dish(cls, menu_id: UUID4, submenu_id: UUID4) -> list[Dish]:
        key = f'dish_list_{menu_id}_{submenu_id}'
        cache_dishes = await Cache.get(key)

        if cache_dishes:
            return cache_dishes

        dishes: list[Dish] = await DishRepository.read(submenu_id)
        dishes_list: list = []
        if not dishes:
            return dishes
        for dish in dishes:
            dish.menu_id = menu_id
            dishes_list.append(dish)
        await Cache.create(key, dishes)
        return dishes_list

    @classmethod
    async def get_dish_by_id(cls, menu_id: UUID4, submenu_id: UUID4, target_id: UUID4) -> Dish:
        key = f'dish_{menu_id}_{submenu_id}_{target_id}'
        cache_dish = await Cache.get(key)

        if cache_dish:
            return cache_dish

        dish: Dish = await DishRepository.read_by_id(submenu_id, target_id)
        if not dish:
            raise HTTPException(status_code=404, detail='dish not found')
        dish.menu_id = menu_id
        await Cache.create(key, dish)
        return dish

    @classmethod
    async def add(cls, menu_id: UUID4, submenu_id: UUID4, dish: AddDishSerializer) -> dict:
        key = [
            'menu_list',
            f'menu_{menu_id}',
            f'submenu_list_{menu_id}',
            f'dish_list_{menu_id}_{submenu_id}',
        ]
        if not await SubmenuRepository.check_object_exists(target_menu_id=menu_id,
                                                           target_submenu_id=submenu_id):
            raise HTTPException(status_code=404, detail='Item not found')
        dish_dump = dish.model_dump()
        dish_dump['submenu_id'] = submenu_id
        dish_dump['id'] = uuid.uuid4()
        await DishRepository.create(**dish_dump)
        dish_dump['menu_id'] = menu_id
        await Cache.delete(key)
        return dish_dump

    @classmethod
    async def update_by_id(cls, menu_id: UUID4, submenu_id: UUID4, target_id: UUID4, **changes) -> dict:
        if not (await SubmenuRepository.check_object_exists(target_menu_id=menu_id,
                                                            target_submenu_id=submenu_id) and await DishRepository.check_object_exists(submenu_id, target_id)):
            raise HTTPException(status_code=404, detail='Item not found')
        key = [
            f'dish_list_{menu_id}_{submenu_id}',
            f'dish_{menu_id}_{submenu_id}_{target_id}'
        ]
        changes['id'] = target_id
        await DishRepository.update_by_id(target_id, **changes)
        changes['menu_id'] = menu_id
        changes['submenu_id'] = submenu_id
        await Cache.delete(key)
        return changes

    @classmethod
    async def delete_by_id(cls, menu_id: UUID4, submenu_id: UUID4, target_id: UUID4) -> str:
        key = [
            'menu_list',
            f'menu_{menu_id}',
            f'submenu_list_{menu_id}',
            f'submenu_{menu_id}_{submenu_id}',
            f'dish_list_{menu_id}_{submenu_id}',
            f'dish_{menu_id}_{submenu_id}_{target_id}',
        ]

        if not (await SubmenuRepository.check_object_exists(target_menu_id=menu_id,
                                                            target_submenu_id=submenu_id) and await DishRepository.check_object_exists(submenu_id, target_id)):
            raise HTTPException(status_code=404, detail='Item not found')
        await DishRepository.delete_by_id(target_id)
        await Cache.delete(key)
        return f'Запись с id {target_id} удалена.'
