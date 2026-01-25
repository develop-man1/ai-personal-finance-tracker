from sqlalchemy.orm import Session
from typing import Optional
from decimal import Decimal
from datetime import datetime

from app.models.transaction import Transaction


class TransactionRepository:
    def __init__(self, db: Session):
        self.db = db
        
    def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        return self.db.query(Transaction).filter(Transaction.id == transaction_id).first()
    
    def create(self, user_id: int, category_id: int, amount: Decimal, date: datetime, description=None,) -> Transaction:
        new_transaction = Transaction(user_id=user_id, category_id=category_id, amount=amount, date=date, description=description)
        self.db.add(new_transaction)
        self.db.commit()
        self.db.refresh(new_transaction)
        return new_transaction