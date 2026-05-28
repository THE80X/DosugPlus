from fastapi import APIRouter

from .v1 import *

main_router = APIRouter(prefix="/v1")

main_router.include_router(v1_auth_router, prefix='/auth')
main_router.include_router(v1_event_router, prefix='/events')
main_router.include_router(v1_user_router, prefix='/user')