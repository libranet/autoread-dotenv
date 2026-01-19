# project


# run all install-steps to full initial installation
[group: 'project']
install: create-dirs dotenv-install uv-sync-all-groups && symlink-venv-dirs


# setup up development environment with precommit-hooks
[group: 'project']
install-dev: install pre-commit-install-hook

alias dev-install := install-dev