from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException, status

from app.models.category import Category
from app.repositories.category_repository import CategoryRepository


class CategoryService:
    
    def __init__(self, db: AsyncSession):
        self.repository = CategoryRepository(db)
        
        
    async def create_category(self, name: str, category_type: str, user_id: int) -> Category:
        
        existing_category = await self.repository.get_by_name_and_user(name, user_id)
        
        if existing_category:
            raise HTTPException(status_code=400, detail="Category already exist")
        
        new_category = await self.repository.create(name=name, category_type=category_type, user_id=user_id)
        
        return new_category
    
    
    async def get_all_categories(self, user_id: int) -> List[Category]:
        
        return await self.repository.get_all_by_user(user_id)
    
    
    async def get_category_by_id(self, category_id: int, user_id: int) -> Category:
        
        my_category = await self.repository.get_by_id_and_user(category_id, user_id)
        
        if not my_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )
            
        return my_category