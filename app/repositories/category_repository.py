from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.category import Category


class CategoryRepository:
    
    def __init__(self, db: Session):
        self.db = db
        
    def get_by_id_and_user(self, category_id: int, user_id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()
        
    def get_by_name_and_user(self, category_name: str, user_id: int) -> Optional[Category]:
        return self.db.query(Category).filter(Category.name == category_name, Category.user_id == user_id).first()
    
    def get_by_type_and_user(self, category_type: str, user_id: int) -> List[Category]:
        return self.db.query(Category).filter(Category.type == category_type, Category.user_id == user_id).all()
    
    def create(self, name: str, category_type: str, user_id: int) -> Category:
        new_category = Category(name=name, type=category_type, user_id=user_id)
        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)
        return new_category