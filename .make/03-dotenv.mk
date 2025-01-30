# See ../makefile

# Source .env.template, because .env might not yet exist.
-include .env.template

# Source .env, if it exists. This Overrides any env-vars sourced in .env.template.
-include .env


.PHONY: dotenv-install-from-example ## instantiate the dotenv-file (no override)
# cp --backup  creates .env~, but will overwrite this next time.
# safest way, is to not overwrite existing .env-files, manual intervention needed.
dotenv-install-from-example:
	@echo -e "Copying .env.template to .env" ;\
	cp -n .env.template .env ;\
	echo "Please review any credentials in the .env-file."


.PHONY: dotenv-set-basedir ## replace placeholder __CDW__ with current working directory
dotenv-set-basedir:
	@echo -e "Replacing string __CWD__ -> $(PWD)" ;\
	$(SED) -i 's@__CWD__@'"$(PWD)"'@'  .env


.PHONY: dotenv-install ## install .env-file from .env.template
dotenv-install: dotenv-install-from-example dotenv-set-basedir