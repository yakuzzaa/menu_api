from fastapi import HTTPException
from sqlalchemy import select, exists, and_
from sqlalchemy.orm import session

from database import async_session_maker
from models.models import Menu
from services.base import BaseServices


class MenuServices(BaseServices):
    model = Menu

    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = await session.execute(select(cls.model))
            menus = query.scalars().all()
            menus_list = []
            if not menus:
                raise HTTPException(status_code=404, detail='Items not found')
            for menu in menus:
                menu.submenus_count = len(menu.submenus)
                menu.dishes_count = sum(len(submenu.dishes) for submenu in menu.submenus)
                menus_list.append(menu)
            return menus_list

    @classmethod
    async def find_by_id(cls, target_id):
        async with async_session_maker() as session:
            query = await session.execute(select(cls.model).filter_by(id=target_id))
            menu = query.scalars().one()
            if not menu:
                raise HTTPException(status_code=404, detail='Item not found')
            menu.submenus_count = str(len(menu.submenus))
            menu.dishes_count = str(sum(len(submenu.dishes) for submenu in menu.submenus))
            return menu

    @classmethod
    async def check_menu_exists(cls, target_id):
        async with async_session_maker() as session:
            query = await session.execute(
                select(exists().where(and_(cls.model.id == target_id))))
            res = query.first()[0]
            return res
