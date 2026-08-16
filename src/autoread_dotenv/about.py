"""autoread_dotenv.about.

Fetch metadata from the package's pyproject.toml.
The package must be properly installed in order the metadata to be available.

"""

from __future__ import annotations  # enables X | Y syntax in annotations for Python <3.10

import importlib.metadata

# by default __package__ is str|None
PACKAGE: str = __package__ or ""

pkginfo: importlib.metadata.PackageMetadata = importlib.metadata.metadata(PACKAGE)

version: str = importlib.metadata.version(PACKAGE)
license_: str = pkginfo["License-Expression"]
authors: str = pkginfo["Author-email"]
