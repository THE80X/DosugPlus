from .default import *
from uuid import UUID as python_UUID
import uuid

class UserModel(Base):
    __tablename__ = "user"
    uuid: Mapped[python_UUID] = mapped_column(UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=uuid.uuid4)
    username: Mapped[str] = mapped_column(VARCHAR(32), unique=True, nullable=False)
    pwd_hash: Mapped[str] = mapped_column(TEXT, nullable=False)


