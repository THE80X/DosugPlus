from .default import *
from uuid import UUID as python_UUID

class RefreshTokenModel(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    user_uuid: Mapped[python_UUID] = mapped_column(UUID,
        ForeignKey("user.uuid", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    token_hash: Mapped[str] = mapped_column(VARCHAR(128), nullable=False, unique=True)
    created_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    expires_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False
    )
    revoked_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=True
    )
    __table_args__ = (
        # Индекс для активных токенов: неотозванные и ещё не истёкшие
        Index(
            "idx_refresh_active_tokens",
            "user_uuid",
            postgresql_where=text("revoked_at IS NULL")
        ),
    )