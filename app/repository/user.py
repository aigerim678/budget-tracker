from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas import UserCreate


async def get_all_users(session: AsyncSession) -> List[User]:
    result = await session.execute(select(User))
    return result.scalars().all()


async def get_user(username: str, session: AsyncSession) -> User:
    result = await session.execute(
        select(User).where(User.username == username)
    )
    return result.scalars().first()


async def authenticate_user(session: AsyncSession, username: str, password: str):
    from app.dependencies import verify_password
    user = await get_user(session=session, username=username)
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user


async def add_user(
        user: UserCreate,
        session: AsyncSession,
) -> User:
    from app.dependencies import get_password_hash
    password_hash = get_password_hash(password=user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password_hash=password_hash
    )
    session.add(new_user)
    try:
        await session.commit()
        await session.refresh(new_user)
        return new_user
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists.",
        )
