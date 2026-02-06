from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
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
def add_category(request: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    service = CategoryService(db)
    
    new_category = service.create_category(name=request.name, category_type=request.type, user_id=current_user.id)
    
    return new_category


@router.get("/", response_model=List[CategoryResponse])
def get_all_categories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    service = CategoryService(db)
    
    categories = service.get_all_categories(user_id=current_user.id)
    
    return categories


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    service = CategoryService(db)
    
    category = service.get_category_by_id(category_id=category_id, user_id=current_user.id)
    
    return category