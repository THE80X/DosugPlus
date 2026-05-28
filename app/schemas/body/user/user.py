from ..default import *
from datetime import datetime
from uuid import UUID as python_UUID

class UserRead(BaseModel):
    uuid: python_UUID
    username: str

    model_config = ConfigDict(from_attributes=True)


class UserEventStatus(BaseModel):
    username: str
    status: str