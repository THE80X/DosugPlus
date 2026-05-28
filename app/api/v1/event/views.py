from fastapi import Request, APIRouter, Response, Depends
from fastapi.responses import JSONResponse
from datetime import datetime

from .utils import *

from app.core.exceptions import ERROR_DETAILS
from app.schemas.enum import ErrorCode

from app.core import *
from app.schemas.body.event import *
from app.schemas.body import ErrorItem
from app.schemas.enum import EventStatuses
from app.schemas.query import SortEventByFlagQuery
from app.models.user import UserModel
from app.services import UserService, AuthServiceJWT, EventService
from app.api.dependencies import DBManagerDep, TokenDep, get_current_user_from_bearer, CredDep

from app.schemas.enum import ErrorCode
from fastapi import HTTPException
from fastapi import status as HTTTP_STATUS


router = APIRouter(tags=["Event"])

@router.post("", response_class=JSONResponse, summary="Создание Мероприятия")
async def create_event(token: TokenDep,  
                       db: DBManagerDep,
                       body: CreateEventSchemaPostRequest, 
                       user: UserModel = Depends(get_current_user_from_bearer))->CreateEventSchemaPostResponse:
    service = EventService(db=db)
    result = await service.create_event_by_user(
        user_uuid=user.uuid,
        name=body.name,
        max_users_amount=body.max_users_amount,
        description=body.description,
        starts_at=datetime.strptime(body.starts_at, "%d.%m.%Y %H:%M"),
        ends_at=datetime.strptime(body.ends_at, "%d.%m.%Y %H:%M"),
        price=body.price
    )
    response = CreateEventSchemaPostResponse(owner_username=user.username, 
                                         event_id=result.id, 
                                         created_at=datetime.strftime(result.created_at, "%d.%m.%Y %H:%M"))
    return response


@router.get("", response_class=JSONResponse, summary="Получение списка существующих мероприятий")
async def get_event_list(token: TokenDep, 
                         db: DBManagerDep, 
                         event_flag: SortEventByFlagQuery,
                         user: UserModel = Depends(get_current_user_from_bearer),
                         limit: int = 10,
                         offset: int = 0)->list[EventSmallSchema]:
    service = EventService(db=db)
    result = await service.get_event_list(flag=event_flag, user_uuid=user.uuid, offset=offset, limit=limit)
    return result


@router.get("/{event_id}", response_class=JSONResponse, summary="Получения мероприятия")
async def get_event(token: TokenDep, 
                          db: DBManagerDep, 
                          event_id:int,
                          user: UserModel = Depends(get_current_user_from_bearer))->EventFullSchema:
    event_service = EventService(db=db)
    event = await event_service.get_event(event_id)
    event_owner, event = await event_service.can_user_see_event(event_id=event_id, user_uuid=user.uuid)

    result = await event_service.get_event_full_schema(event_owner, user, event)
    return result


@router.get("/{event_id}/users", response_class=JSONResponse, summary="Получение списка участников мероприятия")
async def get_event_users_list(token: TokenDep,
                               db: DBManagerDep,
                               event_id:int,
                               status: str = None,
                               user: UserModel = Depends(get_current_user_from_bearer),
                               limit: int = 10,
                               offset: int = 0):
    event_service = EventService(db=db)
    event = await event_service.get_event(event_id=event_id)
    if event.event_owner != user.uuid:
        raise HTTPException(status_code=HTTTP_STATUS.HTTP_400_BAD_REQUEST, detail=ErrorCode.USER_IS_NOT_OWNER.value)
    
    result = await event_service.get_users_event_by_status(event_id=event_id, status=status, limit=limit, offset=offset)
    return result
    """
    1. Проверяем существование этого мероприятия
    2. Проверяем может ли пользователь видеть это мероприятие
    3. Проверяем является ли пользователь владельцем мероприятия
    4. Получаем список пользователей с их последними статусами.
    5. фильтруем по "signed"
    """
    pass


@router.get("/{event_id}/users/me", response_class=JSONResponse, summary="Получение своего статуса")
async def get_event_user_info_status(cred: TokenDep,
                db: DBManagerDep, 
                event_id:int, 
                user: UserModel = Depends(get_current_user_from_bearer)):
    event_service = EventService(db=db)

    event = await event_service.get_event(event_id)
    event_owner, event = await event_service.can_user_see_event(event_id=event_id, user_uuid=user.uuid)

    
    result = await event_service.get_status_for_event_by_user_and_event(user_uuid=user.uuid, event_id=event.id)
    return result


@router.post("/{event_id}/users/me", response_class=JSONResponse, summary="Изменение своего статуса")
async def change_my_user_status(body:EventSchemaUserStatusPost,
                cred: TokenDep,
                db: DBManagerDep, 
                event_id:int, 
                sender_user: UserModel = Depends(get_current_user_from_bearer))->EventStatuses:
    event_service = EventService(db=db)
    user_service = UserService(db=db)
    
    event = await event_service.get_event(event_id)
    target_user = await user_service.get_user(username=sender_user.username)

    print(target_user)

    event_owner, event = await event_service.can_user_see_event(event_id=event_id, user_uuid=sender_user.uuid)
    
    event_full_schema = await event_service.get_event_full_schema(event_owner, sender_user, event)

    result  = await event_service.update_user_status(sender_user, event_full_schema, sender_user, body.status)
    return result.status


@router.post("/{event_id}/users/{username}", response_class=JSONResponse, summary="Изменение статуса выбранного пользователя")
async def change_user_status(body:EventSchemaUserStatusPost,
                username:str,
                cred: TokenDep,
                db: DBManagerDep, 
                event_id:int, 
                sender_user: UserModel = Depends(get_current_user_from_bearer))->EventStatuses:
    event_service = EventService(db=db)
    user_service = UserService(db=db)

    event = await event_service.get_event(event_id)
    target_user = await user_service.get_user(username=username)
    event_owner, event = await event_service.can_user_see_event(event_id=event_id, user_uuid=sender_user.uuid)
    
    event_full_schema = await event_service.get_event_full_schema(event_owner, sender_user, event)

    result  = await event_service.update_user_status(target_user, event_full_schema, sender_user, body.status)
    return result.status