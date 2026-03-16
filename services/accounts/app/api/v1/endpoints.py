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
        print('CREATE_USER не пройдено')
        new_user = await create_user(db, user)
        print('CREATE_USER пройдено')
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already exists')
    except Exception as ERROR: 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Registration failed")
    return CreateUserResponse(email=new_user.email)
 

@router.post('/get-token', response_model=GetToken, status_code=status.HTTP_200_OK)
async def get_token(user_data: User, db: AsyncSession = Depends(get_db)) -> GetToken:
    user_db_data = await find_user(db=db, user_data=user_data)
    if not user_db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    check_password: bool = veryfi_password(raw_password=user_data.password,
                                           hash_password=user_db_data.password)
    if not check_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="passwords do not match")
    return create_tokens(user_db_data.uuid)
    