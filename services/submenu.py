from fastapi import HTTPException
from sqlalchemy import select, exists, and_, func

from database.database import async_session_maker
from database.models import Submenu, Dish
from services.base import BaseServices


class SubmenuServices(BaseServices):
    model = Submenu

    @classmethod
    async def find_all(cls, target_menu_id):
        async with async_session_maker() as session:
            query = (
                select(
                    Submenu,
                    func.count(Dish.id),
                )
                .join(
                    Submenu.dishes,
                    isouter=True,
                )
                .filter(
                    Submenu.menu_id == target_menu_id,
                )
                .group_by(Submenu.id)
            )
            query_result = await session.execute(query)
            submenus = query_result.all()
            submenu_list = []
            if not submenus:
                return submenus
            for submenu in submenus:
                item = submenu[0]
                item.dishes_count = submenu[1]
                submenu_list.append(item)
            return submenu_list

    @classmethod
    async def find_by_id(cls, target_menu_id, target_submenu_id):
        async with async_session_maker() as session:
            query = (
                select(
                    Submenu,
                    func.count(Dish.id),
                )
                .join(
                    Submenu.dishes,
                    isouter=True,
                )
                .filter(
                    Submenu.menu_id == target_menu_id,
                )
                .filter(
                    Submenu.id == target_submenu_id,
                )
                .group_by(
                    Submenu.id,
                )
            )
            query_result = await session.execute(query)
            submenu = query_result.one_or_none()
            if not submenu:
                raise HTTPException(status_code=404, detail="submenu not found")
            result_submenu = submenu[0]
            result_submenu.dishes_count = submenu[1]
            return result_submenu

    @classmethod
    async def check_object_exists(cls, target_menu_id, target_submenu_id):
        async with async_session_maker() as session:
            query = await session.execute(
                select(exists().where(and_(cls.model.menu_id == target_menu_id, cls.model.id == target_submenu_id))))
            res = query.first()[0]
            return res

    @classmethod
    async def add(cls, **data):
        data = await super().add(**data)
        data['dishes_count'] = 0
        return data

    @classmethod
    async def update_by_id(cls, menu_id, target_id, **changes):
        data = await super().update_by_id(target_id, **changes)
        data['dishes_count'] = 0
        data['menu_id'] = menu_id
        return data
