"""Property-based tests for the pure helpers in ``autoread_dotenv.utils``.

These complement the example-based tests in ``test_autoread.py``: the same functions,
fuzzed across their whole input domain instead of hand-picked cases.
"""

import pathlib as pl
import warnings

import hypothesis as ht
import hypothesis.strategies as st
import pytest

from autoread_dotenv.utils import (
    FALSE_VALUES,
    TRUE_VALUES,
    get_dotenv_path,
    get_expected_dotenv_path,
    str_to_bool,
)
from autoread_dotenv.warnings import AutoreadDotenvWarning

#: Arbitrary text, minus the one thing os.environ genuinely cannot hold (NUL).
any_text = st.text(st.characters(exclude_characters="\x00"))

#: A single, boring path component - enough to fuzz the .venv-stripping logic without
#: dragging in cross-platform path-normalisation edge cases (trailing dots/spaces,
#: separators, drive letters, ``.``/``..``).
path_segment = st.text(
    alphabet="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-",
    min_size=1,
    max_size=30,
)


@st.composite
def recased(draw: st.DrawFn, base: frozenset[str]) -> str:
    """Draw a recognised spelling from ``base`` with each letter's case flipped at random."""
    value = draw(st.sampled_from(sorted(base)))
    flips = draw(st.lists(st.booleans(), min_size=len(value), max_size=len(value)))
    return "".join(c.upper() if flip else c.lower() for c, flip in zip(value, flips))


# --------------------------------------------------------------------------- str_to_bool


@ht.given(any_text)
def test_str_to_bool_is_total(value: str) -> None:
    """Every string maps to an actual bool, never an exception."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        result = str_to_bool(value)
    assert result is True or result is False


@ht.given(any_text)
def test_str_to_bool_is_case_insensitive(value: str) -> None:
    """Case never changes the classification - guards the ``.lower()`` call."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        assert str_to_bool(value) is str_to_bool(value.swapcase())


@ht.given(recased(TRUE_VALUES))
def test_str_to_bool_true_spellings_are_true(value: str) -> None:
    assert str_to_bool(value) is True


@ht.given(recased(FALSE_VALUES))
def test_str_to_bool_false_spellings_are_false_and_silent(value: str) -> None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        result = str_to_bool(value)
    assert result is False
    assert caught == []


@ht.given(any_text.filter(lambda s: s.lower() not in TRUE_VALUES | FALSE_VALUES))
def test_str_to_bool_unrecognised_warns_once_and_is_false(value: str) -> None:
    with pytest.warns(AutoreadDotenvWarning, match="Unrecognized boolean value"):
        result = str_to_bool(value)
    assert result is False


# ----------------------------------------------------------------- get_expected_dotenv_path


@ht.given(path_segment)
def test_expected_path_uses_override_verbatim(monkeypatch: pytest.MonkeyPatch, raw: str) -> None:
    """A set AUTOREAD_DOTENV_PATH is returned as-is, regardless of sys.prefix."""
    monkeypatch.setenv("AUTOREAD_DOTENV_PATH", raw)
    monkeypatch.setattr("sys.prefix", "/some/unrelated/prefix/.venv")
    assert get_expected_dotenv_path() == pl.Path(raw)


@ht.given(path_segment)
def test_expected_path_strips_venv_component_iff_present(
    monkeypatch: pytest.MonkeyPatch,
    segment: str,
) -> None:
    """With no override, the result is always ``<sys.prefix sans trailing .venv>/.env``."""
    monkeypatch.delenv("AUTOREAD_DOTENV_PATH", raising=False)
    base = pl.Path("/tmp") / segment  # noqa: S108  (not a real path, just a fixed anchor)

    monkeypatch.setattr("sys.prefix", str(base / ".venv"))
    assert get_expected_dotenv_path() == base / ".env"

    monkeypatch.setattr("sys.prefix", str(base))  # .name != ".venv"
    assert get_expected_dotenv_path() == base / ".env"


# ------------------------------------------------------------------------ get_dotenv_path


@ht.given(any_text.filter(lambda s: "\x00" not in s and s.strip()))
def test_get_dotenv_path_is_none_or_the_expected_path(
    monkeypatch: pytest.MonkeyPatch,
    raw: str,
) -> None:
    """Whatever the override, the result is only ever None or exactly the expected path."""
    monkeypatch.setenv("AUTOREAD_DOTENV_PATH", raw)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # a pathological path may warn; behaviour is what matters
        assert get_dotenv_path() in (None, get_expected_dotenv_path())


@ht.given(create=st.booleans())
def test_get_dotenv_path_agrees_with_the_filesystem(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pl.Path,
    *,
    create: bool,
) -> None:
    """Returns the path exactly when the file is there, None when it is not."""
    target = tmp_path / ".env"
    monkeypatch.setenv("AUTOREAD_DOTENV_PATH", str(target))
    if create:
        target.write_text("X=1\n")
    else:
        target.unlink(missing_ok=True)
    assert get_dotenv_path() == (target if create else None)
