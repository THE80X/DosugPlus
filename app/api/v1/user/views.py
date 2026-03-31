from fastapi import Request, APIRouter, Response, Depends
from fastapi.responses import JSONResponse
# from app.schemas.auth import *
from .utils import *
from app.core import *
from app.schemas.auth import *
from app.api.dependencies import DBManagerDep

router = APIRouter(tags=["User"])


@router.get("/event/created", response_class=JSONResponse, summary="Получение списка мероприятий, которые создал пользователь")
async def login(username:str, response: Response, db: DBManagerDep):
    data = {}


@router.get("/event/signed", response_class=JSONResponse, summary="Получение списка мероприятий, на которые записан пользователь")
async def login(username:str, response: Response, db: DBManagerDep):
    data = {}


@router.delete("/event/{event_id}", response_class=JSONResponse, summary="Покидание мероприятия")
async def login(username:str, event_id:int, response: Response, db: DBManagerDep):
    data = {}


@router.post("/event/{event_id}", response_class=JSONResponse, summary="Запись на мероприятие")
async def login(username:str, event_id:int, response: Response, db: DBManagerDep):
    data = {}