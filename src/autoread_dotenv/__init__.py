"""autoread_dotenv.__init__.

We assume following directory-structure:
The virtualenv of your project **must** be created as a
.venv-subfolder inside your project-directory.

This corresponds to poetry-config "in-project = true".
The .env-file must reside in the root of your project-directory.

.. code-block:: python

  <project-root>
      .env
      .venv/
          bin/
              python
          lib/
          lib64/
          pyvenv.cfg

  We also support toplevel-symlinks to the corresponding .venv-files:

.. code-block:: python

      bin/       -> .venv/bin/
      lib/       -> .venv/lib/
      lib64/     -> .venv/lib64/
      pyvenv.cfg -> .venv/pyvenv.cfg

"""

__version__ = "1.0.1"
__copyright__ = "Copyright 2023 Libranet"
__license__ = "MIT License"

import os
import pathlib as pl
import sys
import typing as tp
import warnings

try:
    import dotenv

    DOTENV_INSTALLED = 1
except ImportError:  # pragma: no cover
    DOTENV_INSTALLED = 0


class SimpleWarning:
    """Simple warning-formatting ."""

    def __init__(self) -> None:
        """Initialize class."""
        self.old_format: tp.Optional[tp.Callable] = warnings.formatwarning

    def __enter__(self) -> "SimpleWarning":
        """Enter contextmanager."""
        warnings.formatwarning = self.simple_message  # type: ignore
        return self

    def __exit__(self, *args) -> None:
        """Exit contextmanager."""
        warnings.formatwarning = self.old_format  # type: ignore

    @staticmethod
    def simple_message(message: str, *args, **kwargs) -> str:  # pylint: disable=unused-argument
        """Return a simple warning-message without any traceback-info."""
        return f"Warning from {__name__}: {message}\n"


def get_dotenv_path() -> pl.Path:
    """Return the location of the .env for in-project virtualenvs.

    Return None of no .env-file is found.
    """
    # sys.prefix is <project-root>/.venv or <project-root> when using toplevel symlinks to .venv
    prefix = pl.Path(sys.prefix)
    base_dir = prefix.parent if prefix.name == ".venv" else prefix
    dotenv_file = base_dir / ".env"
    return dotenv_file


def entrypoint() -> None:
    """Set environment-variable from the in-project .env-file."""
    if not DOTENV_INSTALLED:  # pragma: no cover
        with SimpleWarning():
            warnings.warn("Module 'dotenv' not found. Please pip install 'python-dotenv'.")
        return

    if not dotenv_file.exists():  # pragma: no cover
        with SimpleWarning():
            warnings.warn(f"{dotenv_file} does not yet exist, please create it.")
        return
        
    dotenv_file: pl.Path = get_dotenv_path()
    enforce_dotenv: bool = bool(os.getenv("ENFORCE_DOTENV", "1"))

    try:
        dotenv.load_dotenv(dotenv_file, override=enforce_dotenv, interpolate=True, verbose=True)
    except AttributeError:  # pragma: no cover
        warnings.warn(
            "Module 'dotenv.load_dotenv' not found."
            + "This occurs when django-dotenv was installed while we depend on python-dotenv."
        )


def cancel():
    """No-op function that can be used the cancel a registered entrypoint.

    Imagine you have multiple sitecustomize-entrypoints. If these entrypoints
    are registered via third-party packages, you cannot control the order of execution.

    Now suppose some of these entrypoints need an environment-variable that first need to be set
    by ``autoread_dotenv`` needs to be executed before the others

    entrypoint 1:  foo.needs_envvar:bar
    entrypoint 2:  autoread_dotenv.autoread:autoread_dotenv

    in your project's pyproject.toml:

    [tool.poetry.plugins."sitecustomize"]

    # cancel the first registration using the original name
    autoread_dotenv = "autoread_dotenv.autoread:cancel"

    # re-register the same function under different name
    zz_autoread_dotenv = "autoread_dotenv.autoread:autoread_dotenv"

    """
    pass  # pylint: disable=unnecessary-pass
