from datetime import datetime
import uuid

from pydantic import BaseModel, Field


username_config = Field(max_length=20)


class User(BaseModel):
    user_uuid: uuid.UUID
    username: str = username_config


class RegisterUser(BaseModel):
    username: str


class DbUser(BaseModel):
    user_uuid: uuid.UUID
    username: str = username_config
    created_at: datetime


class GetToken(BaseModel):
    access_token: str
    refresh_token: str


class TokensPayload(BaseModel):
    sub: uuid.UUID
    iat: int
    exp: int
    token_type: str
