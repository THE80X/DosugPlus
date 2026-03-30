from typing import Annotated
from app.db import SessionLocal, DBManager
from fastapi import Depends


async def get_db_manager():
    async with DBManager(SessionLocal) as manager:
        yield manager


DBManagerDep = Annotated[DBManager, Depends(get_db_manager)]