import uuid

from fastapi import HTTPException
from sqlalchemy import select, insert, exists,and_

from database import async_session_maker
from models.models import Submenu, Menu
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
                raise HTTPException(status_code=404, detail='Items not found')
            for submenu in submenus:
                submenu.dishes_count = str(len(submenu.dishes))
                submenus_list.append(submenu)
            return submenus_list

    @classmethod
    async def find_by_id(cls, target_menu_id, target_submenu_id):
        async with async_session_maker() as session:
            query = await session.execute(select(cls.model).filter_by(menu_id=target_menu_id, id=target_submenu_id))
            submenu = query.scalars().one()
            if not submenu:
                raise HTTPException(status_code=404, detail='Item not found')
            submenu.dishes_count = str(len(submenu.dishes))
            return submenu

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = await session.execute(
                select(exists().where(and_(Menu.id == data["menu_id"]))))
            res = query.first()[0]
            if not res:
                raise HTTPException(status_code=404, detail='Menu not found')
            data["id"] = uuid.uuid4()
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
            return data
