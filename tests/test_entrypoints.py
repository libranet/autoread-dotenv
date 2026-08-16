"""Testing of module sitecustomize."""

import os
import pathlib as pl
import subprocess
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


def test_entrypoint_fires_in_subprocess(tmp_path: pl.Path) -> None:
    """The sitecustomize hook actually fires in a real child process.

    Every other test in this test-suite exercises the logic in-process: it monkeypatches
    sys.prefix and calls entrypoint() directly. That proves the logic is correct, but not
    that Python actually discovers and runs it via the sitecustomize entrypoint at
    interpreter start-up - the one thing unit tests can't catch (for example an editable
    install silently missing entry-point metadata, or sitecustomize-entrypoints failing to
    wire itself into site.py).

    We spawn sys.executable itself as the subprocess: it is a real interpreter that has
    autoread_dotenv installed with a registered "sitecustomize" entrypoint (see
    test_entrypoint_registration above), so a plain `python -c ...` invocation is enough to
    prove the whole chain fires end-to-end - no throwaway venv needs to be built for this.
    AUTOREAD_DOTENV_PATH (see test_autoread.py) points the child directly at a throwaway
    .env, independent of whatever sys.prefix resolves to for that interpreter.
    """
    dotenv_file = tmp_path / "subprocess.env"
    dotenv_file.write_text("SUBPROCESS_TEST_VAR=hello-from-subprocess\n")

    env = os.environ.copy()
    env["AUTOREAD_DOTENV_PATH"] = str(dotenv_file)
    env.pop("SUBPROCESS_TEST_VAR", None)

    result = subprocess.run(
        [sys.executable, "-c", "import os; print(os.environ.get('SUBPROCESS_TEST_VAR', ''))"],
        env=env,
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    )

    assert result.stdout.strip() == "hello-from-subprocess"


def test_entrypoint_does_not_fire_with_python_dash_s(tmp_path: pl.Path) -> None:
    """Sanity-check for the test above: python -S skips site.py (and therefore sitecustomize).

    Confirms the previous test's assertion is actually driven by the sitecustomize hook, not
    by e.g. AUTOREAD_DOTENV_PATH leaking into the child through some other mechanism.
    """
    dotenv_file = tmp_path / "subprocess.env"
    dotenv_file.write_text("SUBPROCESS_TEST_VAR=hello-from-subprocess\n")

    env = os.environ.copy()
    env["AUTOREAD_DOTENV_PATH"] = str(dotenv_file)
    env.pop("SUBPROCESS_TEST_VAR", None)

    result = subprocess.run(
        [sys.executable, "-S", "-c", "import os; print(os.environ.get('SUBPROCESS_TEST_VAR', ''))"],
        env=env,
        capture_output=True,
        text=True,
        check=True,
        timeout=30,
    )

    assert result.stdout.strip() == ""
