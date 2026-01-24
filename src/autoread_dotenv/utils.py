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

"""

from __future__ import annotations

import pathlib as pl
import sys


def get_expected_dotenv_path() -> pl.Path:
    """Return the expected location of the .env for in-project virtualenvs.

    sys.prefix is <project-root>/.venv or
    <project-root> when using toplevel symlinks to .venv
    """
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
