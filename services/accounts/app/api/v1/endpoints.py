from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.deps import get_db
from app.schemas.pydantic_schemas import User, CreateUserResponse, GetToken
from app.repositories.crud import create_user, find_user
from app.core.security import veryfi_password, create_tokens


router = APIRouter()


@router.post('/register', response_model=CreateUserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: User, db: AsyncSession = Depends(get_db)) -> CreateUserResponse:
    try:
        new_user = await create_user(db, user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=[{"loc": "email",
                                                                           "msg": "Email already exists"}])
    return CreateUserResponse(email=new_user.email, user_uuid=new_user.user_uuid)
 

@router.post('/get-token', response_model=GetToken, status_code=status.HTTP_200_OK)
async def get_token(user_data: User, db: AsyncSession = Depends(get_db)) -> GetToken:
    user_db_data = await find_user(db=db, user_data=user_data)
    exception_detail = [{"loc": ["email", "password"], "msg": "Invalid password or email", "type": "auth-failed"}]
    if not user_db_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=exception_detail)

    check_password: bool = veryfi_password(raw_password=user_data.password,
                                           hash_password=user_db_data.password)
    if not check_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=exception_detail)
    return create_tokens(user_db_data.user_uuid)
    