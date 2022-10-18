import pytest
from celery import states
from pytest_mock import MockerFixture

from api.workers.run import wait_for


def test_wait_for(mocker: MockerFixture) -> None:
    seconds = 1
    mocker.patch("api.workers.run.sleep")
    assert wait_for(seconds, fail=False) == f"Waited for {seconds} seconds."
    with pytest.raises(RuntimeError):
        wait_for(seconds, fail=True)


@pytest.mark.integration
@pytest.mark.usefixtures("celery_session_worker")
def test_worker_success() -> None:
    seconds = 3
    task = wait_for.delay(seconds=seconds)
    while task.status == states.PENDING:
        pass
    assert task.status == states.SUCCESS
    assert task.result == f"Waited for {seconds} seconds."
