from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.models.user import User


class UserRepository:
    
    def __init__(self, db: AsyncSession):
        
        self.db = db
        
    async def get_by_username(self, username: str) -> Optional[User]:
        
        stmt = select(User).where(User.username == username)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
        
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        
        result = await self.db.get(User, user_id)
        return result
    
    async def create(self, username: str, hashed_password: str) -> User:
        
        new_user = User(username=username, hashed_password=hashed_password)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user