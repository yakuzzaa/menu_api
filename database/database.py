import uuid

from sqlalchemy import Column, NullPool, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings

DB_URL: str = (
    f'postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}')
DATABASE_PARAMS: dict = {'poolclass': NullPool}

engine: create_async_engine = create_async_engine(url=DB_URL, **DATABASE_PARAMS)
async_session_maker: sessionmaker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
