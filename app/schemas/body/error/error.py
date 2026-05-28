from ..default import *
from app.schemas.enum import ErrorCode

class ErrorItem(BaseModel):
    error_code: ErrorCode
    detail: str   