autoread_dotenv.about
=====================

.. py:module:: autoread_dotenv.about

.. autoapi-nested-parse::

   autoread_dotenv.about.

   Fetch metadata from the package's pyproject.toml.
   The package must be properly installed in order the metadata to be available.



Attributes
----------

.. autoapisummary::

   autoread_dotenv.about.PACKAGE
   autoread_dotenv.about.pkginfo
   autoread_dotenv.about.version
   autoread_dotenv.about.license_
   autoread_dotenv.about.authors


Classes
-------

.. autoapisummary::

   autoread_dotenv.about.PkgInfo


Functions
---------

.. autoapisummary::

   autoread_dotenv.about.get_metadata_package


Module Contents
---------------

.. py:data:: PACKAGE
   :type:  str
   :value: ''


.. py:class:: PkgInfo

   Bases: :py:obj:`TypedDict`


   Typed subset of a distribution's metadata.


   .. py:attribute:: author_email
      :type:  str


   .. py:attribute:: license
      :type:  str


   .. py:attribute:: version
      :type:  str


.. py:function:: get_metadata_package(pkgname = '')

   Fetch a typed subset of ``pkgname``'s distribution metadata.

   Defaults to this package (``PACKAGE``) when ``pkgname`` is not given.
   Falls back to "unknown" values when the metadata cannot be found, so that this module -
   which runs on every Python process start via the ``sitecustomize`` entrypoint - never raises
   at import time.


.. py:data:: pkginfo
   :type:  PkgInfo

.. py:data:: version
   :type:  str

.. py:data:: license_
   :type:  str

.. py:data:: authors
   :type:  str

