# See ../makefile

GIT_CLONE_URL := $(shell git remote get-url --push origin)
CLONE_DIR := 'var/tmp/cloned'

.PHONY: git-init  ## initialize  new git-repo
git-init:
	git init


.PHONY: git-remote-show-origin  ## git-remote-show-origin
git-remote-show-origin:
	git remote show origin


.PHONY: git-fetch-tags  ## git fetch --tags
git-fetch-tags:
	git fetch --tags


.PHONY: git-show-remote-tags  ## git ls-remote --tags
git-show-remote-tags:
	git ls-remote --tags


.PHONY: git-show-local-tags  ## git tag -l
git-show-local-tags: git-fetch-tags
	echo -e "Local tags"
	git tag -l


.PHONY: git-show-tags  ## show local & remote tags
git-show-tags:
	@echo -e "Local tags"
	git tag -l
	@echo -e "Remote tags"
	git ls-remote --tags

.PHONY: git-show-url  ## show clone-url
git-show-url:
	@ git remote get-url --push origin


.PHONY: git-tmp-clone  ## clone repo to tmp-dir
git-tmp-clone:
	LATEST_TAG=$$(git describe --tags --abbrev=0)
	cd ${CLONE_DIR}-${LATEST_TAG}
	@ git clone ${GIT_CLONE_URL} ${CLONE_DIR}


.PHONY: git-latest-tag  ## show latest tag
git-latest-tag:
	$(eval LATEST_TAG := $(git describe --tags --abbrev=0)) \
	@ echo -e "Latest tag: ${LATEST_TAG}"
	export LATEST_TAG


.PHONY: publish-to-pypi  ## publish-to-pypi
publish-to-pypi: git-tmp-clone
	set -e ; \
	$(eval LATEST_TAG := $(git describe --tags --abbrev=0)) \
	mkdir -p ${CLONE_DIR}-${LATEST_TAG}
	cd ${CLONE_DIR}-${LATEST_TAG} && \
	git fetch --tags && \
	&& \
	git checkout ${LATEST_TAG}
	poetry build && \
	poetry publish