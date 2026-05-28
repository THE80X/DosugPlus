from ..default import *
from datetime import datetime
from app.schemas.enum import ErrorCode
from app.core.exceptions import ERROR_DETAILS
from uuid import UUID

class CreateEventSchemaPostRequest(BaseModel):
    name: str
    max_users_amount: int = Field(
        description="Максимальное число участников которое может принять организатор мероприятия. Не может быть 0",
        examples=["1"]
    )
    description: str = Field(
        description="Описание мероприятия. Туда можно вписать хэштеги и все необходимые ключевые слова а также описание самого мероприятия.",
        examples=["Мероприятие посвященное организации мероприятий"]
    )

    starts_at: str = Field(
        description="Дата начала в формате DD.MM.YYYY HH:MM",
        examples=["12.12.2012 17:00"]
    )

    ends_at: str = Field(
        description="Дата окончания в формате DD.MM.YYYY HH:MM",
        examples=["12.12.2012 19:00"]
    )

    price: int = Field(
        description="Стоимость записи на мероприятие. Может быть бесплатным, для этого нужно вписать 0",
        examples=["250"]
    )

    @field_validator("max_users_amount")
    @classmethod
    def validate_member_amount(cls, value):
        if value <= 0:
            raise ValueError(ErrorCode.MAX_USERS_NEGATIVE.value)
        else:
            return value
        
    @field_validator("price")
    @classmethod
    def validate_price(cls, value):
        if value < 0:
            raise ValueError(ErrorCode.PRICE_NEGATIVE.value)
        else:
            return value

    @field_validator("starts_at", "ends_at")
    @classmethod
    def validate_datetime(cls, value):
        try:
            datetime.strptime(value, "%d.%m.%Y %H:%M")
            return value
        except ValueError:
            raise ValueError(ErrorCode.WRONG_DATETIME_FORMAT.value)

    @model_validator(mode="after")
    def validate_dates(self):
        start = datetime.strptime(self.starts_at, "%d.%m.%Y %H:%M")
        end = datetime.strptime(self.ends_at, "%d.%m.%Y %H:%M")

        if end <= start:
            raise ValueError(ErrorCode.END_BEFORE_START_OR_EQUAL.value)

        return self


class CreateEventSchemaPostResponse(BaseModel):
    owner_username: str
    event_id: int
    created_at: str


class EventSmallSchema(BaseModel):
    id: int
    name: str
    price: int
    owner_username: str
    starts_at: str


class EventFullSchema(EventSmallSchema):
    max_users_amount: int
    total_users_amount:int
    description: str
    ends_at: str
    user_is_owner: bool
    

class EventSchemaUserStatusPost(BaseModel):
    status: str