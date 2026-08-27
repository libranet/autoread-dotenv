"""Pytest fixtures for isolating .env discovery from the real project layout.

The package resolves the expected .env file relative to sys.prefix, which makes the
lookup depend on the active virtualenv and project-root layout. These fixtures create
an isolated temporary project tree and override sys.prefix so tests do not depend on
the real repository layout or any developer-local environment.

This keeps the tests hermetic while exercising the same discovery logic used at runtime.

For more information about conftest.py, please see:

 - https://docs.pytest.org/en/latest/writing_plugins.html
 - https://pytest-flask.readthedocs.io/en/latest/tutorial.html
 - https://stackoverflow.com/questions/34466027/in-pytest-what-is-the-use-of-conftest-py-files

The tests directory itself is intentionally not a Python package (no __init__.py).
Please avoid adding an __init__.py here; doing so can interfere with pytest's import
mechanics and break plugin discovery.

Usage:
======
  # run all tests from the project root:
  > pytest tests

  # display the full list of tests being run:
  > pytest tests -vv

  # stop on the first failure and drop into an interactive debugger:
  > pytest tests --pdb

  # run only specific tests or modules matching a glob:
  > pytest tests/foo/test_bar*
  > pytest tests/test_foo/test_bar*::*test_baz

  # run only tests marked with a given tag:
  > pytest -v -m "integration"
  > pytest -v -m "not integration"

  # generate coverage in the terminal and HTML report:
  > pytest --cov="autoread_dotenv" --cov-report=term --cov-report=html
"""

import importlib
import pathlib as pl

import pytest

import autoread_dotenv

# Reload the package modules during collection so the coverage report reflects the
# actual runtime state of the imported code under test.
importlib.reload(autoread_dotenv)
importlib.reload(autoread_dotenv.utils)
importlib.reload(autoread_dotenv.warnings)


@pytest.fixture
def dotenv_project(tmp_path: pl.Path, monkeypatch) -> pl.Path:
    """Build an isolated <project-root>/.venv + .env layout, independent of the real repo .env.

    autoread_dotenv locates the .env relative to sys.prefix (see utils.get_expected_dotenv_path),
    so pointing sys.prefix at a throwaway .venv is enough to sandbox these tests.
    """
    venv_dir = tmp_path / ".venv"
    venv_dir.mkdir()
    (tmp_path / ".env").write_text("FOO=foo\n")
    monkeypatch.setattr("sys.prefix", str(venv_dir))
    return tmp_path
