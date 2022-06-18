import pytest
from celery import states
from pytest_mock import MockerFixture

from api.workers.examples import wait_for


def test_wait_for(mocker: MockerFixture) -> None:
    seconds = 5
    mocker.patch("api.workers.examples.sleep")
    assert wait_for(seconds) == f"Waited for {seconds} seconds."
    with pytest.raises(RuntimeError):
        wait_for(1)


@pytest.mark.integration
@pytest.mark.usefixtures("celery_session_worker")
def test_worker_success() -> None:
    seconds = 5
    task = wait_for.delay(seconds=seconds)
    while task.status == states.PENDING:
        pass
    assert task.status == states.SUCCESS
    assert task.result == f"Waited for {seconds} seconds."
