from fastapi import FastAPI
from app.middleware.cors import setup_cors
from app.middleware.logging import setup_logging
from app.middleware.rate_limit import setup_limiter
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

setup_cors(app)
setup_logging(app)
setup_limiter(app)

app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(transactions_router)
app.include_router(users_router)


@app.get("/")
async def root():
    return {"status": "ok"}