# Changelog

All notable changes to this project will be documented in this file.

## 1.1.0 (YYYY-MM-DD)

- Add codespell as dev-dependency for spellchecking.

- Drop pylint as linter.

- Drop Python 3.8 support.

- Refactor `SimpleWarning` class to `simple_warning()` context manager function.

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
