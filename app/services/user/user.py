from app.core import securityHLP
from app.db import DBManager
from app.core.exceptions.token import *
from uuid import UUID
from typing import Optional

from app.schemas.enum import ErrorCode
from fastapi import HTTPException
from fastapi import status as HTTTP_STATUS

class UserService:
    def __init__(self, db: DBManager):
        self.db = db

    async def register(self, name: str, password: str):
        existing = await self.db.users.get_user_by_name(name)
        if existing:
            raise UserAlreadyExistsError
        user = await self.db.users.create_user(username=name, password_hash=securityHLP.hash_password(password))
        await self.db.session.commit()
        return user
    
    async def get_user(self, *, user_uuid: Optional[UUID] = None, username:Optional[str] = None):
        if (user_uuid is not None) ^ (username is not None):
            if user_uuid is not None:
                user = await self.db.users.get_user_by_id(user_uuid)
            else:
                user = await self.db.users.get_user_by_name(username)
            return user
        else:
            raise HTTPException(status_code=HTTTP_STATUS.HTTP_400_BAD_REQUEST, detail=ErrorCode.USER_NOT_EXIST.value)