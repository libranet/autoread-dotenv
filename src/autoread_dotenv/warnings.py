"""autoread_dotenv.warnings - Warning utilities."""

from __future__ import annotations

import contextlib
import typing as tp
import warnings


@contextlib.contextmanager
def simple_warning() -> tp.Iterator[None]:
    """Context manager for simplified warning formatting without tracebacks."""
    old_format = warnings.formatwarning

    def simple_format(
        message: object,
        category: type[Warning],
        filename: str,
        lineno: int,
        line: str | None = None,
    ) -> str:
        return f"Warning from {__name__}: {message}\n"

    warnings.formatwarning = simple_format
    try:
        yield
    finally:
        warnings.formatwarning = old_format
