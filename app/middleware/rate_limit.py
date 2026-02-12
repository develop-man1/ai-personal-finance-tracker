from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse


limiter = Limiter(key_func=get_remote_address)


def setup_limiter(app: FastAPI) -> None:
    
    app.add_exception_handler(
        RateLimitExceeded,
        lambda request, exc: JSONResponse(
            status_code=429,
            content={"detail": "Too many requests"}
        ),
    )
    
    app.add_middleware(SlowAPIMiddleware)