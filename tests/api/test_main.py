import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.unit
def test_redirect_to_docs(client: TestClient) -> None:
    resp = client.get("/")
    assert resp.history[0].status_code == status.HTTP_307_TEMPORARY_REDIRECT
    assert resp.status_code == status.HTTP_200_OK
