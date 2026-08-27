# autoread-dotenv

[![Testing](https://img.shields.io/github/actions/workflow/status/libranet/autoread-dotenv/testing.yaml?branch=main&longCache=true&style=flat-square&label=tests&logo=GitHub%20Actions&logoColor=fff%22)](https://github.com/libranet/autoread-dotenv/actions/workflows/testing.yaml)
[![Linting](https://img.shields.io/github/actions/workflow/status/libranet/autoread-dotenv/linting.yaml?branch=main&longCache=true&style=flat-square&label=linting&logo=GitHub%20Actions&logoColor=fff%22)](https://github.com/libranet/autoread-dotenv/actions/workflows/linting.yaml)
[![Read the Docs](https://readthedocs.org/projects/autoread-dotenv/badge/?version=latest)](https://autoread-dotenv.readthedocs.io/en/latest/)
[![Codecov](https://codecov.io/gh/libranet/autoread-dotenv/branch/main/graph/badge.svg?token=QTOWRXGH61)](https://codecov.io/gh/libranet/autoread-dotenv)
[![PyPi Package](https://img.shields.io/pypi/v/autoread-dotenv?color=%2334D058&label=pypi%20package)](https://pypi.org/project/autoread-dotenv/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/libranet/autoread-dotenv/blob/main/docs/license.md)

autoread-dotenv parses your `.env` file when starting any venv-based Python process:

![Demo](img/demo-autoread-dotenv.png)

## Installation

Install with uv (preferred):

```bash
> uv add autoread-dotenv
```

If you are using Poetry:

```bash
> poetry add autoread-dotenv
```

Install via pip:

```bash
> bin/pip install autoread-dotenv
```

## Set up a local development environment

```bash
> just install
```

## Usage

The only thing left to do for you is the create a `.env` in the root of your project.

## Registered sitecustomize-entrypoint

The `autoread_dotenv.entrypoint`-function is registered as a `sitecustomize`-entrypoint in our pyproject.toml\_:

```toml

    [project.entry-points.sitecustomize]
    autoread_dotenv = "autoread_dotenv:entrypoint"
```

Sitecustomize and all its registered entrypoints will be executed at the start of *every* python-process.
For more information, please see [sitecustomize-entrypoints](http://pypi.python.org/pypi/sitecustomize-entrypoints)

## Avoid overriding existing environments variables

By default, your .env-file read by `autoread-dotenv` will override any pre-existing environment variables.
You can avoid this behaviour by setting `AUTOREAD_ENFORCE_DOTENV=0`.

## Overriding where the .env-file is looked up

By default, `autoread-dotenv` locates your `.env` relative to `sys.prefix`, assuming the
in-project-virtualenv layout described above. For setups that don't follow that convention
(global installs, containers, editable mounts, ...), set `AUTOREAD_DOTENV_PATH` to the full path
of the `.env`-file to use instead - it takes precedence and skips the `sys.prefix`-based lookup
entirely:

```bash
> export AUTOREAD_DOTENV_PATH=/etc/myapp/production.env
```

## Performance

`autoread-dotenv` runs on the start of every Python process in the venv, so its startup-time
cost is measured and tracked explicitly - see [docs/performance.md](performance.md) for the
current numbers and how to reproduce them.

## Compatibility

[![Python Version](https://img.shields.io/pypi/pyversions/autoread-dotenv?:alt:PyPI-PythonVersion)](https://pypi.org/project/autoread-dotenv/)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/autoread-dotenv?:alt:PyPI-Implementation)](https://pypi.org/project/autoread-dotenv/)

`autoread-dotenv` works on Python 3.9+, including PyPy3. Tested until Python 3.14.

## Notable dependencies

- [sitecustomize-entrypoints](http://pypi.python.org/pypi/sitecustomize-entrypoints)
- [python-dotenv](http://pypi.python.org/pypi/python-dotenv)
