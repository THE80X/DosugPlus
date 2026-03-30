from fastapi import Request, APIRouter, Response, Depends
from fastapi.responses import JSONResponse
# from app.schemas.auth import *
from .utils import *
from app.core import *
from app.schemas.auth import *
from app.api.dependencies import DBManagerDep

router = APIRouter(tags=["User"])


@router.post("/create", response_class=JSONResponse, summary="Создание пользователя")
async def create_user(body: AuthSchemaPostRequest, response: Response, db: DBManagerDep):
    data = {}

@router.get("/events", response_class=JSONResponse, summary="Получение списка существующих мероприятий")
async def login(body: AuthSchemaPostRequest, response: Response, db: DBManagerDep):
    data = {}