# See ../makefile

.PHONY: git-init  ## initialize  new git-repo
git-init:
	git init


.PHONY: git-remote-show-origin  ## git-remote-show-origin
git-remote-show-origin:
	git remote show origin
