# See ../makefile

.PHONY: flake8-pylint  ## show which pylint is used
pylint-which:
	@ which pylint


.PHONY: pylint  ## run pylint on python-files
pylint: pylint-which
	- pylint src/ tests/
