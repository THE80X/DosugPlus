import jwt

from app.core import settings, tokenHLP
from app.api.dependencies.db import SessionDep

from fastapi import status, HTTPException, Request

from app.models.user import UserModel

async def get_current_user_from_bearer(request: Request, session: SessionDep) -> UserModel:
    raw_token = _extract_access_token(request)
    try:
        payload = tokenHLP.decode_token(raw_token, expected_type="access")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expired") from None
    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token") from None
    user_uuid = payload["sub"]
    user = await session.get(UserModel, user_uuid)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "User not found")
    return user


def _extract_access_token(request: Request) -> str:
    header = request.headers.get("Authorization")
    if header and header.lower().startswith("bearer "):
        return header.split(" ", 1)[1].strip()
    cookie_token = request.cookies.get(settings.ACCESS_COOKIE_NAME)
    if cookie_token:
        return cookie_token
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing access token")