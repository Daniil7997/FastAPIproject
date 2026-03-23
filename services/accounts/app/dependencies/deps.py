from typing import AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.db.database import async_session_factory
from app.core.config import settings
from app.core.security import decode_token
from app.schemas.pydantic_schemas import TokensPayload


auth_scheme = HTTPBearer()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as db:
        yield db  

def verify_token(token: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> TokensPayload:
    payload: TokensPayload = decode_token(token=token.credentials)
    return payload


