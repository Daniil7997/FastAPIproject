import uuid

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    email: EmailStr
    password: str = Field(min_length=3, max_length=20)


class CreateUserResponse(BaseModel):
    email: EmailStr
    

class GetToken(BaseModel):
    access_token: str
    refresh_token: str


class DbUserData(BaseModel):
    uuid: uuid.UUID
    email: EmailStr
    password: str
    

class TokensPayload(BaseModel):
    sub: uuid.UUID
    iat: int
    exp: int
    token_type: str 
