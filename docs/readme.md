[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/libranet/autoread-dotenv/blob/main/docs/license.md) [![Read the Docs](https://readthedocs.org/projects/autoread-dotenv/badge/?version=latest)](https://autoread-dotenv.readthedocs.io/en/latest/) [![PyPi Package](https://img.shields.io/pypi/v/autoread-dotenv?color=%2334D058&label=pypi%20package)](https://pypi.org/project/autoread-dotenv/)


## Installation

Install via pip:

```bash
> bin/pip install autoread_dotenv
```

Or add to your poetry-based project:

```bash
> poetry add autoread_dotenv
```


## Usage

The only thing left to do for you is the create a ``.env`` in the root of your project.


## Registered sitecustomize-entrypoint

The ``autoread_dotenv``-function is registered as a ``sitecustomize``-entrypoint in our pyproject.toml_:

``` toml
    [tool.poetry.plugins]
    [tool.poetry.plugins."sitecustomize"]
    autoread_dotenv = "autoread_dotenv.autoread:autoread_dotenv"
```

Sitecustomize and all its registered entrypoints will be executed at the start of *every* python-process.
For more information, please see [sitecustomize-entrypoints](http://pypi.python.org/pypi/sitecustomize-entrypoints)


## Compatibility

 [![Python Version](https://img.shields.io/pypi/pyversions/autoread-dotenv?:alt:PyPI-PythonVersion)](https://pypi.org/project/autoread-dotenv/)
 [![PyPI - Implementation](https://img.shields.io/pypi/implementation/autoread-dotenv?:alt:PyPI-Implementation)](https://pypi.org/project/autoread-dotenv/)

``autoread-dotenv``  works on Python 3.8+, including PyPy3. Tested until Python 3.11,


## Notable dependencies

- [sitecustomize-entrypoints](http://pypi.python.org/pypi/sitecustomize-entrypoints)
- [python-dotenv](http://pypi.python.org/pypi/python-dotenv)