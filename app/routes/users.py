from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.user import UserResponse
from app.models.user import User
from app.utils.dependencies import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user