# MkDocs + Material -- see ../mkdocs.yaml


# show which mkdocs is used
[group: 'mkdocs']
mkdocs-which:
    @ which mkdocs


# build the static site into var/html-docs (strict: fail on broken refs/links)
[group: 'mkdocs']
mkdocs-docs:
    mkdocs build --strict
    @echo
    @echo "Build finished -> var/html-docs (see site_dir in ../mkdocs.yaml)"


# Extra args pass through, e.g.
#   just mkdocs-serve -a 0.0.0.0:8000   # bind all interfaces (then browse localhost, NOT 0.0.0.0)
#   just mkdocs-serve --no-strict
# live-reloading preview on http://127.0.0.1:8000/ (or http://localhost:8000/ from a WSL2 browser)
[group: 'mkdocs']
mkdocs-serve *args:
    mkdocs serve {{ args }}


# alias for mkdocs-docs
alias docs := mkdocs-docs
