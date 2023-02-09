import datetime as dt


def to_utc_datetime(date: dt.datetime | dt.date | None) -> dt.datetime | None:
    if not date:
        return None
    if isinstance(date, dt.date):
        date = dt.datetime.fromordinal(date.toordinal())
    return date.replace(tzinfo=dt.timezone.utc)
