from fastapi import HTTPException
from sqlalchemy import select, exists, and_

from database.database import async_session_maker
from database.models import Submenu
from services.base import BaseServices


class SubmenuServices(BaseServices):
    model = Submenu

    @classmethod
    async def find_all(cls, target_menu_id):
        async with async_session_maker() as session:
            query = await session.execute(select(cls.model).filter_by(menu_id=target_menu_id))
            submenus = query.scalars().all()
            submenus_list = []
            if not submenus:
                return submenus_list
            for submenu in submenus:
                submenu.dishes_count = len(submenu.dishes)
                submenus_list.append(submenu)
            return submenus_list

    @classmethod
    async def find_by_id(cls, target_menu_id, target_submenu_id):
        async with async_session_maker() as session:
            query = await session.execute(select(cls.model).filter_by(menu_id=target_menu_id, id=target_submenu_id))
            submenu = query.scalars().one_or_none()
            if not submenu:
                raise HTTPException(status_code=404, detail="submenu not found")
            submenu.dishes_count = str(len(submenu.dishes))
            return submenu

    @classmethod
    async def check_object_exists(cls, target_menu_id, target_submenu_id):
        async with async_session_maker() as session:
            query = await session.execute(
                select(exists().where(and_(cls.model.menu_id == target_menu_id, cls.model.id == target_submenu_id))))
            res = query.first()[0]
            return res