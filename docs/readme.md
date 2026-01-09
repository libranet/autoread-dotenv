[![Testing](https://img.shields.io/github/actions/workflow/status/libranet/autoread-dotenv/testing.yaml?branch=main&longCache=true&style=flat-square&label=tests&logo=GitHub%20Actions&logoColor=fff")](https://github.com/libranet/autoread-dotenv/actions/workflows/testing.yaml)
[![Linting](https://img.shields.io/github/actions/workflow/status/libranet/autoread-dotenv/linting.yaml?branch=main&longCache=true&style=flat-square&label=linting&logo=GitHub%20Actions&logoColor=fff")](https://github.com/libranet/autoread-dotenv/actions/workflows/linting.yaml)
[![Read the Docs](https://readthedocs.org/projects/autoread-dotenv/badge/?version=latest)](https://autoread-dotenv.readthedocs.io/en/latest/)
[![Codecov](https://codecov.io/gh/libranet/autoread-dotenv/branch/main/graph/badge.svg?token=QTOWRXGH61)](https://codecov.io/gh/libranet/autoread-dotenv)
[![PyPi Package](https://img.shields.io/pypi/v/autoread-dotenv?color=%2334D058&label=pypi%20package)](https://pypi.org/project/autoread-dotenv/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/libranet/autoread-dotenv/blob/main/docs/license.md)

## Installation

Install via uv:

```bash
> uv add autoread-dotenv
```

Or add to your poetry-based project:

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

The only thing left to do for you is the create a ``.env`` in the root of your project.

## Registered sitecustomize-entrypoint

The ``autoread_dotenv.entrypoint``-function is registered as a ``sitecustomize``-entrypoint in our pyproject.toml_:

``` toml

    [project.entry-points.sitecustomize]
    autoread_dotenv = "autoread_dotenv:entrypoint"
```

Sitecustomize and all its registered entrypoints will be executed at the start of *every* python-process.
For more information, please see [sitecustomize-entrypoints](http://pypi.python.org/pypi/sitecustomize-entrypoints)

## Avoid overriding existing environments variables

By default, your .env-file read by ``autoread-dotenv`` will override any pre-existing environment variables.
You can avoid this behaviour by setting ``AUTOREAD_ENFORCE_DOTENV=0``.

## Compatibility

 [![Python Version](https://img.shields.io/pypi/pyversions/autoread-dotenv?:alt:PyPI-PythonVersion)](https://pypi.org/project/autoread-dotenv/)
 [![PyPI - Implementation](https://img.shields.io/pypi/implementation/autoread-dotenv?:alt:PyPI-Implementation)](https://pypi.org/project/autoread-dotenv/)

``autoread-dotenv``  works on Python 3.8+, including PyPy3. Tested until Python 3.13,

## Notable dependencies

- [sitecustomize-entrypoints](http://pypi.python.org/pypi/sitecustomize-entrypoints)
- [python-dotenv](http://pypi.python.org/pypi/python-dotenv)
