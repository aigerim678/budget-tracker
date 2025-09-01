from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import UserOut, UserCreate
from app.repository import get_all_users, add_user
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=List[UserOut], description="For admins")
async def read_all_users(current_user: Annotated[UserOut, Depends(get_current_user)],
                         db: Annotated[AsyncSession, Depends(get_db)]) -> List[UserOut]:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await get_all_users(session=db)


@router.get("/me", response_model=UserOut)
async def read_me(current_user: Annotated[UserOut, Depends(get_current_user)], ):
    return current_user


@router.post("/", response_model=UserOut, description="Create a new user to login")
async def create_user(user: UserCreate, db: Annotated[AsyncSession, Depends(get_db)]):
    return await add_user(user=user, session=db)
