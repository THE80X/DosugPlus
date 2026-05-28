from app.schemas import TokenPair
from app.db import DBManager
from uuid import UUID
from datetime import datetime
from app.schemas.body.event import *
from app.schemas.body.user import UserEventStatus
from datetime import datetime
from typing import Optional

from app.models.user import UserModel
from app.models.event import EventModel
from app.schemas.enum import ErrorCode
from fastapi import HTTPException
from fastapi import status as HTTTP_STATUS

class EventService:
    def __init__(self, db: DBManager):
        self.db = db
    
    async def create_event_by_user(self, user_uuid: UUID, name:str, max_users_amount:int, description:str, starts_at:datetime, ends_at:datetime, price: int):
        new_event = await self.db.event.create_event(
            name=name,
            max_users_amount=max_users_amount,
            description=description,
            starts_at=starts_at,
            ends_at=ends_at,
            price=price,
            event_owner=user_uuid,
        )
        await self.db.session.commit()
        return new_event


    async def get_event_list(self, flag:str, user_uuid: UUID, offset: int = 0, limit: int = 10):
        event_list = await self.db.event.get_event_by_user_id(user_uuid, flag, offset, limit)
        return [EventSmallSchema(name=event.name,
                                 id=event.id, 
                                 owner_username=user.username, 
                                 price=event.price, 
                                 starts_at=datetime.strftime(event.starts_at,"%d.%m.%Y %H:%M")) for user, event in event_list.all()]


    async def get_status_for_event_by_user_and_event(self, user_uuid:UUID, event_id:int):
        is_has_history = await self.db.event.get_event_user_status(event_id=event_id, user_uuid=user_uuid)
        if is_has_history is not None:
            return is_has_history.status
        else:
            return None


    async def update_user_status(self, target_user:UserModel, event_full_schema:EventFullSchema, sender_user:UserModel, status:str):
        def status_checking(result):
            logical_object = {
                "kicked": ["signed"],
                "left": ["signed"],
                "signed": ["left", "kicked"],
            }
            if result is not None:
                if status in logical_object[result]:
                    return True
                else:
                    return False
            else:
                return True
        
        print(target_user, sender_user)
        is_user = target_user.username == sender_user.username
        is_owner = sender_user.username == event_full_schema.owner_username
        result = await self.get_status_for_event_by_user_and_event(user_uuid=target_user.uuid, event_id=event_full_schema.id)
        passed_status = status_checking(result)

        if passed_status and (is_owner ^ is_user):
            if is_owner:
                match status:
                    case "kicked":
                        return await self.post_new_status(event_full_schema.id, target_user.uuid, status)
                    case _:
                        raise HTTPException(status_code=HTTTP_STATUS.HTTP_400_BAD_REQUEST, detail=ErrorCode.UNKNOWN_STATUS.value)
            if is_user:
                match status:
                    case "left":
                        return await self.post_new_status(event_full_schema.id, target_user.uuid, status)
                    case "signed":
                        if event_full_schema.max_users_amount - event_full_schema.total_users_amount > 0:
                            return await self.post_new_status(event_full_schema.id, target_user.uuid, status)
                        else:
                            raise HTTPException(status_code=HTTTP_STATUS.HTTP_400_BAD_REQUEST, detail=ErrorCode.EVENT_FULL.value)
                    case _:
                        raise HTTPException(status_code=HTTTP_STATUS.HTTP_400_BAD_REQUEST, detail=ErrorCode.UNKNOWN_STATUS.value)
        elif(not passed_status):
            raise HTTPException(status_code=HTTTP_STATUS.HTTP_400_BAD_REQUEST, detail=ErrorCode.WRONG_STATUS.value)
        elif(is_owner and is_user):
            raise HTTPException(status_code=HTTTP_STATUS.HTTP_400_BAD_REQUEST, detail=ErrorCode.USER_IS_OWNER.value)
        else:
            raise HTTPException(status_code=HTTTP_STATUS.HTTP_400_BAD_REQUEST, detail=ErrorCode.NOT_USER_OR_OWNER.value)


    async def post_new_status(self, event_id:int, user_uuid:UUID, status:str):
        result = await self.db.event.post_new_event_user_status(event_id=event_id, user_uuid=user_uuid, status=status)
        await self.db.session.commit()
        return result

    
    async def get_event(self, event_id:int):
        result = await self.db.event.get_event_by_id(event_id=event_id)
        if result is not None:
            return result
        else:
            raise HTTPException(status_code=HTTTP_STATUS.HTTP_400_BAD_REQUEST, detail=ErrorCode.EVENT_NOT_EXIST.value)


    async def can_user_see_event(self, event_id:int, user_uuid: UUID):
        result = await self.db.event.get_event_by_id_and_user_id(user_uuid=user_uuid, event_id=event_id)
        if result is None:
            raise HTTPException(status_code=HTTTP_STATUS.HTTP_400_BAD_REQUEST, detail=ErrorCode.EVENT_NOT_EXIST.value)
        return result


    async def get_users_event_by_status(self, event_id, status=None, offset: int = 0, limit: int = 10):
        answer_list = []
        result = await self.db.event.get_event_people_by_status(event_id=event_id, status=status, offset=offset, limit=limit)
        if result is not []:
            answer_list = [UserEventStatus(username=user.username, status=user_status.status) for user, user_status in result]
        return answer_list

    async def get_event_full_schema(self, event_owner:UserModel, user: UserModel, event: EventModel):
        total_people = await self.get_users_event_by_status(event_id=event.id, status="signed")
        print(total_people)
        return EventFullSchema(name=event.name,
                            id=event.id,
                            owner_username=event_owner.username,
                            price=event.price,
                            starts_at=datetime.strftime(event.starts_at,"%d.%m.%Y %H:%M"),
                            ends_at=datetime.strftime(event.ends_at,"%d.%m.%Y %H:%M"),
                            max_users_amount=event.max_users_amount,
                            total_users_amount=len(total_people),
                            description=event.description,
                            user_is_owner = True if user.uuid == event.event_owner else False
                            )