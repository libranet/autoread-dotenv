"""autoread_dotenv.__init__.

Automatically load the in-project `.env` when Python starts.

We assume the following directory-structure. The virtualenv of your project
**must** be created as a `.venv` subfolder inside your project-directory (this
corresponds to poetry-config `in-project = true`), and the `.env` file must
reside in the root of your project-directory:

```text
<project-root>
    .env
    .venv/
        bin/
            python
        lib/
        lib64/
        pyvenv.cfg
```

Toplevel symlinks to the corresponding `.venv` files are also supported:

```text
bin/       -> .venv/bin/
lib/       -> .venv/lib/
lib64/     -> .venv/lib64/
pyvenv.cfg -> .venv/pyvenv.cfg
```

For layouts that don't follow this convention (global installs, containers,
editable mounts, ...), set the `AUTOREAD_DOTENV_PATH` environment-variable to the
`.env` file to use instead - it bypasses `sys.prefix`-based discovery entirely.
See [`autoread_dotenv.utils.get_expected_dotenv_path`][].
"""

from __future__ import annotations  # enables X | Y syntax in annotations for Python <3.10

import os
import typing as tp
import warnings as stdlib_warnings

if tp.TYPE_CHECKING:  # pragma: no cover
    import pathlib as pl

from autoread_dotenv.status import LoadStatus
from autoread_dotenv.utils import (
    AUTOREAD_DOTENV_QUIET_VAR,
    get_dotenv_path,
    get_expected_dotenv_path,
    str_to_bool,
)
from autoread_dotenv.warnings import AutoreadDotenvWarning, simple_warning

__all__: list[str] = [
    "AutoreadDotenvWarning",
    "LoadStatus",
    "entrypoint",
    "last_load_status",
]


#: Outcome of the most recent `entrypoint()` call. `LoadStatus.NOT_RUN` until
#: `entrypoint()` has run once (it runs from `sitecustomize` on interpreter startup).
last_load_status: LoadStatus = LoadStatus.NOT_RUN


def entrypoint() -> LoadStatus:
    """Set environment-variables from the in-project .env-file.

    Returns the outcome as a [`LoadStatus`][autoread_dotenv.status.LoadStatus] and also
    records it in the module-level `last_load_status`, so a caller that discards the
    return value (`sitecustomize` does) can still be asked afterwards whether loading
    succeeded. A configuration problem is warned about, never raised - this runs on
    every interpreter startup. Every such warning uses the
    [`AutoreadDotenvWarning`][autoread_dotenv.AutoreadDotenvWarning] category (re-exported
    here from `autoread_dotenv.warnings`); see the "Silencing warnings" section of
    `docs/configuration.md` for how to filter it (and why `PYTHONWARNINGS` cannot).
    Setting `AUTOREAD_DOTENV_QUIET=1` suppresses every such warning for the process.
    """
    global last_load_status  # noqa: PLW0603

    if str_to_bool(os.getenv(AUTOREAD_DOTENV_QUIET_VAR, "0")):
        # Opt-out: silence every AutoreadDotenvWarning for the rest of this process.
        # Installed as a real filter (rather than just skipped here) so warnings emitted
        # later in this call - and by any later entrypoint() call - are covered too.
        stdlib_warnings.filterwarnings("ignore", category=AutoreadDotenvWarning)

    dotenv_file: pl.Path | None = get_dotenv_path()

    if not dotenv_file:
        with simple_warning():
            expected_path = get_expected_dotenv_path()
            stdlib_warnings.warn(
                f"{expected_path} does not exist, please create it.",
                AutoreadDotenvWarning,
                stacklevel=2,
            )
        last_load_status = LoadStatus.MISSING
        return last_load_status

    try:
        # This hook runs from sitecustomize on every Python startup, so the optional
        # dependency is imported only after we know there is a .env file to load.
        # That keeps the hot path cheap when the project is not using a local .env.
        import dotenv  # noqa: PLC0415
    except ImportError:  # pragma: no cover
        with simple_warning():
            stdlib_warnings.warn(
                "Module 'dotenv' not found. Please pip install 'python-dotenv'.",
                AutoreadDotenvWarning,
                stacklevel=2,
            )
        last_load_status = LoadStatus.DOTENV_NOT_INSTALLED
        return last_load_status

    enforce_dotenv: bool = str_to_bool(os.getenv("AUTOREAD_ENFORCE_DOTENV", "1"))

    try:
        dotenv.load_dotenv(dotenv_file, override=enforce_dotenv, interpolate=True, verbose=True)
    except AttributeError:  # pragma: no cover
        with simple_warning():
            stdlib_warnings.warn(
                "Module 'dotenv.load_dotenv' not found. "
                "This occurs when django-dotenv was installed while we depend on python-dotenv.",
                AutoreadDotenvWarning,
                stacklevel=2,
            )
        last_load_status = LoadStatus.LOAD_FAILED
        return last_load_status
    except OSError as exc:
        # e.g. a permission-denied .env: get_dotenv_path() only checked is_file(), not
        # readability. Warn instead of letting this crash every process in the venv.
        with simple_warning():
            stdlib_warnings.warn(f"Could not read {dotenv_file}: {exc}", AutoreadDotenvWarning, stacklevel=2)
        last_load_status = LoadStatus.LOAD_FAILED
        return last_load_status

    last_load_status = LoadStatus.LOADED
    return last_load_status
