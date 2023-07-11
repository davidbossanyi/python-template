from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class AzureStorageConfig(BaseSettings):
    key: str
    queue_url: str
    connection_string: str

    model_config = SettingsConfigDict(
        env_prefix="azure_storage_account_", env_file=Path(__file__).parent.parent.parent / "azurite.env"
    )
