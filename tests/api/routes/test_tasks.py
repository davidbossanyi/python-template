import uuid

import pytest
from celery import states
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.integration
@pytest.mark.usefixtures("celery_session_worker")
def test_get_status(client: TestClient, any_uuid: uuid.UUID) -> None:
    response = client.get(f"/api/tasks/status/{any_uuid}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("task_id") == str(any_uuid)
    assert response.json().get("status") == states.PENDING
    assert response.json().get("result") is None


def test_get_status_validation_error(client: TestClient, any_string: str) -> None:
    response = client.get(f"/api/tasks/status/{any_string}")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
