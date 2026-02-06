from fastapi import FastAPI
from app.config import settings
from app.routes import auth_router, categories_router, transactions_router, users_router

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(transactions_router)
app.include_router(users_router)

@app.get("/")
def root():
    return {"status": "ok"}