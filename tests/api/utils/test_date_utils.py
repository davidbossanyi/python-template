import datetime as dt

import pytest

from api.utils.date_utils import to_utc_datetime


@pytest.mark.parametrize(
    "date, expected",
    [
        (
            dt.date(year=2022, month=10, day=16),
            dt.datetime(year=2022, month=10, day=16, tzinfo=dt.timezone.utc),
        ),
        (
            dt.datetime(year=2022, month=10, day=16, hour=1),
            dt.datetime(year=2022, month=10, day=16, hour=0, tzinfo=dt.timezone.utc),
        ),
        (
            None,
            None,
        ),
    ],
)
def test_to_utc_datetime(date: dt.datetime | dt.date, expected: dt.datetime) -> None:
    actual = to_utc_datetime(date)
    assert actual == expected
