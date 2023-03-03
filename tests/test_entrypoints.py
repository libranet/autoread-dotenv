# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel
# pylint: disable=missing-function-docstring
"""Testing of module autoread_dotenv.patch."""
import packaging.version


def test_import_sitecustomize():

    try:
        import sitecustomize
    except ImportError:
        # package sitecustomize-entrypoints is not installed
        assert False



def test_entrypoint():
    from sitecustomize._vendor.importlib_metadata import entry_points

    found = False
    for entry_point in entry_points(group="sitecustomize"):
        if entry_point.name == "autoread_dotenv":
            found = True
    assert found is True
