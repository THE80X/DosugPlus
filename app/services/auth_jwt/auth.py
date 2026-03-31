from app.core import tokenHLP, securityHLP, settings
from app.schemas import TokenPair
from app.db import DBManager
from app.core.exceptions.token import *
from datetime import datetime, timedelta, timezone
from uuid import UUID as python_UUID


class AuthServiceJWT:
    def __init__(self, db: DBManager):
        self.db = db

    async def login(self, name: str, password: str):
        user = await self._get_user_or_raise(name, password)
        pair = await self._issue_tokens(user.uuid)
        return pair.access_token, pair.refresh_token

    async def refresh(self, raw_refresh_token: str):
        stored = await self._get_valid_refresh(raw_refresh_token)
        user = await self._get_user_for_token(stored.user_uuid)
        await self.db.auth.delete_refresh_token(stored)  # можно удалять пачками через cron
        pair = await self._issue_tokens(user.uuid)
        return pair

    async def _get_valid_refresh(self, raw_refresh_token: str):
        token_hash = tokenHLP.hash_session_token(raw_refresh_token)
        stored = await self.db.auth.get_refresh_token(token_hash)
        if not stored or stored.revoked_at is not None:
            raise RefreshTokenNotFoundError
        now = datetime.now(timezone.utc)
        if stored.expires_at <= now:
            await self.db.auth.delete_refresh_token(stored)  # можно удалять пачками через cron
            raise RefreshTokenExpiredError
        return stored

    async def _get_user_for_token(self, user_id: int):
        user = await self.db.users.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError
        return user

    async def _get_user_or_raise(self, username: str, password: str):
        user = await self.db.users.get_user_by_name(username)
        if not user or not securityHLP.verify_password(password, user.pwd_hash):
            raise InvalidCredentialsError
        return user

    def _refresh_expiry(self) -> datetime:
        return datetime.now(timezone.utc) + timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS)

    async def _issue_tokens(self, user_uuid: python_UUID) -> TokenPair:
        access_token = tokenHLP.create_access_token(user_uuid)
        refresh_token = tokenHLP.create_refresh_token()
        refresh_hash = tokenHLP.hash_session_token(refresh_token)
        expires_at = self._refresh_expiry()
        await self.db.auth.create_refresh_token(user_uuid=user_uuid, token_hash=refresh_hash, expires_at=expires_at)
        await self.db.session.commit()
        return TokenPair(access_token=access_token, refresh_token=refresh_token)
