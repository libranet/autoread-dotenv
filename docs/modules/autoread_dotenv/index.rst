:py:mod:`autoread_dotenv`
=========================

.. py:module:: autoread_dotenv

.. autoapi-nested-parse::

   autoread_dotenv.__init__.

   We assume following directory-structure:
   The virtualenv of your project **must** be created as a
   .venv-subfolder inside your project-directory.

   This corresponds to poetry-config "in-project = true".
   The .env-file must reside in the root of your project-directory.

   .. code-block:: python

     <project-root>
         .env
         .venv/
             bin/
                 python
             lib/
             lib64/
             pyvenv.cfg

     We also support toplevel-symlinks to the corresponding .venv-files:

   .. code-block:: python

         bin/       -> .venv/bin/
         lib/       -> .venv/lib/
         lib64/     -> .venv/lib64/
         pyvenv.cfg -> .venv/pyvenv.cfg



Package Contents
----------------

Classes
~~~~~~~

.. autoapisummary::

   autoread_dotenv.SimpleWarning



Functions
~~~~~~~~~

.. autoapisummary::

   autoread_dotenv.get_dotenv_path
   autoread_dotenv.entrypoint
   autoread_dotenv.cancel



Attributes
~~~~~~~~~~

.. autoapisummary::

   autoread_dotenv.__version__
   autoread_dotenv.__copyright__
   autoread_dotenv.__license__
   autoread_dotenv.DOTENV_INSTALLED


.. py:data:: __version__
   :value: '1.0.1'



.. py:data:: __copyright__
   :value: 'Copyright 2023 Libranet'



.. py:data:: __license__
   :value: 'MIT License'



.. py:data:: DOTENV_INSTALLED
   :value: 1



.. py:class:: SimpleWarning

   Simple warning-formatting .

   .. py:method:: simple_message(msg, *args, **kwargs)
      :classmethod:

      Simple warning-message without any traceback-info.


   .. py:method:: __enter__()


   .. py:method:: __exit__(*args)



.. py:function:: get_dotenv_path()

   Return the location of the .env for in-project virtualenvs.
   Return None of no .env-file is found.


.. py:function:: entrypoint()

   Set environment-variable from the in-project .env-file.


.. py:function:: cancel()

   No-op function that can be used the cancel a registered entrypoint.

   Imagine you have multiple sitecustomize-entrypoints. If these entrypoints
   are registered via third-party packages, you cannot control the order of execution.

   Now suppose some of these entrypoints need an environment-variable that first need to be set
   by ``autoread_dotenv`` needs to be executed before the others

   entrypoint 1:  foo.needs_envvar:bar
   entrypoint 2:  autoread_dotenv.autoread:autoread_dotenv

   in your project's pyproject.toml:

   [tool.poetry.plugins."sitecustomize"]

   # cancel the first registration using the original name
   autoread_dotenv = "autoread_dotenv.autoread:cancel"

   # re-register the same function under different name
   zz_autoread_dotenv = "autoread_dotenv.autoread:autoread_dotenv"



