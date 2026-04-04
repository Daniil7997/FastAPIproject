from datetime import datetime
import uuid

from pydantic import BaseModel, Field


username_config = Field(max_length=20)
post_config = Field(max_length=750)


class User(BaseModel):
    user_uuid: uuid.UUID
    username: str = username_config


class RegisterUser(BaseModel):
    username: str


class DbUser(BaseModel):
    user_uuid: uuid.UUID
    username: str = username_config
    created_at: datetime


class TokensPayload(BaseModel):
    sub: uuid.UUID
    iat: int
    exp: int
    token_type: str


class PostData(BaseModel):
    content: str = post_config


class CreatePostReturn(BaseModel):
    content: str = post_config
    user_uuid: uuid.UUID
    author: str
    created_at: datetime
