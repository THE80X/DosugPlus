from fastapi import Request, APIRouter, Response, Depends
from fastapi.responses import JSONResponse

from .utils import *

from app.core import *
from app.schemas.body.auth import *
from app.schemas.query import SortEventByFlagQuery
from app.models.user import UserModel
from app.api.dependencies import DBManagerDep, TokenDep, get_current_user_from_bearer

router = APIRouter(tags=["User"])


# @router.delete("/event/{event_id}", response_class=JSONResponse, summary="Покидание мероприятия")
# async def login(token: TokenDep, 
#                 db: DBManagerDep,
#                 event_id: int,
#                 user: UserModel = Depends(get_current_user_from_bearer)):
#     data = {}


# @router.get("/event/{event_id}", response_class=JSONResponse, summary="Получение статуса пользователя для мероприятия")
# async def login(token: TokenDep, 
#                 db: DBManagerDep,
#                 event_id: int,
#                 user: UserModel = Depends(get_current_user_from_bearer)):
#     service = EventService(db=db)
#     event = await service.get_event_by_id(event_id=event_id, user_uuid=user.uuid)
#     if event is not None:
#         is_has_history = await service.get_status_for_event_by_user_and_event(user_uuid=user.uuid, event_id=event_id)
#         if is_has_history is not None:
#             return is_has_history.status
#         else:
#             return None
#     else:
#         return None