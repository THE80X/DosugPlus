import asyncio
import uvicorn
from app.db import init_db
from fastapi.middleware.cors import CORSMiddleware
from app.api import main_router
from app.web_views.default import static_dir
from app.web_views import web_router
from app.core.config import app


from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


app.include_router(main_router)
app.include_router(web_router)

app.mount("/static", static_dir, name="static")


class CookieToBearerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Читаем access_token из cookie
        access_token = request.cookies.get("access_token")
        
        # Если токен есть и Authorization header отсутствует
        if access_token and not request.headers.get("Authorization"):
            # Подменяем заголовки
            request.scope["headers"] = list(request.scope["headers"])
            request.scope["headers"].append(
                (b"authorization", f"Bearer {access_token}".encode())
            )
        
        response = await call_next(request)
        return response


app.add_middleware(CookieToBearerMiddleware)


if __name__ == "__main__":
    asyncio.run(init_db())
    uvicorn.run(
        "main:app",
        # host = "localhost",
        # host="192.168.0.1",
        host="192.168.1.100",
        port=8000,
        reload=True,
    )