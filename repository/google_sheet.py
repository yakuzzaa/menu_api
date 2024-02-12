from decimal import Decimal

from sqlalchemy import select

from database.database import async_session_maker
from database.models import Dish, Menu, Submenu


async def create_update_menu(menu) -> dict:
    async with async_session_maker() as session:
        query = await session.execute(select(Menu).filter_by(id=menu['id']))
        result = query.scalar_one_or_none()

        if result:
            result.title = menu['title']
            result.description = menu['description']
            await session.commit()
        else:
            create_menu = Menu(id=menu['id'], title=menu['title'], description=menu['description'])
            session.add(create_menu)
            await session.commit()
            await session.refresh(create_menu)
        return menu


async def create_update_submenu(submenu) -> dict:
    async with async_session_maker() as session:
        query = await session.execute(select(Submenu).filter_by(id=submenu['id']))
        result = query.scalar_one_or_none()

        if result:
            result.title = submenu['title']
            result.description = submenu['description']
            await session.commit()
        else:
            create_submenu = Submenu(id=submenu['id'], menu_id=submenu['menu_id'], title=submenu['title'],
                                     description=submenu['description'])
            session.add(create_submenu)
            await session.commit()
            await session.refresh(create_submenu)
        return submenu


async def create_update_dish(dish) -> dict:
    async with async_session_maker() as session:
        query = await session.execute(select(Dish).filter_by(id=dish['id']))
        result = query.scalar_one_or_none()

        if result:
            result.title = dish['title']
            result.description = dish['description']
            result.price = Decimal(dish['price'])
            await session.commit()
        else:
            create_dish = Dish(id=dish['id'], submenu_id=dish['submenu_id'], title=dish['title'],
                               description=dish['description'],
                               price=Decimal(dish['price']))
            session.add(create_dish)
            await session.commit()
            await session.refresh(create_dish)
        return dish


async def check_and_delite_menu(menu_id) -> None:
    async with async_session_maker() as session:
        query = await session.execute(select(Menu).filter_by(id=menu_id))
        result = query.scalar_one_or_none()
        if result:
            await session.delete(result)
            await session.commit()


async def check_and_delite_submenu(submenu_id) -> None:
    async with async_session_maker() as session:
        query = await session.execute(select(Submenu).filter_by(id=submenu_id))
        result = query.scalar_one_or_none()
        if result:
            await session.delete(result)
            await session.commit()


async def check_and_delite_dish(dish_id) -> None:
    async with async_session_maker() as session:
        query = await session.execute(select(Dish).filter_by(id=dish_id))
        result = query.scalar_one_or_none()
        if result:
            await session.delete(result)
            await session.commit()
