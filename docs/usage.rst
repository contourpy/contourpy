Usage
=====

The standard approach to use ContourPy is to:

#. Call :func:`~.contour_generator` passing your 2D ``z`` array and optional ``x`` and ``y``
   arrays as arguments to return a :class:`~.ContourGenerator` object, such as the default
   :class:`.SerialContourGenerator`.

#. Call :class:`~.ContourGenerator` member functions
   :meth:`~.ContourGenerator.lines` and/or :meth:`~.ContourGenerator.filled`
   repeatedly to calculate and return contours for that (x, y, z) grid:

   - :meth:`~.ContourGenerator.lines` calculates contour lines at a particular z-level.
   - :meth:`~.ContourGenerator.filled` calculates filled contours (polygons) between two
     z-levels.

There are many arguments for :func:`~.contour_generator` but only ``z`` is compulsory and
there are sensible defaults for the others.

.. note::

   Although it is possible to create objects of classes derived from
   :class:`~.ContourGenerator` directly from the `pybind11`_-wrapped C++ code in
   ``wrap.cpp``, this is discouraged as :func:`~.contour_generator` provides better
   argument checking and also support for numpy masked ``z`` arrays.

There are some utility functions in the :mod:`contourpy.util` module for testing and examples,
including producing graphical output using `Matplotlib`_ and `Bokeh`_.
