from typing import Optional

from pydantic import UUID4

from serializers.menu import AddMenuSerializer, GetMenuSerializer, MenuResponseSerializer
from fastapi import APIRouter

from services.menu import MenuServices

router = APIRouter(
    prefix="/v1/menus",
    tags=["Меню"],
)


@router.get("")
async def get_menu() -> list[GetMenuSerializer]:
    return await MenuServices.find_all()


@router.get("/{target_menu_id}")
async def get_menu(target_menu_id: Optional[UUID4]) -> GetMenuSerializer:
    return await MenuServices.find_by_id(target_id=target_menu_id)


@router.post("")
async def add_menu(menu: AddMenuSerializer) -> MenuResponseSerializer:
    return await MenuServices.add(**menu.model_dump())


@router.patch("/{target_menu_id}")
async def update_menu(target_menu_id: Optional[UUID4], changes: AddMenuSerializer) -> MenuResponseSerializer:
    return await MenuServices.update_by_id(target_id=target_menu_id, **changes.model_dump())


@router.delete("/{target_menu_id}")
async def delete_menu(target_menu_id: Optional[UUID4]):
    return await MenuServices.delete_by_id(target_id=target_menu_id)
