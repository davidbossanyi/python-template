import re

from api.dependencies import get_azure_storage_config, get_version


def test_get_version() -> None:
    get_version.cache_clear()
    version = get_version()
    assert re.match("^(0|[1-9]d*).(0|[1-9]d*).(0|[1-9]d*)", version)


def test_get_azure_storage_config(azurite_account_key: str) -> None:
    get_azure_storage_config.cache_clear()
    actual = get_azure_storage_config()
    assert actual.key == azurite_account_key
