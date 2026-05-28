from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import UserModel, UserRole, RoleTypes
from uuid import UUID


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_name(self, username: str) -> Optional[UserModel]:
        return await self.session.scalar(select(UserModel).where(UserModel.username == username))

    async def get_user_by_id(self, user_uuid: UUID) -> Optional[UserModel]:
        return await self.session.get(UserModel, user_uuid)

    async def create_user(self, username: str, password_hash: str) -> UserModel:
        user = UserModel(username=username, pwd_hash=password_hash)
        self.session.add(user)
        await self.session.flush()
        user_role = UserRole(user_uuid=user.uuid, role=RoleTypes.user)
        self.session.add(user_role)
        return user