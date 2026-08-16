"""Testing of module sitecustomize."""

import sys

if sys.version_info >= (3, 10):  # entry_points(group=...) is stdlib-native from here on
    from importlib.metadata import entry_points
else:  # pragma: no cover
    from importlib_metadata import entry_points


def test_import_sitecustomize() -> None:
    try:
        import sitecustomize  # noqa: F401
    except ImportError as exc:
        # package sitecustomize-entrypoints is not installed
        raise AssertionError from exc


def test_entrypoint_registration() -> None:
    assert "autoread_dotenv" in entry_points(group="sitecustomize").names
