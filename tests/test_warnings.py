# pylint: disable=import-outside-toplevel
# pylint: disable=missing-function-docstring
"""Testing of module autoread_dotenv.__init__."""

import warnings

MODULE_NAME = "autoread_dotenv"


def test_simple_warning() -> None:
    from autoread_dotenv import SimpleWarning

    with warnings.catch_warnings(record=True) as warning_list, SimpleWarning():
        warnings.warn("This is a test warning.", stacklevel=2)

        assert len(warning_list) == 1
        warning = warning_list[-1]
        assert issubclass(warning.category, UserWarning)
        assert str(warning.message) == "This is a test warning."
