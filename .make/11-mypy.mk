# See ../makefile

.PHONY: mypy ## run mypy on python-files
mypy:
	mypy src tests

.PHONY: mypy-report ## run mypy with html-reporting
mypy-report:
	mypy src tests --html-report  var/coverage-mypy/