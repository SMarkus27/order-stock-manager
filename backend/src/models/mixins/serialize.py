from base64 import b64encode
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import Any, Self, Union
from uuid import UUID

from sqlalchemy.inspection import inspect
from sqlalchemy.orm.base import NO_VALUE

from src.utils.helpers.datetime import to_iso_format


class SerializeMixin:
    __abstract__ = True

    _blacklisted_columns = {
        "id",
        "created_ip",
        "updated_ip",
        "password",
        "external_id_str",
        "created_by_id",
        "updated_by_id",
    }

    def serialize(
        self: Self,
        skip_columns: set[str] | None = None,
        max_depth: int = 10,
        _current_depth: int = 0,
        use_enum_values: bool = False,
    ) -> Any:  # noqa: ANN401
        if skip_columns is None:
            skip_columns = set()

        if max_depth < 0:
            raise ValueError("max_depth deve ser um número inteiro não negativo.")

        if _current_depth > max_depth:
            return self._empty_based_on_uselist(self)

        if isinstance(self, list):
            return [
                item.serialize(skip_columns, max_depth, _current_depth + 1)
                for item in self
            ]

        result = {}
        state = inspect(self)
        mapper = state.mapper
        attrs = state.attrs
        unloaded = state.unloaded
        column_attrs = mapper.column_attrs
        relationship_attrs = mapper.relationships

        skip_column_set = {col.split(".")[0] for col in skip_columns}.union(
            self._blacklisted_columns
        )

        for attr in column_attrs:
            key = attr.key
            if key not in skip_column_set and key not in unloaded:
                value = attrs[key].loaded_value
                if value is not NO_VALUE:
                    result[key] = self._format_value(value, use_enum_values)

        for attr in relationship_attrs:
            key = attr.key
            if key not in skip_column_set and key not in unloaded:
                value = getattr(self, key, None)
                if value is None:
                    result[key] = self._empty_based_on_uselist(attr)
                elif isinstance(value, list):
                    result[key] = [
                        item.serialize(
                            self._get_nested_skip_columns(key, skip_columns),
                            max_depth,
                            _current_depth + 1,
                        )
                        for item in value
                        if item
                    ]
                else:
                    result[key] = value.serialize(
                        self._get_nested_skip_columns(key, skip_columns),
                        max_depth,
                        _current_depth + 1,
                    )

        return result

    @staticmethod
    def _empty_based_on_uselist(
        attr: Union["SerializeMixin", None],
    ) -> dict | list:

        if isinstance(attr, list) or getattr(attr, "uselist", False):
            return []
        return None

    @staticmethod
    def _get_nested_skip_columns(parent: str, skip_columns: set[str]) -> set[str]:
        prefix = f"{parent}."
        prefix_len = len(prefix)
        return {col[prefix_len:] for col in skip_columns if col.startswith(prefix)}

    @staticmethod
    def _format_value(
        value: datetime | date | time | Enum | list | dict, use_enum_value: bool
    ) -> str | int | float | list | dict:
        if isinstance(value, str | int | float):
            return value
        elif isinstance(value, datetime | date | time):
            return to_iso_format(value)
        elif isinstance(value, Enum):
            return value.value if use_enum_value else value.name
        elif isinstance(value, Decimal):
            return float(value)
        elif isinstance(value, bytes):
            return SerializeMixin._process_bytes(value)
        elif isinstance(value, UUID):
            return str(value)
        elif isinstance(value, list):
            return [SerializeMixin._format_value(item) for item in value]
        elif isinstance(value, dict):
            return {k: SerializeMixin._format_value(v) for k, v in value.items()}
        elif hasattr(value, "serialize"):
            return value.serialize()
        return value

    @staticmethod
    def _process_bytes(value: bytes) -> str:

        uuid_byte_length = 16
        if len(value) == uuid_byte_length:
            try:
                return str(UUID(bytes=value))
            except ValueError:
                pass

        try:
            return value.decode("utf-8")
        except UnicodeDecodeError:
            pass

        return b64encode(value).decode("utf-8")
