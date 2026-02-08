from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.config import settings
from app.routes import auth_router, categories_router, transactions_router, users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Старт
    print("Программа запустилась")
    
    yield
    # Отключение
    print("Программа отключилась")


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    lifespan=lifespan,
)

app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(transactions_router)
app.include_router(users_router)


@app.get("/")
async def root():
    return {"status": "ok"}