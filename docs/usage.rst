Usage
=====

The standard approach to use ContourPy is to:

#. Call :func:`~.contour_generator` passing your 2D ``z`` array and optional ``x`` and ``y``
   arrays as arguments to return a :class:`~.ContourGenerator` object, such as the default
   :class:`.SerialContourGenerator`. There are many arguments for :func:`~.contour_generator` but
   only ``z`` is compulsory and there are sensible defaults for the others.

#. To calculate contour lines at a particular z-level call :class:`~.ContourGenerator` member
   function :meth:`~.ContourGenerator.lines`. To calculate contour lines at multiple levels either
   repeatedly call :meth:`~.ContourGenerator.lines` or use
   :meth:`~.ContourGenerator.multi_lines` instead.

#. To calculate filled contours (polygons) between two z-levels call :class:`~.ContourGenerator`
   member function :meth:`~.ContourGenerator.filled`. To calculate filled contours between multiple
   pairs of z-levels either repeatedly call  :meth:`~.ContourGenerator.filled` or use
   :meth:`~.ContourGenerator.multi_filled` instead.

.. note::

   Although it is possible to create objects of classes derived from
   :class:`~.ContourGenerator` directly from the `pybind11`_-wrapped C++ code in
   ``wrap.cpp``, this is discouraged as :func:`~.contour_generator` provides better
   argument checking and also support for numpy masked ``z`` arrays.

There are some utility functions in the :mod:`contourpy.util` module for testing and examples,
including producing graphical output using `Matplotlib`_ and `Bokeh`_.
