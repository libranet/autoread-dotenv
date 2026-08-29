"""autoread_dotenv.warnings - Warning utilities."""

from __future__ import annotations

import contextlib
import typing as tp
import warnings


class AutoreadDotenvWarning(UserWarning):
    """Category for every runtime warning `autoread-dotenv` emits.

    A dedicated subclass of `UserWarning` lets callers silence *only* this package
    without also muting unrelated `UserWarning`s from the rest of their app, using
    the standard mechanisms - e.g.::

        PYTHONWARNINGS=ignore::autoread_dotenv.warnings.AutoreadDotenvWarning

    or `warnings.filterwarnings("ignore", category=AutoreadDotenvWarning)`, or
    pytest's `filterwarnings` marker.
    """


@contextlib.contextmanager
def simple_warning() -> tp.Iterator[None]:
    """Context manager for simplified warning formatting without tracebacks."""
    old_format = warnings.formatwarning

    def simple_format(
        message: Warning | str,
        category: type[Warning],  # noqa: ARG001
        filename: str,  # noqa: ARG001
        lineno: int,  # noqa: ARG001
        line: str | None = None,  # noqa: ARG001
    ) -> str:
        return f"Warning from {__name__}: {message}\n"

    # Keep runtime warnings concise and actionable: users see the warning text without
    # a full stacktrace-style traceback for a library-level configuration issue.
    warnings.formatwarning = simple_format  # ty: ignore[invalid-assignment]
    try:
        yield
    finally:
        warnings.formatwarning = old_format
