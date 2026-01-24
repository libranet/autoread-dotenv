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
        message: Warning | str,
        category: type[Warning],  # noqa: ARG001
        filename: str,  # noqa: ARG001
        lineno: int,  # noqa: ARG001
        line: str | None = None,  # noqa: ARG001
    ) -> str:
        return f"Warning from {__name__}: {message}\n"

   # intentional monkeypatch
    warnings.formatwarning = simple_format  # ty: ignore[invalid-assignment]
    try:
        yield
    finally:
        warnings.formatwarning = old_format
