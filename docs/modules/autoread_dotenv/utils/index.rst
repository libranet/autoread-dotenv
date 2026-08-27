autoread_dotenv.utils
=====================

.. py:module:: autoread_dotenv.utils

.. autoapi-nested-parse::

   autoread_dotenv.utils.

   We assume following directory-structure:
   The virtualenv of your project **must** be created as a
   .venv-subfolder inside your project-directory.

   This matches the standard uv in-project virtualenv layout, where the project root
   contains a .venv directory and the .env-file lives at the project root.
   This also corresponds to the standard layout expected by tools like Poetry when using in-project virtualenvs.

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

   For layouts that don't follow this convention (global installs, containers, editable
   mounts, ...), set the ``AUTOREAD_DOTENV_PATH`` environment-variable to the .env-file to
   use instead - it bypasses sys.prefix-based discovery entirely. See
   :func:`autoread_dotenv.utils.get_expected_dotenv_path`.



Attributes
----------

.. autoapisummary::

   autoread_dotenv.utils.AUTOREAD_DOTENV_PATH_VAR


Functions
---------

.. autoapisummary::

   autoread_dotenv.utils.get_expected_dotenv_path
   autoread_dotenv.utils.get_dotenv_path
   autoread_dotenv.utils.str_to_bool


Module Contents
---------------

.. py:data:: AUTOREAD_DOTENV_PATH_VAR
   :type:  str
   :value: 'AUTOREAD_DOTENV_PATH'


.. py:function:: get_expected_dotenv_path()

   Return the expected location of the .env-file.

   Honors the ``AUTOREAD_DOTENV_PATH`` environment-variable when set: it is used verbatim
   as the path to the .env-file, for setups that don't follow the in-project-virtualenv
   convention (global installs, containers, editable mounts, ...).

   Otherwise falls back to the in-project-virtualenv convention:
   sys.prefix is <project-root>/.venv or
   <project-root> when using toplevel symlinks to .venv


.. py:function:: get_dotenv_path()

   Return the location of the .env for in-project virtualenvs.

   Return None if the .env-file does not exist.


.. py:function:: str_to_bool(value)

   Convert a string value to a boolean.


