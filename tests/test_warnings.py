"""Testing of module autoread_dotenv.warnings."""

import warnings


def test_autoread_dotenv_warning_is_user_warning_subclass() -> None:
    from autoread_dotenv.warnings import AutoreadDotenvWarning

    assert issubclass(AutoreadDotenvWarning, UserWarning)


def test_autoread_dotenv_warning_is_reexported_from_package() -> None:
    """The category is part of the top-level public API, next to LoadStatus."""
    import autoread_dotenv
    from autoread_dotenv.warnings import AutoreadDotenvWarning

    assert autoread_dotenv.AutoreadDotenvWarning is AutoreadDotenvWarning
    assert "AutoreadDotenvWarning" in autoread_dotenv.__all__


def test_autoread_dotenv_warning_can_be_filtered_in_isolation() -> None:
    """Silencing our category must leave unrelated UserWarnings untouched."""
    from autoread_dotenv.warnings import AutoreadDotenvWarning

    with warnings.catch_warnings(record=True) as warning_list:
        warnings.simplefilter("always")
        warnings.filterwarnings("ignore", category=AutoreadDotenvWarning)
        warnings.warn("ours", AutoreadDotenvWarning, stacklevel=2)
        warnings.warn("theirs", UserWarning, stacklevel=2)

    assert [str(w.message) for w in warning_list] == ["theirs"]


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
