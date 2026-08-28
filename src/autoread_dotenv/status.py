"""autoread_dotenv.status."""

import enum


class LoadStatus(enum.Enum):
    """Outcome of the most recent :func:`entrypoint` call.

    ``entrypoint()`` never raises for a configuration problem - it warns and records the
    reason here instead. Query it via the module-level :data:`last_load_status`, or use
    the value ``entrypoint()`` returns.
    """

    NOT_RUN = "not-run"
    LOADED = "loaded"
    MISSING = "missing"
    DOTENV_NOT_INSTALLED = "dotenv-not-installed"
    LOAD_FAILED = "load-failed"
