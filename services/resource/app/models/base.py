import uuid
from datetime import datetime

from sqlalchemy.orm import (MappedAsDataclass,
                            DeclarativeBase,
                            Mapped,
                            mapped_column,
                            relationship)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey, String, func, DateTime


class Base(MappedAsDataclass, DeclarativeBase, kw_only=True):
    pass


class UserData(Base):
    __tablename__ = "user_data"

    user_uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        init=True
    )
    username: Mapped[str] = mapped_column(String(20))

    posts: Mapped[list["Posts"]] = relationship(
        "Posts", back_populates="author", init=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(),
                                                 default=func.now(),
                                                 init=False)


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user_data.user_uuid"),
        init=True
    )
    author: Mapped["UserData"] = relationship(
        "UserData", back_populates="posts", init=False)
    content: Mapped[str] = mapped_column(String(750))
    created_at: Mapped[datetime] = mapped_column(DateTime(),
                                                 default=func.now(),
                                                 init=False)
