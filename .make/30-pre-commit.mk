# See ../makefile


.PHONY: precommit-install-hook  ## install the pre-commit-hook in .git/hooks
precommit-install-hook:
	pre-commit install


.PHONY: precommit-run-files  ## run all precommit-steps on all files
precommit-run-files:
	pre-commit run --all-files

