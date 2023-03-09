# See ../makefile

# define an alias for an existing target
.PHONY : docs  ## alias for sphinx-docs
docs : sphinx-docs


.PHONY: sphinx-docs  ## generate sphinx-docs in var/html-docs
sphinx-docs: poetry-export-requirements-docs
	.venv/bin/sphinx-build -b html -d var/cache/sphinx-doctrees -w var/log/sphinx-build.log docs var/html-docs
	@echo
	@echo "Build finished."