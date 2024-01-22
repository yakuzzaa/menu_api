from typing import Optional, List

from pydantic import UUID4

from fastapi import APIRouter, HTTPException

from serializers.submenu import GetSubmenuSerializer, AddSubmenuSerializer, SubmenuResponseSerializer
from services.menu import MenuServices
from services.submenu import SubmenuServices

router = APIRouter(
    prefix="/api/v1/menus",
    tags=["Подменю"],
)


@router.get("/{target_menu_id}/submenus")
async def get_submenu(target_menu_id: Optional[UUID4] = None) -> List[GetSubmenuSerializer]:
    return await SubmenuServices.find_all(target_menu_id=target_menu_id)


@router.get("/{target_menu_id}/submenus/{target_submenu_id}")
async def get_submenu(target_menu_id: Optional[UUID4] = None,
                      target_submenu_id: Optional[UUID4] = None) -> GetSubmenuSerializer:
    return await SubmenuServices.find_by_id(target_menu_id=target_menu_id, target_submenu_id=target_submenu_id)


@router.post("/{target_menu_id}/submenus", status_code=201)
async def post_submenu(target_menu_id: Optional[UUID4], submenu: AddSubmenuSerializer) -> SubmenuResponseSerializer:
    if not await MenuServices.check_menu_exists(target_id=target_menu_id):
        raise HTTPException(404, "Menu not found")
    submenu_dump = submenu.model_dump()
    submenu_dump["menu_id"] = target_menu_id
    return await SubmenuServices.add(**submenu_dump)


@router.patch("/{target_menu_id}/submenus/{target_submenu_id}")
async def put_submenu(target_menu_id: Optional[UUID4], target_submenu_id: Optional[UUID4],
                      changes: AddSubmenuSerializer) -> SubmenuResponseSerializer:
    if not await SubmenuServices.check_object_exists(target_menu_id=target_menu_id,
                                                     target_submenu_id=target_submenu_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return await SubmenuServices.update_by_id(target_id=target_submenu_id, **changes.model_dump())


@router.delete("/{target_menu_id}/submenus/{target_submenu_id}")
async def delete_submenu(target_menu_id: Optional[UUID4], target_submenu_id: Optional[UUID4]):
    if not await SubmenuServices.check_object_exists(target_menu_id=target_menu_id,
                                                     target_submenu_id=target_submenu_id):
        raise HTTPException(status_code=404, detail="Item not found")
    return await SubmenuServices.delete_by_id(target_id=target_submenu_id)
