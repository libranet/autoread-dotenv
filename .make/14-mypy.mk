# See ../makefile

.PHONY: mypy-which  ## show which mypy is used
mypy-which:
	@ which mypy


.PHONY: mypy ## run mypy on python-files
mypy: mypy-which
	mypy src tests


.PHONY: mypy-report ## run mypy with html-reporting
mypy-report: mypy-which
	@ mkdir -p var/html/mypy/
	mypy src tests --html-report var/html/mypy/


.PHONY: mypy-html ## alias for mypy-report
mypy-html: mypy-report