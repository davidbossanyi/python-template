from pytest_mock import MockerFixture

from api.dependencies import get_azure_storage_config, get_version


def test_get_version(mocker: MockerFixture, any_string: str) -> None:
    get_version.cache_clear()
    mocker.patch(
        "api.dependencies.tomllib.load",
        return_value={"tool": {"poetry": {"version": any_string}}},
    )
    assert get_version() == any_string


def test_get_azure_storage_config(any_string: str, azurite_account_key: str) -> None:
    get_azure_storage_config.cache_clear()
    actual = get_azure_storage_config()
    assert actual.key == azurite_account_key
