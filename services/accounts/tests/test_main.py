from httpx import ASGITransport, AsyncClient
import pytest
from uuid import UUID

from app.main import application
from app.schemas.pydantic_schemas import (User, 
                                          DbUserData)
from app.repositories.crud import (find_user_by_email, 
                                   create_user)
from app.core.security import create_tokens
from tests.utils_for_tests import test_users


@pytest.mark.integration
@pytest.mark.asyncio
async def test_register(global_sessionmaker):
    async with AsyncClient(transport=ASGITransport(app=application), 
                           base_url="http://test")as ac:
        user: User = test_users[0]
        response = await ac.post(
            "/register", 
            json={
                "email": user.email,
                "password": user.password
            }
        )
        assert response.status_code == 201
        assert isinstance(UUID(response.json()['user_uuid']), UUID)
        assert response.json()["email"] == user.email


@pytest.mark.integration
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
            access_json = response.json()["access_token"]
            refresh_json = response.json()["refresh_token"]
            assert isinstance(access_json, str)
            assert isinstance(refresh_json, str)      


@pytest.mark.integration
@pytest.mark.asyncio
async def test_change_password(global_sessionmaker):
    async with AsyncClient(transport=ASGITransport(app=application), 
                           base_url="http://test")as ac:
        async with global_sessionmaker() as session:
            user: User = test_users[0]
            db_user_before = await create_user(db=session, user_data=user)
            tokens = create_tokens(db_user_before.user_uuid)
            response = await ac.post(
                "/change-password", 
                json={
                    "current_password": user.password,
                    "new_password": "veryStrongPas1957"
                },
                headers={"Authorization": f"Bearer {tokens.access_token}"}
            )
            assert response.status_code == 200
            db_user_after: DbUserData = await find_user_by_email(
                db=session, 
                user_email=user.email
                )
            assert db_user_after.password != db_user_before.password
