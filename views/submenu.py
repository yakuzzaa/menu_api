from fastapi import APIRouter
from pydantic import UUID4

from database.models import Submenu
from serializers.submenu import (
    AddSubmenuSerializer,
    GetSubmenuSerializer,
    SubmenuResponseSerializer,
)
from services.submenu import SubmenuServices

router = APIRouter(
    prefix='/api/v1/menus/{target_menu_id}/submenus',
    tags=['Подменю'],
)


@router.get('', summary='Получить список подменю', response_model=list[GetSubmenuSerializer],
            responses={200: {'description': 'Returns submenu list'}})
async def get_submenus(target_menu_id: UUID4 | None = None) -> list[Submenu]:
    """Возвращает список подменю с количеством всех блюд"""
    return await SubmenuServices.find_all(menu_id=target_menu_id)


@router.get(path='/{target_submenu_id}',
            summary='Получить конкретное подменю',
            response_model=GetSubmenuSerializer,
            responses={200: {'description': 'Returns submenu'},
                       404: {'description': 'Submenu object not found'}
                       })
async def get_submenu(target_menu_id: UUID4 | None = None,
                      target_submenu_id: UUID4 | None = None) -> Submenu:
    """Возвращает подменю с количеством всех блюд"""
    return await SubmenuServices.find_by_id(menu_id=target_menu_id, target_id=target_submenu_id)


@router.post(path='',
             status_code=201,
             summary='Добавить подменю',
             response_model=SubmenuResponseSerializer,
             responses={201: {'description': 'Submenu object succesfull created, return object'},
                        404: {'description': 'Menu object not found'}
                        })
async def post_submenu(target_menu_id: UUID4 | None, submenu: AddSubmenuSerializer) -> dict:
    """Создает подменю c количеством блюд равным 0"""
    return await SubmenuServices.add(menu_id=target_menu_id, submenu=submenu)


@router.patch(path='/{target_submenu_id}',
              summary='Обновить конкретное подменю',
              response_model=SubmenuResponseSerializer,
              responses={200: {'description': 'Returns the updated submenu'},
                         404: {'description': 'Submenu object not found'}
                         })
async def patch_submenu(target_menu_id: UUID4 | None, target_submenu_id: UUID4 | None,
                        changes: AddSubmenuSerializer) -> dict:
    """Обновляет подменю с определенным id"""
    return await SubmenuServices.update_by_id(menu_id=target_menu_id, target_id=target_submenu_id,
                                              **changes.model_dump())


@router.delete(path='/{target_submenu_id}',
               summary='Удалить конкретное подменю',
               responses={200: {'description': 'Submenu object deleted from the database'},
                          404: {'description': 'Submenu object not found'}
                          })
async def delete_submenu(target_menu_id: UUID4 | None, target_submenu_id: UUID4 | None) -> str:
    """Удаляет подменю с определенным id"""
    return await SubmenuServices.delete_by_id(menu_id=target_menu_id, target_id=target_submenu_id)
