# pytest


# run pytest
[group: 'pytest']
pytest *args:
    uv run pytest {{args}}


# run pytest with markers
[group: 'pytest']
pytest-marked markers="" *args:
    uv run pytest -m '{{markers}}' {{args}}


# run pytest with coverage
[group: 'pytest']
pytest-coverage *args:
    uv run pytest --color=yes --cov=src --cov-report html:var/coverage/html --cov-report xml:var/coverage/pytest-cobertura.xml --cov-report term-missing --junit-xml='var/coverage/pytest-junit.xml' {{args}}

alias pytest-cov := pytest-coverage

# run pytest with pdb
[group: 'pytest']
pytest-pdb *args:
    uv run pytest --color=yes --pdb -v {{args}}


# run pytest with last-failed
[group: 'pytest']
pytest-failed *args:
    uv run pytest --color=yes --lf {{args}}

alias pytest-lf := pytest-failed


# run pytest with pdb + last-failed
[group: 'pytest']
pytest-pdb-failed *args:
    uv run pytest --color=yes --pdb --lf {{args}}

alias pytest-lf-pdf := pytest-pdb-failed


# run pytest with filter
[group: 'pytest']
pytest-filter filter *args:
    uv run pytest --color=yes -k {{filter}} {{args}}
