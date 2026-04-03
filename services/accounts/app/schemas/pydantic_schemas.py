import uuid

from pydantic import BaseModel, EmailStr, Field


PASSWORD_CONFIG = Field(min_length=3, max_length=20)


class User(BaseModel):
    email: EmailStr
    password: str = PASSWORD_CONFIG


class UserConfirmPass(BaseModel):
    current_password: str = PASSWORD_CONFIG
    new_password: str = PASSWORD_CONFIG


class CreateUserResponse(BaseModel):
    email: EmailStr
    user_uuid: uuid.UUID


class GetToken(BaseModel):
    access_token: str
    refresh_token: str


class AccessToken(BaseModel):
    access_token: str


class DbUserData(BaseModel):
    user_uuid: uuid.UUID
    email: EmailStr
    password: str


class TokensPayload(BaseModel):
    sub: uuid.UUID
    iat: int
    exp: int
    token_type: str
