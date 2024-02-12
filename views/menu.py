from typing import Any

from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import UUID4

from database.models import Menu
from serializers.menu import (
    AddMenuSerializer,
    GetFullMenuSerializer,
    GetMenuSerializer,
    MenuResponseSerializer,
)
from services.menu import MenuServices

router = APIRouter(
    prefix='/api/v1/menus',
    tags=['Меню'],
)


@router.get(path='/all',
            summary='Получить список всех меню со всеми подменю и блюдами',
            response_model=list[GetFullMenuSerializer],
            responses={200: {'description': 'Returns full menu list'}})
async def get_all(response: MenuServices = Depends(),
                  background_tasks: BackgroundTasks = BackgroundTasks()) -> list[dict] | dict[str, Any] | list[Menu]:
    return await response.full_menu_info()


@router.get(path='',
            summary='Получить список меню',
            response_model=list[GetMenuSerializer],
            responses={200: {'description': 'Returns menu list'}})
async def get_menus(response: MenuServices = Depends(),
                    background_tasks: BackgroundTasks = BackgroundTasks()) -> list[Menu] | list[dict[str, Any]] | dict[str, Any]:
    """Возвращает список меню с количеством всех подменю и блюд"""
    return await response.find_all()


@router.get(path='/{target_menu_id}',
            summary='Получить конкретное меню',
            response_model=GetMenuSerializer,
            responses={200: {'description': 'Returns menu'},
                       404: {'description': 'Menu object not found'}
                       })
async def get_menu(target_menu_id: UUID4 | None,
                   response: MenuServices = Depends(),
                   background_tasks: BackgroundTasks = BackgroundTasks()
                   ) -> Menu | dict[str, Any]:
    """Возвращает меню с количеством всех подменю и блюд"""
    return await response.find_by_id(target_id=target_menu_id)


@router.post(path='',
             status_code=201,
             summary='Добавить меню',
             response_model=MenuResponseSerializer,
             responses={201: {'description': 'Menu object succesfull created, return object'}})
async def post_menu(menu: AddMenuSerializer,
                    response: MenuServices = Depends(),
                    background_tasks: BackgroundTasks = BackgroundTasks()
                    ) -> dict[str, Any]:
    """Создает меню с количеством подменю и блюд равным нулю"""
    return await response.add(**menu.model_dump())


@router.patch(path='/{target_menu_id}',
              summary='Обновить конкретное меню',
              response_model=MenuResponseSerializer,
              responses={200: {'description': 'Returns the updated menu'},
                         404: {'description': 'Menu object not found'}
                         })
async def patch_menu(target_menu_id: UUID4 | None,
                     changes: AddMenuSerializer,
                     response: MenuServices = Depends(),
                     background_tasks: BackgroundTasks = BackgroundTasks()
                     ) -> dict[str, Any]:
    """Обновляет меню c определенным id"""
    return await response.update_by_id(target_id=target_menu_id, **changes.model_dump())


@router.delete(path='/{target_menu_id}',
               summary='Удалить конкретное меню',
               responses={200: {'description': 'Menu object deleted from the database'},
                          404: {'description': 'Menu object not found'}})
async def delete_menu(target_menu_id: UUID4 | None,
                      response: MenuServices = Depends(),
                      background_tasks: BackgroundTasks = BackgroundTasks()
                      ) -> str:
    """Удаляет меню с определенным id"""
    return await response.delete_by_id(target_id=target_menu_id)
