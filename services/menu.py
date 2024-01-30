from fastapi import HTTPException
from sqlalchemy import select, exists, and_, func, distinct

from database.database import async_session_maker
from database.models import Menu, Dish, Submenu
from services.base import BaseServices


class MenuServices(BaseServices):
    model = Menu

    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = (
                select(
                    Menu,
                    func.count(distinct(Submenu.id)),
                    func.count(Dish.id),
                )
                .join(
                    Menu.submenus,
                    isouter=True,
                )
                .join(
                    Submenu.dishes,
                    isouter=True,
                )
                .group_by(
                    Menu.id,
                )
            )
            query_result = await session.execute(query)
            menus = query_result.all()
            menu_list = []
            if not menus:
                return menus
            for menu in menus:
                item = menu[0]
                item.submenus_count = menu[1]
                item.dishes_count = menu[2]
                menu_list.append(item)
            return menu_list

    @classmethod
    async def find_by_id(cls, target_id):
        async with async_session_maker() as session:
            query = (
                select(
                    Menu,
                    func.count(distinct(Submenu.id)),
                    func.count(Dish.id),
                )
                .join(
                    Menu.submenus,
                    isouter=True,
                )
                .join(
                    Submenu.dishes,
                    isouter=True,
                )
                .filter(Menu.id == target_id)
                .group_by(Menu.id)
            )
            query_result = await session.execute(query)
            menu = query_result.one_or_none()
            if not menu:
                raise HTTPException(status_code=404, detail="menu not found")
            result_menu = menu[0]
            result_menu.submenus_count = menu[1]
            result_menu.dishes_count = menu[2]
            return result_menu

    @classmethod
    async def check_menu_exists(cls, target_id):
        async with async_session_maker() as session:
            query = await session.execute(
                select(exists().where(and_(cls.model.id == target_id))))
            res = query.first()[0]
            return res

    @classmethod
    async def add(cls, **data):
        data = await super().add(**data)
        data['submenus_count'] = 0
        data['dishes_count'] = 0
        return data

    @classmethod
    async def update_by_id(cls, target_id, **changes):
        data = await super().update_by_id(target_id, **changes)
        data['submenus_count'] = 0
        data['dishes_count'] = 0
        return data

