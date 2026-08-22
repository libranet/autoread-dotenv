# Changelog

All notable changes to this project will be documented in this file.

## Unreleased

- Fix `just install` failing on Windows with `error: justfile does not contain recipe 'uv-set-python-version'`: the recipe was tagged `[unix]`-only with no `[windows]`
  counterpart, unlike its siblings (`create-dirs`, `symlink-venv-dirs`,
  `dotenv-install-from-template`, `dotenv-set-basedir`), which already had both. Added the
  missing `[windows]` variant (PowerShell `Move-Item`/`Set-Content`). Found by the new
  `windows-latest` CI job below actually failing on it.

- Add a `windows-latest` job (Python 3.14) to the `testing.yaml` CI matrix. The
  `Operating System :: Microsoft :: Windows` classifier was previously unbacked by any CI
  run: only `ubuntu-latest` was tested, and the one permission-related test that differs on
  Windows (`test_autoread_dotenv_unreadable_file_warns`) is `skipif`'d there, so that path
  was untested on the platform it'd differ from most. Gates the ubuntu-only
  `ubuntu-remove-global-sitecustomize` step behind `runner.os == 'Linux'` and forces `bash`
  as the default shell so the existing `${VAR}`-style steps work identically on Windows'
  Git Bash instead of falling back to incompatible pwsh syntax.

- Remove stale `# pragma: no cover` markers on `get_metadata_package()`'s `ValueError`/
  `PackageNotFoundError` fallbacks in `about.py`. Both branches are already exercised by
  `tests/test_about.py` and hit 100% coverage on their own; the pragmas were just masking
  that fact, making it look like these import-time safety nets were trusted rather than
  tested.

- Fix `get_dotenv_path()` crashing on Python < 3.12 when `is_file()` itself raises
  `PermissionError` (e.g. an unreadable parent directory) instead of reporting "not found" the
  way it does on 3.12+. It now optimistically returns the path and lets `load_dotenv()`
  downstream report the real, more specific error.

- Make `str_to_bool()` warn on unrecognized values (e.g. `AUTOREAD_ENFORCE_DOTENV=fasle`) instead
  of silently treating them the same as `false`.

- Rename `.github/workflows/release.yaml` to `releasing.yaml`.

- Add `pypi` and `test-pypi` entries to `[project.urls]`.

- Fix `docs/security.md`'s "Supported Versions" table listing a `1.1.x` line that was never
  released; trim the leftover GitHub template text and a grammar typo in the same section.

- Fix typo in `.github/CODEOWNERS`.

- Cap `PYTEST_ADDOPTS`'s `--numprocesses auto` to `--numprocesses 4` in `.env.template`, avoiding
  noisy `CoverageWarning: No data was collected` from idle pytest-xdist workers on our small test
  suite.

- Configure the `ty` VS Code extension as the Python language server (`ty.importStrategy`,
  `ty.interpreter`, `python.languageServer`), replacing the disabled `mypy-type-checker` settings.

- Enable `python.terminal.useEnvFile` so VS Code integrated terminals load `.env`.

- Add `just release`-integrated `bump-dev-version`/`bump-stable-version` recipes so the version is
  automatically bumped to the next dev-marker after each release, instead of relying on remembering
  to do it by hand.

- Fix the broken `uv-bump-version` justfile recipe: it ran `uv version {{value}}` (which tries to
  set the version to the literal string, e.g. `"patch"`) instead of `uv version --bump {{value}}`.

- Bump development version to `1.0.6.dev1`.

- Add a `codespell` pre-commit hook.

- Fix typo in `.just/ty.justfile` comment.

- Add an `AUTOREAD_DOTENV_PATH` environment-variable to override where the `.env`-file is looked
  up, for setups that don't follow the in-project-virtualenv convention (global installs,
  containers, editable mounts, ...). Takes precedence over the `sys.prefix`-based discovery. See
  `docs/readme.md` and the `autoread_dotenv.utils.get_expected_dotenv_path` docstring.

