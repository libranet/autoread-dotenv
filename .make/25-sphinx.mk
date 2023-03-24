# See ../makefile

.PHONY: sphinx-docs  ## generate sphinx-docs in var/html-docs
sphinx-docs: poetry-export-requirements-docs
	sphinx-build -b html -d var/cache/sphinx-doctrees -w var/log/sphinx-build.log docs var/html-docs
	@echo
	@echo "Build finished."


.PHONY : docs  ## alias for sphinx-docs
docs : sphinx-docs