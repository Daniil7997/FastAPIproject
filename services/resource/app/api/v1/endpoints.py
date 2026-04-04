from fastapi import (Depends,
                     HTTPException,
                     APIRouter,
                     status)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.deps import get_db, verify_token
from app.schemas.pydantic_schemas import (CreatePostReturn,
                                          DbUser,
                                          PostData,
                                          User,
                                          TokensPayload,
                                          RegisterUser)
from app.repositories.crud import create_user, create_post


router = APIRouter()


@router.post('/create-user',
             response_model=DbUser,
             status_code=status.HTTP_201_CREATED)
async def register_user(user_data: RegisterUser,
                        db: AsyncSession = Depends(get_db),
                        payload: TokensPayload = Depends(verify_token)
                        ) -> DbUser:
    data = User(user_uuid=payload.sub, username=user_data.username)
    try:
        db_data: DbUser = await create_user(db=db, data=data)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=[{"loc": "email",
                                     "msg": "Profile already exists",
                                     "type": "conflict"}])
    return db_data


@router.post('/send-post',
             response_model=CreatePostReturn,
             status_code=status.HTTP_201_CREATED)
async def send_post(postdata: PostData,
                    db: AsyncSession = Depends(get_db),
                    payload: TokensPayload = Depends(verify_token)
                    ) -> DbUser:
    try:
        new_post: CreatePostReturn = await create_post(db=db,
                                                       user_uuid=payload.sub,
                                                       data=postdata)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=[
                {
                    "loc": ["body", "user_uuid"],
                    "msg": "profile not created",
                    "type": "profile-not-created"
                }
            ]
        )
    return new_post
