from datetime import UTC, datetime
from typing import Self

from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.engine import Dialect
from sqlalchemy.types import TypeDecorator

MIN_FSP = 0
MAX_FSP = 6
DEFAULT_FSP = 6


class UTCDateTime(TypeDecorator):
    impl = DATETIME
    cache_ok = True

    def __init__(self: Self, fsp: int = DEFAULT_FSP) -> None:

        if not (MIN_FSP <= fsp <= MAX_FSP):
            raise ValueError("O valor de fsp deve estar entre 0 e 6.")

        self.impl = DATETIME(fsp=fsp)

    def process_bind_param(
        self: Self, value: datetime | None, dialect: Dialect
    ) -> datetime | None:  # noqa: ARG002
        if value is None:
            return None

        if not isinstance(value, datetime):
            raise TypeError("O valor deve ser uma instância de datetime.")

        if value.tzinfo is None:
            raise ValueError(
                "O objeto datetime deve conter informação de fuso horário."
            )

        return value.astimezone(UTC)

    def process_result_value(
        self: Self, value: datetime | None, dialect: Dialect
    ) -> datetime | None:  # noqa: ARG002

        if value is None:
            return None

        return value.replace(tzinfo=UTC)
