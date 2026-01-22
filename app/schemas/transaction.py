from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime


class TransactionBase(BaseModel):
    
    amount: Decimal = Field(..., description="Money spent")
    description: Optional[str] = Field(None, description="Just description")
    category_id: int = Field(..., description="Category ID")
    

class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    
    id: int
    date: datetime
    created_at: datetime
    
    
    class Config:
        from_attributes = True