import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture
def any_string() -> str:
    return "any-string"


@pytest.fixture
def client() -> TestClient:
    return TestClient(app=app)


@pytest.fixture
def azurite_account_name() -> str:
    return "devstoreaccount1"
