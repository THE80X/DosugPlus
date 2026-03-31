from fastapi import Request, APIRouter, Response, Depends
from fastapi.responses import JSONResponse
# from app.schemas.auth import *
from .utils import *
from app.core import *
from app.schemas.auth import *
from app.api.dependencies import DBManagerDep


router = APIRouter(tags=["Event"])


@router.post("", response_class=JSONResponse, summary="Создание Мероприятия")
async def login():
    data = {}


@router.get("", response_class=JSONResponse, summary="Получение списка существующих мероприятий")
async def login():
    data = {}


@router.delete("/{event_id}", response_class=JSONResponse, summary="Удаление Мероприятия")
async def login(event_id:int):
    data = {}

@router.delete("/{event_id}/user/{username}", response_class=JSONResponse, summary="Исключение пользователя из мероприятия")
async def login(event_id:int, username:str):
    data = {}

@router.get("/{event_id}/user/{username}", response_class=JSONResponse, summary="Получение пользователя мероприятия")
async def login(event_id:int, username:str):
    data = {}

@router.get("/{event_id}/user", response_class=JSONResponse, summary="Получение списка участников мероприятия")
async def login(event_id:int):
    data = {}

@router.get("/{event_id}", response_class=JSONResponse, summary="Получения мероприятия")
async def login(event_id:int):
    data = {}

@router.put("/{event_id}", response_class=JSONResponse, summary="Обновление информации о мероприятии")
async def login(event_id:int):
    data = {}