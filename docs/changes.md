# Changelog

All notable changes to this project will be documented in this file.

## 1.1.0 (YYY-MM-DD)

- Drop Python 3.8 support.

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
