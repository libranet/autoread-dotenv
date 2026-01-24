# pylint: disable=import-outside-toplevel
# pylint: disable=missing-function-docstring
# mypy: disallow_untyped_defs=False

"""Testing of module autoread_dotenv."""

import os
import pathlib as pl


def test_env_path() -> None:
    from autoread_dotenv import get_dotenv_path

    env_path = get_dotenv_path()
    assert env_path


def test_autoread_dotenv(monkeypatch) -> None:
    from autoread_dotenv import entrypoint

    # initially already set via sitecustomize
    monkeypatch.delenv("FOO", raising=False)

    # foo_value = os.getenv("FOO")
    # if foo_value:
    #     del os.environ["FOO"]

    # test cleared environment
    foo_value = os.getenv("FOO")
    assert foo_value is None

    entrypoint()
    foo_value = os.getenv("FOO")
    assert foo_value == "foo"


def test_autoread_dotenv_enforce_dotenv(monkeypatch) -> None:
    from autoread_dotenv import entrypoint, str_to_bool

    enforce_dotenv = str_to_bool(os.getenv("AUTOREAD_ENFORCE_DOTENV", "1"))
    assert enforce_dotenv is True

    # initially already set in .env & loaded via sitecustomize
    # Unset the environment variable
    monkeypatch.delenv("FOO", raising=False)
    # foo = os.getenv("FOO")
    # if foo:
    #     del os.environ["FOO"]

    monkeypatch.setenv("FOO", "bar")
    # test cleared environment
    foo_value = os.getenv("FOO")
    assert foo_value == "bar"

    entrypoint()
    foo_value = os.getenv("FOO")
    assert foo_value == "foo"


def test_autoread_dotenv_not_enforce_dotenv(monkeypatch) -> None:
    from autoread_dotenv import entrypoint, str_to_bool

    # existing env-vars will now not be overridden by anything set in the .env
    monkeypatch.setenv("AUTOREAD_ENFORCE_DOTENV", "")

    enforce_dotenv = str_to_bool(os.getenv("AUTOREAD_ENFORCE_DOTENV", "1"))
    assert enforce_dotenv is False

    # initially already set in .env & loaded via sitecustomize
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
