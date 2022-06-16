import pytest
from pytest_mock import MockerFixture

from api.workers.celery_workers import wait_for


@pytest.mark.unit
def test_wait_for(mocker: MockerFixture) -> None:
    mocker.patch("api.workers.celery_workers.sleep")
    assert wait_for(5) == "Waited for 5 seconds."
    with pytest.raises(RuntimeError):
        wait_for(1)
