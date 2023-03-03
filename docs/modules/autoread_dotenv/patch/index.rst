:py:mod:`autoread_dotenv.patch`
===============================

.. py:module:: autoread_dotenv.patch

.. autoapi-nested-parse::

   autoread_dotenv.patch

   IMPORTANT: a sitecustomize-module is loaded automatically for every python-process
   started in the virtualenv where this module is installed.

   For more information, please see:
     - https://pymotw.com/2/site/
     - https://nedbatchelder.com/blog/201001/running_code_at_python_startup.html

   - return-statements are not allowed in the special module.

   - pytest-coverage does not like if-statements in this special module:
     It reports the if-condition as "didn't jump to the function exit".
     As a work-around we use an assignment with a ternary operator.

     if condition:
       do

     becomes:

     _ = do if condition else False

   - Assumed directory-structure:
     The virtualenv of your project **must** be created as a
     .venv-subfolder inside your project-directory.
     This corresponds to poetry-config "in-project = true".
     The .env-file must reside in the root of your project-directory.

     <project-root>
         .env
         .venv/
             bin/
                 python
             lib/
             pyvenv.cfg

     We also support toplevel-symlinks to the corresponding .venv-files
         bin/       -> .venv/bin/
         lib/       -> .venv/lib/
         pyvenv.cfg -> .venv/pyvenv.cfg



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   autoread_dotenv.patch.get_dotenv_path
   autoread_dotenv.patch.autoread_dotenv



Attributes
~~~~~~~~~~

.. autoapisummary::

   autoread_dotenv.patch.dotenv_available


.. py:data:: dotenv_available
   :value: 1

   

.. py:function:: get_dotenv_path()


.. py:function:: autoread_dotenv()


