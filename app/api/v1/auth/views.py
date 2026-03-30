from fastapi import Request, APIRouter, Response, Depends
from fastapi.responses import JSONResponse
# from app.schemas.auth import *
from .utils import *
from app.core import *
from app.schemas.auth import *


router = APIRouter(tags=["Auth"])


@router.post("/login", response_class=JSONResponse, summary="Авторизация пользователя")
async def login(body: AuthSchemaPostRequest):
    data = {}
    return data