from httpx import ASGITransport, AsyncClient
import pytest
from uuid import UUID

from app.main import application
from app.schemas.pydantic_schemas import User, DbUserData
from app.repositories.crud import find_user, create_user
from tests.utils_for_tests import test_users


@pytest.mark.asyncio
async def test_register(global_sessionmaker):
    async with AsyncClient(transport=ASGITransport(app=application), 
                           base_url="http://test")as ac:
        async with global_sessionmaker() as session:
            user: User = test_users[0]
            response = await ac.post(
                "/register", 
                json={
                    "email": user.email,
                    "password": user.password
                }
            )
            assert response.status_code == 201
            db_user: DbUserData = await find_user(db=session, user_data=user)
            assert db_user.password != user.password
            assert isinstance(db_user.uuid, UUID)
            assert response.json()["email"] == user.email


@pytest.mark.asyncio
async def test_token(global_sessionmaker):
    async with AsyncClient(transport=ASGITransport(app=application),
                       base_url="http://test")as ac:
        async with global_sessionmaker() as session:
            user: User = test_users[1]
            await create_user(db=session, user_data=user)
            response = await ac.post(
                "/get-token", 
                json={
                    "email": user.email,
                    "password": user.password
                }
            )
            assert response.status_code == 200
