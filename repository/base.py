from typing import Generic, TypeVar

from sqlalchemy import ValuesBase, delete, insert, update
from sqlalchemy.sql.dml import DMLWhereBase, Update

from database.database import Base, async_session_maker

T_Base = TypeVar('T_Base', bound=Base)


class BaseRepository(Generic[T_Base]):
    model: T_Base

    @classmethod
    async def create(cls, **data) -> None:
        async with async_session_maker() as session:
            query: ValuesBase = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_by_id(cls, target_id, **changes) -> None:
        async with async_session_maker() as session:
            query: Update = update(cls.model).where(cls.model.id == target_id).values(**changes)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete_by_id(cls, target_id) -> None:
        async with async_session_maker() as session:
            query: DMLWhereBase = delete(cls.model).where(cls.model.id == target_id)
            await session.execute(query)
            await session.commit()
