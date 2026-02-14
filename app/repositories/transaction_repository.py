from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import Optional, List
from decimal import Decimal
from datetime import datetime

from app.models.transaction import Transaction


class TransactionRepository:
    def __init__(self, db: AsyncSession):
        
        self.db = db
        
    async def get_by_id(self, transaction_id: int) -> Optional[Transaction]:
        stmt = select(Transaction).where(Transaction.id == transaction_id)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
        
    
    async def get_all_by_user(self, user_id: int) -> List[Transaction]:
        # return self.db.query(Transaction).filter(Transaction.user_id == user_id).all()
        stmt = select(Transaction).where(Transaction.user_id == user_id).options(selectinload(Transaction.category))
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    async def create(self, user_id: int, category_id: int, amount: Decimal, date: datetime, description=None,) -> Transaction:
        # new_transaction = Transaction(user_id=user_id, category_id=category_id, amount=amount, date=date, description=description)
        # self.db.add(new_transaction)
        # self.db.commit()
        # self.db.refresh(new_transaction)
        # return new_transaction
        new_transaction = Transaction(user_id=user_id, category_id=category_id, amount=amount, date=date, description=description)
        self.db.add(new_transaction)
        await self.db.commit()
        await self.db.refresh(new_transaction)
        return new_transaction

    async def delete(self, transaction_id: int) -> None:
        # transaction = self.get_by_id(transaction_id)
        # if transaction:
        #     self.db.delete(transaction)
        #     self.db.commit()
        stmt = select(Transaction).where(Transaction.id == transaction_id)
        result = await self.db.execute(stmt)
        transaction = result.scalar_one_or_none()
        
        if transaction:
            _ = self.db.delete(transaction)
            await self.db.commit()
        