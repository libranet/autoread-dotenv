"""Testing of module autoread_dotenv."""

import os
import pathlib as pl
import sys
import warnings

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


def test_autoread_dotenv_path_override(tmp_path: pl.Path, monkeypatch) -> None:
    """AUTOREAD_DOTENV_PATH must take precedence over sys.prefix-based discovery."""
    from autoread_dotenv import get_dotenv_path, get_expected_dotenv_path

    # sys.prefix resolves to a project-root with its own (different) .env
    fake_venv = tmp_path / "project" / ".venv"
    fake_venv.mkdir(parents=True)
    (tmp_path / "project" / ".env").write_text("FOO=from-sys-prefix\n")
    monkeypatch.setattr("sys.prefix", str(fake_venv))

    # the override points elsewhere entirely
    override_file = tmp_path / "elsewhere" / "custom.env"
    override_file.parent.mkdir()
    override_file.write_text("FOO=from-override\n")
    monkeypatch.setenv("AUTOREAD_DOTENV_PATH", str(override_file))

    assert get_expected_dotenv_path() == override_file
    assert get_dotenv_path() == override_file


def test_autoread_dotenv_path_override_missing_file(tmp_path: pl.Path, monkeypatch) -> None:
    """A set-but-nonexistent AUTOREAD_DOTENV_PATH still overrides sys.prefix discovery.

    get_dotenv_path() reports None (no valid .env found) rather than silently falling back
    to the sys.prefix-based .env, since the override was explicit.
    """
    from autoread_dotenv import get_dotenv_path

    fake_venv = tmp_path / "project" / ".venv"
    fake_venv.mkdir(parents=True)
    (tmp_path / "project" / ".env").write_text("FOO=from-sys-prefix\n")
    monkeypatch.setattr("sys.prefix", str(fake_venv))

    monkeypatch.setenv("AUTOREAD_DOTENV_PATH", str(tmp_path / "does-not-exist.env"))

    assert get_dotenv_path() is None


def test_autoread_dotenv_path_override_entrypoint(tmp_path: pl.Path, monkeypatch) -> None:
    """entrypoint() actually loads env-vars from the AUTOREAD_DOTENV_PATH override."""
    from autoread_dotenv import entrypoint

    override_file = tmp_path / "custom.env"
    override_file.write_text("FOO=from-override\n")
    monkeypatch.setenv("AUTOREAD_DOTENV_PATH", str(override_file))
    monkeypatch.delenv("FOO", raising=False)

    entrypoint()
    assert os.getenv("FOO") == "from-override"


@pytest.mark.skipif(sys.platform == "win32", reason="chmod-based permission-denial isn't reliable on Windows")
def test_autoread_dotenv_unreadable_file_warns(tmp_path: pl.Path, monkeypatch) -> None:
    """An unreadable .env (passes is_file(), fails to open) warns instead of crashing."""
    from autoread_dotenv import entrypoint

    unreadable_file = tmp_path / "unreadable.env"
    unreadable_file.write_text("FOO=foo\n")
    unreadable_file.chmod(0o000)
    monkeypatch.setenv("AUTOREAD_DOTENV_PATH", str(unreadable_file))
    monkeypatch.delenv("FOO", raising=False)

    try:
        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter("always")
            entrypoint()  # must not raise

        assert os.getenv("FOO") is None  # nothing was loaded
        assert len(warning_list) == 1
        assert "Could not read" in str(warning_list[-1].message)
    finally:
        unreadable_file.chmod(0o644)


def test_get_dotenv_path_permission_error_on_stat(monkeypatch) -> None:
    """A PermissionError raised by is_file() itself must not crash get_dotenv_path().

    Pathlib does this on Python < 3.12 for an unreadable parent directory, unlike the
    "file just doesn't exist" case. get_dotenv_path() should optimistically return the
    path and let load_dotenv() downstream report the real, more specific error instead.
    """
    from autoread_dotenv import get_dotenv_path, get_expected_dotenv_path

    def raise_permission_error(_self: pl.Path) -> bool:
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr(pl.Path, "is_file", raise_permission_error)

    assert get_dotenv_path() == get_expected_dotenv_path()


def test_str_to_bool_warns_on_unrecognized_value() -> None:
    """A typo like "fasle" must warn instead of silently behaving like "false"."""
    from autoread_dotenv import str_to_bool

    with warnings.catch_warnings(record=True) as warning_list:
        warnings.simplefilter("always")
        result = str_to_bool("fasle")

    assert result is False
    assert len(warning_list) == 1
    assert "Unrecognized boolean value" in str(warning_list[-1].message)


@pytest.mark.parametrize("value", ["1", "true", "Yes", "0", "false", "No", ""])
def test_str_to_bool_recognized_values_do_not_warn(value: str) -> None:
    """None of the documented true/false spellings should trigger the typo-warning."""
    from autoread_dotenv import str_to_bool

    with warnings.catch_warnings(record=True) as warning_list:
        warnings.simplefilter("always")
        str_to_bool(value)

    assert len(warning_list) == 0
