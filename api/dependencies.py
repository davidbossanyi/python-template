from functools import lru_cache
from pathlib import Path

import tomllib
from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient

from api.config.storage import AzureStorageConfig
from api.repositories.celery import AzureBlobCeleryRepository


@lru_cache
def get_azure_storage_config() -> AzureStorageConfig:
    return AzureStorageConfig()


@lru_cache
def get_version() -> str:
    with open(Path(__file__).parent.parent / "pyproject.toml", "rb") as f:
        project = tomllib.load(f)
    return str(project["tool"]["poetry"]["version"])


def azure_blob_celery_repository() -> AzureBlobCeleryRepository:
    azure_storage_config = get_azure_storage_config()
    service_client: BlobServiceClient = BlobServiceClient.from_connection_string(azure_storage_config.connection_string)
    try:
        container_client = service_client.create_container("celery")
    except ResourceExistsError:
        container_client = service_client.get_container_client("celery")
    return AzureBlobCeleryRepository(container_client)
