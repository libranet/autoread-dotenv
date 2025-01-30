# pylint: disable=import-outside-toplevel
# pylint: disable=missing-function-docstring
"""Testing of module autoread_dotenv.__init__."""

import warnings

MODULE_NAME = "autoread_dotenv"


def test_simple_warning():
    from autoread_dotenv import SimpleWarning

    with warnings.catch_warnings(record=True) as warning_list:
        with SimpleWarning():
            warnings.warn("This is a test warning.")

            assert len(warning_list) == 1
            warning = warning_list[-1]
            assert issubclass(warning.category, UserWarning)
            assert str(warning.message) == "This is a test warning."
            # assert f"Warning from {MODULE_NAME}" in str(warning.message)
