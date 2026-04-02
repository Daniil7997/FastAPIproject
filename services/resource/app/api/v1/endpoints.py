from fastapi import (Depends,
                     HTTPException,
                     APIRouter,
                     status)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.deps import get_db, verify_token
from app.schemas.pydantic_schemas import DbUser, User, TokensPayload
from app.repositories.crud import create_user

router = APIRouter()


@router.post('/create-user')
async def register_user(username: str,
                        db: AsyncSession = Depends(get_db),
                        payload: TokensPayload = Depends(verify_token)
                        ) -> DbUser:
    data = User(user_uuid=payload.sub, username=username)
    try:
        db_data: DbUser = await create_user(db=db, data=data)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=[{"loc": "email",
                                     "msg": "Email already exists",
                                     "type": "conflict"}])
    return db_data
