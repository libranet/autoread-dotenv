# mypy: disallow_untyped_defs=False

"""Testing of module autoread_dotenv."""

import os
import pathlib as pl

import pytest


def test_env_path(dotenv_project: pl.Path) -> None:
    from autoread_dotenv import get_dotenv_path

    env_path = get_dotenv_path()
    assert env_path == dotenv_project / ".env"


@pytest.mark.usefixtures("dotenv_project")
def test_autoread_dotenv(monkeypatch) -> None:
    from autoread_dotenv import entrypoint

    monkeypatch.delenv("FOO", raising=False)

    # test cleared environment
    foo_value = os.getenv("FOO")
    assert foo_value is None

    entrypoint()
    foo_value = os.getenv("FOO")
    assert foo_value == "foo"


@pytest.mark.usefixtures("dotenv_project")
def test_autoread_dotenv_enforce_dotenv(monkeypatch) -> None:
    from autoread_dotenv import entrypoint, str_to_bool

    enforce_dotenv = str_to_bool(os.getenv("AUTOREAD_ENFORCE_DOTENV", "1"))
    assert enforce_dotenv is True

    # Unset the environment variable, then set to a value that .env should override
    monkeypatch.delenv("FOO", raising=False)
    monkeypatch.setenv("FOO", "bar")

    # test cleared environment
    foo_value = os.getenv("FOO")
    assert foo_value == "bar"

    entrypoint()
    foo_value = os.getenv("FOO")
    assert foo_value == "foo"


@pytest.mark.usefixtures("dotenv_project")
def test_autoread_dotenv_not_enforce_dotenv(monkeypatch) -> None:
    from autoread_dotenv import entrypoint, str_to_bool

    # existing env-vars will now not be overridden by anything set in the .env
    monkeypatch.setenv("AUTOREAD_ENFORCE_DOTENV", "")

    enforce_dotenv = str_to_bool(os.getenv("AUTOREAD_ENFORCE_DOTENV", "1"))
    assert enforce_dotenv is False

    monkeypatch.delenv("FOO", raising=False)
    monkeypatch.setenv("FOO", "bar")

    # test cleared environment
    foo_value = os.getenv("FOO")
    assert foo_value == "bar"

    entrypoint()
    foo_value = os.getenv("FOO")
    assert foo_value == "bar"  # value in .env is ignored


def test_get_dotenv_path_returns_none(tmp_path: pl.Path, monkeypatch) -> None:
    """Test get_dotenv_path returns None when .env doesn't exist."""
    from autoread_dotenv import get_dotenv_path

    # Create a fake .venv directory without a .env file
    fake_venv = tmp_path / ".venv"
    fake_venv.mkdir()

    monkeypatch.setattr("sys.prefix", str(fake_venv))

    result = get_dotenv_path()
    assert result is None
