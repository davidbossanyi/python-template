import pytest

from src.main import hello_world


@pytest.mark.parametrize("name", ["spam", "eggs"])
def test_hello_world(name: str) -> None:
    assert hello_world(name=name) == f"Hello {name}!"
