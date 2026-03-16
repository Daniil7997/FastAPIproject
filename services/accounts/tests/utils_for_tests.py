from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.users import AuthUsers
from app.core.security import hash_password
from app.schemas.pydantic_schemas import User
from app.dependencies.deps import get_db
from tests.test_config_db import settings_test


test_engine: AsyncEngine = create_async_engine(
    url=settings_test.url_db_asyncpg,
    echo=True,
    )

test_sessionmaker: async_sessionmaker = async_sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
    )


# async def test_get_db_overrides() -> AsyncGenerator[AsyncSession, None]:
#     db = test_sessionmaker()
#     await db.begin()
#     await db.begin_nested()
#     try:
#         yield db  
#     finally:
#         await db.rollback()
#         await db.close()


async def test_get_db_overrides() -> AsyncGenerator[AsyncSession, None]:
    async with test_sessionmaker() as db:
        yield db  


# async def get_session_from_generator():
#     generator = test_get_db_overrides()
#     session = await anext(generator)
#     return session

   
test_users = (
    User(email="user1@gmail.com", password="MyStrongPassword"),
    User(email="user2@gmail.com", password="strongpassword123"),
    User(email="user2@gmail.com", password="somestring4567890")
    )

