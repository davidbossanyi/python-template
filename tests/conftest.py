import uuid

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.workers.config import CeleryConfig


@pytest.fixture
def any_string() -> str:
    return "any-string"


@pytest.fixture
def any_uuid() -> uuid.UUID:
    return uuid.uuid4()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app=app)


@pytest.fixture
def azurite_account_key() -> str:
    return "Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw=="


@pytest.fixture(scope="session")
def celery_config() -> dict:
    return {"broker_url": CeleryConfig.broker_url, "result_backend": CeleryConfig.result_backend}
