Welcome to ContourPy's documentation!
=====================================

**ContourPy** is a Python library for calculating contours of 2D quadrilateral grids.
It is written in C++11 and wrapped using `pybind11`_.

It contains the 2005 and 2014 algorithms used in `Matplotlib`_ as well as a newer algorithm that
includes more features and is available in both serial and multithreaded versions.
It provides an easy way for Python libraries to use contouring algorithms without having to include
Matplotlib as a dependency.

Advantages of the new algorithm compared to Matplotlib's default algorithm of 2014 - 2022:

#. Improved performance in many situations (see :ref:`benchmarks`).
#. Multiple return types for both contour lines and filled contours, with different complexity and
   performance tradeoffs (see :ref:`line_type` and :ref:`fill_type`).
#. Multiple ways to specify chunk sizes and/or counts (see :ref:`chunks`).
#. Supports treating quads a four triangles for more detailed contours (see :ref:`quad_as_tri`).
#. Supports alternative forms of interpolation of z-values (currently only logarithmic) (see
   :ref:`z_interp`).
#. Multithreaded option (this should be considered experimental) (see :ref:`threads`).

.. toctree::
   :maxdepth: 1
   :caption: Basics

   installation
   usage
   quickstart
   user_guide/index

.. toctree::
   :maxdepth: 1
   :caption: Reference

   api/index
   changelog

.. toctree::
   :maxdepth: 1
   :caption: Extra Information

   developer_guide
   benchmarks/index
   description
   config
