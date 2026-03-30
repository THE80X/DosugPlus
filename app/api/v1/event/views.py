from fastapi import Request, APIRouter, Response, Depends
from fastapi.responses import JSONResponse
# from app.schemas.auth import *
from .utils import *
from app.core import *
from app.schemas.auth import *


router = APIRouter(tags=["Event"])


@router.post("/create", response_class=JSONResponse, summary="Создание Мероприятия")
async def login(body: AuthSchemaPostRequest):
    data = {}

@router.get("/{event_id}/users", response_class=JSONResponse, summary="Получение списка участников мероприятия")
async def login(body: AuthSchemaPostRequest, event_id:int):
    data = {}

@router.get("/{event_id}", response_class=JSONResponse, summary="Получения мероприятия")
async def login(body: AuthSchemaPostRequest, event_id:int):
    data = {}