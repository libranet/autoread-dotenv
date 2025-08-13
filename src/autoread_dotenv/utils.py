"""
autoread_dotenv.utils.

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

from __future__ import annotations

import pathlib as pl
import sys
import typing as tp
import warnings

from typing_extensions import Self



class SimpleWarning:
    """Simple warning-formatting ."""

    def __init__(self) -> None:
        """Initialize class."""
        self.old_format: tp.Callable | None = warnings.formatwarning

    def __enter__(self) -> Self:
        """Enter contextmanager."""
        warnings.formatwarning = self.simple_message  # type: ignore[assignment]
        return self

    def __exit__(self, *args: object, **kwargs: dict[str, tp.Any]) -> None:
        """Exit contextmanager."""
        warnings.formatwarning = self.old_format  # type: ignore[assignment]

    @staticmethod
    def simple_message(message: str) -> str:
        """Return a simple warning-message without any traceback-info."""
        return f"Warning from {__name__}: {message}\n"


def get_dotenv_path() -> pl.Path | None:
    """
    Return the location of the .env for in-project virtualenvs.

    Return None of the .env-file does not exist.
    """
    # sys.prefix is <project-root>/.venv or <project-root> when using toplevel symlinks to .venv
    prefix = pl.Path(sys.prefix)
    base_dir = prefix.parent if prefix.name == ".venv" else prefix
    dotenv_file = base_dir / ".env"

    if dotenv_file.is_file():
        return dotenv_file

    return None


def str_to_bool(value: str) -> bool:
    """Convert a string value to a boolean."""
    return value.lower() in {"1", "true", "yes"}

