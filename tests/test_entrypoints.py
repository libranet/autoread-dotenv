# -*- coding: utf-8 -*-
# pylint: disable=import-outside-toplevel
# pylint: disable=missing-function-docstring
"""Testing of module autoread_dotenv.patch."""

def test_import_sitecustomize():

    try:
        import sitecustomize
    except ImportError:
        # package sitecustomize-entrypoints is not installed
        assert False



def test_entrypoint_registration():
    from sitecustomize._vendor.importlib_metadata import entry_points
    assert "autoread_dotenv" in entry_points(group="sitecustomize").names