- Fix `entrypoint()` crashing every Python process in the venv when `.env` exists but can't be
  read (e.g. permission-denied): `dotenv.load_dotenv(...)` now catches `OSError` and warns via
  `simple_warning()`, consistent with the other failure paths in that function. Also fixed the
  existing "django-dotenv installed instead of python-dotenv" warning to go through
  `simple_warning()` too (it previously bypassed it), and cleaned up a stray-whitespace bug in
  that message's line-continuation.

- Add a real subprocess-based integration test (`test_entrypoint_fires_in_subprocess` in
  `tests/test_entrypoints.py`): spawns `sys.executable` as a genuine child process and asserts
  the sitecustomize hook actually fires and populates its `os.environ`, using
  `AUTOREAD_DOTENV_PATH` to point it at a throwaway `.env`. The rest of the test-suite only
  exercises the logic in-process (`monkeypatch.setattr("sys.prefix", ...)` + calling
  `entrypoint()` directly), which can't catch the hook failing to fire across a real process
  boundary (e.g. an editable install silently missing entry-point metadata). Paired with a
  `python -S` sanity-check (`test_entrypoint_does_not_fire_with_python_dash_s`) confirming the
  first test is actually driven by the sitecustomize hook and not some other leak.

- Add Python 3.15 (currently at rc1) to the `testing.yaml` CI matrix, ahead of the stable
  release. Verified locally first: `uv python install "3.15"` resolves to `3.15.0rc1` (there is
  no stable 3.15 release yet, so `uv` treats the rc as the match), and the full test-suite
  passes against it unmodified.

