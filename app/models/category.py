from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False) # доход или расходы
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category", cascade="all, delete")