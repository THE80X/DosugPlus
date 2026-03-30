from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserModel
from uuid import UUID


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_name(self, name: str) -> Optional[UserModel]:
        return await self.session.scalar(select(UserModel).where(UserModel.username == name))

    async def get_user_by_id(self, user_uuid: UUID) -> Optional[UserModel]:
        return await self.session.get(UserModel, user_uuid)

    async def create_user(self, name: str, password_hash: str) -> UserModel:
        user = UserModel(username=name, pwd_hash=password_hash)
        self.session.add(user)
        await self.session.flush()
        return user