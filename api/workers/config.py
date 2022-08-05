from api.dependencies import get_azure_storage_config

azure_storage_config = get_azure_storage_config()


class CeleryConfig:
    broker_url = f"azurestoragequeues://{azure_storage_config.key}@{azure_storage_config.queue_url}"
    result_backend = f"azureblockblob://{azure_storage_config.connection_string}"