- Document and fix autoread-dotenv's startup-time cost in the new `docs/performance.md`, since it
  runs on every Python process start in the venv. Measured with `hyperfine`: opting into
  `sitecustomize-entrypoints`'s entry-point discovery costs ~2.9x a bare venv's startup time
  regardless of which entrypoints are registered (not autoread-dotenv's to fix); autoread-dotenv
  itself was adding another ~24-25ms on top of that, entirely import cost (`import dotenv` +
  `about.py`'s eager `importlib.metadata` lookup), not actual `.env`-parsing work. Fixed both:
  `entrypoint()` now checks whether a `.env` exists before importing `dotenv` at all, and
  `__init__.py` no longer imports `about.py` (see BREAKING note below). The "no `.env` found" case
  dropped from 60.4ms to 38.7ms - now within noise of the bare hook-mechanism floor. Added
  `.just/benchmark.justfile` (`just benchmark-startup`, `just benchmark-importtime`) so the
  numbers are reproducible rather than a one-off snapshot. Tracking is doc-only / re-run manually
  for now, no CI job or third-party benchmarking service.

- **BREAKING:** Remove `autoread_dotenv.__version__`, `__author__`, and `__license__`. They forced
  `about.py`'s `importlib.metadata` lookup to run on every process start via the sitecustomize
  hook, whether or not anything read them (see above). Use
  `autoread_dotenv.about.version`/`.license_`/`.authors` directly instead - unchanged, just no
  longer re-exported from the package root.

## 1.0.5 (2026-08-16)

- Add codespell as dev-dependency for spellchecking.

- Drop pylint as linter.

- Drop Python 3.8 support.

- Fix `TypeError: SimpleWarning.simple_message() takes 1 positional argument but 5 were given`,
  raised whenever a warning fired inside the `sitecustomize` entrypoint (e.g. a missing `.env`
  file). `SimpleWarning.simple_message` was assigned directly to `warnings.formatwarning`, which
  the stdlib calls as `formatwarning(message, category, filename, lineno, line=None)` - up to 5
  positional arguments, not the 1 `simple_message` accepted. Refactored `SimpleWarning` into the
  `simple_warning()` context manager, whose `simple_format()` callback matches that signature.

- Move warning utilities from `utils.py` to new `warnings.py` module.

- Fix warning message to show full expected `.env` path instead of `None`.

- Add `get_expected_dotenv_path()` helper function.

- Use `monkeypatch` consistently in tests.

- Improve test coverage for warning formatting.

- Remove redundant `autoapi` dependency (use `sphinx-autoapi` only).

- Update `from __future__ import annotations` comments.

- Add `.just/zizmor.justfile` and an active `security` dependency-group to lint GitHub Actions
  workflows with `zizmor`.

- Wire the `pyroma` dependency-group into `pre-commit` instead of leaving it unused.

- Change `DOTENV_INSTALLED` from an `int` sentinel to a plain `bool`.

- Use `license.md`'s copyright year as "2023-present" so it never needs manual bumping.

- Fix `.just/release.justfile` reading `tool.poetry.version` (a poetry-to-uv leftover) instead of
  `project.version`.

- Fix `docs/readme.md` still saying "Python 3.8+" instead of "3.9+".

- Fix the unusable `tomli` fallback in `docs/conf.py` by declaring it in the `docs`
  dependency-group for Python \<3.11.

- Declare `packaging` and `importlib_metadata` explicitly in the `testing` dependency-group
  instead of relying on them being pulled in transitively.

- Stop importing the private `sitecustomize._vendor.importlib_metadata` in
  `tests/test_entrypoints.py`; use stdlib `importlib.metadata` (Python >=3.10) or the
  `importlib_metadata` backport instead.

- Add `uv audit` dependency-vulnerability scanning as a `pre-commit` hook and `just uv-audit`
  recipe.

- Restore the defensive metadata fallback in `about.py`: `get_metadata_package()` no longer
  raises `KeyError`/`PackageNotFoundError` at import time, falling back to "unknown" values.

- Add a trusted-publishing release workflow (`.github/workflows/release.yaml`): builds and signs
  build provenance for the package, publishes every `main` push to TestPyPI, and publishes to
  PyPI via OIDC Trusted Publishing when a GitHub Release is published.

## 1.0.4 (2026-01-18)

- Switch from `poetry` to `uv` to manage this package.

- Switch from `make` to `just` as task-runner.

- Add support for Python 3.14.

- Increase test coverage to 100%.

- Modernize GitHub Actions workflows and re-enable dependabot.

- Add `fail-fast: false` to linting workflow to run all Python versions.

- Fix codecov upload configuration.

- Fix mypy type-ignore comments for Python 3.8 compatibility.

- Modernize readthedocs configuration.

- Add `.just/gh.justfile` with GitHub CLI commands.

- Update justfiles to use `uv run` instead of direct `.venv/bin` paths.

- Bump locked dependency versions.

- No functional changes in the package.

## 1.0.3 (2025-01-15)

- Rename environment-variable `ENFORCE_DOTENV` into `AUTOREAD_ENFORCE_DOTENV`.

- Fix string to bool conversion when "AUTOREAD_ENFORCE_DOTENV" env-variable is set.

## 1.0.2 (2023-04-30)

- Add `py.typed` file to package.

- Add security-checks with `bandit`.

- Remove function `autoread_dotenv.cancel`, since it has been been moved `sitecustomize-entrypoints` v1.1.0?

- Remove range-pinning `python = ">=3.8.0,<4.0"`, only specify bottom-range `">=3.8.0"`.

- Remove range-pinned dependencies `tox`, `nox`.

## 1.0.1 (2023-03-30)

- Refactoring of granular makefiles.

- Refactored and renamed entrypoint into `autoread_dotenv.entrypoint`.

- Add boilerplate-files to comply with Github's [_Community Standards_](https://github.com/libranet/autoread-dotenv/community)

- Test releasing via `poetry-release`.

- Convert docs from restructured text to markdown.

- Update project-description in pyproject.toml. [WouterVH]

## 1.0 (2023-03-09)

- Add `.readthedocs.yaml`.

- Package created by \[Wouter Vanden Hove <wouter@libranet.eu>\]
