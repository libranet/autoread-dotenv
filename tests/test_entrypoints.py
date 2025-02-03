# pylint: disable=import-outside-toplevel
# pylint: disable=missing-function-docstring
"""Testing of module sitecustomize."""


def test_import_sitecustomize() -> None:
    # pylint: disable=unused-import
    try:
        import sitecustomize  # noqa: F401
    except ImportError as exc:
        # package sitecustomize-entrypoints is not installed
        raise AssertionError from exc


def test_entrypoint_registration() -> None:
    from sitecustomize._vendor.importlib_metadata import entry_points

    assert "autoread_dotenv" in entry_points(group="sitecustomize").names
