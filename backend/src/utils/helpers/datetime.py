from datetime import UTC, date, datetime, time, timedelta, timezone


def utcnow() -> datetime:
    return datetime.now(UTC)


def to_iso_format(dt: date | datetime | time) -> str:
    if isinstance(dt, datetime | time):
        if dt.tzinfo is None:
            raise ValueError("O objeto deve conter um fuso horário.")

    return dt.isoformat()


def from_iso_format(iso_string: str, default_tz: timezone = UTC) -> datetime:
    dt = datetime.fromisoformat(iso_string)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=default_tz)
    return dt


def add_days(days: int, start_datetime: datetime | None = None) -> datetime:
    if start_datetime is None:
        start_datetime = utcnow()
    return start_datetime + timedelta(days=days)


def subtract_days(days: int, start_datetime: datetime | None = None) -> datetime:
    if start_datetime is None:
        start_datetime = utcnow()
    return start_datetime - timedelta(days=days)
