from fastapi import Request, APIRouter, Response, Depends, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
# from app.schemas.auth import *
from .utils import *
from ..default import static_dir, templates
from app.core import *
from app.schemas.body.auth import *
from app.api.dependencies import DBManagerDep


router = APIRouter(tags=["Web"])



@router.get("/", response_class=HTMLResponse, summary="Получение экрана авторизации")
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@router.get("/main", response_class=HTMLResponse, summary="Получение главного экрана")
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="main.html"
    )


@router.get("/main/event/{event_id}", response_class=HTMLResponse, summary="Получение Экрана о мероприятии")
async def index(request: Request, event_id:int):
    return templates.TemplateResponse(
        request=request, name="event.html"
    )


@router.get("/test", response_class=HTMLResponse, summary="Получение Экрана о мероприятии")
async def index(request: Request):
    return templates.TemplateResponse(
        request=request, name="test.html"
    )