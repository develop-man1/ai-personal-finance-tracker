import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from unittest.mock import patch  # ← добавь

from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.models.category import Category
from app.utils.security import get_password_hash

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest_asyncio.fixture(scope="function")
async def db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def client(db):
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    # ← Отключаем rate limiter в тестах
    with patch("app.middleware.rate_limit.limiter.enabled", False):
        async with AsyncClient(
            transport=ASGITransport(app=app),  # type: ignore
            base_url="http://test"
        ) as ac:
            yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(db):
    user = User(
        username="testuser",
        hashed_password=get_password_hash("testpassword123")
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest_asyncio.fixture
async def auth_token(client, test_user):
    response = await client.post(
        "/auth/login",
        data={"username": "testuser", "password": "testpassword123"}
    )
    return response.json()["access_token"]


@pytest_asyncio.fixture
async def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest_asyncio.fixture
async def test_category(db, test_user):
    category = Category(name="Food", type="Expense", user_id=test_user.id)
    db.add(category)
    await db.commit()
    await db.refresh(category)
    return category