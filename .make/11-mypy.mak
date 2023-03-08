# See ../makefile

# See ../makefile

.PHONY: mypy ## run mypy on python-files
mypy:
	.venv/bin/mypy src tests

.PHONY: mypy-report ## run mypy with html-reporting
mypy-report:
	.venv/bin/mypy src tests --html-report  var/coverage-mypy/