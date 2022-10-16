import uuid

import pytest
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient, ContainerClient
from fastapi.testclient import TestClient

from api.dependencies import get_azure_storage_config
from api.main import app
from api.workers.config import CeleryConfig

azure_storage_config = get_azure_storage_config()


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
    return azure_storage_config.key


@pytest.fixture(scope="session")
def celery_config() -> dict:
    return {"broker_url": CeleryConfig.broker_url, "result_backend": CeleryConfig.result_backend}


@pytest.fixture(scope="session")
def celery_container_client() -> ContainerClient:
    service_client = BlobServiceClient.from_connection_string(azure_storage_config.connection_string)
    try:
        container_client = service_client.create_container("celery-test")
    except ResourceExistsError:
        container_client = service_client.get_container_client("celery-test")
    return container_client
