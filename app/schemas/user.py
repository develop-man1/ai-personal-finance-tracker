from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    
    username: str = Field(..., min_length=2, max_length=15, description="Username our client")
    
    
class UserCreate(UserBase):
    
    password: str = Field(..., min_length=8, description="Password our client")
    
    
class UserResponse(UserBase): # Класс нужен для ответа от сервера, чтобы фильтровать исходящие запросы
    id: int
    created_at: datetime
    
    
    class Config:
        from_attributes = True