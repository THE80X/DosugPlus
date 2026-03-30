from typing import Optional, Tuple
from datetime import datetime
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from app.models.event import EventModel, EventUserModel, EventUserStatusModel
from app.models.user import UserModel
from uuid import UUID


class EventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_event_by_name(self, name: str) -> Optional[EventModel]:
        return await self.session.scalar(select(EventModel).where(EventModel.name == name))

    async def get_event_by_id(self, event_id: int) -> Optional[EventModel]:
        return await self.session.get(EventModel, event_id)

    async def create_event(self, 
                           name: str, 
                           max_users_amount:int, 
                           description: str, 
                           starts_at: datetime, 
                           ends_at: datetime, 
                           price:int, 
                           event_owner: UUID) -> EventModel:
        user = EventModel(
            name=name,
            max_users_amount=max_users_amount,
            description=description,
            starts_at=starts_at,
            ends_at=ends_at,
            price=price,
            event_owner=event_owner,
        )
        self.session.add(user)
        await self.session.flush()
        return user
    

class EventUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def get_event_user_by_event_and_user(self, event_id: int, user_uuid: UUID) -> Optional[EventUserModel]:
        return await self.session.scalar(select(EventUserModel).where(
            and_(
                    EventUserModel.event_id == event_id, 
                    EventUserModel.user_uuid == user_uuid
                )
        ))


    async def get_event_user_by_id(self, event_user_id: int) -> Optional[EventModel]:
        return await self.session.get(EventModel, event_user_id)
    

    async def create_event_user(self, event_id:int, user_uuid:UUID) -> Tuple[EventUserModel, EventUserStatusModel]:
        event_user = EventUserModel(
            event_id=event_id,
            user_uuid=user_uuid,
        )
        self.session.add(event_user)
        await self.session.flush()
        event_user_status = await self.create_event_user_status(event_user_id=event_user.id)

        return event_user, event_user_status


    async def create_event_user_status(self, event_user_id:int, status:str="reserved") -> EventUserStatusModel:
        event_user_status = EventUserStatusModel(
            event_user_id=event_user_id,
            status=status,
        )
        self.session.add(event_user_status)
        await self.session.flush()
        return event_user_status

    
    async def get_event_user_status_by_event_user_id_and_status(self, event_user_id: int, status:str, since: Optional[datetime] = None) -> Optional[EventUserStatusModel]:
        '''
        Взятие данных о наличии определенного статуса
        event_user_id - id связи между мероприятием и пользователем.
        status - интересующий нас статус. Статус может принимать только следующие значения:
        -  signed
        -  kicked
        -  left
        -  payment_refuse
        -  reserve
        since - дата с которой нужно проверять всю информацию
        '''
        query = (
            select(EventUserStatusModel)
            .where(
                EventUserStatusModel.event_user_id == event_user_id,
                EventUserStatusModel.status == status,
            )
        )

        if since is not None:
            query = query.where(EventUserStatusModel.created_at > since)
        
        query = query.order_by(EventUserStatusModel.created_at.desc())


        return await self.session.scalar(query)


    async def get_event_users_by_status(self, event_id:int, status:Optional[str] = None, since: Optional[datetime] = None) -> Optional[EventUserStatusModel]:
        '''
        Взятие данных о статусах пользователей по мероприятию и времени если оно передано.
        '''
        S = aliased(EventUserStatusModel)

        # подзапрос: для каждого event_user_id находим max(created_at) (с учётом since и status фильтров, если заданы)
        subq_stmt = (
            select(
                S.event_user_id.label("event_user_id"),
                func.max(S.created_at).label("max_created_at"),
                func.max(S.id).label("max_id")  # для tie-breaker при одинаковых created_at
            )
            .join(EventUserModel, EventUserModel.id == S.event_user_id)
            .where(EventUserModel.event_id == event_id)
        )

        # добавляем опциональные фильтры в подзапрос (чтобы max бралась только среди подходящих записей)
        conditions = []
        if status is not None:
            conditions.append(S.status == status)
        if since is not None:
            conditions.append(S.created_at > since)  # или >= если нужно включительно

        if conditions:
            subq_stmt = subq_stmt.where(and_(*conditions))

        subq = subq_stmt.group_by(S.event_user_id).subquery()

        # основной запрос: соединяем event_users -> их последние записи в event_user_statuses
        EUS = EventUserStatusModel
        stmt = (
            select(EventUserModel, EUS)
            .join(EUS, EventUserModel.id == EUS.event_user_id)
            .join(
                subq,
                and_(
                    EUS.event_user_id == subq.c.event_user_id,
                    EUS.created_at == subq.c.max_created_at,
                    EUS.id == subq.c.max_id  # tie-breaker: гарантируем единственную строку
                )
            )
            .where(EventUserModel.event_id == event_id)
            .order_by(EUS.created_at.desc(), EUS.id.desc())  # сортировка по дате (новые первыми)
        )

        return await self.session.scalars(stmt)