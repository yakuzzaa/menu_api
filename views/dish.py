from fastapi import APIRouter
from pydantic import UUID4

from database.models import Dish
from serializers.dish import (
    AddDishSerializer,
    DishResponseSerializer,
    GetDishSerializer,
)
from services.dish import DishServices

router = APIRouter(
    prefix='/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes',
    tags=['Блюда'],
)


@router.get(path='',
            summary='Получить список блюд',
            response_model=list[GetDishSerializer],
            responses={200: {'description': 'Returns dishes list'}})
async def get_dishes(target_menu_id: UUID4 | None = None,
                     target_submenu_id: UUID4 | None = None) -> list[Dish]:
    """Возвращает список всех блюд"""
    return await DishServices.get_dish(menu_id=target_menu_id, submenu_id=target_submenu_id)


@router.get(path='/{target_dish_id}',
            summary='Получить конкретное блюдо',
            response_model=GetDishSerializer,
            responses={200: {'description': 'Returns dish'},
                       404: {'description': 'Dish object not found'}
                       })
async def get_dish(target_menu_id: UUID4 | None = None, target_submenu_id: UUID4 | None = None,
                   target_dish_id: UUID4 | None = None) -> Dish:
    """Возвращает блюдо"""
    return await DishServices.get_dish_by_id(menu_id=target_menu_id,
                                             submenu_id=target_submenu_id,
                                             target_id=target_dish_id)


@router.post(path='',
             status_code=201,
             summary='Добавить блюдо',
             response_model=DishResponseSerializer,
             responses={201: {'description': 'Dish object succesfull created, return object'},
                        404: {'description': 'Menu or submenu object not found'}
                        }
             )
async def post_dish(target_menu_id: UUID4 | None, target_submenu_id: UUID4 | None,
                    dish: AddDishSerializer) -> dict:
    """Создает новое блюдо"""
    return await DishServices.add(menu_id=target_menu_id, submenu_id=target_submenu_id, dish=dish)


@router.patch(path='/{target_dish_id}',
              summary='Обновить конкретное блюдо',
              response_model=DishResponseSerializer,
              responses={200: {'description': 'Returns the updated dish'},
                         404: {'description': 'Dish object not found'}
                         }
              )
async def patch_dish(target_menu_id: UUID4 | None, target_submenu_id: UUID4 | None,
                     target_dish_id: UUID4 | None, dish: AddDishSerializer) -> dict:
    """Обновляет блюдо с определенным id"""
    return await DishServices.update_by_id(menu_id=target_menu_id,
                                           submenu_id=target_submenu_id,
                                           target_id=target_dish_id,
                                           **dish.model_dump())


@router.delete(path='/{target_dish_id}',
               summary='Удалить конкретное блюдо',
               responses={200: {'description': 'Dish object deleted from the database'},
                          404: {'description': 'Dish object not found'}
                          }
               )
async def delete_dish(target_menu_id: UUID4 | None, target_submenu_id: UUID4 | None,
                      target_dish_id: UUID4 | None) -> str:
    """Удаляет блюдо с определнным id"""
    return await DishServices.delete_by_id(menu_id=target_menu_id,
                                           submenu_id=target_submenu_id,
                                           target_id=target_dish_id)
