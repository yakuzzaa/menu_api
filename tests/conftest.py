import asyncio

import pytest
from httpx import AsyncClient
from sqlalchemy_utils import create_database, database_exists

from database.database import Base, async_session_maker, engine
from main import app as fastapi_app


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    if not database_exists:
        create_database(engine.url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='function')
async def async_client():
    async with AsyncClient(app=fastapi_app, base_url='http://test') as async_client:
        yield async_client


@pytest.fixture(scope='function')
async def session():
    async with async_session_maker() as session:
        yield session
