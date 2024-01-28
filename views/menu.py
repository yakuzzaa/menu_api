from typing import Optional

from pydantic import UUID4

from serializers.menu import AddMenuSerializer, GetMenuSerializer, MenuResponseSerializer
from fastapi import APIRouter, HTTPException

from services.menu import MenuServices

router = APIRouter(
    prefix="/api/v1/menus",
    tags=["Меню"],
)


@router.get("")
async def get_menu() -> list[GetMenuSerializer]:
    return await MenuServices.find_all()


@router.get("/{target_menu_id}")
async def get_menu(target_menu_id: Optional[UUID4]) -> GetMenuSerializer | list:
    return await MenuServices.find_by_id(target_id=target_menu_id)


@router.post("", status_code=201)
async def add_menu(menu: AddMenuSerializer) -> MenuResponseSerializer:
    return await MenuServices.add(**menu.model_dump())


@router.patch("/{target_menu_id}")
async def update_menu(target_menu_id: Optional[UUID4], changes: AddMenuSerializer) -> MenuResponseSerializer:
    if not await MenuServices.check_menu_exists(target_id=target_menu_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return await MenuServices.update_by_id(target_id=target_menu_id, **changes.model_dump())


@router.delete("/{target_menu_id}")
async def delete_menu(target_menu_id: Optional[UUID4]):
    if not await MenuServices.check_menu_exists(target_id=target_menu_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return await MenuServices.delete_by_id(target_id=target_menu_id)
