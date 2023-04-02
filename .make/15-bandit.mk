# See ../makefile

.PHONY: randit-which  ## show which bandit is used
bandit-which:
	@ which bandit


.PHONY: bandit  ## run bandit
bandit:
# bandit --configfile pyproject.toml --recursive src --baseline etc/bandit-baseline.json
	bandit --configfile pyproject.toml --recursive .


.PHONY: bandit-html ## run bandit with htm-report
bandit-html:
	@ mkdir -p var/html/bandit
	@ echo -e "Bandit-report generated in var/html/bandit/bandit.html"
	bandit --config pyproject.toml --recursive . --format html > var/html/bandit/bandit.html


.PHONY: bandit-update-baseline  ## update bandit baseline
bandit-update-baseline:
	bandit --configfile pyproject.toml --recursive .  --format json --output etc/bandit-baseline.json