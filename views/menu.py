from typing import Optional, Annotated

from pydantic import UUID4

from serializers.menu import AddMenuSerializer, GetMenuSerializer
from fastapi import APIRouter

from services.menu import MenuServices

router = APIRouter(
    prefix="/menus",
    tags=["Меню"],
)


@router.get("")
async def get_menu() -> list[GetMenuSerializer]:
    return await MenuServices.find_all()


@router.get("/{target_menu_id}")
async def get_menu(target_menu_id: Optional[UUID4] = None) -> GetMenuSerializer:
    return await MenuServices.find_by_id(target_id=target_menu_id)


@router.post("")
async def add_menu(menu: AddMenuSerializer):
    return await MenuServices.add(**menu.model_dump())


@router.patch("/{target_menu_id}")
async def update_menu(target_menu_id: int):
    pass


@router.delete("/{target_menu_id}")
async def delete_menu(target_menu_id: int):
    pass
