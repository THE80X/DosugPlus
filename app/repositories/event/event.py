from typing import Optional, Tuple
from datetime import datetime

from sqlalchemy import select, and_, func, exists, or_, case, Select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.models.event import EventModel, EventUserModel, EventUserStatusModel
from app.models.user import UserModel, UserBlackListModel

from app.schemas.enum import EventStatuses

from uuid import UUID


class EventRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

# -------------------------- Блок ответственный за создание и поиск мероприятий, без привязки к пользователю --------------------------


    async def create_event(self, 
                           name: str, 
                           max_users_amount:int, 
                           description: str, 
                           starts_at: datetime, 
                           ends_at: datetime, 
                           price:int, 
                           event_owner: UUID) -> EventModel:
        event = EventModel(
            name=name,
            max_users_amount=max_users_amount,
            description=description,
            starts_at=starts_at,
            ends_at=ends_at,
            price=price,
            event_owner=event_owner,
        )
        self.session.add(event)
        await self.session.flush()
        return event


    async def get_event_by_name(self, name: str) -> Optional[EventModel]:
        return await self.session.scalar(select(EventModel).where(EventModel.name == name))


    async def get_event_by_id(self, event_id: int) -> Optional[EventModel]:
        return await self.session.get(EventModel, event_id)


# -------------------------- Блок ответственный за создание и поиск мероприятий, без привязки к пользователю -------------------------- 


# ------------------------------ Блок ответственный за создание связи между пользователем и мероприятием ------------------------------


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


    async def get_event_user_by_event_and_user(self, event_id: int, user_uuid: UUID) -> Optional[EventUserModel]:
        return await self.session.scalar(select(EventUserModel).where(
            and_(
                    EventUserModel.event_id == event_id, 
                    EventUserModel.user_uuid == user_uuid
                )
        ))


# ------------------------------ Блок ответственный за создание связи между пользователем и мероприятием ------------------------------


# ----------------------------- Блок ответственный за получение меропртиятий имеющих связь с пользователем ----------------------------


    async def get_query_event_by_user_id(self, user_uuid: UUID, flag:str)->Select:
        async def get_event_list() -> Select:
            return select(UserModel, EventModel).join(UserModel, UserModel.uuid == EventModel.event_owner)
        
        async def get_event_by_user_id_not_blacklist_or_blacklisted(user_uuid: UUID)->Select:
            blacklist_subquery = (
                select(
                    case(
                        (
                            UserBlackListModel.user_uuid == user_uuid,
                            UserBlackListModel.blacklisted_user_uuid
                        ),
                        (
                            UserBlackListModel.blacklisted_user_uuid == user_uuid,
                            UserBlackListModel.user_uuid
                        ),
                        else_=UserBlackListModel.user_uuid
                    ).label("blocked_uuid")
                )
                .where(
                    or_(
                        UserBlackListModel.user_uuid == user_uuid,
                        UserBlackListModel.blacklisted_user_uuid == user_uuid
                    )
                )
                .subquery()
            )

            query = select(UserModel, EventModel)\
                    .join(
                        UserModel,
                        UserModel.uuid == EventModel.event_owner)\
                    .where(
                        EventModel.event_owner.not_in(select(blacklist_subquery.c.blocked_uuid))
            )

            return query
        
        async def get_event_by_user_id_and_status(user_uuid:UUID, status:str)->Select:
            # Подзапрос для получения последнего статуса (по максимальной дате) для каждого event_user
            latest_status_subquery = (
                select(
                    EventUserStatusModel.event_user_id,
                    func.max(EventUserStatusModel.created_at).label("max_created_at")
                )
                .group_by(EventUserStatusModel.event_user_id)
                .subquery("latest_status")
            )
            
            # Основной запрос: сначала UserModel, потом EventModel
            query = (
                select(UserModel, EventModel)
                .join(
                    EventModel,
                    EventModel.event_owner == UserModel.uuid  # связь User -> Event (владелец события)
                )
                .join(
                    EventUserModel,
                    EventUserModel.event_id == EventModel.id
                )
                .join(
                    latest_status_subquery,
                    latest_status_subquery.c.event_user_id == EventUserModel.id
                )
                .join(
                    EventUserStatusModel,
                    and_(
                        EventUserStatusModel.event_user_id == EventUserModel.id,
                        EventUserStatusModel.created_at == latest_status_subquery.c.max_created_at
                    )
                )
                .where(
                    EventUserModel.user_uuid == user_uuid,
                    EventUserStatusModel.status == status
                )
            )
            
            return query
        
        
        query = select(UserModel, EventModel)

        match flag:
            case "created":
                return query.join(UserModel, UserModel.uuid == EventModel.event_owner).where(EventModel.event_owner==user_uuid)
            case "signed":
                return await get_event_by_user_id_and_status(user_uuid, "signed")
            case "for_user":
                return await get_event_by_user_id_not_blacklist_or_blacklisted(user_uuid)
            case "all":
                return await get_event_list()
            case _:
                return None
            
    
    async def get_event_by_user_id(self, user_uuid: UUID, flag:str, offset: int = 0, limit: int = 10):
        """Функция ИСПОЛНИТЕЛЬ. Её цель по патерну сделать запрос"""
        query = await self.get_query_event_by_user_id(user_uuid=user_uuid, flag=flag)
        if query is not None:
            return await self.session.execute(query.offset(offset).limit(limit))
        else:
            return None


