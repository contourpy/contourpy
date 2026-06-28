# Usage

The standard approach to use ContourPy is to:

1. Call {py:func}`~.contour_generator` passing your 2D `z` array and optional `x` and `y`
   arrays as arguments to return a {py:class}`~.ContourGenerator` object, such as the default
   {py:class}`.SerialContourGenerator`. There are many arguments for {py:func}`~.contour_generator`
   but only `z` is compulsory and there are sensible defaults for the others.

2. To calculate contour lines at a particular z-level call {py:class}`~.ContourGenerator` member
   function {py:meth}`~.ContourGenerator.lines`. To calculate contour lines at multiple levels either
   repeatedly call {py:meth}`~.ContourGenerator.lines` or use
   {py:meth}`~.ContourGenerator.multi_lines` instead.

3. To calculate filled contours (polygons) between two z-levels call {py:class}`~.ContourGenerator`
   member function {py:meth}`~.ContourGenerator.filled`. To calculate filled contours between
   multiple pairs of z-levels either repeatedly call  {py:meth}`~.ContourGenerator.filled` or use
   {py:meth}`~.ContourGenerator.multi_filled` instead.

```{note}
   Although it is possible to create objects of classes derived from
   {py:class}`~.ContourGenerator` directly from the {{ pybind11 }}-wrapped C++ code in
   `wrap.cpp`, this is discouraged as {py:func}`~.contour_generator` provides better
   argument checking and also support for numpy masked `z` arrays.
```

There are some utility functions in the {py:mod}`contourpy.util` module for testing and examples,
including producing graphical output using {{ Matplotlib }} and {{ Bokeh }}.
