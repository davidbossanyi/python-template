import os

from kombu.utils.url import safequote

from api.dependencies import get_azure_storage_config

azure_storage_config = get_azure_storage_config()


class CeleryConfig:
    broker_url = (
        os.getenv("LOCAL_CELERY_BROKER_URL")
        or f"azurestoragequeues://:{safequote(azure_storage_config.key)}@{azure_storage_config.name}"
    )
    result_backend = f"azureblockblob://{azure_storage_config.connection_string}"
