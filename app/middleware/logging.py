import time
import logging
from fastapi import FastAPI, Request


logger = logging.getLogger("app_logger")


def setup_logging(app: FastAPI) -> None:
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )
    
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start_time = time.time()
        
        logger.info(f"→ {request.method} {request.url.path}") # запрос пришёл
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        
        logger.info(
            f"← {request.method} {request.url.path} "
            f"Status: {response.status_code} "
            f"Time: {process_time:.4f}s"
        )
        
        return response