from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import UserData
from app.schemas.pydantic_schemas import User, DbUser


async def create_user(db: AsyncSession, data: User) -> DbUser:
    new_user = UserData(user_uuid=data.user_uuid,
                        username=data.username)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return DbUser(user_uuid=new_user.user_uuid,
                  username=new_user.username,
                  created_at=new_user.created_at)
