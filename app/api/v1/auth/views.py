from fastapi import Request, APIRouter, Response, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.core import *
from app.schemas import *
from app.services import UserService, AuthServiceJWT
from app.api.dependencies import DBManagerDep, get_current_user_from_bearer, TokenDep
from app.models.user import UserModel
from app.core.exceptions import *
from fastapi.security import OAuth2PasswordRequestForm

from typing import Annotated

router = APIRouter(tags=["Auth"])


def _set_token_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    response.set_cookie(
        key=settings.ACCESS_COOKIE_NAME,
        value=access_token,
        httponly=True,
        secure=settings.SESSION_COOKIE_SECURE,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        domain=settings.SESSION_COOKIE_DOMAIN,
        path="/",
    )
    response.set_cookie(
        key=settings.RESFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=settings.SESSION_COOKIE_SECURE,
        samesite="lax",
        max_age=settings.REFRESH_TOKEN_EXPIRE_SECONDS,
        domain=settings.SESSION_COOKIE_DOMAIN,
        path="/",
    )


@router.post("/login", response_class=JSONResponse, summary="Авторизация пользователя")
async def login(
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    # data: LoginSchemaPostRequest, 
    response: Response, db: DBManagerDep)->TokenPair:
    jwt_service = AuthServiceJWT(db)
    try:
        access_token, refresh_token = await jwt_service.login(data.username, data.password)
    except InvalidCredentialsError as err:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=str(err)) from err
    _set_token_cookies(response, access_token, refresh_token)
    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
    )

@router.post("/register", response_class=JSONResponse, summary="Создание пользователя")
async def register(data: RegisterSchemaPostRequest, db: DBManagerDep)->UserRead:
    service = UserService(db)
    try:
        return await service.register(data.username, data.password)
    except Exception as err:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="USER_ALREDY_EXISTS") from err
    

@router.post("/refresh", response_class=JSONResponse, summary="Обновление access/ refresh")
async def refresh_tokens(request: Request, 
                         response: Response, db: DBManagerDep
) -> TokenPair:
    jwt_service = AuthServiceJWT(db)
    try:
        pair = await jwt_service.refresh(request.cookies['refresh_token'])
    except Exception as err:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail=str(err)) from err
    _set_token_cookies(response, pair.access_token, pair.refresh_token)
    return pair


@router.get("/info", summary="Профиль по JWT (access)")
async def me_jwt(user: UserModel = Depends(get_current_user_from_bearer)) -> UserRead:
    return user