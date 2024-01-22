import uuid

from sqlalchemy import insert, update, delete

from database.database import async_session_maker


class BaseServices:
    model = None

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            data["id"] = uuid.uuid4()
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()
            return data

    @classmethod
    async def update_by_id(cls, target_id, **changes):
        async with async_session_maker() as session:
            query = update(cls.model).where(cls.model.id == target_id).values(**changes)
            await session.execute(query)
            await session.commit()
            changes["id"] = target_id
            return changes

    @classmethod
    async def delete_by_id(cls, target_id):
        async with async_session_maker() as session:
            query = delete(cls.model).where(cls.model.id == target_id)
            await session.execute(query)
            await session.commit()

            return f"Запись с id {target_id} удалена."


