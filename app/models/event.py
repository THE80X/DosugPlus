from .default import *
from uuid import UUID as python_UUID
from app.schemas.enum import EventStatuses


class EventModel(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(TEXT, nullable=False)
    max_users_amount: Mapped[int] = mapped_column(INTEGER, nullable=False)
    description: Mapped[str] = mapped_column(TEXT, nullable=False)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    starts_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    ends_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    revoked_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    price: Mapped[int] = mapped_column(BIGINT, nullable=False)
    event_owner: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.uuid", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )


# ------------------------
# Пользователи события
# ------------------------
class EventUserModel(Base):
    __tablename__ = "event_users"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    event_id: Mapped[int] = mapped_column(
        INTEGER,
        ForeignKey("event.id"),
        nullable=False
    )
    user_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.uuid"),
        nullable=False
    )


# ------------------------
# Статусы пользователей события
# ------------------------
class EventUserStatusModel(Base):
    __tablename__ = "event_user_statuses"

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    event_user_id: Mapped[int] = mapped_column(
        INTEGER,
        ForeignKey("event_users.id"),
        nullable=False
    )
    status: Mapped[EventStatuses] = mapped_column(
        Enum(EventStatuses, name="event_statuses"),
        nullable=False
    )
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    )