from pydantic import BaseSettings


class AzureStorageConfig(BaseSettings):
    key: str
    name: str
    connection_string: str

    class Config:
        env_prefix = "azure_storage_account_"
        env_file = "azurite.env"
