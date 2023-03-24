# See ../makefile

.PHONY: ruff  ## run ruff on python-files
ruff:
	- ruff docs/ src/ tests/


.PHONY: ruff-check  ## run ruff --fcheck on python-files
ruff-fix:
	- ruff --check docs/ src/ tests/


.PHONY: ruff-fix  ## run ruff --fix on python-files
ruff-fix:
	- ruff --fix docs/ src/ tests/