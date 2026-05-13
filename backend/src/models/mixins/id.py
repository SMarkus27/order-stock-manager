from uuid import UUID as PyUUID

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy.types import Integer
from uuid6 import uuid7


class IdMixin:
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        unique=True,
        autoincrement=True,
        nullable=False,
    )

    external_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
        default=uuid7,
        index=True,
    )

    @property
    def external_id_str(self) -> str:
        return str(UUID(bytes=self.external_id))

    @staticmethod
    def uuid_to_str(uuid_bin: bytes) -> str:
        return str(UUID(bytes=uuid_bin))

    @staticmethod
    def str_to_uuid(uuid_str: str) -> bytes:
        return UUID(uuid_str).bytes
