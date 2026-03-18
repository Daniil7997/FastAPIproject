import pytest
import asyncio
import sys

from sqlalchemy import delete

from app.main import application
from app.dependencies.deps import get_db
from app.models.users import AuthUsers
from tests.utils_for_tests import test_get_db_overrides, test_sessionmaker


# if sys.platform == "win32":
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


@pytest.fixture(scope="function", autouse=True)
async def setup_db_override():
    application.dependency_overrides[get_db] = test_get_db_overrides
    yield
    application.dependency_overrides.clear()


@pytest.fixture(scope='function', autouse=True)
async def db_truncate(setup_db_override):
    async with test_sessionmaker() as session:
        await session.execute(delete(AuthUsers))
        await session.commit()
        