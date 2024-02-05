from sqlalchemy import and_, distinct, exists, func, select

from database.database import async_session_maker
from database.models import Dish, Menu, Submenu
from repository.base import BaseRepository


class MenuRepository(BaseRepository):
    model = Menu

    @classmethod
    async def read(cls) -> list[Menu]:
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
            return query_result.all()

    @classmethod
    async def read_by_id(cls, menu_id) -> Menu:
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
                .filter(Menu.id == menu_id)
                .group_by(Menu.id)
            )
            query_result = await session.execute(query)
            return query_result.one_or_none()

    @classmethod
    async def check_object_exists(cls, target_id) -> bool:
        async with async_session_maker() as session:
            query = await session.execute(
                select(exists().where(and_(cls.model.id == target_id))))
            res = query.first()[0]
            return res
