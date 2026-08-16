"""autoread_dotenv.utils.

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

from __future__ import annotations

import os
import pathlib as pl
import sys

#: Escape hatch for layouts where sys.prefix does not resolve to the project-root
#: (global installs, containers, editable mounts, ...). When set, it points directly
#: at the .env file to use, bypassing the sys.prefix-based discovery below entirely.
AUTOREAD_DOTENV_PATH_VAR: str = "AUTOREAD_DOTENV_PATH"


def get_expected_dotenv_path() -> pl.Path:
    """Return the expected location of the .env-file.

    Honors the ``AUTOREAD_DOTENV_PATH`` environment-variable when set: it is used verbatim
    as the path to the .env-file, for setups that don't follow the in-project-virtualenv
    convention (global installs, containers, editable mounts, ...).

    Otherwise falls back to the in-project-virtualenv convention:
    sys.prefix is <project-root>/.venv or
    <project-root> when using toplevel symlinks to .venv
    """
    override = os.getenv(AUTOREAD_DOTENV_PATH_VAR)
    if override:
        return pl.Path(override)

    prefix: pl.Path = pl.Path(sys.prefix)
    base_dir: pl.Path = prefix.parent if prefix.name == ".venv" else prefix
    return base_dir / ".env"


def get_dotenv_path() -> pl.Path | None:
    """Return the location of the .env for in-project virtualenvs.

    Return None if the .env-file does not exist.
    """
    dotenv_file = get_expected_dotenv_path()
    if dotenv_file.is_file():
        return dotenv_file
    return None


def str_to_bool(value: str) -> bool:
    """Convert a string value to a boolean."""
    return value.lower() in {"1", "true", "yes"}
