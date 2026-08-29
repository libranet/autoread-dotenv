"""autoread_dotenv.warnings - Warning utilities."""

from __future__ import annotations

import contextlib
import typing as tp
import warnings


class AutoreadDotenvWarning(UserWarning):
    """Category for every runtime warning `autoread-dotenv` emits.

    A dedicated subclass of `UserWarning` lets callers silence *only* this package
    without also muting unrelated `UserWarning`s, via
    `warnings.filterwarnings("ignore", category=AutoreadDotenvWarning)` or pytest's
    `filterwarnings` config. Re-exported as `autoread_dotenv.AutoreadDotenvWarning`.

    Note: `PYTHONWARNINGS` / `-W` cannot reference this category - the interpreter
    parses those filters before `site-packages` is importable, so only built-in
    categories resolve there. And because `entrypoint()` runs from `sitecustomize`
    at startup, an in-process filter only affects a later manual `entrypoint()` call,
    not the startup pass. See `docs/configuration.md`.
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
