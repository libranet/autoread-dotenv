autoread_dotenv.utils
=====================

.. py:module:: autoread_dotenv.utils

.. autoapi-nested-parse::

   autoread_dotenv.utils.

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



Functions
---------

.. autoapisummary::

   autoread_dotenv.utils.get_expected_dotenv_path
   autoread_dotenv.utils.get_dotenv_path
   autoread_dotenv.utils.str_to_bool


Module Contents
---------------

.. py:function:: get_expected_dotenv_path()

   Return the expected location of the .env for in-project virtualenvs.


.. py:function:: get_dotenv_path()

   Return the location of the .env for in-project virtualenvs.

   Return None if the .env-file does not exist.


.. py:function:: str_to_bool(value)

   Convert a string value to a boolean.


