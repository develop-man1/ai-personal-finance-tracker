from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.user import User
from app.utils.security import decode_access_token


# =========================
# OAuth2 scheme
# =========================

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# =========================
# Current user dependency
# =========================

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    """
    Возвращает текущего авторизованного пользователя.
    
    Как это работает:
    1. Извлекает токен из заголовка Authorization (делает oauth2_scheme)
    2. Декодирует токен и получает username
    3. Ищет пользователя в БД по username
    4. Возвращает объект User или выбрасывает 401 ошибку
    """
    
    # Декодируем токен
    payload = decode_access_token(token)

    # Извлекаем username из токена (поле "sub")
    username: str | None = payload.get("sub")
    
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Ищем пользователя в БД
    # user = db.query(User).filter(User.username == username).first()
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user