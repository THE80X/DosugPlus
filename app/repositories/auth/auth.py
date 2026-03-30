from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.auth import RefreshTokenModel
from uuid import UUID

class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_refresh_token(self, user_uuid: UUID, token_hash: str, expires_at: datetime) -> RefreshTokenModel:
        token = RefreshTokenModel(user_id=user_uuid, token_hash=token_hash, expires_at=expires_at)
        self.session.add(token)
        await self.session.flush()
        return token

    async def get_refresh_token(self, token_hash: str) -> Optional[RefreshTokenModel]:
        return await self.session.scalar(select(RefreshTokenModel).where(RefreshTokenModel.token_hash == token_hash))

    async def delete_refresh_token(self, token_obj: RefreshTokenModel) -> None:
        await self.session.delete(token_obj)
