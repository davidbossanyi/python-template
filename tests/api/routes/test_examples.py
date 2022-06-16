import pytest
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture


class MockTask:
    id: str = "any-string"


@pytest.mark.unit
def test_wait(mocker: MockerFixture, client: TestClient, any_string: str) -> None:
    mocker.patch("api.routes.examples.wait_for.delay", return_value=MockTask)
    response = client.get("/api/examples/wait?seconds=5")
    assert response.status_code == 200
    assert response.json().get("task_id") == any_string
