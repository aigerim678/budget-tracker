from typing import List, Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import CategoryOut, CategoryCreate, UserOut
from app.repository import get_all_categories, get_category_by_id, add_category, get_my_categories
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/category",
    tags=["Category"],
    responses={404: {"description": "Not found"}}
)


@router.get("/all", response_model=List[CategoryOut], dependencies=[Depends(get_current_user)])
async def read_all_categories(db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_all_categories(session=db)


@router.get("/mine", response_model=List[CategoryOut])
async def read_my_categories(current_user: Annotated[UserOut, Depends(get_current_user)],
                             db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_my_categories(user_id=current_user.id, session=db)


@router.get("/{id}", response_model=CategoryOut, dependencies=[Depends(get_current_user)])
async def read_category(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_category_by_id(category_id=id, session=db)


@router.post("/create", response_model=CategoryOut)
async def create_category(category: CategoryCreate, current_user: Annotated[UserOut, Depends(get_current_user)],
                          db: Annotated[AsyncSession, Depends(get_db)]):
    return await add_category(category=category, user_id=current_user.id, session=db)
