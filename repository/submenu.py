from sqlalchemy import and_, exists, func, select

from database.database import async_session_maker
from database.models import Dish, Submenu
from repository.base import BaseRepository


class SubmenuRepository(BaseRepository):
    model = Submenu

    @classmethod
    async def read(cls, menu_id) -> list[Submenu]:
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
                    Submenu.menu_id == menu_id,
                )
                .group_by(Submenu.id)
            )
            query_result = await session.execute(query)
            return query_result.all()

    @classmethod
    async def read_by_id(cls, menu_id, submenu_id) -> Submenu:
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
                    Submenu.menu_id == menu_id,
                )
                .filter(
                    Submenu.id == submenu_id,
                )
                .group_by(
                    Submenu.id,
                )
            )
            query_result = await session.execute(query)
            return query_result.one_or_none()

    @classmethod
    async def check_object_exists(cls, target_menu_id, target_submenu_id) -> bool:
        async with async_session_maker() as session:
            query = await session.execute(
                select(exists().where(and_(cls.model.menu_id == target_menu_id, cls.model.id == target_submenu_id))))
            res = query.first()[0]
            return res
