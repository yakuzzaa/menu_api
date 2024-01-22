from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import UUID4

from serializers.dish import GetDishSerializer, AddDishSerializer, DishResponseSerializer
from services.dish import DishServices

router = APIRouter(
    prefix="/menus",
    tags=["Блюда"],
)


@router.get("/{target_menu_id}/submenus/{target_submenu_id}/dishes")
async def get_dish(target_menu_id: Optional[UUID4] = None, target_submenu_id: Optional[UUID4] = None) -> List[
    GetDishSerializer]:
    return await DishServices.get_dish(target_menu_id, target_submenu_id)


@router.get("/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
async def get_dish_by_id(target_menu_id: Optional[UUID4] = None, target_submenu_id: Optional[UUID4] = None,
                         target_dish_id: Optional[UUID4] = None) -> GetDishSerializer:
    return await DishServices.get_dish_by_id(target_menu_id, target_submenu_id, target_dish_id)


@router.post("/{target_menu_id}/submenus/{target_submenu_id}/dishes")
async def post_dish(target_menu_id: Optional[UUID4], target_submenu_id: Optional[UUID4],
                    dish: AddDishSerializer) -> DishResponseSerializer:
    if not await DishServices.check_object_exists(target_menu_id=target_menu_id, target_submenu_id=target_submenu_id):
        raise HTTPException(status_code=404, detail="Item not found")
    dish_dump = dish.model_dump()
    dish_dump["submenu_id"] = target_submenu_id
    return await DishServices.add(**dish_dump)


@router.patch("/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
async def update_dish(target_menu_id: Optional[UUID4], target_submenu_id: Optional[UUID4],
                      target_dish_id: Optional[UUID4], dish: AddDishSerializer) -> DishResponseSerializer:
    if not await (DishServices.check_object_exists(target_menu_id=target_menu_id,
                                                   target_submenu_id=target_submenu_id) and DishServices.get_dish_by_submenu(
        target_submenu_id, target_dish_id)):
        raise HTTPException(status_code=404, detail="Item not found")

    return await DishServices.update_by_id(target_id=target_dish_id, **dish.model_dump())


@router.delete("/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}")
async def delete_dish(target_menu_id: Optional[UUID4], target_submenu_id: Optional[UUID4],
                      target_dish_id: Optional[UUID4]):
    if not await (DishServices.check_object_exists(target_menu_id=target_menu_id,
                                                   target_submenu_id=target_submenu_id) and DishServices.get_dish_by_submenu(
        target_submenu_id, target_dish_id)):
        raise HTTPException(status_code=404, detail="Item not found")

    return await DishServices.delete_by_id(target_id=target_dish_id)
