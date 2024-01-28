import asyncio

import pytest

base_url = "/api/v1/menus"

from database.database import Base, engine, async_session_maker
from main import app as fastapi_app

from fastapi.testclient import TestClient
from httpx import AsyncClient


@pytest.fixture(scope="session")
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def async_client():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as async_client:
        yield async_client


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
