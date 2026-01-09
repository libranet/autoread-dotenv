# See ../justfile


# show which pyroma is used
[group: 'pyroma']
pyroma-which:
    @ which pyroma


# run pyroma
[group: 'pyroma']
pyroma *args: pyroma-which
    - pyroma . {{args}}
