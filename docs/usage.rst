Usage
=====

The standard approach to use ContourPy is to:

#. Call :func:`~contourpy.contour_generator` passing your 2D ``z`` array and optional ``x`` and ``y``
   arrays as arguments to return a :class:`~contourpy.ContourGenerator` object, such as the default
   :class:`~contourpy.SerialContourGenerator`.

#. Call :class:`~contourpy.ContourGenerator` member functions
   :meth:`~contourpy.ContourGenerator.lines` and/or :meth:`~contourpy.ContourGenerator.filled`
   repeatedly to calculate and return contours for that (x, y, z) grid:

   - :meth:`~contourpy.ContourGenerator.lines` calculates contour lines at a particular z-level.
   - :meth:`~contourpy.ContourGenerator.filled` calculates filled contours (polygons) between two
     z-levels.

There are many arguments for :func:`~contourpy.contour_generator` but only ``z`` is compulsory and
there are sensible defaults for the others.

.. note::

   Although it is possible to create objects of classes derived from
   :class:`~contourpy.ContourGenerator` directly from the `pybind11`_-wrapped C++ code in
   ``wrap.cpp``, this is discouraged as :func:`~contourpy.contour_generator` provides better
   argument checking and also support for numpy masked ``z`` arrays.

There are some utility functions in the :mod:`contourpy.util` module for testing and examples,
including producing graphical output using `Matplotlib`_ and `Bokeh`_.
