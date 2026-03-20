from httpx import ASGITransport, AsyncClient
import pytest
from uuid import UUID

from app.main import application
from app.schemas.pydantic_schemas import User, DbUserData, TokensPayload
from app.repositories.crud import find_user, create_user
from app.core.security import decode_token
from tests.utils_for_tests import test_users


@pytest.mark.integration
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
            assert isinstance(db_user.user_uuid, UUID)
            assert isinstance(UUID(response.json()['user_uuid']), UUID)
            assert response.json()['user_uuid'] == str(db_user.user_uuid)
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
            access_token:TokensPayload = decode_token(token=response.json()["access_token"])
            refresh_token:TokensPayload = decode_token(token=response.json()["refresh_token"])
            db_user:DbUserData = await find_user(db=session, user_data=user)
            assert access_token.sub == db_user.user_uuid
            assert refresh_token.sub == db_user.user_uuid
            assert access_token.token_type == 'access'
            assert refresh_token.token_type == 'refresh'
            assert access_token.iat < access_token.exp
            assert refresh_token.iat < refresh_token.exp
            assert len(str(access_token.iat)) == 10
            assert len(str(refresh_token.iat)) == 10
