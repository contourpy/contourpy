# Welcome to ContourPy's documentation!

**ContourPy** is a Python library for calculating contours of 2D quadrilateral grids.
It is written in C++11 and wrapped using {{ pybind11 }}.

It contains the 2005 and 2014 algorithms used in [Matplotlib](https://matplotlib.org) as well as a newer algorithm that
includes more features and is available in both serial and multithreaded versions.
It provides an easy way for Python libraries to use contouring algorithms without having to include
Matplotlib as a dependency.

Advantages of the new algorithm compared to Matplotlib's default algorithm of 2014 - 2022:

1. Improved performance in many situations (see {ref}`benchmarks`).
2. Multiple return types for both contour lines and filled contours, with different complexity and
   performance tradeoffs (see {ref}`line_type` and {ref}`fill_type`).
3. Multiple ways to specify chunk sizes and/or counts (see {ref}`chunks`).
4. Supports treating quads a four triangles for more detailed contours (see {ref}`quad_as_tri`).
5. Supports alternative forms of interpolation of z-values (currently only logarithmic) (see
   {ref}`z_interp`).
6. Multithreaded option (see {ref}`threads`).

```{toctree}
:caption: Basics
:maxdepth: 1

installation
usage
quickstart
```

```{toctree}
:caption: User Guide
:maxdepth: 1

user_guide/calculate/index
user_guide/manipulate/index
user_guide/external/index
```

```{toctree}
:caption: Reference
:maxdepth: 1

api/index
changelog
```

```{toctree}
:caption: Extra Information
:maxdepth: 1

developer_guide
benchmarks/index
description
config
```
