
Overview
--------


Dependencies
 - python-dotenv_
 - sitecustomize-entrypoints_

.. _python-dotenv: http://pypi.python.org/pypi/python-dotenv
.. _sitecustomize-entrypoints:  http://pypi.python.org/pypi/sitecustomize-entrypoints

Installation
------------

Install via pip:

.. code-block:: python

        > pip install autread_dotenv

Or add to your poetry-based project:

.. code-block:: python

        > poetry add autoread_dotenv


Registered sitecustomize-entrypoint
------------------------------------

The ``autoread_dotenv``-function is registered 
as a ``sitecustomize``-entrypoint in pyproject.toml_:

.. code-block:: python

    [tool.poetry.plugins]
    [tool.poetry.plugins."sitecustomize"]
    autoread_dotenv = "autoread_dotenv.autoread:autoread_dotenv"

This entrypoint will be executed in every python-process.

.. _pyproject.toml: https://python-poetry.org/docs/pyproject/#plugins

Usage
-----
The only thing left to do for you is the create a ``.env`` 
in the root of your project.
