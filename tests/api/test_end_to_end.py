import time

import pytest
import requests  # type: ignore


@pytest.mark.integration
def test_end_to_end_success() -> None:
    secs = 4
    response_wait = requests.get(
        f"http://localhost:8000/api/examples/wait?seconds={secs}"
    )
    assert response_wait.status_code == 200
    task_id = response_wait.json().get("task_id")
    response_status_pending = requests.get(
        f"http://localhost:8000/api/tasks/status/{task_id}"
    )
    assert response_status_pending.status_code == 200
    assert response_status_pending.json().get("task_id") == task_id
    assert response_status_pending.json().get("status") == "PENDING"
    assert response_status_pending.json().get("result") is None
    time.sleep(secs + 1)
    response_status_success = requests.get(
        f"http://localhost:8000/api/tasks/status/{task_id}"
    )
    assert response_status_success.status_code == 200
    assert response_status_success.json().get("task_id") == task_id
    assert response_status_success.json().get("status") == "SUCCESS"
    assert response_status_success.json().get("result") == f"Waited for {secs} seconds."


@pytest.mark.integration
def test_end_to_end_failure() -> None:
    secs = 1
    response_wait = requests.get(
        f"http://localhost:8000/api/examples/wait?seconds={secs}"
    )
    assert response_wait.status_code == 200
    task_id = response_wait.json().get("task_id")
    time.sleep(secs + 1)
    response_status_pending = requests.get(
        f"http://localhost:8000/api/tasks/status/{task_id}"
    )
    assert response_status_pending.status_code == 200
    assert response_status_pending.json().get("task_id") == task_id
    assert response_status_pending.json().get("status") == "FAILURE"
    assert response_status_pending.json().get("result") is None
