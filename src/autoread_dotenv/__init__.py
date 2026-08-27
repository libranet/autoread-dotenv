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

For layouts that don't follow this convention (global installs, containers, editable
mounts, ...), set the ``AUTOREAD_DOTENV_PATH`` environment-variable to the .env-file to
use instead - it bypasses sys.prefix-based discovery entirely. See
:func:`autoread_dotenv.utils.get_expected_dotenv_path`.

"""

from __future__ import annotations  # enables X | Y syntax in annotations for Python <3.10

import os
import typing as tp
import warnings as stdlib_warnings

if tp.TYPE_CHECKING:  # pragma: no cover
    import pathlib as pl

from autoread_dotenv.utils import get_dotenv_path, get_expected_dotenv_path, str_to_bool
from autoread_dotenv.warnings import simple_warning

__all__: list[str] = [
    "entrypoint",
    "get_dotenv_path",
    "simple_warning",
    "str_to_bool",
]


def entrypoint() -> None:
    """Set environment-variable from the in-project .env-file."""
    dotenv_file: pl.Path | None = get_dotenv_path()

    if not dotenv_file:  # pragma: no cover
        with simple_warning():
            expected_path = get_expected_dotenv_path()
            stdlib_warnings.warn(f"{expected_path} does not exist, please create it.", stacklevel=2)
        return

    try:
        # This hook runs from sitecustomize on every Python startup, so the optional
        # dependency is imported only after we know there is a .env file to load.
        # That keeps the hot path cheap when the project is not using a local .env.
        import dotenv  # noqa: PLC0415
    except ImportError:  # pragma: no cover
        with simple_warning():
            stdlib_warnings.warn("Module 'dotenv' not found. Please pip install 'python-dotenv'.", stacklevel=2)
        return

    enforce_dotenv: bool = str_to_bool(os.getenv("AUTOREAD_ENFORCE_DOTENV", "1"))

    try:
        dotenv.load_dotenv(dotenv_file, override=enforce_dotenv, interpolate=True, verbose=True)
    except AttributeError:  # pragma: no cover
        with simple_warning():
            stdlib_warnings.warn(
                "Module 'dotenv.load_dotenv' not found. "
                "This occurs when django-dotenv was installed while we depend on python-dotenv.",
                stacklevel=2,
            )
    except OSError as exc:
        # e.g. a permission-denied .env: get_dotenv_path() only checked is_file(), not
        # readability. Warn instead of letting this crash every process in the venv.
        with simple_warning():
            stdlib_warnings.warn(f"Could not read {dotenv_file}: {exc}", stacklevel=2)
