Usage
=====

The standard approach to use ``contourpy`` is to:

#. Call :func:`~contourpy.contour_generator` passing your 2D ``z`` array and optional ``x`` and ``y``
   arrays as arguments to return a ``ContourGenerator`` object, such as the default
   :class:`~contourpy.SerialContourGenerator`.

#. Call ``ContourGenerator`` member functions :meth:`~contourpy.SerialContourGenerator.lines` and/or
   :meth:`~contourpy.SerialContourGenerator.filled` repeatedly to calculate and return contours for
   that (x, y, z) grid:

    a. :meth:`~contourpy.SerialContourGenerator.lines` calculates contour lines at a particular
       z-level.

    b. :meth:`~contourpy.SerialContourGenerator.filled` calculates filled contours (polygons)
       between two z-levels.

There are many arguments for :func:`~contourpy.contour_generator` but only ``z`` is compulsory and
there are sensible defaults for the others.

.. note::

   Although it is possible to create ``ContourGenerator`` objects directly from the
   `pybind11`_-wrapped C++ code in ``wrap.cpp``, this is discouraged as
   :func:`~contourpy.contour_generator` provides better argument checking and also support for
   numpy masked ``z`` arrays.

There are some utility functions in the :mod:`contourpy.util` module for testing and examples,
including producing graphical output using `Matplotlib`_ and `Bokeh`_.
