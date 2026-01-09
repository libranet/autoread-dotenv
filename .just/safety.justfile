# safety, see ../justfile


# show which safety is used
[group: 'safety']
safety-which:
    @ echo -e "Using uv run safety"


# run safety check
[group: 'safety']
safety-check *args:
    uv run safety check {{args}}


# run safety check with html-report
[group: 'safety']
safety-check-html:
    @ mkdir -p var/html/safety
    uv run safety check --save-html var/html/safety/safety.html
