import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import UserData, Posts
from app.schemas.pydantic_schemas import (PostData,
                                          User,
                                          DbUser,
                                          CreatePostReturn)


async def create_user(db: AsyncSession, data: User) -> DbUser:
    new_user = UserData(user_uuid=data.user_uuid,
                        username=data.username)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user, attribute_names=['created_at'])
    return DbUser(user_uuid=new_user.user_uuid,
                  username=new_user.username,
                  created_at=new_user.created_at)


async def create_post(db: AsyncSession,
                      data: PostData,
                      user_uuid: uuid.UUID) -> CreatePostReturn:
    new_post = Posts(content=data.content,
                     user_uuid=user_uuid)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post, attribute_names=['author'])
    return CreatePostReturn(content=new_post.content,
                            user_uuid=new_post.user_uuid,
                            author=new_post.author.username,
                            created_at=new_post.created_at)
