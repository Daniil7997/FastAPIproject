import uuid
from datetime import datetime

from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, Integer, DateTime, func


class Base(MappedAsDataclass, DeclarativeBase, kw_only=True):
    pass


class AuthUsers(Base):
    __tablename__ = "auth_users"

    user_uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid7,
        init=False
    )
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=func.now(), onupdate=func.now())


class RefreshTokens(Base):
    __tablename__ = "refresh_tokens"
    
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    user_uuid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
         init=True
    )
    refresh_token: Mapped[str] = mapped_column(String(256))
    updated_at: Mapped[datetime] = mapped_column(DateTime(), default=func.now(), onupdate=func.now())
    