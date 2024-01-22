from fastapi import HTTPException
from sqlalchemy import select, exists, and_
from sqlalchemy.orm import query

from database import async_session_maker
from models.models import Dish, Submenu
from services.base import BaseServices


class DishServices(BaseServices):
    model = Dish

    @classmethod
    async def get_dish(cls, target_menu_id, target_submenu_id):
        async with async_session_maker() as session:
            query = await session.execute(select(cls.model).filter_by(submenu_id=target_submenu_id))
            dishes = query.scalars().all()
            dishes_list = []
            if not dishes:
                raise HTTPException(status_code=404, detail='Items not found')
            for dish in dishes:
                dish.menu_id = target_menu_id
                dishes_list.append(dish)
            return dishes_list

    @classmethod
    async def get_dish_by_id(cls, target_menu_id, target_submenu_id, target_dish_id):
        async with async_session_maker() as session:
            query = await session.execute(select(cls.model).filter_by(submenu_id=target_submenu_id, id=target_dish_id))
            dish = query.scalars().one()
            if not dish:
                raise HTTPException(status_code=404, detail='Item not found')
            dish.menu_id = target_menu_id
            return dish

    @classmethod
    async def get_dish_by_submenu(cls, target_submenu_id, dish_id):
        async with async_session_maker() as session:
            query = await session.execute(
                select(exists().where(and_(Dish.submenu_id == target_submenu_id, Dish.id == dish_id))))
            res = query.first()[0]
            return res
