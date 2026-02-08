from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

engine = create_async_engine("sqlite+aiosqlite:///./finance_tracker.db")

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    
    async with AsyncSessionLocal() as session:
        yield session