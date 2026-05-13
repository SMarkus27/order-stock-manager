from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from src.models.mixins.base import BaseMixin


class AuditLog(BaseMixin):
    __tablename__ = "audit_logs"

    entity: Mapped[str] = mapped_column(String(50))
    action: Mapped[str] = mapped_column(String(50))

    entity_id: Mapped[str] = mapped_column(String(100))

    message: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
