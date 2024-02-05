from sqlalchemy import and_, exists, select

from database.database import async_session_maker
from database.models import Dish
from repository.base import BaseRepository


class DishRepository(BaseRepository):
    model = Dish

    @classmethod
    async def read(cls, submenu_id) -> list[Dish]:
        async with async_session_maker() as session:
            query = await session.execute(select(cls.model).filter_by(submenu_id=submenu_id))
            return query.scalars().all()

    @classmethod
    async def read_by_id(cls, submenu_id, dish_id) -> Dish:
        async with async_session_maker() as session:
            query = await session.execute(select(cls.model).filter_by(submenu_id=submenu_id, id=dish_id))
            return query.scalars().one_or_none()

    @classmethod
    async def check_object_exists(cls, target_submenu_id, dish_id) -> bool:
        async with async_session_maker() as session:
            query = await session.execute(
                select(exists().where(and_(Dish.submenu_id == target_submenu_id, Dish.id == dish_id))))
            res = query.first()[0]
            return res
