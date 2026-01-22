from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


class CategoryBase(BaseModel):
    
    name: str = Field(..., min_length=2, max_length=20, description="Category Name")
    type: Literal["Income", "Expense"] = Field(..., description="Type of category")


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    
    id: int
    created_at: datetime
    
    
    class Config:
        from_attributes = True