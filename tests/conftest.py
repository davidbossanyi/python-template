import uuid

import pytest
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient, ContainerClient
from fastapi.testclient import TestClient

from api.dependencies import azure_blob_celery_repository, get_azure_storage_config
from api.main import app
from api.models.tasks.metadata import CeleryTaskMetaData
from api.repositories.celery import InMemoryCeleryRepository
from api.workers.config import CeleryConfig

azure_storage_config = get_azure_storage_config()


@pytest.fixture
def any_string() -> str:
    return "any-string"


@pytest.fixture
def any_uuid() -> uuid.UUID:
    return uuid.uuid4()


@pytest.fixture
def client(in_memory_celery_repository: InMemoryCeleryRepository) -> TestClient:
    app.dependency_overrides[azure_blob_celery_repository] = lambda: in_memory_celery_repository
    return TestClient(app=app)


@pytest.fixture
def azurite_account_key() -> str:
    return azure_storage_config.key


@pytest.fixture(scope="session")
def celery_config() -> dict:
    return {"broker_url": CeleryConfig.broker_url, "result_backend": CeleryConfig.result_backend}


@pytest.fixture(scope="session")
def celery_container_client() -> ContainerClient:
    service_client: BlobServiceClient = BlobServiceClient.from_connection_string(azure_storage_config.connection_string)
    try:
        container_client = service_client.create_container("celery-test")
    except ResourceExistsError:
        container_client = service_client.get_container_client("celery-test")
    return container_client


@pytest.fixture(scope="session")
def in_memory_celery_repository() -> InMemoryCeleryRepository:
    repo = InMemoryCeleryRepository()
    task_1 = CeleryTaskMetaData(id="task_1", status="SUCCESS")
    task_2 = CeleryTaskMetaData(id="task_2", status="FAILURE")
    repo.save(tasks=[task_1, task_2])
    return repo
