"""autoread_dotenv.autoread

IMPORTANT: a sitecustomize-module is loaded automatically for every python-process
started in the virtualenv where this module is installed.

For more information, please see:
  - https://pymotw.com/2/site/
  - https://nedbatchelder.com/blog/201001/running_code_at_python_startup.html

- return-statements are not allowed in the special module.

- pytest-coverage does not like if-statements in this special module:
  It reports the if-condition as "didn't jump to the function exit".
  As a work-around we use an assignment with a ternary operator.

  if condition:
    do

  becomes:

  _ = do if condition else False

- Assumed directory-structure:
  The virtualenv of your project **must** be created as a
  .venv-subfolder inside your project-directory.
  This corresponds to poetry-config "in-project = true".
  The .env-file must reside in the root of your project-directory.

  <project-root>
      .env
      .venv/
          bin/
              python
          lib/
          pyvenv.cfg

  We also support toplevel-symlinks to the corresponding .venv-files
      bin/       -> .venv/bin/
      lib/       -> .venv/lib/
      pyvenv.cfg -> .venv/pyvenv.cfg

"""
import pathlib as pl
import sys

try:
    import dotenv

    dotenv_available = 1  # pylint: disable=invalid-name
except ImportError:  # pragma: no cover
    dotenv_available = 0  # pylint: disable=invalid-name


def get_dotenv_path() -> pl.Path:
    """"""
    # sys.prefix is <project-root>/.venv or <project-root> when using toplevel symlinks to .venv
    prefix = pl.Path(sys.prefix)
    base_dir = prefix.parent if prefix.name == ".venv" else prefix
    dotenv_file = base_dir / ".env"

    if not dotenv_file.exists(): # pragma: no cover
        return None

    return dotenv_file


def autoread_dotenv() -> None:
    """"""
    dotenv_file = get_dotenv_path()

    if dotenv_file and dotenv_available:
        try:
            dotenv.load_dotenv(dotenv_file, override=False, interpolate=True, verbose=True)
        except AttributeError:  # pragma: no cover
            # this happens when django-dotenv was installed
            # while we depend on python-dotenv.
            pass
