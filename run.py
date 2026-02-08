import asyncio
import sys
import uvicorn
from app.config import settings

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == '__main__':
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=8000,
        reload=settings.debug
    )