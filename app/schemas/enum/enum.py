from enum import Enum
from ..body.default import *

class SortEventByFlagField(str, Enum):
    created = "created"
    signed = "signed"
    all = "all"
    for_user= "for_user"


class RoleField(str, Enum):
    user = "user"
    developer = "developer"


class RoleTypes(str, Enum):
    developer = "developer"
    user = "user"


class EventStatuses(str, Enum):
    signed = "signed"
    kicked = "kicked"
    left = "left"
    payment_refuse = "payment_refuse"
    reserve = "reserve"


class ErrorCode(str, Enum):
    USER_ALREDY_EXISTS = "USER_ALREDY_EXISTS"
    MAX_USERS_NEGATIVE = "MAX_USERS_NEGATIVE"
    PRICE_NEGATIVE = "PRICE_NEGATIVE"
    WRONG_DATETIME_FORMAT = "WRONG_DATETIME_FORMAT"
    END_BEFORE_START_OR_EQUAL = "END_BEFORE_START_OR_EQUAL"
    
    UNKNOWN_STATUS = "UNKNOWN_STATUS"
    EVENT_FULL = "EVENT_FULL"
    WRONG_STATUS = "WRONG_STATUS"
    USER_IS_OWNER = "USER_IS_OWNER"
    USER_IS_NOT_OWNER = "USER_IS_NOT_OWNER"
    NOT_USER_OR_OWNER = "NOT_USER_OR_OWNER"
    USER_NOT_EXIST = "USER_NOT_EXIST"
    EVENT_NOT_EXIST = "EVENT_NOT_EXIST"
