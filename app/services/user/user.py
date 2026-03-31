from app.core import securityHLP
from app.db import DBManager
from app.core.exceptions.token import *

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