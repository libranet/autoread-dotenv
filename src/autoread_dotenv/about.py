"""autoread_dotenv.about.

Fetch metadata from the package's pyproject.toml.
The package must be properly installed in order the metadata to be available.

"""

from __future__ import annotations

import importlib.metadata
import typing as tp

# by default __package__ is str|None
PACKAGE: str = __package__ or ""


class PkgInfo(tp.TypedDict):
    """Typed subset of a distribution's metadata."""

    author_email: str
    license: str
    version: str


def get_metadata_package(pkgname: str = "") -> PkgInfo:
    """Fetch a typed subset of ``pkgname``'s distribution metadata.

    Defaults to this package (``PACKAGE``) when ``pkgname`` is not given.
    Falls back to "unknown" values when the metadata cannot be found, so that this module -
    which runs on every Python process start via the ``sitecustomize`` entrypoint - never raises
    at import time.
    """
    if not pkgname:
        pkgname = PACKAGE

    try:
        msg = importlib.metadata.metadata(pkgname)
    except ValueError:
        # A distribution name is required. __package__ is None/empty.
        return PkgInfo(author_email="unknown", license="unknown", version="unknown")
    except importlib.metadata.PackageNotFoundError:
        # fallback if this package is not properly installed
        return PkgInfo(author_email="unknown", license="unknown", version="unknown")

    def field(key: str) -> str | None:
        # `PackageMetadata` only guarantees `in` / `[]` (no `.get()`), and `[]` on a missing key
        # is deprecated (None) or raises KeyError depending on the Python version.
        return msg[key] if key in msg else None  # noqa: SIM401 - no .get() on the protocol

    return PkgInfo(
        author_email=field("Author-email") or "unknown",
        license=field("License-Expression") or field("License") or "unknown",
        version=field("Version") or "unknown",
    )


pkginfo: PkgInfo = get_metadata_package()

version: str = pkginfo.get("version", "unknown")
license_: str = pkginfo.get("license", "unknown")
authors: str = pkginfo.get("author_email", "unknown")
