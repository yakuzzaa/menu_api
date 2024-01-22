from typing import Optional, List

from pydantic import UUID4

from fastapi import APIRouter

from serializers.submenu import GetSubmenuSerializer, AddSubmenuSerializer
from services.submenu import SubmenuServices

router = APIRouter(
    prefix="/menus",
    tags=["Подменю"],
)


@router.get("/{target_menu_id}/submenus")
async def get_submenu(target_menu_id: Optional[UUID4] = None) -> List[GetSubmenuSerializer]:
    return await SubmenuServices.find_all(target_menu_id=target_menu_id)


@router.get("/{target_menu_id}/submenus/{target_submenu_id}")
async def get_submenu(target_menu_id: Optional[UUID4] = None,
                      target_submenu_id: Optional[UUID4] = None) -> GetSubmenuSerializer:
    return await SubmenuServices.find_by_id(target_menu_id=target_menu_id, target_submenu_id=target_submenu_id)


@router.post("/{target_menu_id}/submenus")
async def post_submenu(target_menu_id: Optional[UUID4], submenu: AddSubmenuSerializer):
    submenu_dump = submenu.model_dump()
    submenu_dump["menu_id"] = target_menu_id
    return await SubmenuServices.add(**submenu_dump)


@router.patch("/{target_menu_id}/submenus")
async def put_submenu():
    pass


@router.delete("/{target_menu_id}/submenus")
async def delete_submenu():
    pass
