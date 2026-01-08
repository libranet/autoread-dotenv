# ruff



# show which ruff is used
[group: 'ruff']
ruff-which:
    @ echo -e "Using uv run ruff"


# run ruff on python-files
[group: 'ruff']
ruff *args:
    - uv run ruff docs/ etc/ src/ tests/ {{args}}


# run ruff --check on python-files
[group: 'ruff']
ruff-check *args:
    - uv run ruff check docs/ etc/ src/ tests/ {{args}}


# run ruff --fix on python-files
[group: 'ruff']
ruff-check-fix *args:
    - uv run ruff check docs/ etc/ src/ tests/ --fix {{args}}

alias ruff-fix := ruff-check-fix


# run ruff --fix on python-files
[group: 'ruff']
ruff-check-fix-unsafe *args:
    - uv run ruff check docs/ etc/ src/ tests/ --fix --unsafe-fixes {{args}}

alias ruff-fix-unsafe := ruff-check-fix-unsafe


# run ruff format on python-files
[group: 'ruff']
ruff-format *args:
    - uv run ruff format docs/ etc/ src/ tests/ {{args}}