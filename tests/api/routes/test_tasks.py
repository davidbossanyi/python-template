import pytest
from celery import states
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture


class MockAsyncResultSuccess:
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.status = states.SUCCESS
        self.result = "any-string"


class MockAsyncResultFailure:
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.status = states.FAILURE
        self.result = Exception()


@pytest.mark.unit
def test_get_status_success(
    mocker: MockerFixture, client: TestClient, any_string: str
) -> None:
    mocker.patch("api.routes.tasks.celery_app.AsyncResult", MockAsyncResultSuccess)
    response = client.get(f"/api/tasks/status/{any_string}")
    assert response.status_code == 200
    assert response.json().get("task_id") == any_string
    assert response.json().get("status") == states.SUCCESS
    assert response.json().get("result") == any_string


@pytest.mark.unit
def test_get_status_failure(
    mocker: MockerFixture, client: TestClient, any_string: str
) -> None:
    mocker.patch("api.routes.tasks.celery_app.AsyncResult", MockAsyncResultFailure)
    response = client.get(f"/api/tasks/status/{any_string}")
    assert response.status_code == 200
    assert response.json().get("task_id") == any_string
    assert response.json().get("status") == states.FAILURE
    assert response.json().get("result") is None
