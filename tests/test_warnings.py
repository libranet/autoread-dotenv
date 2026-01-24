# pylint: disable=import-outside-toplevel
# pylint: disable=missing-function-docstring
"""Testing of module autoread_dotenv.warnings."""

import warnings


def test_simple_warning() -> None:
    from autoread_dotenv.warnings import simple_warning

    with warnings.catch_warnings(record=True) as warning_list, simple_warning():
        warnings.warn("This is a test warning.", stacklevel=2)

        assert len(warning_list) == 1
        warning = warning_list[-1]
        assert issubclass(warning.category, UserWarning)
        assert str(warning.message) == "This is a test warning."


def test_simple_warning_format() -> None:
    from autoread_dotenv.warnings import simple_warning

    with simple_warning():
        # formatwarning is replaced inside the context manager
        output = warnings.formatwarning("Test message", UserWarning, "test.py", 1)

    assert "Warning from autoread_dotenv.warnings:" in output
    assert "Test message" in output
