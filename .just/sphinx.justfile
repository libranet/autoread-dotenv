# See ../makefile


# show which sphinx-build is used
[group: 'sphinx']
sphinx-build-which:
	@ which sphinx-build


# generate sphinx-docs in var/html-docs
[group: 'sphinx']
sphinx-docs:
	sphinx-build -b html -d var/cache/sphinx-doctrees -w var/log/sphinx-build.log docs var/html-docs
	@echo
	@echo "Build finished."


# alias for sphinx-docs
alias docs := sphinx-docs