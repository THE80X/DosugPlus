from .default import *
from uuid import UUID as python_UUID
import uuid
from app.schemas.enum import RoleTypes

class UserModel(Base):
    __tablename__ = "user"
    uuid: Mapped[python_UUID] = mapped_column(UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4)
    username: Mapped[str] = mapped_column(VARCHAR(32), unique=True, nullable=False)
    pwd_hash: Mapped[str] = mapped_column(TEXT, nullable=False)


class UserBlackListModel(Base):
    __tablename__ = "user_blacklist"
    id: Mapped[int] = int_pk_funk()
    user_uuid: Mapped[python_UUID] = int_fk_funk("user", "uuid")
    blacklisted_user_uuid: Mapped[python_UUID] = int_fk_funk("user", "uuid")


class UserRole(Base):
    __tablename__ = "user_role"
    user_uuid: Mapped[python_UUID] = mapped_column(ForeignKey("user.uuid"),
                                                   primary_key=True, autoincrement=False, nullable=False, unique=True
                                                   )
    role: Mapped[RoleTypes] = mapped_column(
        Enum(RoleTypes, name="role_types"),
        nullable=False
    )