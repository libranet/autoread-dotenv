# See ../makefile

.PHONY: pytest ## run pytest on python-files
pytest:
	- .venv/bin/pytest tests


.PHONY: pytest-pdb  ## run pytest on python-files with the --pdb-flag
pytest-pdb:
	- .venv/bin/pytest tests --pdb


.PHONY: pytest-cov  ## run pytest and generate html-coverage --pdb-flag
pytest-cov:
	- .venv/bin/pytest tests --cov=src --cov-report html  --cov-report xml --cov-report term  -v


.PHONY: pytest-pdb-cov  ## run pytest with the --pdb-flag and generate html-coverage
pytest-pdb-cov:
	- .venv/bin/pytest tests --cov=src --cov-report html  --cov-report xml --cov-report term  -v  --pdb


.PHONY: pytest-pdb-cov-lf
pytest-pdb-cov-lf:
	- .venv/bin/pytest tests --cov=src --cov-report html -v --pdb --lf
