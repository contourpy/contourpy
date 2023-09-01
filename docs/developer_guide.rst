.. _developer_guide:

Developer guide
===============

C++ compiler
------------

To build ContourPy you will need a C++ compiler. This is usually `GCC`_ on Linux, `Clang`_ on
macOS, or `MSVC`_ on Windows. You will also need `ninja`_, binary wheels are available for many
platforms that can be installed using ``pip``.

Installing from source
----------------------

The source code for ContourPy is available from `github`_.
Either ``git clone`` it directly, or fork and ``git clone`` it from your fork, as usual.
It is recommended to install ContourPy from source into a new virtual environment using
`conda`_, `pyenv`_ or `virtualenv`_ for example, rather than using your system Python.

.. note::

   To use all of the installation features described below you will need a recent version of
   ``pip >= 23.1``. You can upgrade your installed ``pip`` using:

   .. code-block:: console

      $ python -m pip install --upgrade pip

From the base directory of your local ``contourpy`` git repository, build and install it using:

.. code-block:: console

   $ python -m pip install -v .

This is the simplest approach and uses a temporarily isolated environment to build ContourPy
and then installs the built package into the current environment. If you make any changes to the
source code (Python or C++) you will need to rerun this command to rebuild and reinstall.

.. warning::

   Compiling from source using ``pip install`` within a conda environment can cause problems if
   your system compiler is significantly different from the one used to compile your ``conda``
   packages. A typical problem on Linux is incompatible versions of ``GLIBCXX``. If problems occur
   using system compilers, install ``conda`` compilers using

   .. code-block:: console

      $ conda install -c conda-forge gcc_linux-64

   or similar.

Installing using editable mode
------------------------------

To develop ContourPy source code, the recommended approach is to install in editable mode without
using build isolation. Using this approach avoids the need to manually rebuild after making changes
to the source code (Python or C++) as ContourPy is rebuilt automatically whenever it is imported.

Firstly install the build requirements into your working environment:

.. code-block:: console

   $ python -m pip install -r build_requirements.txt

then build ``contourpy`` in editable mode without build isolation:

.. code-block:: console

   $ python -m pip install -ve . --no-build-isolation

Now whenever you ``import contourpy`` it will automatically rebuild if any source code files have
changed. No specific indication is given when this occurs, but the ``import`` will take longer.
If you wish to have visible confirmation of the rebuild then either set the environment variable
``MESONPY_EDITABLE_VERBOSE=1`` or pass an extra configuration flag to your ``pip install`` command
as follows:

.. code-block:: console

   $ python -m pip install -ve . --no-build-isolation -C editable-verbose=true


Install configuration options
-----------------------------

Configuration options can be passed to ``pip install`` to control aspects of the build process.
Some of the most commonly used are described below.
Others are documented on the websites of the build tools `meson`_ and `meson-python`_.

Debug build
^^^^^^^^^^^

The default build type for ContourPy is ``release`` which means it is built with performance
optimisations and without debug symbols. This ensures that the code runs quickly and the binaries
are small, which is what most end-users want.

For development purposes it can help to build in ``debug`` mode. This adds debug symbols, enables
C++ ``assert`` statements, and disables performance optimisations. To produce a ``debug`` build
use:

.. code-block:: console

   $ python -m pip install -v .  -C setup-args=-Dbuildtype=debug -C builddir=build

or the editable mode equivalent.

C++ standard
^^^^^^^^^^^^

Although ContourPy is C++11 compliant the default C++ standard used to build is C++17.
To change the C++ standard to, for example C++14, append ``-C setup-args=-Dcpp_std=c++14`` to the
``pip install`` command. For example:

.. code-block:: console

   $ python -m pip install -v . -C setup-args=-Dcpp_std=c++14


Running tests
-------------

To run the test suite, first ensure that the required dependencies are installed when building
ContourPy and then run the tests using ``pytest``:

.. code-block:: console

   $ python -m pip install -ve .[test]
   $ pytest -v

It is possible to exclude certain tests. To exclude image comparison tests, for example if you do
not have Matplotlib or Pillow installed:

.. code-block:: console

   $ pytest -k "not image"

To exclude threaded tests:

.. code-block:: console

   $ pytest -k "not threads"

Other tests are excluded by default but can be manually enabled. To include tests that generate text
output:

.. code-block:: console

  $ pytest --runtext

.. warning::

   The ContourPy baseline images used for Matplotlib tests assume that the installed Matplotlib was
   built with the version of FreeType that it vendors. If you have built Matplotlib yourself using a
   different version of FreeType, as is usually the case for Linux distro packagers, you should not
   run text tests as the generated images will be different even if everything is working as
   expected.

To include tests that take a long time to run:

.. code-block:: console

  $ pytest --runslow

.. note::

   :class:`~contourpy.util.bokeh_renderer.BokehRenderer` tests will be run if Bokeh is installed,
   otherwise they will be skipped. The generated images for Bokeh tests are sensitive to the version
   of the browser and the Operating System used to generate them, so unless you have experience in
   this area you are advised to leave the generation and testing of Bokeh images to the ContourPy
   Continuous Integration tests.


Building the documentation
--------------------------

To build the documentation:

.. code-block:: console

   $ python -m pip install -v .[docs]
   $ cd docs
   $ make html

and the top-level generated HTML file is ``docs/_build/html/index.html`` relate to the root of your
github repository.


Pre-commit hooks
----------------

Contributors are recommended to install `pre-commit`_ hooks which will automatically run various
checks whenever ``git commit`` is run. First install ``pre-commit`` using either

.. code-block:: bash

   $ pip install pre-commit

or

.. code-block:: bash

   $ conda install -c conda-forge pre-commit

and then install the hooks using

.. code-block:: bash

   $ pre-commit install

The hooks will then be run on each ``git commit``. You can manually run the hooks outside of a
```git commit`` using

.. code-block:: bash

   $ pre-commit run --all-files
