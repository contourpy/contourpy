Installation
============

Installing from prepackaged binaries
------------------------------------

Official releases
^^^^^^^^^^^^^^^^^

Official releases of ContourPy are available from `PyPI`_ and `conda-forge`_ for Linux, macOS and
Windows.

#. To install from `PyPI`_:

   .. code-block:: bash

      $ pip install contourpy

#. To install from `conda-forge`_:

   .. code-block:: bash

      $ conda install -c conda-forge contourpy

The only compulsory runtime dependency is `NumPy`_.

If you want to make use of one of ContourPy's utility renderers in the :mod:`contourpy.util` module
you will also have to install either `Matplotlib`_ or `Bokeh`_.

Pre-releases
^^^^^^^^^^^^

Prepackaged wheels of the latest pre-release ContourPy code, at most a week old, are available as
part of the `Scientific Python`_ nightly wheels service. These are intended to be used for testing
and are not necessarily stable. See `SPEC 4`_ for more details.


Installing from source
----------------------

If you wish to install from source code, see the :ref:`developer_guide`.
