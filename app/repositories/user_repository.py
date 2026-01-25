from sqlalchemy.orm import Session
from typing import Optional

from app.models.user import User


class UserRepository:
    
    def __init__(self, db: Session):
        self.db = db
        
    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def create(self, username: str, hashed_password: str) -> User:
        new_user = User(username=username, hashed_password=hashed_password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user