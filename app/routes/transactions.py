from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.schemas.transaction import TransactionCreate, TransactionResponse
from app.services.transaction_service import TransactionService
from app.database import get_db
from app.models.user import User
from app.utils.dependencies import get_current_user


router = APIRouter(
    prefix="/transactions",
    tags=["transactions"]
)


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(request: TransactionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    service = TransactionService(db)
    
    new_transaction = service.create_transaction(user_id=current_user.id, category_id=request.category_id, amount=request.amount, date=datetime.now(), description=request.description)

    return new_transaction


@router.get("/", response_model=List[TransactionResponse])
def get_all_transactions_by_user(category: Optional[str] = None, date_from: Optional[datetime] = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    service = TransactionService(db)
    
    transactions = service.get_all_transactions_by_user(user_id=current_user.id, category=category, date_from=date_from)
    
    return transactions


@router.get("/balance")
def get_balance(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    service = TransactionService(db)
    
    balance = service.calculate_balance(user_id=current_user.id)
    
    return balance


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    service = TransactionService(db)
    
    service.delete_transaction(transaction_id=transaction_id, user_id=current_user.id)
    
    return None