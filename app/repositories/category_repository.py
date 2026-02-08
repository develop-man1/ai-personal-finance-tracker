from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List

from app.models.category import Category


class CategoryRepository:
    
    def __init__(self, db: AsyncSession):
        self.db = db
        
    async def get_by_id_and_user(self, category_id: int, user_id: int) -> Optional[Category]:
        stmt = select(Category).where(Category.id == category_id, Category.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all_by_user(self, user_id: int) -> List[Category]:
        stmt = select(Category).where(Category.user_id == user_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
        
    async def get_by_name_and_user(self, category_name: str, user_id: int) -> Optional[Category]:
        stmt = select(Category).where(Category.name == category_name, Category.user_id == user_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_type_and_user(self, category_type: str, user_id: int) -> List[Category]:
        stmt = select(Category).where(Category.type == category_type, Category.user_id == user_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def create(self, name: str, category_type: str, user_id: int) -> Category:
        new_category = Category(name=name, type=category_type, user_id=user_id)
        self.db.add(new_category)
        await self.db.commit()
        await self.db.refresh(new_category)
        return new_category