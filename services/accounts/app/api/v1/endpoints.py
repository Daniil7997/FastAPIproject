from fastapi import (Depends,
                     HTTPException,
                     APIRouter,
                     status)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.deps import get_db, verify_token
from app.schemas.pydantic_schemas import (User,
                                          CreateUserResponse,
                                          GetToken,
                                          TokensPayload,
                                          UserConfirmPass,
                                          AccessToken)
from app.repositories.crud import (create_user,
                                   find_user_by_email,
                                   change_user_data)
from app.core.security import (verify_password,
                               create_tokens,
                               hash_password)


router = APIRouter()


@router.post('/register',
             response_model=CreateUserResponse,
             status_code=status.HTTP_201_CREATED)
async def register_user(
        user: User,
        db: AsyncSession = Depends(get_db)) -> CreateUserResponse:
    try:
        new_user = await create_user(db, user)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=[{"loc": "email",
                                     "msg": "Email already exists",
                                     "type": "conflict"}])
    return CreateUserResponse(email=new_user.email,
                              user_uuid=new_user.user_uuid)


@router.post('/get-token',
             response_model=GetToken,
             status_code=status.HTTP_200_OK)
async def get_token(user_data: User,
                    db: AsyncSession = Depends(get_db)) -> GetToken:
    user_db_data = await find_user_by_email(db=db,
                                            user_email=user_data.email)
    exception_detail = [{"loc": ["email", "password"],
                         "msg": "Invalid password or email",
                         "type": "auth-failed"}]
    if not user_db_data:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=exception_detail)

    check_password: bool = verify_password(
        raw_password=user_data.password,
        hash_password=user_db_data.password
        )
    if not check_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=exception_detail)
    return create_tokens(user_db_data.user_uuid)


@router.post('/refresh',
             response_model=AccessToken,
             status_code=200)
async def refresh(refresh_payload: TokensPayload = Depends(verify_token)):
    if refresh_payload.token_type != 'refresh':
        raise HTTPException(
            status_code=403,
            detail=[{"loc": ["header", "Authorization"],
                     "msg": "this is not a refresh token",
                     "type": "access-denied"}]
        )
    new_tokens: GetToken = create_tokens(user_uuid=refresh_payload.sub)
    access_token: AccessToken = new_tokens.access_token
    return access_token


@router.post('/change-password', status_code=status.HTTP_200_OK)
async def change_password(user_data: UserConfirmPass,
                          payload: TokensPayload = Depends(verify_token),
                          db: AsyncSession = Depends(get_db)):
    async with change_user_data(db=db, user_uuid=payload.sub) as db_user:
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=[{"loc": ["header", "Authorization"],
                         "msg": "User with this token does not exists",
                         "type": "user-dont-exist"}]
                                )
        check_password: bool = verify_password(
            raw_password=user_data.current_password,
            hash_password=db_user[0].password
            )
        if not check_password:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=[{"loc": ["body", "password"],
                         "msg": "The passwords don't match",
                         "type": "access-denied"}]
                                )
        db_user[0].password = hash_password(user_data.new_password)
        return {"detail": "Password updated successfully"}
