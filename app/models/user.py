from .default import *
from uuid import UUID as python_UUID

class UserModel(Base):
    __tablename__ = "user"
    uuid: Mapped[python_UUID] = mapped_column(UUID, primary_key=True, unique=True, nullable=False)
    username: Mapped[str] = mapped_column(VARCHAR(32), unique=True, nullable=False)
    pwd_hash: Mapped[str] = mapped_column(TEXT, nullable=False)


