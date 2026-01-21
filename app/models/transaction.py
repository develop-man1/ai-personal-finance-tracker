from sqlalchemy import Column, String, Integer, ForeignKey, Text, Numeric, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..database import Base


class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(10, 2), index=True)
    date = Column(DateTime(timezone=True), nullable=False)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")