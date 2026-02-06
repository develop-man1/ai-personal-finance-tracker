from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from decimal import Decimal
from typing import List

from app.models.transaction import Transaction
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.category_repository import CategoryRepository


class TransactionService:
    
    def __init__(self, db: Session):
        self.transaction_repository = TransactionRepository(db)
        self.category_repository = CategoryRepository(db)
        
    
    def create_transaction(self, user_id: int, category_id: int, amount: Decimal, date: datetime, description=None) -> Transaction:
        
        existing_category = self.category_repository.get_by_id_and_user(category_id, user_id)
        
        if not existing_category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )
            
        set_time_transaction = date if date else datetime.now()
        
        new_transaction = self.transaction_repository.create(user_id=user_id, category_id=category_id, amount=amount, date=set_time_transaction, description=description)
        
        return new_transaction
    
    
    def get_all_transactions_by_user(self, user_id: int, category=None, date_from=None) -> List[Transaction]:
        
        all_transactions = self.transaction_repository.get_all_by_user(user_id)
        
        if category:
            all_transactions = [t for t in all_transactions if t.category.name == category]
            
        if date_from:
            all_transactions = [t for t in all_transactions if t.created_at >= date_from]
            
        return all_transactions
    
    
    def delete_transaction(self, transaction_id: int, user_id: int) -> None:
        
        my_transaction = self.transaction_repository.get_by_id(transaction_id)
        
        if not my_transaction:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found",
            ) 
            
        if my_transaction.user_id != user_id: # type: ignore
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Transaction not found",
            )
            
        self.transaction_repository.delete(transaction_id)
        
    
    def calculate_balance(self, user_id: int) -> dict:
        
        all_transactions = self.transaction_repository.get_all_by_user(user_id)
        
        income = Decimal(0)
        expense = Decimal(0)
        
        for transaction in all_transactions:
            if transaction.category.type == "Income":
                income += transaction.amount
            elif transaction.category.type == "Expense":
                expense += transaction.amount
                
        balance = income - expense
        
        return {
            "income": income,
            "expense": expense,
            "balance": balance
        }