"""autoread_dotenv.utils."""

from __future__ import annotations

import os
import pathlib as pl
import sys
import warnings as stdlib_warnings

from autoread_dotenv.warnings import AutoreadDotenvWarning, simple_warning

#: Escape hatch for layouts where sys.prefix does not resolve to the project-root
#: (global installs, containers, editable mounts, ...). When set, it points directly
#: at the .env file to use, bypassing the sys.prefix-based discovery below entirely.
#:
#: The value is used verbatim - no traversal check, no confinement to the project root.
#: This is deliberate: it is developer/operator-set configuration, not attacker-controlled
#: input. Whoever can set it for a process can already set arbitrary env vars there, so
#: "load an unexpected path" crosses no privilege boundary. See docs/security.md.
AUTOREAD_DOTENV_PATH_VAR: str = "AUTOREAD_DOTENV_PATH"

#: When truthy (parsed by str_to_bool), entrypoint() installs a process-wide filter that
#: silences every AutoreadDotenvWarning - the missing-.env notice and the genuine
#: misconfiguration warnings alike. Like AUTOREAD_DOTENV_PATH it cannot live in .env itself
#: (it is read before .env is parsed). See docs/configuration.md.
AUTOREAD_DOTENV_QUIET_VAR: str = "AUTOREAD_DOTENV_QUIET"

#: Recognized spellings for str_to_bool(), case-insensitive.
TRUE_VALUES: frozenset[str] = frozenset({"1", "true", "yes"})
FALSE_VALUES: frozenset[str] = frozenset({"0", "false", "no", ""})


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

    Return None if the .env-file does not exist. If we can't even tell - e.g. a
    permission-denied parent directory raises from is_file() itself, on Python < 3.12
    where pathlib doesn't swallow that OSError the way it swallows "not found" - assume
    optimistically that it does, and let the load_dotenv() call downstream fail loudly
    with its own, more specific permission error instead of us wrongly reporting here
    that the file doesn't exist.

    Any other OSError (ENAMETOOLONG, ELOOP, a broken mount, ...) is genuinely unexpected
    for a plain stat: name the errno in a warning rather than swallowing it as an
    indistinguishable "permissions issue", then still defer to load_dotenv() downstream.
    """
    dotenv_file = get_expected_dotenv_path()
    try:
        exists = dotenv_file.is_file()
    except PermissionError:
        return dotenv_file
    except OSError as exc:
        with simple_warning():
            stdlib_warnings.warn(
                f"Unexpected {type(exc).__name__} while checking {dotenv_file}: {exc}. "
                "Assuming it exists and deferring to load_dotenv().",
                AutoreadDotenvWarning,
                stacklevel=2,
            )
        return dotenv_file
    return dotenv_file if exists else None


def str_to_bool(value: str) -> bool:
    """Convert a string value to a boolean.

    "1"/"true"/"yes" (case-insensitive) are true; "0"/"false"/"no"/"" are false. Anything
    else is treated as false too, but warns first: an unrecognized value is more likely a
    typo (e.g. AUTOREAD_ENFORCE_DOTENV=fasle) than an intentional one, and silently
    falling back to false would be indistinguishable from setting it on purpose.
    """
    lowered = value.lower()
    if lowered in TRUE_VALUES:
        return True
    if lowered not in FALSE_VALUES:
        with simple_warning():
            stdlib_warnings.warn(
                f"Unrecognized boolean value {value!r}, treating it as false. "
                "Use '1'/'true'/'yes' for true, or '0'/'false'/'no'/'' for false.",
                AutoreadDotenvWarning,
                stacklevel=2,
            )
    return False
