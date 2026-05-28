from ..enum import SortEventByFlagField

from typing import Annotated
from fastapi import Query

SortEventByFlagQuery = Annotated[ SortEventByFlagField, Query(description="Флаг для определения интересующих мероприятий") ]