import asyncio
import uvicorn
from fastapi import FastAPI
from app.db import init_db
from fastapi.middleware.cors import CORSMiddleware
from app.api import main_router

app = FastAPI()

app.include_router(main_router)


if __name__ == "__main__":
    asyncio.run(init_db())
    uvicorn.run(
        "main:app",
        # host="0.0.0.0",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )