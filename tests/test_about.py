"""Testing of module autoread_dotenv.about."""

import typing as tp

import packaging.version


def test_version() -> None:
    from autoread_dotenv.about import version

    assert isinstance(version, str)
    assert packaging.version.parse(version) >= packaging.version.parse("0.0")


def test_license() -> None:
    from autoread_dotenv.about import license_

    assert isinstance(license_, str)
    assert license_ == "MIT"


def test_get_metadata_package_unknown_distribution() -> None:
    """A non-installed distribution-name must fall back to "unknown" values, not raise."""
    from autoread_dotenv.about import get_metadata_package

    pkginfo = get_metadata_package("this-package-does-not-exist")

    assert pkginfo == {"author_email": "unknown", "license": "unknown", "version": "unknown"}


def test_get_metadata_package_value_error(monkeypatch) -> None:
    """A `ValueError` from `importlib.metadata.metadata()` must fall back, not raise.

    A `ValueError` is what `importlib.metadata.metadata("")` raises when `__package__` is None -
    but its behavior for an empty distribution-name is not consistent across Python versions, so
    `metadata()` itself is mocked here instead, to test the fallback deterministically.
    """
    import importlib.metadata

    from autoread_dotenv.about import get_metadata_package

    def raise_value_error(_name) -> tp.NoReturn:
        msg = "A distribution name is required."
        raise ValueError(msg)

    monkeypatch.setattr(importlib.metadata, "metadata", raise_value_error)
    pkginfo = get_metadata_package("autoread-dotenv")

    assert pkginfo == {"author_email": "unknown", "license": "unknown", "version": "unknown"}
