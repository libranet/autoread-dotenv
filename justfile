# Just is a crossplatform task-runner, similar to make.
# And justfiles are equivalent to makefiles.
#
# Official docs:
#  - https://just.systems/man/en
#  - installation: https://just.systems/man/en/pre-built-binaries.html
#
# Usage:
#   > just  # configured to display all available tasks
#   > just --help
#   > just <taskname>
#
# Notes:
#  - Comments immediately preceding a recipe will appear in just --list

# load environment variables from .env file
set dotenv-filename := ".env"
set dotenv-load	:= true

# search for justfiles in parent directories
set fallback

# set tempdir := "var/tmp"

# enable experimental features
set unstable

# set shell to powershell on Windows
set windows-shell := ["pwsh.exe", "-NoLogo", "-Command"]
set shell := ["bash", "-uc"]


# waiting for glob-support, see
# - https://github.com/casey/just/issues/1885
# - https://github.com/casey/just/pull/2376
import '.just/bandit.justfile'
import '.just/dir-structure.justfile'
import '.just/dotenv.justfile'
import '.just/ipython.justfile'
import '.just/just.justfile'
import '.just/mypy.justfile'
import '.just/pre-commit.justfile'
import '.just/project.justfile'
import '.just/pylint.justfile'
import '.just/pyroma.justfile'
import '.just/pytest.justfile'
import '.just/readthedocs.justfile'
import '.just/ruff.justfile'
import '.just/safety.justfile'
import '.just/sshx.justfile'
import '.just/ty.justfile'
import '.just/ubuntu.justfile'
import '.just/uv.justfile'


# Display all canonical tasks (default recipe)
list:
    @ just --list --unsorted --no-aliases
