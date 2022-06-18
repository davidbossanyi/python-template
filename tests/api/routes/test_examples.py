import time

import pytest
from celery import states
from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture


def test_wait_unit(mocker: MockerFixture, client: TestClient, any_string: str) -> None:
    class MockTask:
        id: str = any_string

    mocker.patch("api.routes.examples.wait_for.delay", return_value=MockTask)
    response = client.get("/api/examples/wait?seconds=5")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("task_id") == any_string


@pytest.mark.integration
@pytest.mark.usefixtures("celery_session_worker")
@pytest.mark.parametrize("seconds, expected_status", [(3, states.SUCCESS), (1, states.FAILURE)])
def test_wait_integration(client: TestClient, seconds: int, expected_status: str) -> None:
    response = client.get(f"/api/examples/wait?seconds={seconds}")
    assert response.status_code == status.HTTP_200_OK
    task_id = response.json().get("task_id")
    task_response = client.get(f"/api/tasks/status/{task_id}")
    assert task_response.status_code == status.HTTP_200_OK
    while task_response.json().get("status") == states.PENDING:
        task_response = client.get(f"/api/tasks/status/{task_id}")
        assert task_response.status_code == status.HTTP_200_OK
    time.sleep(0.1)
    assert task_response.json().get("status") == expected_status
