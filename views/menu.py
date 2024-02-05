from fastapi import APIRouter
from pydantic import UUID4

from database.models import Menu
from serializers.menu import (
    AddMenuSerializer,
    GetMenuSerializer,
    MenuResponseSerializer,
)
from services.menu import MenuServices

router = APIRouter(
    prefix='/api/v1/menus',
    tags=['Меню'],
)


@router.get(path='',
            summary='Получить список меню',
            response_model=list[GetMenuSerializer],
            responses={200: {'description': 'Returns menu list'}})
async def get_menus() -> list[Menu]:
    """Возвращает список меню с количеством всех подменю и блюд"""
    return await MenuServices.find_all()


@router.get(path='/{target_menu_id}',
            summary='Получить конкретное меню',
            response_model=GetMenuSerializer,
            responses={200: {'description': 'Returns menu'},
                       404: {'description': 'Menu object not found'}
                       })
async def get_menu(target_menu_id: UUID4 | None) -> Menu:
    """Возвращает меню с количеством всех подменю и блюд"""
    return await MenuServices.find_by_id(target_id=target_menu_id)


@router.post(path='',
             status_code=201,
             summary='Добавить меню',
             response_model=MenuResponseSerializer,
             responses={201: {'description': 'Menu object succesfull created, return object'}})
async def post_menu(menu: AddMenuSerializer) -> dict:
    """Создает меню с количеством подменю и блюд равным нулю"""
    return await MenuServices.add(**menu.model_dump())


@router.patch(path='/{target_menu_id}',
              summary='Обновить конкретное меню',
              response_model=MenuResponseSerializer,
              responses={200: {'description': 'Returns the updated menu'},
                         404: {'description': 'Menu object not found'}
                         })
async def patch_menu(target_menu_id: UUID4 | None, changes: AddMenuSerializer) -> dict:
    """Обновляет меню c определенным id"""
    return await MenuServices.update_by_id(target_id=target_menu_id, **changes.model_dump())


@router.delete(path='/{target_menu_id}',
               summary='Удалить конкретное меню',
               responses={200: {'description': 'Menu object deleted from the database'},
                          404: {'description': 'Menu object not found'}})
async def delete_menu(target_menu_id: UUID4 | None) -> str:
    """Удаляет меню с определенным id"""
    return await MenuServices.delete_by_id(target_id=target_menu_id)
