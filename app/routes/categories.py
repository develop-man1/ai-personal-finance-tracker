from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.schemas.category import CategoryCreate, CategoryResponse
from app.services.category_service import CategoryService
from app.database import get_db
from app.models.user import User
from app.utils.dependencies import get_current_user


router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def add_category(request: CategoryCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    service = CategoryService(db)
    
    new_category = await service.create_category(name=request.name, category_type=request.type, user_id=current_user.id)
    
    return new_category


@router.get("/", response_model=List[CategoryResponse])
async def get_all_categories(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    service = CategoryService(db)
    
    categories = await service.get_all_categories(user_id=current_user.id)
    
    return categories


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    service = CategoryService(db)
    
    category = await service.get_category_by_id(category_id=category_id, user_id=current_user.id)
    
    return category