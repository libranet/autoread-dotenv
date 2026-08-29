"""autoread_dotenv.status.

Load-outcome enum for `entrypoint()`.
"""

import enum


class LoadStatus(enum.Enum):
    """Outcome of the most recent `entrypoint()` call.

    `entrypoint()` never raises for a configuration problem - it warns and records the
    reason here instead. Query it via the module-level `autoread_dotenv.last_load_status`,
    or use the value `entrypoint()` returns.
    """

    NOT_RUN = "not-run"
    LOADED = "loaded"
    MISSING = "missing"
    DOTENV_NOT_INSTALLED = "dotenv-not-installed"
    LOAD_FAILED = "load-failed"
