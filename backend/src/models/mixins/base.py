from datetime import datetime
from typing import Self

from sqlalchemy import DateTime, text
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)

from src.models.mixins.crud import CRUDMixin
from src.models.mixins.id import IdMixin


class BaseMixin(DeclarativeBase, IdMixin, CRUDMixin):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=datetime.utcnow,
        nullable=False,
    )

    @declared_attr.directive
    def __tablename__(cls: Self) -> str:
        return cls.__name__.lower()

    def __repr__(self: Self) -> str:
        return (
            f"<{self.__class__.__name__}(id={self.id}, external_id={self.external_id})>"
        )
