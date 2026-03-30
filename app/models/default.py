from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey
from sqlalchemy import text, select, update, delete, insert, and_, or_, Index, Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TEXT, BIGINT, BOOLEAN, VARCHAR, TIMESTAMP, UUID, INTEGER
from sqlalchemy.sql import func
import datetime

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass


def int_pk_funk(primary_key:bool=True,
                 unique:bool=True, autoincrement:bool=True):
    return mapped_column(primary_key=primary_key,  unique=unique, autoincrement=autoincrement)

def int_fk_funk(table_name:str,
                 key:str,
                 primary_key:bool=False,
                 unique:bool=False,
                 autoincrement:bool=False,
                 nullable:bool=False):
    return mapped_column(ForeignKey(f"{table_name}.{key}"), primary_key=primary_key,  unique=unique, autoincrement=autoincrement, nullable=nullable)