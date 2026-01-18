# pylint: disable=import-outside-toplevel
# pylint: disable=missing-function-docstring
"""Testing of module autoread_dotenv.about."""

import packaging.version


def test_version() -> None:
    from autoread_dotenv.about import version

    assert isinstance(version, str)
    assert packaging.version.parse(version) >= packaging.version.parse("0.0")


def test_license() -> None:
    from autoread_dotenv.about import license_

    assert isinstance(license_, str)
    assert "Copyright" in license_
