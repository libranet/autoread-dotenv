# This is a comment.
# Important: You *must* indent using <TAB>s, not spaces.
#
# For more information, please see
#   - https://www.gnu.org/software/make/manual/make.html
#
# General syntax:
#   targets : prerequisites; recipes
#   <TAB>recipe
#
# - Commands starting with
#     "-" are ignoring their exit-code.
#     "@" do not echo the command itself.
#
# - make starts a new shell process for each recipe line.
#   Thus shell variables, even exported environment variables, cannot propagate upwards.
#   Therefore better concatenate your multiline-commands with ";\" into a single line.

PROJECT_NAME='autoread-dotenv'

# include re-usable makefiles
-include .make/*.mk


.PHONY: install  ## full initial installation
install: create-dirs symlink-venv-dirs dotenv-install pip-upgrade poetry-install


.PHONY: install-rtd  ## installation for readthedocs
install-rtd:
	- python -m pip install --upgrade pip
	- python -m pip install poetry
	- poetry config virtualenvs.create false --local
	- poetry install --with docs --without dev --without ipython --without profiling --without testing --without typing
