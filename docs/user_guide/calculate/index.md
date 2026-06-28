# Calculate contours

Contours are calculated using the {py:meth}`~.ContourGenerator.lines`,
{py:meth}`~.ContourGenerator.filled`, {py:meth}`~.ContourGenerator.multi_lines` and
{py:meth}`~.ContourGenerator.multi_filled` methods of a {py:class}`~.ContourGenerator` object
that is obtained by calling the {py:func}`~.contour_generator` function.
There are many options available for contouring that equate to keyword arguments passed to
the {py:func}`~.contour_generator` function, these are described in turn below.

Before reading this you should check out the {ref}`quickstart`.

The other main source of information is the {ref}`api`.

```{toctree}
:maxdepth: 1

name
z_corner_mask
x_and_y
chunks
line_type
fill_type
quad_as_tri
z_interp
threads
limitations
```
