# See ../makefile

.PHONY: black  ## run black on python-files
black:
	- .venv/bin/black docs/ src/ tests/


.PHONY: flake8  ## run flake8 on python-files
flake8:
	- .venv/bin/flake8 docs/ src/ tests


.PHONY: isort  ## run isort on python-files
isort:
	- .venv/bin/isort --settings-path=pyproject.toml src/**/*.py tests/**/*.py