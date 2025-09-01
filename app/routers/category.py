from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import CategoryOut, CategoryCreate, UserOut
from app.repository import get_all_categories, get_category_by_id, add_category, get_my_categories
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}}
)


@router.get("/all-users", response_model=List[CategoryOut], description="For admins")
async def read_all_categories(current_user: Annotated[UserOut, Depends(get_current_user)],
                              db: Annotated[AsyncSession, Depends(get_db)]):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await get_all_categories(session=db)


@router.get("/", response_model=List[CategoryOut])
async def read_my_categories(current_user: Annotated[UserOut, Depends(get_current_user)],
                             db: Annotated[AsyncSession, Depends(get_db)]):
    return await get_my_categories(user_id=current_user.id, session=db)


@router.get("/{id}", response_model=CategoryOut)
async def read_category(id: int, db: Annotated[AsyncSession, Depends(get_db)]):
    category = await get_category_by_id(category_id=id, session=db)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/", response_model=CategoryOut)
async def create_category(category: CategoryCreate,
                          current_user: Annotated[UserOut, Depends(get_current_user)],
                          db: Annotated[AsyncSession, Depends(get_db)]):
    return await add_category(category=category, user_id=current_user.id, session=db)