# ----------------------------- Блок ответственный за получение меропртиятий имеющих связь с пользователем ----------------------------


# ----------------------------- Блок ответственный за получение информации о меропртиятии для пользвоателя ----------------------------


    async def get_event_by_id_and_user_id(self, user_uuid:UUID, event_id:int) -> None | tuple[UserModel, EventModel]:
        query = await self.get_query_event_by_user_id(user_uuid=user_uuid, flag="for_user")
        return (await self.session.execute(query.where(EventModel.id == event_id))).one_or_none()


    async def get_event_people_amount(self, event_id: int):
        latest_status_subquery = (
            select(
                EventUserStatusModel.event_user_id,
                func.max(EventUserStatusModel.created_at).label("max_created_at")
            )
            .group_by(EventUserStatusModel.event_user_id)
            .subquery()
        )

        # Основной запрос
        query = (
            select(UserModel, EventUserStatusModel)
            .join(
                EventUserModel,
                EventUserModel.user_uuid == UserModel.uuid
            )
            .join(
                latest_status_subquery,
                latest_status_subquery.c.event_user_id == EventUserModel.id
            )
            .join(
                EventUserStatusModel,
                and_(
                    EventUserStatusModel.event_user_id == EventUserModel.id,
                    EventUserStatusModel.created_at == latest_status_subquery.c.max_created_at
                )
            )
            .where(EventUserModel.event_id == event_id)
        )

        return query


    async def get_event_people_by_status(
        self,
        event_id: int,
        status: Optional[EventStatuses] = None,
        offset: int = 0,
        limit: int = 10
    ):

        query = await self.get_event_people_amount(event_id)

        if status is not None:
            query = (query.where(EventUserStatusModel.status == status))

        query = (query
            .offset(offset)
            .limit(limit)
        )

        result = (await self.session.execute(query)).fetchall()

        return result


# ----------------------------- Блок ответственный за получение информации о меропртиятии для пользвоателя ----------------------------



    async def post_new_event_user_status(self, event_id, user_uuid, status:str):
        event_user = await self.get_event_user_by_event_id_and_user_uuid(event_id, user_uuid)
        print(event_user)
        if event_user is None:
            event_user = EventUserModel(
                event_id=event_id,
                user_uuid=user_uuid
            )
            self.session.add(event_user)
            await self.session.flush()
        print(event_user.id)
        new_event_user_status = EventUserStatusModel(
            event_user_id=event_user.id,
            status=status   
        )               
        self.session.add(new_event_user_status)
        await self.session.flush()
        return new_event_user_status


# ----------------------------- Блок ответственный за получение меропртиятий имеющих связь с пользователем ----------------------------
    async def get_event_user_by_event_id_and_user_uuid(self, event_id: int, user_uuid:UUID):
        result = (await self.session.execute(select(EventUserModel).where(and_(EventUserModel.event_id==event_id, EventUserModel.user_uuid==user_uuid)))).scalar_one_or_none()
        return result
    

    async def get_event_user_by_event_id_and_user_username(self, event_id:int, username:str):
        result = (await self.session.execute(select(EventUserModel).join(UserModel, UserModel.uuid==EventUserModel.user_uuid).where(and_(EventUserModel.event_id==event_id, UserModel.username==username)))).scalar_one_or_none()
        return result


    async def get_event_user_status(self, event_id:int, user_uuid:UUID=None, username:str=None):
        print((user_uuid != None) ^ (username != None))
        if (user_uuid != None) ^ (username != None):
            if user_uuid != None:
                result = await self.get_event_user_by_event_id_and_user_uuid(event_id, user_uuid)
                if result is not None:
                    return (await self.session.execute(
                        select(EventUserStatusModel)
                        .where(EventUserStatusModel.event_user_id == result.id)
                        .order_by(desc(EventUserStatusModel.created_at))
                        .limit(1)
                    )).scalar_one_or_none()
                else:
                    return None
            else:
                result = await self.get_event_user_by_event_id_and_user_username(event_id, username)
                if result is not None:
                    return (await self.session.execute(
                        select(EventUserStatusModel)
                        .where(EventUserStatusModel.event_user_id == result.id)
                        .order_by(desc(EventUserStatusModel.created_at))
                        .limit(1)
                    )).scalar_one_or_none()
                else:
                    return None
        else:
            return None
    

    async def get_event_user_by_id(self, event_user_id: int) -> Optional[EventUserModel]:
        return await self.session.get(EventUserModel, event_user_id)
    
    
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