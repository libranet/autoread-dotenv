# See ../makefile

.PHONY: ruff-which  ## show which ruff is used
ruff-which:
	@ which ruff


.PHONY: ruff  ## run ruff on python-files
ruff: ruff-which
	- ruff docs/ src/ tests/


.PHONY: ruff-check  ## run ruff --check on python-files
ruff-check: ruff-which
	- ruff check docs/ src/ tests/


.PHONY: ruff-fix  ## run ruff --fix on python-files
ruff-fix: ruff-which
	- ruff --fix docs/ src/ tests/