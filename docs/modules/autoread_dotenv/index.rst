autoread_dotenv
===============

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



Submodules
----------

.. toctree::
   :maxdepth: 1

   /modules/autoread_dotenv/about/index
   /modules/autoread_dotenv/utils/index
   /modules/autoread_dotenv/warnings/index


Attributes
----------

.. autoapisummary::

   autoread_dotenv.__author__
   autoread_dotenv.__license__
   autoread_dotenv.__version__


Functions
---------

.. autoapisummary::

   autoread_dotenv.get_dotenv_path
   autoread_dotenv.str_to_bool
   autoread_dotenv.simple_warning
   autoread_dotenv.entrypoint


Package Contents
----------------

.. py:data:: __author__
   :type:  str | list[str]

.. py:data:: __license__
   :type:  str | list[str]

.. py:data:: __version__
   :type:  str

.. py:function:: get_dotenv_path()

   Return the location of the .env for in-project virtualenvs.

   Return None if the .env-file does not exist.


.. py:function:: str_to_bool(value)

   Convert a string value to a boolean.


.. py:function:: simple_warning()

   Context manager for simplified warning formatting without tracebacks.


.. py:function:: entrypoint()

   Set environment-variable from the in-project .env-file.


