import time
import uuid

import pytest
from celery import states
from fastapi import status
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from api.models.tasks.responses import CeleryTaskIdList, CeleryTaskStatistics, TaskStatusResponse


def call_wait_endpoint(api_client: TestClient, fail: bool) -> TaskStatusResponse:
    response = api_client.get(f"/api/run/wait?seconds=1&fail={fail}")
    assert response.status_code == status.HTTP_200_OK
    task_id = response.json().get("task_id")
    task_response = api_client.get(f"/api/tasks/status/{task_id}")
    assert task_response.status_code == status.HTTP_200_OK
    while task_response.json().get("status") == states.PENDING:
        task_response = api_client.get(f"/api/tasks/status/{task_id}")
        assert task_response.status_code == status.HTTP_200_OK
    time.sleep(0.1)
    return TaskStatusResponse.model_validate(task_response.json())


def test_wait_unit(mocker: MockerFixture, client: TestClient, any_uuid: uuid.UUID) -> None:
    class MockTask:
        id: uuid.UUID = any_uuid

    mocker.patch("api.routes.run.wait_for.delay", return_value=MockTask)
    response = client.get("/api/run/wait?seconds=5")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("task_id") == str(any_uuid)


@pytest.mark.integration
@pytest.mark.usefixtures("celery_session_worker")
def test_wait_integration_success(client: TestClient) -> None:
    task_response = call_wait_endpoint(client, fail=False)
    assert task_response.status == states.SUCCESS


@pytest.mark.integration
@pytest.mark.usefixtures("celery_session_worker")
def test_wait_integration_failure(client: TestClient) -> None:
    task_response = call_wait_endpoint(client, fail=True)
    assert task_response.status == states.FAILURE


@pytest.mark.integration
def test_that_the_failures_and_statistics_match(client: TestClient) -> None:
    failures_response = client.get("/api/tasks/failures")
    assert failures_response.status_code == status.HTTP_200_OK
    assert len(CeleryTaskIdList.model_validate(failures_response.json()).task_ids) >= 1
    stats_response = client.get("/api/tasks/statistics")
    assert stats_response.status_code == status.HTTP_200_OK
    stats = CeleryTaskStatistics.model_validate(stats_response.json())
    assert stats.total >= 2
    assert stats.pending == 0
    assert stats.succeeded >= 1
    assert stats.failed >= 1
    assert stats.success_rate == stats.succeeded / stats.total
