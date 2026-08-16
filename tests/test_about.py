"""Testing of module autoread_dotenv.about."""

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


def test_get_metadata_package_empty_distribution_name(monkeypatch) -> None:
    """An empty distribution-name (e.g. `__package__` is None) must fall back, not raise."""
    import autoread_dotenv.about as about_module

    monkeypatch.setattr(about_module, "PACKAGE", "")
    pkginfo = about_module.get_metadata_package()

    assert pkginfo == {"author_email": "unknown", "license": "unknown", "version": "unknown"}
