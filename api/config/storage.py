from pathlib import Path

from pydantic import BaseSettings


class AzureStorageConfig(BaseSettings):
    key: str
    queue_url: str
    connection_string: str

    class Config:
        env_prefix = "azure_storage_account_"
        env_file = Path(__file__).parent.parent.parent / "azurite.env"
