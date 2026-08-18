"""autoread_dotenv.about.

Fetch metadata from the package's pyproject.toml.
The package must be properly installed in order the metadata to be available.

"""

from __future__ import annotations  # enables X | Y syntax in annotations for Python <3.10

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

    return PkgInfo(
        author_email=msg.get("Author-email", "unknown"),
        license=msg.get("License-Expression") or msg.get("License") or "unknown",
        version=msg.get("Version", "unknown"),
    )


pkginfo: PkgInfo = get_metadata_package()

version: str = pkginfo.get("version", "unknown")
license_: str = pkginfo.get("license", "unknown")
authors: str = pkginfo.get("author_email", "unknown")
