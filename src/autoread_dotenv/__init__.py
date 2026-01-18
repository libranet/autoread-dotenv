"""
autoread_dotenv.__init__.

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

from __future__ import annotations  # make | in typing work in Python 3.8

import os
import typing as tp
import warnings

if tp.TYPE_CHECKING:  # pragma: no cover
    import pathlib as pl

try:
    import dotenv

    DOTENV_INSTALLED = 1
except ImportError:  # pragma: no cover
    DOTENV_INSTALLED = 0

# pylint: disable=wrong-import-position
from autoread_dotenv.about import (
    authors as __author__,
    license_ as __license__,
    version as __version__,
)
from autoread_dotenv.utils import SimpleWarning, get_dotenv_path, str_to_bool

__all__: list[str] = [
    "__author__",
    "__license__",
    "__version__",
    "entrypoint",
    "get_dotenv_path",
]


def entrypoint() -> None:
    """Set environment-variable from the in-project .env-file."""
    dotenv_file: pl.Path | None = get_dotenv_path()
    enforce_dotenv: bool = str_to_bool(os.getenv("AUTOREAD_ENFORCE_DOTENV", "1"))

    if not DOTENV_INSTALLED:  # pragma: no cover
        with SimpleWarning():
            warnings.warn("Module 'dotenv' not found. Please pip install 'python-dotenv'.", stacklevel=2)
        return

    if not dotenv_file:  # pragma: no cover
        with SimpleWarning():
            warnings.warn(f"{dotenv_file} does not yet exist, please create it.", stacklevel=2)
        return

    try:
        dotenv.load_dotenv(dotenv_file, override=enforce_dotenv, interpolate=True, verbose=True)
    except AttributeError:  # pragma: no cover
        warnings.warn(
            "Module 'dotenv.load_dotenv' not found. \
                This occurs when django-dotenv was installed while we depend on python-dotenv.",
            stacklevel=2,
        )
