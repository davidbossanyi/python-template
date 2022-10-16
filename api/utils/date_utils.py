import datetime as dt
from typing import Optional


def to_utc_datetime(date: Optional[dt.datetime | dt.date]) -> dt.datetime | None:
    if not date:
        return None
    if isinstance(date, dt.date):
        date = dt.datetime.fromordinal(date.toordinal())
    return date.replace(tzinfo=dt.timezone.utc)
