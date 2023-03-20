# See ../makefile


.PHONY: ruff  ## run ruff on python-files
ruff:
	- .venv/bin/ruff src/ tests/


.PHONY: ruff-fix  ## run ruff --fix on python-files
ruff-fix:
	- .venv/bin/ruff --fix src/ tests/