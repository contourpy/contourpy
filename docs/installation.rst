Installation
============

Installing from prepackaged binaries
------------------------------------

Stable releases of ``contourpy`` are available from `PyPI`_, `conda-forge`_, and Anaconda
`default`_ channels for Linux, macOS and Windows.

#. To install from `PyPI`_:

   .. code-block:: bash

      $ pip install contourpy

#. To install from `conda-forge`_:

   .. code-block:: bash

      $ conda install -c conda-forge contourpy

#. To install from Anaconda `default`_ channel:

   .. code-block:: bash

      $ conda install contourpy

The only compulsory runtime dependency is `NumPy`_.

If you want to make use of one of contourpy's utility renderers in the :mod:`contourpy.util` module
you will also have to install either `Matplotlib`_ or `Bokeh`_.

Installing from source
----------------------

The source code for ``contourpy`` is available from `github`_.
Either ``git clone`` it directly, or fork and ``git clone`` it from your fork, as usual.

.. note::

   You should install ``contourpy`` from source into a new virtual environment using ``conda`` or
   ``venv`` for example.
   To use ``venv`` to create a new virtual environment in a directory called ``.venv/contourpy``
   and activate it:

   .. code-block:: console

      $ python -m venv ~/.venv/contourpy
      $ . ~/.venv/contourpy/bin/activate

From the base directory of your local ``contourpy`` git repo, build and install it in editable mode
using:

.. code-block:: console

   $ pip install -ve .


To build in debug mode, which enables ``assert`` statements in the C++ code, use the
``CONTOURPY_DEBUG`` environment variable:

.. code-block:: console

   $ CONTOURPY_DEBUG=1 pip install -ve .


Running tests
-------------

To run the test suite, first ensure that the required dependencies are installed and then run the
tests using ``pytest``:

.. code-block:: console

   $ pip install -ve .[test]
   $ pytest

It is possible to exclude certain tests.

#. To exclude image comparison tests (if you do not have ``matplotlib`` installed):

   .. code-block:: console

      $ pytest -k "not image"

#. To exclude threaded tests (because the ``threaded`` algorithm is not yet fully robust):

   .. code-block:: console

      $ pytest -k "not threads"


Building the documentation
--------------------------

To build the documentation:

.. code-block:: console

   $ pip install -ve .[docs]
   $ cd docs
   $ make html

.. warning::

   If you modify some of the C++ source code and wish to ensure a completely clean build, you can
   first use:

   .. code-block:: console

      $ git clean -fxd

   although use this with care as it will also delete any new files that you have created that have
   not been added to ``git`` and are not mentioned in the ``.gitignore`` file.
