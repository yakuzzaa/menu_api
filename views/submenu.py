from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends
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
async def get_submenus(target_menu_id: UUID4 | None = None,
                       response: SubmenuServices = Depends(),
                       background_tasks: BackgroundTasks = BackgroundTasks()
                       ) -> list[Submenu] | list[dict[str, Any]] | dict[str, Any]:
    """Возвращает список подменю с количеством всех блюд"""
    return await response.find_all(menu_id=target_menu_id)


@router.get(path='/{target_submenu_id}',
            summary='Получить конкретное подменю',
            response_model=GetSubmenuSerializer,
            responses={200: {'description': 'Returns submenu'},
                       404: {'description': 'Submenu object not found'}
                       })
async def get_submenu(target_menu_id: UUID4 | None = None,
                      target_submenu_id: UUID4 | None = None,
                      response: SubmenuServices = Depends(),
                      background_tasks: BackgroundTasks = BackgroundTasks()) -> Submenu | dict[str, Any]:
    """Возвращает подменю с количеством всех блюд"""
    return await response.find_by_id(menu_id=target_menu_id, target_id=target_submenu_id)


@router.post(path='',
             status_code=201,
             summary='Добавить подменю',
             response_model=SubmenuResponseSerializer,
             responses={201: {'description': 'Submenu object succesfull created, return object'},
                        404: {'description': 'Menu object not found'}
                        })
async def post_submenu(target_menu_id: UUID4 | None,
                       submenu: AddSubmenuSerializer,
                       response: SubmenuServices = Depends(),
                       background_tasks: BackgroundTasks = BackgroundTasks()
                       ) -> dict[str, Any]:
    """Создает подменю c количеством блюд равным 0"""
    return await response.add(menu_id=target_menu_id, submenu=submenu)


@router.patch(path='/{target_submenu_id}',
              summary='Обновить конкретное подменю',
              response_model=SubmenuResponseSerializer,
              responses={200: {'description': 'Returns the updated submenu'},
                         404: {'description': 'Submenu object not found'}
                         })
async def patch_submenu(target_menu_id: UUID4 | None,
                        target_submenu_id: UUID4 | None,
                        changes: AddSubmenuSerializer,
                        response: SubmenuServices = Depends(),
                        background_tasks: BackgroundTasks = BackgroundTasks()
                        ) -> dict[str, Any]:
    """Обновляет подменю с определенным id"""
    return await response.update_by_id(menu_id=target_menu_id, target_id=target_submenu_id,
                                       **changes.model_dump())


@router.delete(path='/{target_submenu_id}',
               summary='Удалить конкретное подменю',
               responses={200: {'description': 'Submenu object deleted from the database'},
                          404: {'description': 'Submenu object not found'}
                          })
async def delete_submenu(target_menu_id: UUID4 | None,
                         target_submenu_id: UUID4 | None,
                         response: SubmenuServices = Depends(),
                         background_tasks: BackgroundTasks = BackgroundTasks()
                         ) -> str:
    """Удаляет подменю с определенным id"""
    return await response.delete_by_id(menu_id=target_menu_id, target_id=target_submenu_id)
