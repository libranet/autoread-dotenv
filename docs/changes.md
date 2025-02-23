# Changelog

All notable changes to this project will be documented in this file.


## 1.0.4 (YYY-MM-DD)

- Switch from ``poetry`` to ``uv`` to manage this package.

- Switch from ``make`` to ``just`` as task-runner.


## 1.0.3 (2025-01-15)

- Rename environment-variable ``ENFORCE_DOTENV`` into ``AUTOREAD_AUTOREAD_ENFORCE_DOTENV``.

- Fix string to bool conversion when "AUTOREAD_AUTOREAD_ENFORCE_DOTENV" env-variable is set.


## 1.0.2 (2023-04-30)

- Add ``py.typed`` file to package.

- Add security-checks with ``bandit``.

- Remove function ``autoread_dotenv.cancel``, since it has been been moved ``sitecustomize-entrypoints`` v1.1.0?

- Remove range-pinning ``python = ">=3.8.0,<4.0"``, only specifybotton-range ``">=3.8.0"``

- Remove rang-pinned dependencies ``tox``, ``nox``.          .


## 1.0.1 (2023-03-30)

- Refactoring of granular makefiles.

- Refactored and renamed entrypoint into ``autoread_dotenv.entrypoint``.

- Add boilerplate-files to comply with Github's [_Community Standards_](https://github.com/libranet/autoread-dotenv/community)

- Test releasing via ``poetry-release``.

- Convert docs from restructured text to markdown.

- Update project-description in pyproject.toml. [WouterVH]


## 1.0 (2023-03-09)

- Add ``.readthedocs.yaml``.

- Package created by [Wouter Vanden Hove <wouter@libranet.eu>]
