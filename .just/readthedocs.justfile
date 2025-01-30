# readthedocs, see ../justfile

# readthedocs already provisions a virtualenv for us.
# So we only need to install our packages into that virtualenv.

# installation for readthedocs
[group: 'readthedocs']
install-rtd:
    - python -m pip install --upgrade pip
    - python -m pip install poetry
    - poetry config virtualenvs.create false --local
    - poetry install --only docs
