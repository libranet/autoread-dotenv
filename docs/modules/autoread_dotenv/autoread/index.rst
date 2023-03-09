:py:mod:`autoread_dotenv.autoread`
==================================

.. py:module:: autoread_dotenv.autoread

.. autoapi-nested-parse::

   autoread_dotenv.autoread

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
             pyvenv.cfg

     We also support toplevel-symlinks to the corresponding .venv-files:

   .. code-block:: python

         bin/       -> .venv/bin/
         lib/       -> .venv/lib/
         pyvenv.cfg -> .venv/pyvenv.cfg



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   autoread_dotenv.autoread.get_dotenv_path
   autoread_dotenv.autoread.autoread_dotenv



Attributes
~~~~~~~~~~

.. autoapisummary::

   autoread_dotenv.autoread.dotenv_available


.. py:data:: dotenv_available
   :value: 1

   

.. py:function:: get_dotenv_path()

   Return the location of the .env for in-project virtualenvs.
   Return None of no .env-file is found.


.. py:function:: autoread_dotenv()

   Set environment-variable from the in-project .env-file.


