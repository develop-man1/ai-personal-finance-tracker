from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from fastapi import HTTPException, status

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.utils.security import get_password_hash, verify_password


class AuthService:
    
    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)
    
    
    async def register_user(self, username: str, password: str) -> User:
        
        existing_user = await self.repository.get_by_username(username)
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        
        hashed_password = await asyncio.to_thread(get_password_hash, password)
        
        new_user = await self.repository.create(username=username, hashed_password=hashed_password)
        
        return new_user
    
    
    async def authenticate_user(self, username: str, password: str) -> User:
        
        user = await self.repository.get_by_username(username)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        password_is_correct = verify_password(password, user.hashed_password)
        
        if not password_is_correct:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        return user